import argparse
import configparser
import os
from datetime import datetime, timezone
from email.utils import format_datetime
from urllib.parse import quote
from xml.dom import minidom
from xml.etree import ElementTree as ET


DEFAULT_CONFIG = "test.ini"
DEFAULT_OUTPUT = "rss/trans.opml"
DEFAULT_REPO_SLUG = "rcy1314/Rss-Translation"
DEFAULT_REPO_BRANCH = "main"
DEFAULT_XML_URL_ANCHOR = ""
DEFAULT_USE_GITHUB_PAGES = False
OPML_DOCS = "https://opml.org/spec2.opml"
OPML_LANGUAGE = "zh"
OPML_VERSION = "RSS2.0"


def strip_quotes(value):
    return value.strip().strip('"')


def parse_bool(value):
    value = value.strip().lower()
    if value in ("1", "true", "yes", "y", "on"):
        return True
    if value in ("0", "false", "no", "n", "off", ""):
        return False
    raise argparse.ArgumentTypeError("expected true or false")


def read_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path, encoding="utf-8")
    return config


def source_sections(config):
    return [section for section in config.sections() if section != "cfg"]


def format_opml_time(value):
    return format_datetime(value, usegmt=True)


def format_opml_text(test: str) -> str:
    return test.replace("_", " ").replace("-", " ")


def format_opml_title(repo_slug: str) -> str:
    """Format the repository slug for OPML display fields."""
    return repo_slug.replace("/", "-")


def resolve_owner(config, repo_slug):
    owner_id = repo_slug.split("/", 1)[0]
    return {
        "ownerId": strip_quotes(config.get("cfg", "owner_id", fallback=owner_id)),
        "ownerName": strip_quotes(config.get("cfg", "owner_name", fallback=owner_id)),
        "ownerEmail": strip_quotes(config.get("cfg", "owner_email", fallback="")),
    }


def read_existing_head(output_path):
    if not os.path.exists(output_path):
        return {}

    try:
        root = ET.parse(output_path).getroot()
    except (ET.ParseError, OSError):
        return {}

    head = root.find("head")
    if head is None:
        return {}

    return {
        child.tag: child.text.strip()
        for child in head
        if isinstance(child.tag, str) and child.text and child.text.strip()
    }


def get_feed_path(config, section):
    base = strip_quotes(config.get("cfg", "base", fallback="rss/"))
    name = strip_quotes(config.get(section, "name"))
    return os.path.join(base, f"{name}.xml").replace(os.sep, "/")


def get_github_pages_url(repo_slug, feed_path):
    owner, repo = repo_slug.split("/", 1)
    return f"https://{owner}.github.io/{repo}/{quote(feed_path)}"


def default_feed_xml_url(repo_slug, repo_branch, feed_path):
    return f"https://raw.githubusercontent.com/{repo_slug}/{repo_branch}/{quote(feed_path)}"


def format_xml_url(xml_url, xml_url_anchor):
    if xml_url_anchor:
        return f"{xml_url}#{xml_url_anchor.lstrip('#')}"
    return xml_url


def get_public_feed_url(
    config,
    section,
    repo_slug,
    repo_branch,
    xml_url_anchor=DEFAULT_XML_URL_ANCHOR,
    use_github_pages_url=False,
):
    feed_path = get_feed_path(config, section)
    if use_github_pages_url:
        xml_url = get_github_pages_url(repo_slug, feed_path)
    else:
        xml_url = default_feed_xml_url(repo_slug, repo_branch, feed_path)
    return format_xml_url(xml_url, xml_url_anchor)


def build_opml(
    config,
    repo_slug,
    repo_branch,
    created_at,
    xml_url_anchor=DEFAULT_XML_URL_ANCHOR,
    use_github_pages_url=False,
):
    owner = resolve_owner(config, repo_slug)
    opml_title = format_opml_title(repo_slug)

    opml = ET.Element("opml", version="2.0")
    head = ET.SubElement(opml, "head")
    ET.SubElement(head, "title").text = opml_title
    ET.SubElement(head, "dateCreated").text = created_at
    ET.SubElement(head, "dateModified").text = format_opml_time(datetime.now(timezone.utc))
    ET.SubElement(head, "ownerName").text = owner["ownerName"]
    ET.SubElement(head, "ownerEmail").text = owner["ownerEmail"]
    ET.SubElement(head, "ownerId").text = owner["ownerId"]
    ET.SubElement(head, "docs").text = OPML_DOCS

    body = ET.SubElement(opml, "body")
    group = ET.SubElement(body, "outline", {"text": opml_title, "title": opml_title})

    for section in source_sections(config):
        if not config.has_option(section, "name"):
            continue
        name = strip_quotes(config.get(section, "name"))
        original_url = strip_quotes(config.get(section, "url", fallback=""))
        ET.SubElement(
            group,
            "outline",
            type="rss",
            text=format_opml_text(name),
            title=format_opml_text(name),
            xmlUrl=get_public_feed_url(
                config,
                section,
                repo_slug,
                repo_branch,
                xml_url_anchor,
                use_github_pages_url,
            ),
            htmlUrl=original_url,
            language=OPML_LANGUAGE,
            version=OPML_VERSION,
        )

    return opml


def serialize_opml(opml):
    rough_xml = ET.tostring(opml, encoding="utf-8")
    return minidom.parseString(rough_xml).toprettyxml(indent="  ", encoding="UTF-8")


def opml_signature(element):
    children = []
    for child in element:
        if element.tag == "head" and child.tag == "dateModified":
            continue
        children.append(opml_signature(child))

    return (
        element.tag,
        tuple(sorted(element.attrib.items())),
        (element.text or "").strip(),
        tuple(children),
    )


def existing_content_matches(output_path, candidate_opml):
    if not os.path.exists(output_path):
        return False

    try:
        existing_opml = ET.parse(output_path).getroot()
    except (ET.ParseError, OSError):
        return False

    return opml_signature(existing_opml) == opml_signature(candidate_opml)


def write_if_changed(output_path, opml):
    if existing_content_matches(output_path, opml):
        return False

    content = serialize_opml(opml)
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(content)
    return True


def generate_opml(
    config_path=DEFAULT_CONFIG,
    output_path=DEFAULT_OUTPUT,
    repo_slug=DEFAULT_REPO_SLUG,
    repo_branch=DEFAULT_REPO_BRANCH,
    xml_url_anchor=DEFAULT_XML_URL_ANCHOR,
    use_github_pages=DEFAULT_USE_GITHUB_PAGES,
):
    config = read_config(config_path)
    existing_head = read_existing_head(output_path)
    existing_date_created = existing_head.get(
        "dateCreated",
        format_opml_time(datetime.now(timezone.utc)),
    )
    opml = build_opml(
        config,
        repo_slug,
        repo_branch,
        existing_date_created,
        xml_url_anchor,
        use_github_pages,
    )
    changed = write_if_changed(output_path, opml)
    return output_path, changed


def main():
    parser = argparse.ArgumentParser(description="Generate OPML from RSS source config.")
    parser.add_argument("-c", "--config", default=DEFAULT_CONFIG, help="Config file path.")
    parser.add_argument("-o", "--output", default=DEFAULT_OUTPUT, help="Output OPML file path.")
    parser.add_argument(
        "--repo-slug",
        default=DEFAULT_REPO_SLUG,
        help="GitHub repository slug used to build feed URLs.",
    )
    parser.add_argument(
        "--repo-branch",
        default=DEFAULT_REPO_BRANCH,
        help="GitHub repository branch used to build raw feed URLs.",
    )
    parser.add_argument(
        "--xml-url-anchor",
        default=DEFAULT_XML_URL_ANCHOR,
        help="Anchor fragment appended to OPML xmlUrl values.",
    )
    parser.add_argument(
        "--use-github-pages",
        type=parse_bool,
        default=DEFAULT_USE_GITHUB_PAGES,
        help="Build xmlUrl values from GitHub Pages instead of raw.githubusercontent.com.",
    )
    args = parser.parse_args()

    output_path, changed = generate_opml(
        args.config,
        args.output,
        args.repo_slug,
        args.repo_branch,
        args.xml_url_anchor,
        args.use_github_pages,
    )
    if changed:
        print(f"Generated OPML: {output_path}")
    else:
        print(f"No changes for OPML: {output_path}")


if __name__ == "__main__":
    main()

# coding:utf-8 
import random
min=random.randint(0, 59)
h=random.randint(0, 23)


YML=".github/workflows/circle_translate.yml"

f = open(YML, "r+", encoding="UTF-8")
list1 = f.readlines()           
list1[7] = "   - cron: '%d %d * * *'\n"%(min,h)

f = open(YML, "w+", encoding="UTF-8")
f.writelines(list1)
f.close()
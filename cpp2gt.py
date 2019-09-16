#!/usr/bin/python3
# -*- coding: utf-8 -*-~
# 每个都要design point都要起名字太麻烦了，用这个可以随机命名，在cpp里使用_name_作为名称占用符，会按顺序替换成数字
import re
files=['test2.cpp']

case_total_num = 0

def addRandomeName(files):
  # 用来把字符串中的设计点提取出来，以及替换回去。
  design_point = re.compile(r'[\s\S]*(\$[\s\S]*\$)[\s\S]*')
  # 提取出来的数据
  matchObj = design_point.match(line)
  global case_total_num
  if matchObj:
    return line.replace('_name_', str(case_total_num))
  else:
    # 此行代码 没有设计点，直接返回
    return line

for file in files:
  fr = open("./"+file,'r')
  fw = open(file+'.gt','w')
  for line in fr.readlines():
    line = addRandomeName(line)
    print(line)
    fw.write(line)
  fw.close()
  fr.close()
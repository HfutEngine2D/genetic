#!/usr/bin/python  
# -*- coding: utf-8 -*-~
import re

files=['test.gt.cpp',
      'test2.gt.cpp']
for file in files:
  fr = open("./"+file,'r')
  fw = open(file.replace('.gt',''),'w')
  for line in fr.readlines():
    line = restore(line)
    fw.write(line)
  fw.close()
  fr.close()

def resotre(line):
  """将一些设计点还原为实际的代码
  
  Arguments:
      line {读入的行} -- 判断是否有设计点，如果没有直接返回，有的话还原
  """
  # 用来将设计点的内容分隔开
  resplit = re.compile(r'[\s\,\$]+')
  # 用来把字符串中的设计点提取出来，以及替换会去。
  design_point = re.compile(r'[\s\S]*(\$[\s\S]*\$)[\s\S]*')
  # 打印提取出来的数据
  print(filter(None,resplit.split(design_point.match('if (a>$V1=10,setp=0.5,type=float$)').group(1))))

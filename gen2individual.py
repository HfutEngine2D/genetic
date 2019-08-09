#!/usr/bin/python  
# -*- coding: utf-8 -*-~
import re
import random

files=[ #'test.cpp.gt',
      'test2.cpp.gt']

# 用来将设计点的内容分隔开
reSplitDesignPoint = re.compile(r'[\,\$]+')
# 将表达式根据赋值号分开
reSplitExpress = re.compile(r'[\=\:]+')

def variationCmp(matchstr):
  # 对运算符进行变异
  operDist = {'chance':0.1, }
  for exprLine in matchstr:
    ekey,evalue = reSplitExpress.split(exprLine)
    # print(ekey)
    if (ekey == 'step') or (ekey == 'max') or (ekey == 'min') or (ekey == 'chance'):
      operDist[ekey] = float(evalue)
    elif ekey.find('comp') == 0:
      operDist['Vname']=ekey
      operDist['Vvalue']=evalue
    if operDist['chance'] > random.random():
      randomNumber = random.random()
      if (randomNumber < 0.25):
        operDist['Vvalue']=">"
      elif (randomNumber < 0.5):
        operDist['Vvalue']=">="
      elif (randomNumber < 0.75):
        operDist['Vvalue']="<"
      else:
        operDist['Vvalue']="<="
  return operDist['Vvalue']

def variationVar(matchstr):
  # 对魔数进行变异
  operDist = {'chance':0.2, 'step':0}
  for exprLine in matchstr:
    ekey,evalue = reSplitExpress.split(exprLine)
    if (ekey == 'step') or (ekey == 'max') or (ekey == 'min') or (ekey == 'chance'):
      operDist[ekey] = float(evalue)
    elif ekey.find('V') == 0:
      operDist['Vname']=ekey
      operDist['Vvalue']=float(evalue)
    if operDist['chance'] > random.random():
      if random.random()<0.5:
        operDist['Vvalue'] += operDist['step']
      else:
        operDist['Vvalue'] -= operDist['step']
  return str(operDist['Vvalue'])

def restore(line):
  """将一些设计点还原为实际的代码
  
  Arguments:
      line {读入的行} -- 判断是否有设计点，如果没有直接返回，有的话还原
  """

  # 用来把字符串中的设计点提取出来，以及替换回去。
  design_point = re.compile(r'[\s\S]*(\$[\s\S]*\$)[\s\S]*')
  # 提取出来的数据
  matchObj = design_point.match(line)
  if matchObj:
    # 有设计点，拆分为表达式传入对应类型的变异函数
    matchstr = matchObj.group(1).replace(' ','')
    exprList = filter(None,reSplitDesignPoint.split(matchstr))
    if matchstr.find('$comp') == 0:
      return line.replace(matchObj.group(1),variationCmp(exprList))
    else:
      return line.replace(matchObj.group(1),variationVar(exprList))
    # 
  else:
    # 此行代码 没有设计点，直接返回
    return line
  #matchstr = design_point.match('if (a>$V1 = 10,step = 0.5, type = float$)').group(1).replace(' ','')
  # print(filter(None,reSplitDesignPoint.split(matchstr)))

for file in files:
  fr = open("./"+file,'r')
  fw = open(file.replace('.gt',''),'w')
  for line in fr.readlines():
    line = restore(line)
    print(line)
    # fw.write(line)
  fw.close()
  fr.close()
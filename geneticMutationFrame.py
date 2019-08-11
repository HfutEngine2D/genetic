#!/usr/local/bin/python3
# -*- coding: utf-8 -*-~
import os
import re
import sqlite3
import random
import variation
from database import DbHandler

# 染色体数量
chromosomeNum = 10
design_point = re.compile(r'[\s\S]*(\$[\s\S]*\$)[\s\S]*')
# 用来将设计点的内容分隔开
reSplitDesignPoint = re.compile(r'[\,\$]+')
# 将表达式根据赋值号分开
reSplitExpress = re.compile(r'[\=\:]+')

def initOriginChromosome(files):
  conn = DbHandler('Origin.db')
  conn.Create()
  for file in files:
    fr = open("./"+file,'r')
    for line in fr.readlines():
      matchObj = design_point.match(line)
      if matchObj:
        # 有设计点，拆分为表达式写入数据库
        matchstr = matchObj.group(1).replace(' ','')
        exprList = filter(None,reSplitDesignPoint.split(matchstr))
        ekey,evalue = reSplitExpress.split(list(exprList)[0])
        conn.insert(ekey,evalue,matchstr)
    fr.close()
  conn.close()
  with open('genstate', 'w') as f:
    f.write("0")

def calAdaptability():
  pass

def createGeneration():
  with open('genstate', 'r') as f:
    genstate = f.read()
  print(genstate)
  if genstate == '0':
    conn = DbHandler('Origin.db')
    for i in range(0,chromosomeNum):
      print("chromosomeNum")
      conn_new = DbHandler('{}_{}.db'.format(int(genstate)+1,i))
      conn_new.Create()
      for row in conn.list_chromosome():
        conn_new.insert(row[0],variation.variation(row[2],row[1]),row[2])
      conn_new.close()
    conn.close()
  else:
    pass
  with open('genstate', 'w') as f:
    f.write(str(int(genstate)+1))

def gaSearch():
  createGeneration()

 #
 # 初始化遗传算法
 #
def initGA() :
  # 初始化染色体
  if not os.path.exists('Origin.db'):
    print("不存在源染色体，新建源染色体")
    initOriginChromosome(['test.cpp.gt'])

  gaSearch()
  # 渲染视图
  # draw(resultData)

initGA()
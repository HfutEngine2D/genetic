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
  conn = sqlite3.connect('Origin.db')
  cursor = conn.cursor()
  cursor.execute('create table Chromosome (Vkey varchar(20) primary key, Vvalue varchar(20), paramStr varchar(50))')
  for file in files:
    fr = open("./"+file,'r')
    for line in fr.readlines():
      matchObj = design_point.match(line)
      if matchObj:
        # 有设计点，拆分为表达式写入数据库
        matchstr = matchObj.group(1).replace(' ','')
        exprList = filter(None,reSplitDesignPoint.split(matchstr))
        ekey,evalue = reSplitExpress.split(list(exprList)[0])
        cursor.execute('insert into Chromosome (Vkey, Vvalue, paramStr) values (\'{}\', \'{}\', \'{}\')'
          .format(ekey,evalue,matchstr))
    fr.close()
  cursor.close()
  conn.commit()
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
    conn = sqlite3.connect('Origin.db')
    cursor = conn.cursor()
    for i in range(0,chromosomeNum):
      print("chromosomeNum")
      cursor.execute('select * from Chromosome')
      conn_new = sqlite3.connect('{}_{}.db'.format(int(genstate)+1,i))
      cursor_new = conn_new.cursor()
      cursor_new.execute('create table Chromosome (Vkey varchar(20) primary key, Vvalue varchar(20), paramStr varchar(50))')
      for row in cursor:
        cursor_new.execute('insert into Chromosome (Vkey, Vvalue, paramStr) values (\'{}\', \'{}\', \'{}\')'
          .format(row[0],variation.variation(row[2],row[1]),row[2]))
      cursor_new.close()
      conn_new.commit()
      conn_new.close()
    cursor.close()
    conn.commit()
    conn.close()
  else:
    
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
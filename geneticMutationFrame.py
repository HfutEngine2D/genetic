#!/usr/local/bin/python3
# -*- coding: utf-8 -*-~
import os
import re
import sqlite3
import random
import variation
import operator
import shutil
from database import DbHandler

# 适应度
Adaptability = {}
# 染色体数量
chromosomeNum = 10
# 自然选择概率
selectionProbability = {}
# 染色体复制的比例(每代中保留适应度较高的染色体直接成为下一代)
cp = 0.3
# 迭代次数
iteratorNum = 10
# 交叉的染色体数
crossoverMutationNum = int(chromosomeNum - chromosomeNum * cp)
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
  global Adaptability
  Adaptability.clear()
  with open('genstate', 'r') as f:
    genstate = f.read()
  # 计算适应度
  for i in range(0,chromosomeNum):
    Adaptability['{}_{}.db'.format(int(genstate),i)]=random.randint(30,60)
  with open('./Adaptability/{}_value'.format(int(genstate)), 'w') as f:
    f.write(str(Adaptability))
  # sorted_x=sorted(x.items(), key=operator.itemgetter(1))
  # print(Adaptability)
  # for i in range(0,crossoverMutationNum):

  # # 先随机生成，以后再做，，，
  # for i in range(0,chromosomeNum):
  #   print("chromosomeNum")
  #   with open('./Adaptability/{}_{}_value'.format(int(genstate)+1), 'w') as f:
  #     f.write(str(random.randint(30,60)))

# 计算自然选择概率
def calSelectionProbability():
    global selectionProbability
    global Adaptability
    selectionProbability.clear()
    # 计算适应度总和
    sumAdaptability = 0.0
    for eachvalue in Adaptability.values():
      sumAdaptability+=eachvalue
    # 计算每条染色体的选择概率
    for key, value in Adaptability.items():
        selectionProbability[key]= (value / sumAdaptability)
    
def RWS():
  global selectionProbability
  print(selectionProbability)
  sum = 0
  rand = random.random()
  for key,value in selectionProbability.items():
        sum += value
        if (sum >= rand):
          conn = DbHandler(key)
          return_list = conn.list_chromosome()
          conn.close()
          return return_list

def createGeneration():
  global Adaptability
  with open('genstate', 'r') as f:
    genstate = f.read()
  # print(genstate)
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
    # 交叉，变异
    # crossandmutation
    for i in range(0,crossoverMutationNum):
      # 采用轮盘赌选择父母染色体
      newChromosomeMatrix = []
      chromosomeBaba = RWS()
      chromosomeMama = RWS()
      for j in range(0,len(chromosomeBaba)):
        if random.random()<0.5:
          newChromosomeMatrix.append(chromosomeBaba[j])
        else:
          newChromosomeMatrix.append(chromosomeMama[j])
      print('{}_{}.db'.format(int(genstate)+1,i))
      conn_new = DbHandler('{}_{}.db'.format(int(genstate)+1,i))
      conn_new.Create()
      for row in newChromosomeMatrix:
        conn_new.insert(row[0],variation.variation(row[2],row[1]),row[2])
      conn_new.close()
    sorted_x=sorted(Adaptability.items(), key=operator.itemgetter(1))
    print("move")
    print(Adaptability)
    print(sorted_x)
    for i in range(crossoverMutationNum,chromosomeNum):
      shutil.copy(sorted_x[i][0], '{}_{}.db'.format(int(genstate)+1,i))
  with open('genstate', 'w') as f:
    f.write(str(int(genstate)+1))

def gaSearch():
  for i in range(0,iteratorNum):
    # 生成新一代染色体
    createGeneration()
    # 计算上一代各条染色体的适应度
    calAdaptability()
    # 计算各染色体的适应度
    calSelectionProbability()
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
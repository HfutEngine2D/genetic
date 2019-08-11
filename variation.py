#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sqlite3
import random

' 对数据库进行初始化，进行变异 '

__author__ = 'bcahlit'

# 用来将设计点的内容分隔开
reSplitDesignPoint = re.compile(r'[\,\$]+')
# 将表达式根据赋值号分开
reSplitExpress = re.compile(r'[\=\:]+')

def variationCmp(matchstr, currentValue = None):
  # 对运算符进行初始化
  operDist = {'chance':0.1}
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
      operDist['Vvalue']=[">",">=","<","<="][random.randint(0,3)]
  return operDist['Vvalue']

def variationEnum(matchstr, currentValue = None):
  # 对枚举进行变异
  enumsplit = re.compile(r'\|')
  operDist = {'chance':0.1}
  for exprLine in matchstr:
    ekey,evalue = reSplitExpress.split(exprLine)
    # print(ekey)
    if ekey == 'opt':
      operDist[ekey] = enumsplit.split(evalue)
    elif ekey.find('enum') == 0:
      operDist['Vname']=ekey
      operDist['Vvalue']=evalue
    # if operDist['chance'] > random.random():
    # print(operDist)
  return operDist['opt'][random.randint(0,len(operDist['opt'])-1)]

def variationVar(matchstr, currentValue = None):
  # 对魔数进行变异
  operDist = {'chance':0.2, 'step':0, 'max':53, 'min':-53}
  for exprLine in matchstr:
    ekey,evalue = reSplitExpress.split(exprLine)
    if (ekey == 'step') or (ekey == 'max') or (ekey == 'min') or (ekey == 'chance'):
      operDist[ekey] = float(evalue)
    elif ekey.find('V') == 0:
      operDist['Vname']=ekey
      operDist['Vvalue']=float(evalue)
  if currentValue != None:
    operDist['Vvalue']=float(currentValue)
  if operDist['chance'] > random.random():
    if random.random()<0.5:
      operDist['Vvalue'] += operDist['step']
    else:
      operDist['Vvalue'] -= operDist['step']
  if operDist['Vvalue'] > operDist['max']:
    operDist['Vvalue'] -= operDist['step']
  elif operDist['Vvalue'] < operDist['max']:
    operDist['Vvalue'] += operDist['step']
  return str(operDist['Vvalue'])

def variation(paramStr,value):
  exprList = filter(None,reSplitDesignPoint.split(paramStr))
  if paramStr.find('$comp') == 0:
    return variationCmp(exprList, currentValue = value)
  elif paramStr.find('$enum') == 0:
    return variationEnum(exprList, currentValue = value)
  else:
    return variationVar(exprList, currentValue = value)
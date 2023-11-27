#!/usr/bin/env python
#coding:utf-8
import matplotlib as mpl
from matplotlib import pyplot as plt
import numpy as np
mpl.rcParams[u'font.sans-serif'] = ['simhei']
mpl.rcParams['axes.unicode_minus'] = False
filename = 'primitive_force2.txt'
x, forcex, forcey, forcez, torquex, torquey, torquez =[], [], [], [], [], [], []

# 相比open(),with open()不用手动调用close()方法
with open(filename, 'r') as f:
    # 将txt中的数据逐行存到列表lines里 lines的每一个元素对应于txt中的一行。然后将每个元素中的不同信息提取出来
    lines = f.readlines()
    # i变量，由于这个txt存储时有空行，所以增只读偶数行，主要看txt文件的格式，一般不需要
    # j用于判断读了多少条，step为画图的X轴
    i = 0
    j = 0
    for line in lines:
        temp = line.split(' ')
        t0 = temp[0].split(':')
        t1 = temp[1].split(':')
        t2 = temp[2].split(':')
        t3 = temp[3].split(':')
        t4 = temp[4].split(':')
        t5 = temp[5].split(':')
 
        x.append(j)
        j = j + 1
        forcex.append(float(t0[1]))
        forcey.append(float(t1[1]))
        forcez.append(float(t2[1]))


        torquex.append(float(t3[1]))
        torquey.append(float(t4[1]))
        torquez.append(float(t5[1]))
        
#绘制在一张表格

# 这两行代码解决 plt 中文显示的问题
# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.rcParams['axes.unicode_minus'] = False
plt.figure()
# plt.plot(x, forcex, 'red', label='forcex')
# plt.plot(x, forcey, 'blue', label='forcey')
# plt.plot(x, forcez, 'green', label='forcez')
# plt.plot(x, torquex, 'magenta', label='torquex')
# plt.plot(x, torquey, 'deepskyblue', label='torquey')
plt.plot(x, torquez, 'darkviolet', label='torquez')

plt.xlabel(u'采样点')
plt.ylabel(u'力(N)')
plt.title(u'六维力数值')
plt.legend()
plt.savefig('./primitive_force/torquez.png')
plt.show()
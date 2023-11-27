#!/usr/bin/python
#-*-coding:utf-8-*-
#本文档用于书写卡尔曼滤波器算法
#程序员：陈永*
#版权：哈尔滨工业大学(深圳)
#日期：2020.10.4

import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import numpy as np
mpl.rcParams[u'font.sans-serif'] = ['simhei']
mpl.rcParams['axes.unicode_minus'] = False

#====建立全状态卡尔曼滤波方程=======#
class KalmanFilter(object):
    def __init__(self):
        pass

    #获取建立状态方程和观测方程的参数
    def get_state_measurement_matrix(self, A, B, C):
        #状态转移矩阵
        self.A = np.mat(A)
        #激励转移矩阵
        self.B = np.mat(B)
        #观测矩阵
        self.C = np.mat(C)

    #获取激励矢量和测量误差矢量的协方差
    def get_cov_matrix(self, R, Q = None):
        #误差协方差矩阵
        self.R = np.mat(R)
        #激励激励协方差矩阵
        self.Q = np.mat(Q)

    #获得转移状态协方差矩阵初值
    def get_state_cov_matrix(self, P0):
        self.P = np.mat(P0)

    #获取状态矢量初值
    def get_state_init(self, x0):
        self.x = np.array(x0)

    #计算卡尔曼增益
    def kalman_gain(self):
        #求取卡尔曼增益
        self.K = self.P*self.C.T*(self.C*self.P*self.C.T + self.R).I

        #更新状态转移协方差矩阵
        self.P = self.P - self.K*self.C*self.P

    #输出估计值
    def out_filter_value(self, z):
        # 计算卡尔曼增益
        self.kalman_gain()
        D = np.array(self.A - self.K*self.C*self.A)

        self.x = np.dot(D, self.x) + np.dot(np.array(self.K), z)
        return self.x

def get_force():
    filename = 'primitive_force_add1.txt'
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

    # F = np.zeros([j, 6])
    # for m in range(j): 
    #     F[m, 0] = forcex
    #     F[m, 1] = forcey
    #     F[m, 2] = forcez
    #     F[m, 3] = torquex
    #     F[m, 4] = torquey
    #     F[m, 5] = torquez
    #       #力  横坐标   力的个数
    return x , forcex,forcey,forcez,torquex,torquey,torquez,j






def wrench_filter():
    #从上文卡尔曼滤波建立六维力滤波器
    kalm_filt = KalmanFilter()

    #建立状态方程和观测方程:n=m=p
    n = 6
    I = np.eye(n)
    A = np.copy(I)
    B = 0.1*I
    C = np.copy(I)
    kalm_filt.get_state_measurement_matrix(A, B, C)

    #输入测量误差协方差方程
    R = 0.001*I
    kalm_filt.get_cov_matrix(R)

    #输入状态初值
    x0 = np.zeros(n)
    P0 = np.copy(I)
    kalm_filt.get_state_cov_matrix(P0)
    kalm_filt.get_state_init(x0)

    #获取滤波后的数据：本文制造一组虚拟数据   F
    # num = 1000
    # T = 0.01
    # t = np.linspace(0, (num - 1)*T, num)
    # F = np.zeros([num, n])
    # for i in range(n):
    #     F[:, i] = 10 + 2*np.sin(np.pi * t) + 1*np.random.randn(num)

    
    t , forcex,forcey,forcez,torquex,torquey,torquez,num= get_force()
    F = np.zeros([num, n])
    for i in range(num):
        F[i, :] = [forcex[i],forcey[i],forcez[i],torquex[i],torquey[i],torquez[i]]




    #带入滤波器
    F_filt = np.zeros([num, n])
    for i in range(num):
        # F_filt[i, :] = kalm_filt.out_filter_value(F[i, :])
        F_filt[i, :] = kalm_filt.out_filter_value([forcex[i],forcey[i],forcez[i],torquex[i],torquey[i],torquez[i]])

    #绘画函数,仅考虑第一维
    plt.figure(1)
    plt.plot(t, F[:, 2], label='Fz', color='b')
    plt.plot(t, F_filt[:, 2], label='Fz_filt', color='r')
    plt.title("Kalman_filter")
    plt.xlabel("t/s")
    plt.ylabel("f/N")
    plt.legend()
    plt.savefig('./primitive_force/_add1.png')
    plt.show()

if __name__ == "__main__":
    wrench_filter()

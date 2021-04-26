import networkx as ne #导入建网络模型包，命名ne
import matplotlib.pyplot as plt #导入科学绘图包，命名mp
import random
import numpy as np
import pandas as pd
from collections import Counter

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
# N=10000
# k=6
# p=0.5
Ti=5




class node():
    Na = 1
    Bq={1:0.2}
    def __init__(self,n,t=0,state=0,t_inf=0,vir=0):
        self.id = n
        self.time = t
        self.state=state
        self.t_inf =t_inf
        self.degree=ws.degree(str(n))
        self.neib=list(ws.neighbors(str(n)))
        self.vir=vir
        self.immu=[]
        self.temp=[0,0]#第一个数值代表从t->t+1的状态变化，0--代表正常人保持正常；1--正常人发生感染；2--代表感染者推进病程；3--感染者完成对某一病毒免疫；
                        #当第一个数值为1时间，第二个值代表目前所感染的病毒的编号；第一个数值为3时间，第二值代表对某种病毒发生永久免疫

    def judge_transition(self,nodes):
        def cal_pro(k,q):
            if k == 0: return 0
            s = 1 - pow((1 - q), k)
            if random.random() < s:  # 若被感染
                return [1,s]
            return [0,s]
        if self.state==0:
            ki={}
            sp=0#最大概率
            ss=0#最大概率对应的疾病编号
            for m in self.neib:
                #print(m)
                if nodes[int(m)].state == 1 and nodes[int(m)].vir not in self.immu:#如果邻居节点m的状态为1，并且该节点所感染的病毒没有被免疫
                    if nodes[int(m)].vir in ki.keys():
                        ki[nodes[int(m)].vir] += 1
                    else:
                        ki[nodes[int(m)].vir] = 1

            if len(ki) !=0:#如果ki不为空，说明周围有人感染，否则周围没有人感染
                for i,j in ki.items():
                    sp_temp=cal_pro(j,node.Bq[i])#第i种病毒和q为node.Bq[i]，总共有j个邻居感染了
                    if sp_temp[0]==1 and sp_temp[1]>sp:#多种病毒竞争上岗
                        ss=i
                        sp=sp_temp[1]
                if ss>0:#若被感染
                    self.temp=[1,ss]

                else:
                    self.temp =[0, 0]
            else:
                self.temp = [0, 0]
        else:
            if self.time+1 >= Ti:#过了感染期，进入免疫期(永久免疫）
                self.temp=[3,self.vir]
            else:
                self.temp=[2,0]
        return 0


    def time_proceed(self):
        if self.temp[0]==1:#发生感染
            self.vir=self.temp[1]
            self.time=1
            self.state=1
            self.t_inf=self.t_inf+1
        if self.temp[0]==2:#推进病程
            self.time = self.time+1
        if self.temp[0]==3:#完成某种病毒免疫
            self.time=0
            self.vir=0
            self.state=0
            self.immu.append(self.temp[1])


def get_inf_num(nodes):
    k0=0
    mem=[]
    for i in nodes:
        if i.state==1:
            k0+=1
        mem.append(i.id)
    return k0,mem


def get_vir_i_num(nodes,ik):
    k0=0
    for i in nodes:
        if i.vir==ik:
            k0+=1
    return k0

def self_vir_record(nodes):
    v=[]
    for i in nodes:
        v.append(i.vir)
    return v



def run_one(ppp_list):
    kkkk=1
    retu=[]
    for ppp in ppp_list:
        all_data=[]
        ytt=[]#生病人数统计
        xtt=[]#总时间历程
        yt=[[]]#各类病毒的数量统计
        xt=[[]]#各类病毒出现的
        #初始化
        nodes=[]
        node.Na=1
        node.Bq = {1: 0.2}
        I_ini=random.sample([i for i in range(N)], int(0.1*N))
        #I_ini=[i for i in range(100)]
        for i in range(N):
            if i in I_ini:
                nodes.append(node(i,t=1,state=1,t_inf=1,vir=1))
            else:
                nodes.append(node(i))


        by=0

        #推进
        for tt in range(200):
            #print(tt)
            all_data.append(self_vir_record(nodes))
            #记录时间
            xtt.append(tt+1)
            for i in range(len(yt)):
                xt[i].append(tt)
                yt[i].append(get_vir_i_num(nodes, i+1))

            # #调整生病概率
            # for i,j in node.Bq.items():
            #     if j>0.2:
            #         node.Bq[i]=node.Bq[i]-0.2/Ti
            #     if j< 0.2:
            #         node.Bq[i]=0.2
            #推进
            for i in nodes:
                i.judge_transition(nodes)
            for i in nodes:
                i.time_proceed()
            nn,inf_mem=get_inf_num(nodes)
            ytt.append(nn/N)
            if tt>0 and  by>=ppp:
                xt.append([])
                yt.append([])
                by=0
                I_ini = random.sample(inf_mem, int(0.1 *nn))
                node.Na=node.Na+1
                node.Bq[node.Na]=0.2
                for i in I_ini:
                    nodes[i].time=1
                    nodes[i].state = 1
                    nodes[i].t_inf=nodes[i].t_inf+1
                    nodes[i].vir=node.Na
            by+=random.random()
        retu.append(ytt[-1])
    return retu
    # np_data=np.array(all_data)
    # np_data=np_data.T
    # df=pd.DataFrame(np_data)
    # df.to_excel('N_'+str(N)+'_p_'+str(p)+'_k_'+str(k)+'_by_'+str(ppp)+'.xlsx')



    # plt.subplot(2,5,kkkk)
    # kkkk+=1
    # plt.title(ppp)
    # # for i in range(len(yt)):
    # #     plt.plot(xt[i],yt[i])
    # plt.plot(xtt[:200],ytt[:200])
    # plt.ylim([0,1])
    # plt.suptitle('N='+str(N)+',p='+str(p)+',k='+str(k)+',T='+str(Ti))
#plt.show()
#[0.01,0.02,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
filename=[]
for N in [10000]:
    for k in [6]:
        for p in [0.9]:
            filename.append('N_'+str(N)+'_p_'+str(p)+'_k_'+str(k)+'.gml')

for i in filename:

    ws= ne.read_gml(i)
    ppp_list=[0.1*ii+7.7 for ii in range(20) ]
    rt_all=[]
    for j in range(100):
        print(j)
        rt=run_one(ppp_list)
        rt_all.append(rt)
    df = pd.DataFrame(np.array(rt_all),columns=ppp_list)
    df.to_excel('mth\\'+i+'.xlsx',index=None)

















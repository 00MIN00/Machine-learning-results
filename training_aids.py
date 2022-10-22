import random
import re
import time
from math import log
"""
训练器
"""
# 统计标签
def count_feature(object_feature:object,dict_features:dict)->dict:
    if object_feature not in dict_features.keys():	#如果标签(Label)没有放入统计次数的字典,添加进去
        dict_features[object_feature] = 0
    dict_features[object_feature] += 1	            #Label计数
    return dict_features
#空值删除
def detelenull(list_1:list)->list:
    for i in range(len(list_1)-1):
        if list_1[i]=="" or list_1[i]=='':
            list_1.pop(i)
    return list_1
#经验计算器{
"""
Explain:
    香农熵运算
Parameters:
    int_key          - 概率集合
    int_len          - 概率总数
Returns:
    newEntropy       - 香浓熵
Author:
    MIN
Modify:
    2022-10-8   
"""
def Aromatic_entropy(int_key:int,int_len:int):
    newEntropy = 0.0
    prob = float(int_key /int_len)
    newEntropy -= prob * log(prob, 2)
    return newEntropy
"""
Explain:
    相同字符特征熵运算
Parameters:
	list_probability - 概率集合
	int_len          - 概率总数
Returns:
	list_probability - 香浓熵集合
Author:
	MIN
Modify:
	2022-10-8
"""
def  EntList(list_probability:list[dict],int_len:int):
    i=0
    for dict_features in list_probability:
        newEntropy = 0.0
        if len(dict_features)==1:
            lsit_key = [S for S in dict_features.keys()][0]
            try:
                newEntropy=Aromatic_entropy(dict_features[lsit_key],int_len)
            except:
                newEntropy=1.0
        else:
            for str_key in dict_features.keys() :
                prob = float(dict_features[str_key]/int_len)
                newEntropy += prob *Aromatic_entropy(dict_features[str_key],int_len)
        list_probability[i]= newEntropy
        i+=1
    return list_probability
#   }
#正则组装器{
"""
Explain:
    正则表达式组装器组
Note：
    正则默认为贪婪模式。
    非贪婪模式可以将”Retset_assembly().str_middle“中的值改为'){1}(.*?)?('
Author:
	MIN
Modify:
	2022-10-8
"""
def Retset_assembly(list_treainingresults:list,*str_wend:str):
    str_begin = r'('
    str_end = '){1}'
    if  len(str_wend)==1:
        str_end=str_wend[0]
    str_middle='){1}(.*)?('
    str_Retset=''
    str_Retset+=str_begin
    for i in list_treainingresults:
        str_Retset+=i
        if (list_treainingresults.index(i)+1)!=len(list_treainingresults):
            str_Retset+=str_middle
    if str_wend!='' and len(str_wend)!=0:
        str_Retset+=str_wend
        str_Retset+=str_middle
    str_Retset+=str_end
    return str_Retset
def Retset_escape(list_treainingresults:list[str]):
    list_Retsets = ['?']
    list_Retsetsg = ['\?']
    for str_i in list_treainingresults:
        str_j = str_i
        for j in list_Retsets:
            if str_i.count(j)!=0:
                str_i=str_i.replace(j,list_Retsetsg[list_Retsets.index(j)], str_i.count(j))
        if str_i!=str_j:
            list_treainingresults[list_treainingresults.index(str_j)]=str_i
    return list_treainingresults
def Retset_validation(str_retset,list_treainingSet):
    str_retsettset =re.compile(r''+str_retset)
    int_rd = random.randint(0,len(list_treainingSet)-1)
    # 检查点
    # print( str(str_retsettset.match(list_treainingSet[int_rd]).group())+'\n'+list_treainingSet[int_rd])
    # print(str(str_retsettset.match(list_treainingSet[int_rd]).group())== list_treainingSet[int_rd])
    # a =str(str_retsettset.match(list_treainingSet[int_rd]).group())
    # b = list_treainingSet[int_rd]
    # print(a.count('\n'))
    # print(b.count('\n'))
    if str(str_retsettset.match(list_treainingSet[int_rd]).group())== str(list_treainingSet[int_rd]).replace('\n',''):
        return True
    return False
def Retset_end(str_query_key,list_treainingSet):
    list_probability=list()
    dict_features = dict()
    list_StrList = list()
    str_String=str()
    for i in range(-1,(len(str_query_key)*-1),-1):
        if -len(str_query_key)+1==i:
            break
        str_query_key=str_query_key.replace('\n','',str_query_key.count('\n'))
        for j in list_treainingSet:
            j=j.replace('\n','',j.count('\n'))
            if len(j)-1<=(-i):
                break
            if str_query_key[i]==j[i]:
                try:
                    dict_features = count_feature(str(-i-1),dict_features)
                except :
                    continue
            else:
                try:
                    dict_features = count_feature('not'+str(i),dict_features)
                except :
                    continue
        list_probability.append(dict_features.copy())
        dict_features.clear()
    list_Ent = EntList(list_probability,len(list_treainingSet))
    for key in range(len(list_Ent)):
        if list_Ent[key]<=0.0:
            if str_query_key[key*-1-1]=='\n':
                continue
            if len(str_String)>=10:
                if str_query_key.count(str_String)>1:
                    str_String+=')+(.*?'
                return str_String
            str_String=str_query_key[key*-1-1]+str_String
        elif len(str_String)!=0:
           return str_String
#   }
#同位运算{
"""
Explain:
    同位对照训练
Parameters:
	str_treainingSetPath - 训练集文件路径
Returns:
	re          -正则表达式
Author:
	MIN
Modify:
	2022-10-8
"""
def treaining_aids_tw(str_treainingSetPath:str):
    if str((str_treainingSetPath[-3]+str_treainingSetPath[-2]+str_treainingSetPath[-1]))=='txt':
        IO_treainingSet = open(str_treainingSetPath,'r',encoding='utf-8')
        list_treainingSet=[]
        for str_treainingSet in  IO_treainingSet:
            list_treainingSet.append(str_treainingSet)
    list_treaining = tw(list_treainingSet)
    list_treaining=Retset_escape(list_treaining)
    str_retset = (Retset_assembly(list_treaining))
    if Retset_validation(str_retset,list_treainingSet):
        return re.compile(r''+str_retset)
    list_treaining.append(Retset_end(list_treainingSet[random.randint(0,len(list_treainingSet)-1)],list_treainingSet))
    str_retset = (Retset_assembly(list_treaining))
    if Retset_validation(str_retset,list_treainingSet):
        return re.compile(r''+str_retset)
"""
Explain:
    同位对照主线程
Parameters:
	list_treainingSet - 训练集
Returns:
	list_StrList      - 特征相同组
Author:
	MIN
Modify:
	2022-10-8
"""
def tw(list_treainingSet:list)->list:
    str_query_key = list_treainingSet[random.randint(0,len(list_treainingSet)-1)]
    dict_features = dict()
    list_probability= list()
    str_String = str()
    list_StrList = list()
    for i in range(len(str_query_key)-1):
        if len(str_query_key)-1==i:
            break
        for j in list_treainingSet:
            if len(j)-1<=i:
                break
            if str_query_key[i]==j[i]:
                try:
                    dict_features = count_feature(str(i),dict_features)
                except :
                    continue
            else:
                try:
                    dict_features = count_feature('not'+str(i),dict_features)
                except :
                    continue
        list_probability.append(dict_features.copy())
        dict_features.clear()
    list_Ent = EntList(list_probability, len(list_treainingSet))
    for key in range(len(list_Ent)-1):
        if list_Ent[key]<=0.0:
            str_String+=str_query_key[key]
        elif len(str_String)!=0:
            list_StrList.append(str_String)
            str_String=str()
    return list_StrList
#   }
#邻位运算{
"""
Explain:
    同位对照训练
Parameters:
	str_treainingSetPath - 训练集文件路径
Returns:
	re          -正则表达式
Author:
	MIN
Modify:
	2022-10-8
"""
def treaining_aids_Lw(str_treainingSetPath:str):
    if str((str_treainingSetPath[-3]+str_treainingSetPath[-2]+str_treainingSetPath[-1]))=='txt':
        IO_treainingSet = open(str_treainingSetPath,'r',encoding='utf-8')
        list_treainingSet=[]
        for str_treainingSet in  IO_treainingSet:
            list_treainingSet.append(str_treainingSet)
    list_treaining = Lw(list_treainingSet)
    list_treaining=Retset_escape(list_treaining)
    str_retset = (Retset_assembly(list_treaining))
    if Retset_validation(str_retset,list_treainingSet):
        return re.compile(r''+str_retset)
    list_treaining.append(Retset_end(list_treainingSet[random.randint(0,len(list_treainingSet)-1)],list_treainingSet))
    str_retset = (Retset_assembly(list_treaining))
    if Retset_validation(str_retset,list_treainingSet):
        return re.compile(r''+str_retset)
"""
Explain:
    邻位对照主线程
Parameters:
	list_treainingSet - 训练集
Returns:
	list_StrList      - 特征相同组
Author:
	MIN
Modify:
	2022-10-22
"""
def Lw(list_treainingSet:list)->list:
    list_treainingSet = detelenull(list_treainingSet)
    ExamineStrs = list()
    for i in range(10):
        ExamineStrs.extend(createExamineStrs(list_treainingSet[random.randint(0,len(list_treainingSet))],i))
        ExamineStrs=list(set(ExamineStrs))

    # os = open('sss.txt','w',encoding='utf-8')
    # os.write(str(ExamineStrs))
    # ExamineStrs_copy= ExamineStrs.copy()
    ExamineStrs.remove(None)
    for i in range(10):
        list_Ent = Ent_recount(ExamineStrs,list_treainingSet)
        ExamineStrs=nofollow(list_Ent,ExamineStrs)
    # for i in ExamineStrs:
    #     if i.count('ce')>0:
    #         print(i)
    list_Ent = orientation(ExamineStrs, list_treainingSet)
    ExamineStrs = nofollow(list_Ent,ExamineStrs)

    # so = open('ww.txt','w',encoding='utf-8')
    # for i in ExamineStrs:
    #     s  = []
    #     for sa in list_treainingSet:
    #         s.append(sa.count(i))
    #
    #     print(i+str(set(s))+'\n'+str(len(s)))
    # print(len(ExamineStrs))

    s = {}
    for i in ExamineStrs:
        zl_z=0

        zl_f=0
        qsz = 0

        while_k = True
        while True:
            str_jizun = list_treainingSet[random.randint(0,len(list_treainingSet)-1)]
            if qsz+zl_z>=len(str_jizun):
                break
            jizun = str_jizun[str_jizun.index(i)+zl_z]
            for j in list_treainingSet:
                qsz = j.index(i)
                if qsz+zl_z>=len(j):
                    while_k=False
                    continue
                if jizun!=j[qsz+zl_z]:while_k=False
                if '\n'==j[qsz+zl_z]:while_k=False
            if while_k==False:break


            zl_z+=1
        while_k = True
        while True:

            str_jizun = list_treainingSet[random.randint(0,len(list_treainingSet)-1)]
            jizun = str_jizun[str_jizun.index(i)-zl_f]
            for j in list_treainingSet:
                qsz = j.index(i)
                if qsz+zl_f<=0:
                    while_k=False
                    continue
                if jizun!=j[qsz-zl_f]:
                    while_k=False
                    break
                if '\n'==j[qsz+zl_f]:
                    while_k=False
                    break
            if while_k==False:break
            zl_f+=1
        s[i] = {'z':zl_z,'f':zl_f}
    lp = []
    for i in s.keys():
        str_ss = ''
        str_jizun = list_treainingSet[0]
        str_ss =zhuo(s.get(i)['f']-1,str_jizun.index(i),str_jizun)+\
                str_jizun[str_jizun.index(i)]+\
                rou(str_jizun,str_jizun.index(i),s.get(i)['z']-1)
        lp.append(str_ss)
    lp = set(lp)
    list_Ent = orientation(list(lp), list_treainingSet)
    ExamineStrs = nofollow(list_Ent,list(lp))
    for i in ExamineStrs:
        for j in ExamineStrs:
            if i!=None and j !=None and j!=i:
                try:
                    if j.count(i)>0:
                        ExamineStrs[ExamineStrs.index(i)]=None
                    elif i.count(j)>0:
                        ExamineStrs[ExamineStrs.index(j)]=None
                except:
                    continue
    for i in range(len(ExamineStrs)*10):
        if ExamineStrs.count(None)==0:
            break
        ExamineStrs.remove(None)
    s.clear()
    str_jizun = list_treainingSet[random.randint(0,len(list_treainingSet)-1)]
    for i in ExamineStrs:
        s[str_jizun.index(i)]=i
    list_treaining = list(s.keys())
    list_treaining.sort()
    ExamineStrs= []
    for i in range(len(list_treaining)):
        ExamineStrs.append(s.get(list_treaining[i]))

    return ExamineStrs
def zhuo(int_i:int,int_j:int,str_i:str):
    if int_i<=0:return ''
    if int_j-int_i<=0:
        int_i-=1
    if int_i==1:
        return str_i[int_j-int_i]
    if int_j-int_i>=0:
        try:
            return str_i[int_j-int_i]+zhuo(int_i-1,int_j,str_i)
        except:
            pass
    return ''
def rou(str_i:str,int_j:int,int_i:int):
    if int_j+int_i>=len(str_i):
        int_i-=1
    if int_i==1:
        return str_i[int_j+int_i]
    if int_j+int_i<len(str_i):
        return rou(str_i,int_j,int_i-1)+str_i[int_j+int_i]
    return ''
def orientation(ExamineStrs:list,list_treainingSet):
    dict_features = dict()
    list_probability= list()
    for i in ExamineStrs:
        if i ==None:
            continue
        for j in list_treainingSet:

            # print(j.count(i))
            # time.sleep(1)
            try:
                dict_features = count_feature(str(j.count(i)),dict_features)
            except :
                continue
        if dict_features.get(str(j.count(i)))== len(list_treainingSet) and j.count(i)!=1:
                dict_features= {'0':1,'1':1}
        list_probability.append(dict_features.copy())
        dict_features.clear()
    return EntList(list_probability, len(list_treainingSet))
def nofollow(list_Ent,ExamineStrs):
    for i,j in zip(list_Ent,ExamineStrs):
        if len(list_Ent)!= len(ExamineStrs):
            print("长度不等")
            return ''
        if i ==0.0:
            continue
        else:
            ExamineStrs[ExamineStrs.index(j)]=None
    for i in range(len(ExamineStrs)*10):
        if ExamineStrs.count(None)>0:
            ExamineStrs.remove(None)
    for i in ExamineStrs:
        for j in ExamineStrs:
            if i!=j and i.count(j)>0 and len(i)>len(j):
                ExamineStrs.remove(j)
    return ExamineStrs
def Ent_recount (ExamineStrs,list_treainingSet):
    dict_features = dict()
    list_probability= list()
    for i in ExamineStrs:
        if i ==None:
            continue
        for j in list_treainingSet:
            # print(j.count(i))
            # time.sleep(1)
            if j.count(i)!=0 :
                try:
                    dict_features = count_feature(str(i),dict_features)
                except :
                    continue
            else:
                try:
                    dict_features = count_feature('not'+str(i),dict_features)
                except :
                    continue
        list_probability.append(dict_features.copy())
        dict_features.clear()
    return EntList(list_probability, len(list_treainingSet))
def createExamineStrs(str_str:str,int_js:int):
    set_ExamineStrs=set()
    int_cs =  len(str_str)
    for i in range(int_cs):
    #
    #     int_rad = random.randint(0, len(str_str)-1)
    #     # print(createExamineStr(str_str,int_rad,int_js))
        set_ExamineStrs.add(createExamineStr(str_str,i,int_js))
    #     # time.sleep(0.5)


    return list(set_ExamineStrs)
def createExamineStr(str_str, int_rad, int_w):
    if int_w==0:
        return str_str[int_rad+int_w]
    if int_rad+int_w<len(str_str):
        return createExamineStr(str_str,int_rad,int_w-1)+str_str[int_rad+int_w]


#   }
if __name__ == '__main__':

    str_Path = input("输入训练集绝对地址(.txt)")
    treaining_aids = {'tw':treaining_aids_tw(str_Path),'lw':treaining_aids_Lw(str_Path)}
    str_mod = input("输入训练模式（lw，tw）")
    str_re = treaining_aids[str_mod]
    print("训练出的正则表达式为："+str(str_re))
    while True:
        str_Path = input("输入待处理文件绝对地址(.txt):结束输入0")
        if str_Path==0 or str_Path=='0':
            break
        str_strs = open(str_Path,'r',encoding='utf-8').read()
        sdList = str_re.findall(str_strs)
        for st in sdList:
            s=''
            for t in st:
                s+=t
            print(s)
    pass

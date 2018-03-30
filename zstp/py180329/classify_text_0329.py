# -*- coding: utf-8 -*-
"""
通过训练好的模型，对投诉进行分类
"""

import pandas as pd
import numpy as np
import os
from sklearn.externals import joblib as jl
import time
import jieba, re
import jieba.posseg as pseg
import sys, unicodedata
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter

#数据和模型的存储地址
# main_path = os.path.abspath('.')
main_path='E:\workspalce\python\hello\zstp\py180208'
data_path = main_path+'\\data\\'  #数据保存地址
# model_path=os.main_path+'\\model\\'

#读取模型
def read_model(path=main_path):
    """
    加载已经训练好的模型
    :param path: 文件路径
    :return: 训练好的模型
    """
    t=jl.load(path+'\\tfidf.m') #tfidf模型
    com_chi2=jl.load(path+'\\select_feature.m')#刷选变量模型
    com_model=jl.load(path+'\\classify_svc.m')#分类模型
    return t,com_chi2,com_model


#读取数据
def read_data(path=main_path):
    """
    读取要处理的数据
    :param path: 数据存储地址
    :return: 返回读取的数据，数据框格式
    """
    headers = ['gd_id', 'description']
    dataset = pd.read_csv(path+'\\ldata.csv', header=None, encoding='gbk')#无标题的时候
    dataset.columns = headers
    # dataset=pd.read_csv(path+'\\ldata.csv',encoding='gbk') #有标题的时候用此行
    return dataset

#接受数据
def recive_data(texts):
    """
    从前端接收数据
    :param texts: 前端接收的数据
    :return: 返回数据框格式的数据，方便以后处理
    """
    text_array_des=[]
    text_array_label=[]
    for i in texts.split('*@*'):
        label,des=i.split()
        text_array_label.append(label)
        text_array_des.append(des)
    text_df=pd.DataFrame({'gd_id':text_array_label,'description':\
    text_array_des},columns=['gd_id', 'description'])
    return text_df


#处理数据
def dis_data(dataset):
    """
    处理现有数据
    :param dataset: 要处理的数据
    :return: 处理好的数据
    """
    dataset = dataset[dataset['description'].notnull()]
    dataset.index=range(len(dataset))

    #把投诉描述里面英文字母全部变成小写的
    dataset['text'] = dataset['description'].str.lower()

    #处理一些转换错误的词、同义词/近义词
    dict_path = main_path + '\\dict\\'
    f = open(dict_path + 'words_replace.txt', 'r', encoding='utf8')
    for line in f.readlines():
        value = line.strip().replace('\n','').split(',')
        dataset['text'] = dataset['text'].str.replace(value[0], value[1])

    #停用词
    stopwords_path = dict_path+'stopwords.txt'
    stop_set = set([value.replace('\n','') for value in open(stopwords_path, 'r', encoding='utf8').readlines()])

    userdict_path = dict_path+'word_dict.txt'
    jieba.load_userdict(userdict_path)

    flag_ls = ['a','ad','b','d','f','i','l','m','n','nrt','ns','nt','nz','v','vn','x']

    def pseg_cut(text):
        words = pseg.cut(text)
        return ' '.join([w.word for w in words if w.flag in flag_ls and w.word not in stop_set and len(w.word)>=2])

    dataset['cut'] = dataset['text'].map(pseg_cut)


    # 清洗用的正则表达式
    res = re.compile(r'\s+')
    red = re.compile(r'^(\d+)$')

    # 清洗标点符号等异常字符
    todel = dict.fromkeys(i for i in range(sys.maxunicode)
                          if unicodedata.category(chr(i)) not in ('Lu', 'Ll', 'Lt', 'Lo', 'Nd', 'Nl', 'Zs'))

    # 清洗分词结果的方法
    def cleantext(text):
        # try:
        #     text = unicode(text)
        # except:
        #     pass
        if text != '':
            return re.sub(res, ' ', ' '.join(map(lambda x: re.sub(red, '', x), text.translate(todel).split(' ')))).strip()
        else:
            return text


    # 对分词结果进行清洗
    dataset['cut_clean'] = dataset['cut'].map(cleantext)
    return dataset
def model_fit(dataset,t,con_chi2,com_model):
    """
    预测结果
    :param dataset: 数据
    :param t: tfidf的模型
    :param con_chi2: 刷选变量的文件
    :param com_model: 分类模型
    :return: 预测分类结果
    """

    features = t.transform(dataset['cut_clean'])
    features_chi2 = com_chi2.transform(features)
    predict_id = com_model.predict(features_chi2)
    return predict_id

def dict_df(array_df):
    """"
    将数据框装换成字典形式，表示每个投诉类型的个数。
    Arguments:
    array_df --Series格式数据

    returns:
    返回字典形式的
    """

    df_count=array_df.value_counts()
    dict_count={}
    i=len(df_count)
    for i in range(i):
        dict_count[i]={'name':df_count.index[i],'value':df_count[i]}
    return dict_count

def dict_out(df):
    """
    返回网页输出的json格式要求
    :param df: 数据框结构的数据
    :return: 网页输出要求的字典格式
    """
    out_dict={}
    list_dict=[]
    for i in range(len(df)):
        dict_id={}
        dict_id['id']=df['gd_id'][i]
        dict_id['description']=df['predict_label'][i]
        list_dict.append(dict_id)
    out_dict['rows']=list_dict
    out_dict['total']=len(df)
    return out_dict



if __name__=='__main__':
    # dataset=read_data()#加载数据
    texts = """e0100020170208082551 陪春他们家人旺中大叫受理怎么您这是一个水晶我看看就说说给给给他你说你说也好可以还还有这个工就是卖服务密码也是耳东路的一个是那那个意思然后我给发过来这行吧行好好好就买过那个顺的一个三百也是那种我给买号的工陶峰人民联系来呃也是刚怀璐唉对移动公司吗应该要连接吗南边事儿公分两百功能不好的还是需要一个工作日生风功能吗括弧写个诶这个是干嘛的ok八月份的时候再问哎咱们这个川二千彩虹路三百k对吗这个我一样是吗应该有哎就是推辞哎对是的哦我我中国不是很好啊他说他就是看看也他就是说是一个什么而且然异常然后桥路那个圣村哦的那就哦好对六六运作运的六也这个是什么时间办的他说也是突然经理呢环城南变了呃因为什么人民的连接老头儿清尔多肯定能弄完或者丰满的我今天在的时候可以把这封开通成功ssac春节是快速导航吗带的有因此来退也qxroip点呃连长以后不准嗯嗯但是高手我请说病了葡萄板车销售部营业厅应该是呃可是好的人民要补全说到玩去啊我应该名字的掀起来村现在没生效puk哎手机号码不知道参加了呃国明白口口买号随便高敏就是专门重复一下幺八七抱歉而且而且我朋友去跑解释哎那个钱肯定扣就怕你们的结果要不去没可以帮您催办一下啊开呃欧文的哎我就搞啊我就是所以说青岛哎喂号不穿说的旺去咱们这边确认啊啊刚才我看餐是吧转接ok现在怕骚扰按零好好嗯厚道赔十嗯所以我要么直接派单就可以哦恩恩爱产生的是哪个都可以打哪一些可能忘记了好像赔啊好的*@*
               e0100020170208114037	陪春那边标准王大报大交涉零好了他老家是一个地方水厅和城南局所以海ip刚才卖wifi它喂再看看嗯没完三幺六我隔天wifi他所这个呢呀人民这我还派所说的那么一个外来他说我的gprs呃给开怎么写也没有有在百米刚才一我告诉你哎不是这样那就拿可能麻烦你了啊喂哦哦就是说歌曲的他说这个位置呢器材不对应万信考试的歪了派出所或者三十八元二十四小时收嗯零嗯对佳就是应该是哪个字边一天劫机者应该去哪去号报出来哎我还有退出传说到南区的他肯定扣就怕他们的wifi随便药品ok挺好的嗯区当铺啊就开始赔付他私聊和iphok刚刚嗯s产生的是前两天可以打哪一些平常玩具好的*@*
               e0100020170208132815	啊回春那么家人旺费哦大众销售然后呢看到这些地方自己听我昨天来积分于啊他们所以那个我这是在在其他海盐喂刚才复印证的那我来非得区的有什么危险这个确实呢呃买了有引起的小强能不能一二是五百四十号是湾优那你呃就是一直在长那么下来开机耳机买的推进并开机玩喜龙南坊催南嗯cc嗯拨管吗能有哎推复兴中路幺二十五号吗幺幺零流量包工呃买这就说嘛他挺应该是应该是inaskid就是比我停的朋友问那三十个是闺查是流水声参数的最后一个箱子呃我叫上飞起来啊教程应该是确认是吧不知道吗下一点呃杰陪们车子可能要收收给我品有没有讯的呃有查出一下接电话希望你们头痛呃哎我还可以去传所以完全完全肯定扣就怕去两条开嗯已经是显示的给我呀结果还要赔去六s的肯定清哦现在还没是一条培育走完起来我穿梭打完去远登记的是f盘说的是哪个珀塞那一些呢湾湾区阿飞穿是的赔付开始医疗费哎配一下六而且也有好的本金现在维修家*@*
               e0100220170207091641	尊敬的星级客户您好七八一一话务员为您服务您好工号很高兴为您服务可以帮您哎你好到我这边这个网络没没网络怎么回事不好意思给你添麻烦了先生请问一下您的网络号码能告诉我一下吗或者电话之类的也行哦三六三八三六幺六六幺三八三六幺六请稍等一下先生人民是的这边的话把您这个牡丹重新启动一下试试看呢嗯试过了已经试过了是吧那这边的话您稍等一下我不要挂机我现在为您转接一下我们的维修部还是显示不做一下检查如果转接但是的话您可以通过九六九幺幺二直接报修或者平时关注微信平台自助报障也行"""
    dataset=recive_data(texts)
    t,com_chi2,com_model=read_model()#加载模型
    dataset=dis_data(dataset) #处理数据
    predict_id=model_fit(dataset,t,com_chi2,com_model)#预测问题分类
    dataset['predict_label'] = predict_id#预测标签列
    # for i in range(len(dataset)):#打印预测结果
    #     print('%s 投诉的是  %s 问题' % (dataset['gd_id'][i], dataset['predict_label'][i]))
    dict_freq=dict_df(dataset['predict_label'])    #返回字典形式的投诉类别的种类
    print(dict_freq)
    out_data=dict_out(dataset)
    print(out_data)




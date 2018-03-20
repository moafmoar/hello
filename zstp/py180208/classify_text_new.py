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

#数据和模型的存储地址
# main_path = os.path.abspath('.')
main_path='E:\workspalce\python\hello\zstp\py180208'
data_path = main_path+'\\data\\'  #数据保存地址
# model_path=os.main_path+'\\model\\'

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
    dataset=pd.read_csv(path+'\\ldata.csv',encoding='gbk')
    return dataset
# dataset = pd.read_csv(data_path+'record_info.txt', header=None, encoding='utf8')
# dataset.columns = headers

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


if __name__=='__main__':
    dataset=read_data()#加载数据
    t,com_chi2,com_model=read_model()#加载模型
    dataset=dis_data(dataset) #处理数据
    predict_id=model_fit(dataset,t,com_chi2,com_model)#预测问题分类
    dataset['predict_label'] = predict_id#预测标签列
    for i in range(len(dataset)):#打印预测结果
        print('%s 投诉的是  %s 问题' % (dataset['gd_id'][i], dataset['predict_label'][i]))


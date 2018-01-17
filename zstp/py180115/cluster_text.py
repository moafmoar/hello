""""
聚类脚本
"""

import jieba
import os
import re
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

path='c:\\work\\jpy'
filepath='c:\\work\\jpy\\cdata'




def read_stopword(path=path):
    """
    读取停用词，返回停用词列表
    :param path: 停用词路径
    :return: 返回停用词列表
    """
    path=path+'\\stopwords.txt'
    stopwords=[]
    with open(path,'r',encoding='utf-8') as rf:
        for f in rf.readlines():
            stopwords.append(f.strip())
    return stopwords

def readtext(path):
    """
    读取相应文档
    :param path:
    :return:返回文档字符串
    """
    with open(path,'rb') as rf:
        textdata=rf.read()
    # p=re.compile('\s+')
    # text_data=re.sub(p,'',textdata)
    return textdata

def word_cut(text,stopwords):
    """
    文本分词，并去除停用词
    :param text:文本字符串
    :param stopwords:停用词列表
    :return:分词后的列表
    """
    # for word in jieba.cut(text):
    #     if word in stopwords:
    #         continue
    #     else:
    #         words=" ".join(word)
    words=" ".join([wd.strip('\r\n') for wd in jieba.cut(text) if wd not in stopwords])
    # words=[word for word in jieba.cut(text) if word not in stopwords]
    return words

def readfile(stopwords,path=filepath):
    """
    读取预料库，返回文档矩阵，行为文档，列为词
    :param stopwords:停用词
    :param path:语料的目录
    :return:doc_matrix文档矩阵，多层数组结构
    :return:filename 文件名列表
    """
    filenames=[os.path.join(path,f) for f in os.listdir(filepath)]
    filetexts=[readtext(path) for path in filenames]
    docs=[]
    word_set=set([])
    for file in filetexts:
        doc=word_cut(file,stopwords)
        docs.append(doc)
    filename=[name.split('\\')[-1].split('.')[0] for name in filenames]

    return docs,filename
def readlinetext(path,stopwords):
    """
    读取文档，转换成语料
    :param path:文件路径
    :param stopwords:停用词
    :return:语料列表
    """
    path=path+'\\results.txt'   #将分类的文本储存在一个文件里边，每行是一个文档
    corpus=[]
    fdata=open(path,'r')
    for line in fdata:
        words = " ".join([wd.strip('\r\n') for wd in jieba.cut(text) if wd not in stopwords])
        corpus.append(words)
    return corpus



def sk_tfidf(doc_list,alpha_min=0.05,alpha_max=0.8):
    """
    计算tfidf矩阵
    :param doc_list: 语料列表
    :param alpha_min:词频最小阈值
    :param alpha_max 词频最大阈值
    :return: tfidf矩阵
    """
    vectorizer=CountVectorizer(min_df=alpha_min,max_df=alpha_max)
    transformer=TfidfTransformer()
    tfidf=transformer.fit_transform(vectorizer.fit_transform(doc_list))
    word=vectorizer.get_feature_names()
    tfidf_mat=tfidf.toarray()
    return tfidf_mat

def text_kmeans(tfidf_mat,k=6):
    """
    聚类，返回类号和与类中心的欧式距离之和
    :param tfidf_mat:tfidf矩阵
    :param k:聚类数目
    :return:聚类类标号、与类中心距离之和
    """
    clf=KMeans(n_clusters=k)
    result_kmean=clf.fit(tfidf_mat)
    n,m=tfidf_mat.shape
    labels=dict()
    for i in range(n):
        labels[i]=clf.labels_[i]
    # print(clf.inertia_)
    return labels,clf.inertia_


def get_labels(filenames,label):
    """
    将类标号与文件对应起来
    :param filenames: 文件名列表
    :param label: 类标号
    :return: 文件名对应类标号的字典
    """
    label_dict=dict()
    for key,value in label.items():
        label_dict[filenames[key]]=value
    return label_dict







if __name__=='__main__':
    path = 'c:\\work\\jpy'
    filepath = 'c:\\work\\jpy\\cdata'
    stopwords=read_stopword(path=path)         #读取停用词字典
    docs_list,filenames=readfile(stopwords,path=filepath)  #获得分词后的列表
    # print(docs_list)
    tfidf=sk_tfidf(docs_list)  #转换tfidf矩阵

    # print(tfidf)
    # print(tfidf.shape)
    # labels=text_kmeans(tfidf)
    # print(labels)
    # dict_label=get_labels(filenames,labels)
    # print(dict_label)
    erros=[0]*15 #存放类与类中心的距离
    for k  in range(2,17):
        print(k)
        label,erros[k-2]=text_kmeans(tfidf,k)
        dict_label=get_labels(filenames,label)
        print(dict_label)

    plt.plot(range(2,17),erros)    #聚类个数与类与中心距离关系
    plt.show()





































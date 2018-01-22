"""
对分词进行词性标注
"""
import jieba
import os
import numpy as np
import jieba.posseg as pseg
import pandas as pd

path='F:\\easestar\\zstp20180109' #文件存放目录

def read_stopword(path=path):
    """
    读取停用词
    :param path: 文件目录
    :return: 停用词列表
    """
    path=path+'\\stopwords.txt'
    stopwords=[word.strip('\n') for word in open(path,'r',encoding='utf-8').readlines()]
    return stopwords

def readtext(path=path):
    """
    读取文本，并存储在列表内
    :param path:文件路径
    :return:保存文件的列表
    """
    path=path+'\\test.txt'
    # texts=[text.strip('\n').strip() for text in open(path,'r',encoding='gbk').read()]
    texts=open(path,'r',encoding='utf-8').read().strip('/n').strip()
    return texts

def pseg_cut(text,stopwords=None):
    """
    给定文本进行分词，标注。返回分词和词性数据框
    :param text:字符串
    :return:分词结果和词性列表
    """
    words=[(word,pseg) for word,pseg in pseg.cut(text) if word not in stopwords
           and word !='\n']
    df_word=pd.DataFrame({'word':[words[i][0] for i in range(len(words))],
                          'class':[words[i][1] for i in range(len(words))]},
                         columns=['word','class'])
    return df_word

if __name__=='__main__':
    stopwords=read_stopword()
    texts=readtext()
    # print(texts)
    # words=[pseg_cut(text,stopwords=stopwords) for text in texts]
    words=pseg_cut(texts,stopwords=stopwords)
    print(words)

    # for word in words:
    #     # print(np.shape(word))
    #     if word ==[]:
    #         continue
    #     else:
    #         print(word)


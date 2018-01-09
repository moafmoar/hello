"""
词频统计
"""
import jieba
import numpy as np
from collections import  Counter
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
# jieba.add_word('供给侧')

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
    texts=open(path,'r',encoding='utf-8').read()
    return texts.strip('\n').strip()
def word_count(text,stopword,k=10):
    """
    读取字符串，返回单词和频率数据框,字典结构
    :param text:
    :param stopword:
    :param k 词频排名前k位的
    :return:返回词和频数的数据框
    """
    word_count=dict()
    # word=[]
    words=[wd.strip() for wd in jieba.cut(text) if wd not in stopword and wd!='\n' and wd!='\d']
    for word in words:
        if word not in word_count:
            word_count[word]=1
        else:
            word_count[word] += 1
    # print(Counter(word))
    word_count = sorted(word_count.items(), key=lambda d: d[1], reverse=True)
    word_count1=word_count[:k]
    word_dict=dict(word_count1)
    df_word=pd.DataFrame({'word':[word_count1[i][0]  for i in range(len(word_count1))  ],'freq':[
        word_count1[i][1] for i in range(len(word_count1))
    ]},columns=['word','freq'])

    return df_word,word_dict

def cloud_word(word_freq):
    """
    输入词频字典，返回词云图
    :param word_freq: 词频字典
    :return: 词云图
    """
    word_cloud=WordCloud(font_path = "F:\\easestar\\zstp20180109\\MSYH.TTF",
        background_color='black',max_words=100,
                         max_font_size=100,
                         random_state=42,
                         width=800, height=600)
    word_cloud.generate_from_frequencies(word_freq)
    # cut_text=jieba.cut(text)
    # result='/'.join(cut_text)
    plt.imshow(word_cloud)
    plt.axis('off')
    plt.show()


if __name__=='__main__':
    stopword=read_stopword()
    text=readtext()
    df,word_dict=word_count(text=text,stopword=stopword,k=50)
    print(df)
    #cloud_word(word_dict)




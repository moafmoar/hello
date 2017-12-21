"""
step 0 : 导入相关安装包 & 相关词库
"""
# -*- coding: utf-8 -*-
from collections import defaultdict
import os
import re
import jieba
import codecs
import sys

# 修改各词库的路径
stopword_path = 'E:/workspalce/python/hello/txt/stopwords_1.txt'
degreeword_path = 'E:/workspalce/python/hello/txt/degreewords_1.txt'
sentimentword_path = 'E:/workspalce/python/hello/txt/BosonNLP_sentiment_score_1.txt'

# 加载新词库
jieba.load_userdict('E:/workspalce/python/hello/txt/stock_dict.txt')

# 停用词列表
stopword_file = open(stopword_path, "r",encoding='UTF-8').readlines()
stopwords = [word.replace("\n", "") for word in stopword_file]

# 否定词表
notword = [u'不', u'没', u'无', u'非', u'莫', u'弗', u'勿', u'毋', u'未', u'否', u'别', u'無', u'休', u'难道']

# 程度词表
degreeword_file = open(degreeword_path,'r',encoding='UTF-8').readlines()
degree_dict = {}
for word in degreeword_file:
    word = word.replace("\n", "").split(" ")
    degree_dict[word[0]] = word[1]

# 情感词表
"""
sentimentword_file = open(sentimentword_path, encoding='utf-8').readlines()
sentiment_dict = {}
for word in sentimentword_file:
    word = word.replace("\n","").split(" ")
    sentiment_dict[word[0]] = word[1]
"""
sentimentword_file = open(sentimentword_path,'r',encoding='UTF-8').readlines()
sentiment_dict = {}
for word in sentimentword_file:
    word = word.replace("\n", "").split(",")
    word_sen = word[0].split()
    # print("["+word_sen[0]+":"+word_sen[1]+"]")
    sentiment_dict[word_sen[0]] = word_sen[1]
print("Great!We have loaded all word lists!")

"""
step 1 : 分词且去除停用词
"""
def sent2wordloc(sentence):
    wordlist = []
    wordloc = {}
    # wordlist = [word for word in jieba.cut(sentence) if word not in stopwords]
    wordlist = [word for word in jieba.cut(sentence)]
    wordloc = {word:loc for loc, word in enumerate(wordlist)}
    return wordlist,wordloc
# print("The function sent2word is defined")

# print(sent2wordloc("你好！我惊天非常生气！"))

"""
step 2 : 针对分词结果，定位情感词、否定词及程度词
"""
def wordclassify(sentence):
    wordlist, wordloc = sent2wordloc(sentence)
    sentimentloc, notloc, degreeloc, othersloc = {}, {}, {}, {}
    for word in wordloc.keys():
        if word in sentiment_dict.keys() and word not in notword and word not in degree_dict.keys():
            sentimentloc[wordloc[word]] = sentiment_dict[word]
        elif word in notword and word not in degree_dict.keys():
            notloc[wordloc[word]] = -1
        elif word in degree_dict.keys():
            degreeloc[wordloc[word]] = degree_dict[word]
        else:
            othersloc[wordloc[word]] = 0
    sentimentloc = sorted(sentimentloc.items(), key=lambda x:x[0])
    return sentimentloc, notloc, degreeloc, othersloc, wordlist, wordloc
# print("The function wordclassify is defined")

# print(wordclassify("尼玛阿! 燊很生气！"))


"""
step 3 : 情感打分
"""
def sentscore(sentence):
    sentimentloc, notloc, degreeloc, othersloc, wordlist, wordloc = wordclassify(sentence)
    w = 1
    score = 0
    for i in range(len(sentimentloc)):
        wl = list(sentimentloc[i])[0]
        ww = list(sentimentloc[i])[1]
        score += w*float(ww)
        if i < (len(sentimentloc)-1):
            for j in range(wl+1,list(sentimentloc[i+1])[0]):
                if j in notloc.keys():
                    w *= -1
                elif j in degreeloc.keys():
                    w *= float(degreeloc[j])
    return score
# print("The function sentscore is defined")
# test
# a, b  = sent2wordloc("这个事情非常难做，我非常非常不开心")
# print(a)
# print(b)

# print(sentscore("这个事情非常难做，我非常非常不开心."))

if __name__ == '__main__':
    keywords = sys.argv[1]
    testresult = sentscore(keywords)
    print('%.5f'%testresult)

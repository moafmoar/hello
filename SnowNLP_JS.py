
# -*- coding: utf-8 -*-
from snownlp import SnowNLP
import json
from flask import Flask, render_template, request, jsonify,Response
#from collections import defaultdict
#import os
#import re
#import jieba
import jieba, re
#import codecs
#import configparser
#===================================
import numpy as np
from collections import Counter
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba.posseg as pseg
import sys, unicodedata
import datetime

app = Flask(__name__)
@app.route('/') #如果有多个方法，需要添加该改注解
@app.route('/getfunc', methods=['POST', 'GET'])
def getfunc():
    #data = json.loads(request.form.get('data'))
    # resp = Response(data)
    #Response.headers['Access-Control-Allow-Origin'] = '*'
    # data = json.loads(request.get_json())
    # story_data = json.loads(request.get_data().decode('utf-8'))
    #context = data['lesson']
    jsonp_callback = request.args.get('callback', 'jsonpCallback1') # 这里的callback对应的值需要和ajax请求的callback保持一致。
    context = request.values['content']
    print(context)
    s = SnowNLP(context)
    '''
    s = SnowNLP("是不是还不是就这样子了，完全不行，我觉得这车完全不行！")
    '''
    arry = []
    '''' for sentence in s.sentences:
     #print(sentence)
     '''
    '''
    s0 = SnowNLP(s.sentences[0])
    s1 = SnowNLP(s.sentences[1])
    s2 = SnowNLP(s.sentences[2])
    s3 = SnowNLP(s.sentences[3])
    s4 = SnowNLP(s.sentences[4])
    '''
    _snownlpNum = 0
    for k in s.sentences:
        print(k)
        _snownlpvalue = SnowNLP(k)
        print(_snownlpvalue.sentiments)
        arry.insert(_snownlpNum, _snownlpvalue.sentiments)
        _snownlpNum + 1

    '''
        print(s0.sentiments)
        print(s1.sentiments)
        print(s2.sentiments)
        print(s3.sentiments)
        print(s4.sentiments)
        arry.insert(0,s0.sentiments)
        arry.insert(1,s1.sentiments)
        arry.insert(2,s2.sentiments)
        arry.insert(3,s3.sentiments)
        arry.insert(4,s4.sentiments)
        print(arry)
        s2 = SnowNLP(sentence[1])
        print("s2:"+s2.sentiments)
    '''
    positive = []
    negative = []
    value = 0
    value1 = 0
    num = 0
    for i in arry:
        # print(i)
        if (i < 0.5):
            print("负面词：" + str(i))
            value += i
            positive.insert(num, i)
            num + 1
        elif (i > 0.5):
            print("正面词：" + str(i))
            value1 += i
            negative.insert(num, i)
            num + 1

    # ("负面词结果:" + str(value / 2))
    # print("正面词结果:" + str(value1 / 3))
    # print("正面词结果1:" + str((0.8342 + 0.8584 + 0.6251) / 3))
    # print("负面词结果1:" + str((0.3280 + 0.3281) / 2))
    print(negative)
    print(positive.__len__())
    print(positive)
    # _result_positive = 0
    # np.positive()
    _result_positive = sum(positive)
    _result_negative = sum(negative)
    '''
    print(_result_positive/positive.__len__())
    print(_result_negative/negative.__len__())

    print(_result_positive)
    print(_result_negative)
    '''
    print(_result_positive / (_result_positive + _result_negative))
    print(_result_negative / (_result_positive + _result_negative))
    '''
    _data_result1 = [{"_result_positive": _result_positive / (_result_positive + _result_negative),
                      "_result_negative": _result_negative / (_result_positive + _result_negative)},
                     {"_result_positive_len": positive.__len__(),
                      "_result_negative_len": negative.__len__()}]
    _data_result = {"_result_positive":_result_positive/(_result_positive+_result_negative),"_result_negative":_result_negative/(_result_positive+_result_negative)}
    '''
    # print('%.5f'%(0.555555555))

    jsondate = {'_result_positive':'%.5f'%(_result_positive / (_result_positive + _result_negative)),
                    '_result_negative' :'%.5f'%(_result_negative / (_result_positive + _result_negative)),
                    '_result_positive_len':positive.__len__(),
                    '_result_negative_len':negative.__len__()}
    return Response( # return的时候需要通过response返回数据并且将callback一并返回给客户端，这样才能请求成功。
            "%s(%s);" % (jsonp_callback, json.dumps({'ok': True, 'data': jsondate})),
            mimetype="text/javascript"
        )
# ----------------------------------------------------- 以上为SnowNLP分词并处理的结果 ----------------------------------------------

def __init__():
    # print("sdsdfsf")
    # 修改各词库的路径
    stopword_path = 'E:/workspalce/python/hello/txt/stopwords_1.txt'
    degreeword_path = 'E:/workspalce/python/hello/txt/degreewords_1.txt'
    sentimentword_path = 'E:/workspalce/python/hello/txt/BosonNLP_sentiment_score_1.txt'

    # 加载新词库
    jieba.load_userdict('E:/workspalce/python/hello/txt/stock_dict.txt')

    # 停用词列表
    stopword_file = open(stopword_path, "r", encoding='UTF-8').readlines()
    stopwords = [word.replace("\n", "") for word in stopword_file]

    # 否定词表
    notword = [u'不', u'没', u'无', u'非', u'莫', u'弗', u'勿', u'毋', u'未', u'否', u'别', u'無', u'休', u'难道']

    # 程度词表
    degreeword_file = open(degreeword_path, 'r', encoding='UTF-8').readlines()
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
    sentimentword_file = open(sentimentword_path, 'r', encoding='UTF-8').readlines()
    sentiment_dict = {}
    for word in sentimentword_file:
        word = word.replace("\n", "").split(",")
        word_sen = word[0].split()
        # print("["+word_sen[0]+":"+word_sen[1]+"]")
        sentiment_dict[word_sen[0]] = word_sen[1]
    print("Great!We have loaded all word lists!")
    return degree_dict,degree_dict

'''
# 修改各词库的路径
stopword_path = 'E:/workspalce/python/hello/txt/stopwords_1.txt'
degreeword_path = 'E:/workspalce/python/hello/txt/degreewords_1.txt'
sentimentword_path = 'E:/workspalce/python/hello/txt/BosonNLP_sentiment_score_1.txt'

# 加载新词库
jieba.load_userdict('E:/workspalce/python/hello/txt/stock_dict.txt')

# 停用词列表
stopword_file = open(stopword_path, "r", encoding='UTF-8').readlines()
stopwords = [word.replace("\n", "") for word in stopword_file]

# 否定词表
notword = [u'不', u'没', u'无', u'非', u'莫', u'弗', u'勿', u'毋', u'未', u'否', u'别', u'無', u'休', u'难道']

# 程度词表
degreeword_file = open(degreeword_path, 'r', encoding='UTF-8').readlines()
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
sentimentword_file = open(sentimentword_path, 'r', encoding='UTF-8').readlines()
sentiment_dict = {}
for word in sentimentword_file:
    word = word.replace("\n", "").split(",")
    word_sen = word[0].split()
    # print("["+word_sen[0]+":"+word_sen[1]+"]")
    sentiment_dict[word_sen[0]] = word_sen[1]
print("Great!We have loaded all word lists!")
'''
"""

step 1 : 分词且去除停用词
"""

def sent2wordloc(sentence):
    wordlist = []
    wordloc = {}
    # wordlist = [word for word in jieba.cut(sentence) if word not in stopwords]
    wordlist = [word for word in jieba.cut(sentence)]
    wordloc = {word: loc for loc, word in enumerate(wordlist)}
    return wordlist, wordloc

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
    sentimentloc = sorted(sentimentloc.items(), key=lambda x: x[0])
    return sentimentloc, notloc, degreeloc, othersloc, wordlist, wordloc

# print("The function wordclassify is defined")

# print(wordclassify("尼玛阿! 燊很生气！"))


"""
step 3 : 情感打分
"""
@app.route('/sentscore', methods=['POST', 'GET'])
def sentscore():
    jsonp_callback = request.args.get('callback', 'jsonpCallback1')  # 这里的callback对应的值需要和ajax请求的callback保持一致。
    sentence = request.values['content']
    sentimentloc, notloc, degreeloc, othersloc, wordlist, wordloc = wordclassify(sentence)
    w = 1
    score = 0
    for i in range(len(sentimentloc)):
        wl = list(sentimentloc[i])[0]
        ww = list(sentimentloc[i])[1]
        score += w * float(ww)
        if i < (len(sentimentloc) - 1):
            for j in range(wl + 1, list(sentimentloc[i + 1])[0]):
                if j in notloc.keys():
                    w *= -1
                elif j in degreeloc.keys():
                    w *= float(degreeloc[j])
    return Response( # return的时候需要通过response返回数据并且将callback一并返回给客户端，这样才能请求成功。
        "%s(%s);" % (jsonp_callback, json.dumps({'ok': True, 'data': score})),
        mimetype="text/javascript"
    )

@app.route('/test',methods=['POST','GET'])
def test():
    jsonp_callback = request.args.get('callback', 'jsonpCallback1')  # 这里的callback对应的值需要和ajax请求的callback保持一致。
    print("测试调用方式");
    return Response(  # return的时候需要通过response返回数据并且将callback一并返回给客户端，这样才能请求成功。
        "%s(%s);" % (jsonp_callback, json.dumps({'ok': True, 'data': "调用成功"})),
        mimetype="text/javascript")

'''
词频统计功能
'''
@app.route('/word_count',methods=['POST','GET'])
def word_count(k=10):
    '''
     读取字符串，返回单词和频率数据框,字典结构
    :param text:
    :param stopword:
    :param k 词频排名前k位的
    :return:返回词和频数的数据框
    '''
    jsonp_callback = request.args.get('callback', 'jsonpCallback1')  # 这里的callback对应的值需要和ajax请求的callback保持一致。
    #text = '读取字符串，返回单词和频率数据框,字典结构'
    text = request.values['text']
    print(text)
    path = 'F:\\easestar\\zstp20180109\\stopwords.txt'
    stopword = [word.strip('\n') for word in open(path, 'r', encoding='utf-8').readlines()]
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

    '''
    df_word=pd.DataFrame({'word':[word_count1[i][0]  for i in range(len(word_count1))],
                          'freq':[word_count1[i][1] for i in range(len(word_count1))]},columns=['word','freq'])
    '''
    #return df_word,word_dict
    return Response(  # return的时候需要通过response返回数据并且将callback一并返回给客户端，这样才能请求成功。
        "%s(%s);" % (jsonp_callback, json.dumps({'ok': True, 'data': word_dict},ensure_ascii=False)),
        mimetype="text/javascript")


################################################ 180122_new word_count_new start #########################################################################
@app.route('/word_count_new',methods=['POST','GET'])
def word_count_new(k=10):
    '''
     读取字符串，返回单词和频率数据框,字典结构
    :param text:
    :param stopword:
    :param k 词频排名前k位的
    :return:返回词和频数的数据框
    '''
    jsonp_callback = request.args.get('callback', 'jsonpCallback1')  # 这里的callback对应的值需要和ajax请求的callback保持一致。
    #text = '读取字符串，返回单词和频率数据框,字典结构'
    text = request.values['text']
    print(text)
    path = 'F:\\easestar\\zstp20180109\\stopwords.txt'
    stopwords = [word.strip('\n') for word in open(path, 'r', encoding='utf-8').readlines()]

    # word=[]
    # words=[wd.strip() for wd in jieba.cut(text) if wd not in stopword and wd!='\n' and wd!='\d']
    '''
    for word in words:
        if word not in word_count:
            word_count[word]=1
        else:
            word_count[word] += 1
    # print(Counter(word))
    word_count = sorted(word_count.items(), key=lambda d: d[1], reverse=True)
    word_count1=word_count[:k]
    word_dict=dict(word_count1)
    '''
    #df1 = pseg_cut(text, stopwords=stopword)
    '''
     第一步：pseg_cut
    '''
    words = [(word, pseg) for word, pseg in pseg.cut(text) if word not in stopwords
             and word != '\n' and word != '\d']

    df_word1 = pd.DataFrame({'word': [words[i][0] for i in range(len(words))],
                            'class': [words[i][1] for i in range(len(words))]},
                           columns=['word', 'class'])
    df_word1 = df_word1.drop_duplicates()
    '''
     第二步：word_count2
    '''
    #df2, word_dict = word_count2(text, stopword,10)
    word_count = dict()
    # word=[]
    words2 = [wd.strip() for wd in jieba.cut(text) if wd not in stopwords and wd != '\n' and wd != '\d']
    for word in words2:
        if word not in word_count:
            word_count[word] = 1
        else:
            word_count[word] += 1
    # print(Counter(word))
    word_count = sorted(word_count.items(), key=lambda d: d[1], reverse=True)
    if k is not None:
        word_count1 = word_count[:k]
    else:
        word_count1 = word_count

    word_dict = dict(word_count1)
    df_word2 = pd.DataFrame({'word': [word_count1[i][0] for i in range(len(word_count1))], 'freq': [
        word_count1[i][1] for i in range(len(word_count1))
    ]}, columns=['word', 'freq'])

    '''
     第三步：merge_df
    '''
    #df = merge_df(df2, df1)
    df_word = pd.merge(df_word2, df_word1)
    df_word.index = range(len(df_word))
    df_word['out'] = df_word['word'] + '/' + df_word['class'] + '/' + df_word['freq'].astype(str)

    '''
     第四步：color_df
    '''
    df_cl = color_df(df_word)

    '''
     第五步：dict_df
    '''
    df_dict = dict_df(df_cl)  # 你们需要调用的字典形式的返回文件

    print(len(df_dict))
    dataMap = []
    for key, valuein in df_dict.items():
        print(key, valuein)
        #dataMap.insert(key,valuein)
        #dataMap.values(valuein)
        dataMap.append(valuein)

    '''
    df_word=pd.DataFrame({'word':[word_count1[i][0]  for i in range(len(word_count1))],
                          'freq':[word_count1[i][1] for i in range(len(word_count1))]},columns=['word','freq'])
    '''
    #return df_word,word_dict
    return Response(  # return的时候需要通过response返回数据并且将callback一并返回给客户端，这样才能请求成功。
        "%s(%s);" % (jsonp_callback, json.dumps({'ok': True, 'data': str(dataMap)},ensure_ascii=False)),
        mimetype="text/javascript")

def pseg_cut(text,stopwords):
    """
    给定文本进行分词，标注。返回分词和词性数据框
    :param text:字符串
    :return:分词结果和词性列表
    """
    words=[(word,pseg) for word,pseg in pseg.cut(text) if word not in stopwords
           and word !='\n' and word !='\d']


    df_word=pd.DataFrame({'word':[words[i][0] for i in range(len(words))],
                          'class':[words[i][1] for i in range(len(words))]},
                         columns=['word','class'])
    df_word=df_word.drop_duplicates()

    return df_word
def word_count2(text,stopword,k):
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
    if k is not None:
       word_count1=word_count[:k]
    else:
        word_count1 = word_count

    word_dict=dict(word_count1)
    df_word=pd.DataFrame({'word':[word_count1[i][0]  for i in range(len(word_count1))  ],'freq':[
        word_count1[i][1] for i in range(len(word_count1))
    ]},columns=['word','freq'])

    return df_word,word_dict

def merge_df(df_word,df_count):
    df_word=pd.merge(df_word,df_count)
    df_word.index=range(len(df_word))
    df_word['out']=df_word['word']+'/'+df_word['class']+'/'+df_word['freq'].astype(str)

    return df_word


def color_df(df_word):
    """"
    返回每个词性对应的颜色的数据框
    """
    color={
	   'n'   : "#ff8000" ,
	   'nr'  :"#FFF68F" ,
	   'nr1' :"#FFEFD5"  ,
	   'nr2' : "#FFE4E1" ,
	   'nrj' : "#FFDEAD" ,
	   'nrf' : "#FFC1C1" ,
	   'ns'  : "#FFB90F" ,
	   'nsf' : "#FFA54F" ,
	   'nt'  : "#FF34B3" ,
	   'nz'  :"#FF8C00"  ,
	   'nl'  :"#FF7F50"  ,
	   'ng'  :"#FF6EB4"  ,
	   'l'   : "#ff8000" ,
	   'eng'  :"#FF0080"  ,
	   't'   : "#FF4500" ,
	   'tg' : "#FF3030"  ,
	   's'  : "#aaaaff"  ,
	   'f'  : "#97cbff"  ,
	   'v'  : "#0080ff"  ,
	   'vd' : "#C1CDCD"  ,
	   'vn' : "#BFEFFF"  ,
	   'an' : "#BDBDBD"  ,
	  'vyou': "#BC8F8F"  ,
	   'vf' : "#B9D3EE"  ,
	   'vx' : "#B5B5B5"  ,
	   'vi' : "#B3EE3A"  ,
	  'vl'  : "#B22222"  ,
	  'vg'  : "#B23AEE"  ,
	   'a'  : "#deffac"  ,
	   'ad' : "#8B795E"  ,
	  'vshi': "#8B6969"  ,
	   'ag' : "#7EC0EE"  ,
	   'al' : "#7CFC00"  ,
	   'b'  : "#ffb5b5"  ,
	   'bl' : "#6B8E23"  ,
	   'z'  : "#e2c2de"  ,
       'zg' : "#e2c2de",
	   'r'  : "#00EEEE"  ,
	   'rr' : "#c1ffe4"  ,
	   'vz' : "#c1ffe4"  ,
	   'rzt': "#008B8B"  ,
	   'rzs': "#00688B"  ,
	   'rzv': "#27408B"  ,
	   'ry' : "#218868"  ,
	   'ryt': "#20B2AA"  ,
	   'rys': "#2E8B57"  ,
	   'ryv': "#228B22"  ,
	   'rg' : "#218868"  ,
	   'rz' : "#548B54"  ,
	   'm'  : "#6C7E92"  ,
	   'mq' :"#0000CD"   ,
	   'q'  : "#a3d1d1"  ,
	   'qv' : "#0000EE"  ,
	   'qt' : "#ca8eff"  ,
	   'd'  : "#b8b8dc"  ,
	   'p'  : "#ffd9ec"  ,
	   'pba': "#00FA9A"  ,
	   'pbei': "#00F5FF" ,
	   'c'  : "#ffe6d9"  ,
	   'cc' : "#00EE76"  ,
	   'u'  : "#d9b3b3"  ,
	   'ul' : "#d9b3b9"  ,
	   'uzhe': "#00E5EE" ,
	   'ule' : "#00CED1" ,
	   'uguo': "#00CD66" ,
	   'ude1': "#8B2252" ,
	   'ude2': "#8B008B" ,
	   'ude3': "#8968CD" ,
	   'usuo': "#878787" ,
	  'udeng': "#838B8B" ,
	   'uyy' : "#7FFFD4" ,
	   'udh' : "#7D9EC0" ,
	   'uls' : "#7CCD7C" ,
	   'uzhi': "#7A7A7A" ,
	  'ulian': "#708090" ,
	   'uj'  : "#8080FF" ,
	   'uv'  : "#B0E11E" ,
	   'uz'  : "#00FF80" ,
	   'i'   : "#408080" ,
	   'j'   : "#566CA9" ,
	   'ug'  : "#408080" ,
	   'dg'  : "#408080" ,
	   'e'   : "#cdcd9a" ,
	   'y'   : "#9f35ff" ,
	   'o'   : "#ffed97" ,
	   'h'   : "#ffbfff" ,
	   'k'   : "#84c1ff" ,
	   'x'   : "#bbffbb" ,
	   'xs'  : "#000080" ,
	   'xm'  : "#008B45" ,
	   'xu'  : "#006400" ,
	   'xe'  : "#EE2C2C" ,
	   'w'   : "#bebebe" ,
	   'wkz' : "#6495ED" ,
	   'wky' : "#607B8B" ,
	   'wyz' : "#5CACEE" ,
	   'wyy' : "#575757" ,
	   'wj'  : "#528B8B" ,
	   'ww'  : "#483D8B" ,
	   'wt'  : "#458B74" ,
	   'wd'  : "#436EEE" ,
	   'wf'  : "#3A5FCD" ,
	   'wn'  : "#2F4F4F" ,
	   'wm'  : "#20B2AA" ,
	   'ws'  : "#1C86EE" ,
	   'wp'  : "#1874CD" ,
	   'wb'  : "#104E8B" ,
	   'wh'  : "#00FF7F" ,
'userDefine' : "#0080FF"
	}
    df_word['color']=list(map(lambda x:color[x],df_word['class']))
    df_word['ind']=list(range(len(df_word)))
    return df_word

def dict_df(df_word):
    """
    返回要求的字典形式
    :param df_word: 词频、词性数据框
    :return: 返回字典形式
    """
    df_dict={}
    for i in range(len(df_word)):
        x=df_word.loc[i,:]
        if x['ind'] not in df_dict:
            df_dict[x['ind']]={}
            df_dict[x['ind']]={'name':x['out'] ,'itemStyle': {'normal':{'color':x['color']}},'value':10000-x['ind']*1000}

    return df_dict


################################################ 180122_new word_count_new end #########################################################################


################################################ 180122_new start pseg_cut#########################################################################
'''
词性标注功能
'''
@app.route('/pseg_cut',methods=['POST','GET'])
def pseg_cut():
    """
    给定文本进行分词，标注。返回分词和词性数据框
    :param text:字符串
    :return:分词结果和词性列表
    """
    jsonp_callback = request.args.get('callback', 'jsonpCallback1')  # 这里的callback对应的值需要和ajax请求的callback保持一致。
    # text = '读取字符串，返回单词和频率数据框,字典结构'
    text = request.values['text']
    print(text)
    path = 'F:\\easestar\\zstp20180109\\stopwords.txt'
    stopwords = [word.strip('\n') for word in open(path, 'r', encoding='utf-8').readlines()]

    '''
    words=[(word,pseg) for word,pseg in pseg.cut(text) if word not in stopwords
           and word !='\n']
    df_word=pd.DataFrame({'word':[words[i][0] for i in range(len(words))],
                          'class':[words[i][1] for i in range(len(words))]},
                         columns=['word','class'])
    '''

    '''
    第一步 pseg_cut
    '''
    words = [(word, pseg) for word, pseg in pseg.cut(text) if word not in stopwords
             and word != '\n']
    df_word = pd.DataFrame({'word': [words[i][0] for i in range(len(words))],
                            'class': [words[i][1] for i in range(len(words))]},
                           columns=['word', 'class'])
    df_word = df_word.drop_duplicates()
    df_word.index = range(len(df_word))


    '''
    第二步  color_df_psegCut
    '''
    words = color_df_psegCut(df_word)
    # print(words)

    '''
    第三步 cov_dict
    '''
    df_dict = cov_dict(words)

    '''
    第四步 封装返回数据
    '''
    dataMap = []
    for key, valuein in df_dict.items():
        print(key, valuein)
        # dataMap.insert(key,valuein)
        # dataMap.values(valuein)
        dataMap.append(valuein)

    #return df_word
    return Response(  # return的时候需要通过response返回数据并且将callback一并返回给客户端，这样才能请求成功。
        "%s(%s);" % (jsonp_callback, json.dumps({'ok': True, 'data': str(dataMap)}, ensure_ascii=False)),
        mimetype="text/javascript")


def color_df_psegCut(df_word):
    """"
    返回每个词性对应的颜色的数据框
    """
    color={
	   'n'   : "#ff8000" ,
	   'nr'  :"#FFF68F" ,
	   'nr1' :"#FFEFD5"  ,
	   'nr2' : "#FFE4E1" ,
	   'nrj' : "#FFDEAD" ,
	   'nrf' : "#FFC1C1" ,
       'nrt': "#FFC1C1",
	   'ns'  : "#FFB90F" ,
	   'nsf' : "#FFA54F" ,
	   'nt'  : "#FF34B3" ,
	   'nz'  :"#FF8C00"  ,
	   'nl'  :"#FF7F50"  ,
	   'ng'  :"#FF6EB4"  ,
	   'l'   : "#ff8000" ,
	   'eng'  :"#FF0080"  ,
	   't'   : "#FF4500" ,
	   'tg' : "#FF3030"  ,
	   's'  : "#aaaaff"  ,
	   'f'  : "#97cbff"  ,
	   'v'  : "#0080ff"  ,
	   'vd' : "#C1CDCD"  ,
	   'vn' : "#BFEFFF"  ,
	   'an' : "#BDBDBD"  ,
	  'vyou': "#BC8F8F"  ,
	   'vf' : "#B9D3EE"  ,
	   'vx' : "#B5B5B5"  ,
	   'vi' : "#B3EE3A"  ,
	  'vl'  : "#B22222"  ,
	  'vg'  : "#B23AEE"  ,
	   'a'  : "#deffac"  ,
	   'ad' : "#8B795E"  ,
	  'vshi': "#8B6969"  ,
	   'ag' : "#7EC0EE"  ,
	   'al' : "#7CFC00"  ,
	   'b'  : "#ffb5b5"  ,
	   'bl' : "#6B8E23"  ,
	   'z'  : "#e2c2de"  ,
       'zg' : "#e2c2de",
	   'r'  : "#00EEEE"  ,
	   'rr' : "#c1ffe4"  ,
	   'vz' : "#c1ffe4"  ,
	   'rzt': "#008B8B"  ,
	   'rzs': "#00688B"  ,
	   'rzv': "#27408B"  ,
	   'ry' : "#218868"  ,
	   'ryt': "#20B2AA"  ,
	   'rys': "#2E8B57"  ,
	   'ryv': "#228B22"  ,
	   'rg' : "#218868"  ,
	   'rz' : "#548B54"  ,
	   'm'  : "#6C7E92"  ,
	   'mq' :"#0000CD"   ,
	   'q'  : "#a3d1d1"  ,
	   'qv' : "#0000EE"  ,
	   'qt' : "#ca8eff"  ,
	   'd'  : "#b8b8dc"  ,
	   'p'  : "#ffd9ec"  ,
	   'pba': "#00FA9A"  ,
	   'pbei': "#00F5FF" ,
	   'c'  : "#ffe6d9"  ,
	   'cc' : "#00EE76"  ,
	   'u'  : "#d9b3b3"  ,
	   'ul' : "#d9b3b9"  ,
	   'uzhe': "#00E5EE" ,
	   'ule' : "#00CED1" ,
	   'uguo': "#00CD66" ,
	   'ude1': "#8B2252" ,
	   'ude2': "#8B008B" ,
	   'ude3': "#8968CD" ,
	   'usuo': "#878787" ,
	  'udeng': "#838B8B" ,
	   'uyy' : "#7FFFD4" ,
	   'udh' : "#7D9EC0" ,
	   'uls' : "#7CCD7C" ,
	   'uzhi': "#7A7A7A" ,
	  'ulian': "#708090" ,
	   'uj'  : "#8080FF" ,
	   'uv'  : "#B0E11E" ,
	   'uz'  : "#00FF80" ,
	   'i'   : "#408080" ,
	   'j'   : "#566CA9" ,
	   'ug'  : "#408080" ,
	   'dg'  : "#408080" ,
	   'e'   : "#cdcd9a" ,
	   'y'   : "#9f35ff" ,
	   'o'   : "#ffed97" ,
	   'h'   : "#ffbfff" ,
	   'k'   : "#84c1ff" ,
	   'x'   : "#bbffbb" ,
	   'xs'  : "#000080" ,
	   'xm'  : "#008B45" ,
	   'xu'  : "#006400" ,
	   'xe'  : "#EE2C2C" ,
	   'w'   : "#bebebe" ,
	   'wkz' : "#6495ED" ,
	   'wky' : "#607B8B" ,
	   'wyz' : "#5CACEE" ,
	   'wyy' : "#575757" ,
	   'wj'  : "#528B8B" ,
	   'ww'  : "#483D8B" ,
	   'wt'  : "#458B74" ,
	   'wd'  : "#436EEE" ,
	   'wf'  : "#3A5FCD" ,
	   'wn'  : "#2F4F4F" ,
	   'wm'  : "#20B2AA" ,
	   'ws'  : "#1C86EE" ,
	   'wp'  : "#1874CD" ,
	   'wb'  : "#104E8B" ,
	   'wh'  : "#00FF7F" ,
'userDefine' : "#0080FF"
	}
    df_word['color']=list(map(lambda x:color[x],df_word['class']))
    return df_word

def cov_dict(df_word):
	"""
	返回要求的字典形式
	:param df_word: 词频、词性数据框
	:return: 返回字典形式
	"""
	df_word['ind']=pd.Series(df_word.index)
	df_dict = {}
	for i in range(len(df_word)):
		x = df_word.loc[i, :]
		if x['ind'] not in df_dict:
			df_dict[x['ind']] = {}
			df_dict[x['ind']] = {'name': x['word'], 'class': x['class'],'color':x['color']}

	return df_dict
########################################################################## 180122 end pseg_cut############################################################################


###############################################180306 词频统计 start#####################################

@app.route('/word_count_chart',methods=['POST','GET'])
def word_count_chart():
    '''
     step 1 加载停用词并且获取前台传递的参数
    '''

    jsonp_callback = request.args.get('callback', 'jsonpCallback1')  # 这里的callback对应的值需要和ajax请求的callback保持一致。
    # text = '读取字符串，返回单词和频率数据框,字典结构'
    text = request.values['text']
    print(text)
    path = 'F:\\easestar\\zstp20180109\\stopwords.txt'
    stopwords = [word.strip('\n') for word in open(path, 'r', encoding='utf-8').readlines()]
    '''
    step 2 pseg_cut
    '''
    words = [(word, pseg) for word, pseg in pseg.cut(text) if word not in stopwords
             and word != '\n' and word != '\d']

    df_word1 = pd.DataFrame({'word': [words[i][0] for i in range(len(words))],
                             'class': [words[i][1] for i in range(len(words))]},
                            columns=['word', 'class'])
    df_word1 = df_word1.drop_duplicates()

    '''
    step 3 word_count2
    '''
    # df2, word_dict = word_count2(text, stopword,10)
    word_count = dict()
    # word=[]
    words2 = [wd.strip() for wd in jieba.cut(text) if wd not in stopwords and wd != '\n' and wd != '\d']
    for word in words2:
        if word not in word_count:
            word_count[word] = 1
        else:
            word_count[word] += 1
    # print(Counter(word))
    word_count = sorted(word_count.items(), key=lambda d: d[1], reverse=True)
    k = words.__len__();
    if k is not None:
        word_count1 = word_count[:k]
    else:
        word_count1 = word_count

    word_dict = dict(word_count1)
    df_word2 = pd.DataFrame({'word': [word_count1[i][0] for i in range(len(word_count1))], 'freq': [
        word_count1[i][1] for i in range(len(word_count1))
    ]}, columns=['word', 'freq'])

    '''
     step 4 merge_df
    '''
    # df = merge_df(df2, df1)
    df_word = pd.merge(df_word2, df_word1)
    df_word.index = range(len(df_word))
    df_word['out'] = df_word['word'] + '/' + df_word['class'] + '/' + df_word['freq'].astype(str)

    '''
    step 5 x_y_df
    '''
    x_y_dict = {}
    for i in df_word['class'].unique():
        x = df_word[df_word['class'] == i]
        x_y_dict[i] = dict()
        x_y_dict[i]['X'] = list(x['word'])
        x_y_dict[i]['Y'] = list(x['freq'])
    print(x_y_dict)


    return Response(  # return的时候需要通过response返回数据并且将callback一并返回给客户端，这样才能请求成功。
        "%s(%s);" % (jsonp_callback, json.dumps({'ok': True, 'data': str(x_y_dict)}, ensure_ascii=False)),
        mimetype="text/javascript")
'''
def x_y_df():
    x_y_dict = {}
    for i in df['class'].unique():
        x = df[df['class'] == i]
        x_y_dict[i] = dict()
        x_y_dict[i]['X'] = list(x['word'])
        x_y_dict[i]['Y'] = list(x['freq'])
    return x_y_dict

'''
###############################################180228 词频统计 end  #####################################

###############################################180320 聚类分析 start  #####################################


'''
  聚类分析
'''
from sklearn.externals import joblib as jl
@app.route('/classify_text',methods=['POST','GET'])
def classify_text():
    starttime = datetime.datetime.now()
    jsonp_callback = request.args.get('callback', 'jsonpCallback1')  # 这里的callback对应的值需要和ajax请求的callback保持一致。
    # text = '读取字符串，返回单词和频率数据框,字典结构'

    texts = request.values['text']
    print(texts)
    main_path = 'E:\workspalce\python\hello\zstp\py180208'
    '''
    step 1 接收封装数据
    '''
    dataset = recive_data(texts)  # 从前端接收数据

    '''
    step 2  加载模型
    '''
    t,com_chi2, com_model = read_model(main_path)  # 加载模型
    '''
    step 2  处理数据
    '''
    dataset = dis_data(dataset,main_path)  # 处理数据

    '''
    step 3 预测数据分类
    '''
    predict_id = model_fit(dataset, t, com_chi2, com_model)  # 预测问题分类

    '''
    step 4 预测标签列
    '''
    dataset['predict_label'] = predict_id  # 预测标签列

    '''
    step 5 返回字典形式的投诉类别的种类
    '''
    dict_freq = dict_df_classify(dataset['predict_label'])  # 返回字典形式的投诉类别的种类
    print(dict_freq)
    endtime = datetime.datetime.now()
    print("耗时 ："+str((endtime - starttime).seconds)+ " 秒")
    return Response(  # return的时候需要通过response返回数据并且将callback一并返回给客户端，这样才能请求成功。
        "%s(%s);" % (jsonp_callback, json.dumps({'ok': True, 'data': str(dict_freq)}, ensure_ascii=False)),
        mimetype="text/javascript")

#接受数据
def recive_data(texts):
    """
    从前端接收数据
    :param texts: 前端接收的数据
    :return: 返回数据框格式的数据，方便以后处理
    """
    text_array=[]
    for i in texts.split('*@*'):
        text_array.append(i)
    text_df=pd.DataFrame({'gd_id':list(range(len(text_array))),'description':
    text_array},columns=['gd_id', 'description'])
    return text_df

def read_model(main_path):
    """
    加载已经训练好的模型
    :param path: 文件路径
    :return: 训练好的模型
    """
    t=jl.load(main_path+'\\tfidf.m') #tfidf模型
    com_chi2=jl.load(main_path+'\\select_feature.m')#刷选变量模型
    com_model=jl.load(main_path+'\\classify_svc.m')#分类模型
    return t,com_chi2,com_model


#处理数据
def dis_data(dataset,main_path):
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

    def pseg_cut_classify(text):
        words = pseg.cut(text)
        return ' '.join([w.word for w in words if w.flag in flag_ls and w.word not in stop_set and len(w.word)>=2])

    dataset['cut'] = dataset['text'].map(pseg_cut_classify)


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

def model_fit(dataset,t,com_chi2,com_model):
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


def dict_df_classify(array_df):
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

###############################################180320 聚类分析 end  #####################################


#########################################180327 聚类分析新功能 start ########################################
@app.route('/classify_text_new',methods=['POST','GET'])
def classify_text_new():
    starttime = datetime.datetime.now()
    jsonp_callback = request.args.get('callback', 'jsonpCallback2')  # 这里的callback对应的值需要和ajax请求的callback保持一致。
    # text = '读取字符串，返回单词和频率数据框,字典结构'

    texts = request.values['text']
    print(texts)
    main_path = 'E:\workspalce\python\hello\zstp\py180208'

    dataset = recive_data_new(texts)
    t, com_chi2, com_model = read_model_new(main_path)  # 加载模型
    dataset = dis_data_new(dataset,main_path)  # 处理数据
    predict_id = model_fit_new(dataset, t, com_chi2, com_model)  # 预测问题分类
    dataset['predict_label'] = predict_id  # 预测标签列
    dict_freq = dict_df_new(dataset['predict_label'])  # 返回字典形式的投诉类别的种类
    out_data = dict_out_new(dataset)
    return Response(  # return的时候需要通过response返回数据并且将callback一并返回给客户端，这样才能请求成功。
        "%s(%s);" % (jsonp_callback, json.dumps({'ok': True, 'data': str(out_data)}, ensure_ascii=False)),
        mimetype="text/javascript")


def recive_data_new(texts):
    """
    从前端接收数据
    :param texts: 前端接收的数据
    :return: 返回数据框格式的数据，方便以后处理
    """
    text_array=[]
    for i in texts.split('*@*'):
        text_array.append(i)
    text_df=pd.DataFrame({'gd_id':list(range(len(text_array))),'description':\
    text_array},columns=['gd_id', 'description'])
    return text_df

#读取模型
def read_model_new(main_path):
    """
    加载已经训练好的模型
    :param path: 文件路径
    :return: 训练好的模型
    """
    t=jl.load(main_path+'\\tfidf.m') #tfidf模型
    com_chi2=jl.load(main_path+'\\select_feature.m')#刷选变量模型
    com_model=jl.load(main_path+'\\classify_svc.m')#分类模型
    return t,com_chi2,com_model


def dis_data_new(dataset,main_path):
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
def model_fit_new(dataset,t,com_chi2,com_model):
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

def dict_df_new(array_df):
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

def dict_out_new(df):
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
#########################################180327 聚类分析新功能 end  ########################################


#########################################180329 聚类分析新功能 start  ########################################

@app.route('/classify_text_new2',methods=['POST','GET'])
def classify_text_new2():
    starttime = datetime.datetime.now()
    jsonp_callback = request.args.get('callback', 'jsonpCallback2')  # 这里的callback对应的值需要和ajax请求的callback保持一致。
    # text = '读取字符串，返回单词和频率数据框,字典结构'

    texts = request.values['text']
    print(texts)
    main_path = 'E:\workspalce\python\hello\zstp\py180208'
    '''
    step 1
    '''
    dataset = recive_data_new2(texts)

    '''
    step 2
    '''
    t, com_chi2, com_model = read_model_new2(main_path)  # 加载模型

    '''
    step 3
    '''
    dataset = dis_data_new2(dataset,main_path)  # 处理数据

    '''
    step 4
    '''
    predict_id = model_fit_new2(dataset, t, com_chi2, com_model)  # 预测问题分类

    '''
    step 5 
    '''
    dataset['predict_label'] = predict_id  # 预测标签列

    '''
    step 6
    '''
    dict_freq = dict_df_new2(dataset['predict_label'])  # 返回字典形式的投诉类别的种类

    '''
    step 7
    '''
    out_data = dict_out_new2(dataset)
    print(out_data)

    return Response(  # return的时候需要通过response返回数据并且将callback一并返回给客户端，这样才能请求成功。
        "%s(%s);" % (jsonp_callback, json.dumps({'ok': True, 'data': str(out_data)}, ensure_ascii=False)),
        mimetype="text/javascript")


#接受数据
def recive_data_new2(texts):
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

#读取模型
def read_model_new2(main_path):
    """
    加载已经训练好的模型
    :param path: 文件路径
    :return: 训练好的模型
    """
    t=jl.load(main_path+'\\tfidf.m') #tfidf模型
    com_chi2=jl.load(main_path+'\\select_feature.m')#刷选变量模型
    com_model=jl.load(main_path+'\\classify_svc.m')#分类模型
    return t,com_chi2,com_model

#处理数据
def dis_data_new2(dataset,main_path):
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

def model_fit_new2(dataset,t,com_chi2,com_model):
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

def dict_df_new2(array_df):
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

def dict_out_new2(df):
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

#########################################180329 聚类分析新功能 end    ########################################

# __init__()
if __name__ == "__main__":
    # app = __init__()
    app.run()
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
    df_word = df_word.drop_duplicates()
    df_word.index=range(len(df_word))
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
			df_dict[x['ind']] = {'name': x['word'], 'class': x['class'],'colour':x['color']}

	return df_dict




if __name__=='__main__':
    path='F:\\easestar\\zstp20180109'
    stopwords=read_stopword(path=path)
    texts=readtext(path=path)

    words=pseg_cut(texts,stopwords=stopwords)
    words=color_df(words)
    # print(words)
    df_dict=cov_dict(words)

    print(df_dict)




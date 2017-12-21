# -*- coding: utf-8 -*-
from snownlp import SnowNLP
import json
import numpy as np
import sys

'''
def getresult():
    text = u""
    s = SnowNLP(u"我今天很快乐。我今天很愤怒。")
    print(s.sentiments)
    return s.sentiments
'''

def getfunc(keywords):
    #y_t = np.loadtxt(keywords)
    #print(y_t)
    s = SnowNLP(keywords)
    '''
    s = SnowNLP("是不是还不是就这样子了，完全不行，我觉得这车完全不行！")
    '''
    arry = []
    ''''
    for sentence in s.sentences:
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
        #print(k)
        _snownlpvalue = SnowNLP(k)
        #print(_snownlpvalue.sentiments)
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
            #print("负面词：" + str(i))
            value += i
            positive.insert(num, i)
            num + 1
        elif (i > 0.5):
            #print("正面词：" + str(i))
            value1 += i
            negative.insert(num, i)
            num + 1
    '''
    print("负面词结果:" + str(value / 2))
    print("正面词结果:" + str(value1 / 3))
    print("正面词结果1:" + str((0.8342 + 0.8584 + 0.6251) / 3))
    print("负面词结果1:" + str((0.3280 + 0.3281) / 2))
    
    print(negative)
    print(positive.__len__())
    print(positive)
    '''
    # _result_positive = 0
    # np.positive()
    _result_positive = sum(positive)
    _result_negative = sum(negative)
    '''
    print(_result_positive/positive.__len__())
    print(_result_negative/negative.__len__())
    
    print(_result_positive)
    print(_result_negative)
    
    print(_result_positive / (_result_positive + _result_negative))
    print(_result_negative / (_result_positive + _result_negative))
    '''
    _data_result1 = [{"_result_positive": _result_positive / (_result_positive + _result_negative),
                      "_result_negative": _result_negative / (_result_positive + _result_negative)},
                     {"_result_positive_len": positive.__len__(),
                      "_result_negative_len": negative.__len__()}]
    # _data_result = {"_result_positive":_result_positive/(_result_positive+_result_negative),"_result_negative":_result_negative/(_result_positive+_result_negative)}

    return _data_result1

'''
def hello():
    return 'test'
'''
#print(getfunc("是不是还不是就这样子了，完全不行，我觉得这车完全不行！"))
# getresult()
if __name__ == '__main__':
        keywords = sys.argv[1]
        testresult = getfunc(keywords)
        print(testresult)



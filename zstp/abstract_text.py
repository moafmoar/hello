"""
提取文本输入摘要
通过snownlp库
步骤：
    1.读取文件
    2.提取摘要


"""
import jieba
import re
import os
import pandas as pd
import numpy as np
from snownlp import SnowNLP

path = 'C:\\work\\jpy\\ab_test.txt'


def read_text(path=path):
    """
    读取文件
    :param path: 读入文件的路径
    :return: 返回文本字符串
    """
    text_data = open(path, 'r', encoding='utf-8')
    texts = text_data.read()  # 将整个文件作为一个字符串
    return texts


def abstract_text(texts, n=3):
    """
    提取整个字符串的摘要
    :param texts: 字符串
               n:  整数类型，字符串摘要的数目
    :return: 返回摘要
    """
    ab_text = SnowNLP(tests)
    text_abstract = ab_text.summary(n)
    return text_abstract


if __name__ == '__main__':
    path = 'C:\\work\\jpy\\ab_text.txt'
    tests = read_text(path)
    s1 = abstract_text(tests, n=3)
    for i in s1:
        print(i)

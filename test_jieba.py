import jieba
import numpy as np
import pandas as pd
from tqdm import *
import os
import re

main_path = os.path.abspath('.')
path = main_path+'\\test.txt'

def seg_cut(text):
    if text != '':
        return ' '.join(jieba.cut(text))
    else:
        return text

def word_cut(path=path):
    corpus = [value.strip('\n') for value in open(path,'r',encoding='gbk').readlines()]
    words = list(map(seg_cut, corpus))
    return words
	
# def add_a_b(a,b):
#     s=a+b
#     print(s)
#     return s

# print(add_a_b(3,4))
if __name__ == '__main__':
    words = word_cut()
    for value in words:
        print(value)
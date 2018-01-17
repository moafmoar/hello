'''
 分词脚本
'''


import jieba
import datetime
path=r'E:\\workspalce\\python\\hello\\txt\\test.txt'
def word_cut(path=path):
    words = []
    re_data=open(path,'r',encoding='utf-8')
    st_data=re_data.readlines()
    # for word in st_data:
        # print(word)

    words.append("    ".join([wd.strip('\n') for word in st_data
                              for wd in jieba.cut(word)]))
        # print(words)
    return words
# def add_a_b(a,b):
#     s=a+b
#     print(s)
#     return s
        

   
# print(add_a_b(3,4))

if __name__=='__main__':
    # begin = datetime.datetime.now()
    print(word_cut())
    # end = datetime.datetime.now()
    # print(end-begin)
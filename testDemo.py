
from zstp import word_count
# import wewe


def test001():
    '''
    stopword = word_count.read_stopword(path)
    text = word_count.readtext()
    df,word_dict = word_count.word_count(text=text, stopword=stopword, k=50)
    print(df)
    print(wewe.adder(2,3))
    print("123123123123")

    print("123123123123")
    '''
    a = '32323232323'
    return a


if __name__=='__main__':
    stopword = word_count.read_stopword()
    text = word_count.readtext()
    df, word_dict = word_count.word_count(text=text, stopword=stopword, k=50)
    print(df)
    # cloud_word(word_dict)

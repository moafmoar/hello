
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import json
import requests

def test2java():
    SENTIMENT_URL = 'http://api.bosonnlp.com/sentiment/analysis'
    # 注意：在测试时请更换为您的API Token
    headers = {'X-Token': '0TzmvoQC.21373.Jpr2vO03qwED'}

    s = ['这辆车车型不错，但是力量不行，油耗太大！可是由于跑市区所以应该没有问题。这车完全不能用。']
    data = json.dumps(s)
    resp = requests.post(SENTIMENT_URL, headers=headers, data=data.encode('utf-8'))

    print(resp.text)
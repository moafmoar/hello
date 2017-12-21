
# -*- coding: utf-8 -*-
from snownlp import SnowNLP
import json
from flask import Flask, render_template, request, jsonify,Response

app = Flask(__name__)
# @app.route('/')
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
    jsondate = {'_result_positive':_result_positive / (_result_positive + _result_negative),
                    '_result_negative':_result_negative / (_result_positive + _result_negative),
                    '_result_positive_len':positive.__len__(),
                    '_result_negative_len':negative.__len__()}
    return Response( # return的时候需要通过response返回数据并且将callback一并返回给客户端，这样才能请求成功。
            "%s(%s);" % (jsonp_callback, json.dumps({'ok': True, 'data': jsondate})),
            mimetype="text/javascript"
        )
   # return jsondate

#print(getfunc())

'''
@app.route('/testajax')
def testAjax(request):
    func = request.GET.get('callback')
    content = '%s(100000)' % (func,)
    return HttpResponse(content)

@app.route('/demo', methods=['POST'])
def home():
    data = json.loads(request.form.get('data'))
    result_json = json.dumps(data)
    # Response
    resp = Response(result_json)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

def request_ajax_url(url, body, referer=None, cookie=None, **headers):
    import urllib
    req = urllib2.Request(url)

    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Requested-With','XMLHttpRequest')

    if cookie:
        req.add_header('Cookie', cookie)

    if referer:
        req.add_header('Referer', referer)

    if headers:
        for k in headers.keys():
            req.add_header(k, headers[k])

    postBody = json.dumps(body)

    response = urllib2.urlopen(req, postBody)

    if response:
        return response
    
@app.route('/run')
def run():
    import time
    "use username:xfkxfk; use password:123456"

    login_url = 'http://www.xx.com/member/Login.aspx'
    login_body = {"action":"login","UserName":"xfkxfk","Password":"123456","AutomaticLogin":False}
    login_referer = "http://www.xx.com/member/Login.aspx?ReturnUrl=aHR0cDovL3d3dy5sdXNlbi5jb20vRGVmYXVsdC5hc3B4"

    url = 'http://www.xx.com/Member/MobileValidate.aspx'
    referer = "http://www.xx.com/Member/ModifyMobileValidate.aspx"

    headers = {}

    response = request_ajax_url(login_url, login_body, login_referer)

    if response.read() == "1":
        print(" Login Success !!!")

    if response.headers.has_key('set-cookie'):
        set_cookie = response.headers['set-cookie']
    else :
        print (" Get set-cookie Failed !!! May Send Messages Failed ~~~")

    if len(sys.argv) < 3:
        print ("\nUsage: python " + sys.argv[0] + "mobile_number" + "count\n")
        sys.exit()

    mobile_number = sys.argv[1]
    count = sys.argv[2]
    body = {"action":"GetValidateCode","Mobile":mobile_number}

    i=0
    while i < int(count):
        response = request_ajax_url(url,body,referer,set_cookie)
        i= i+1

    if response.read() == "发送成功":
        print(" Send " + count + " Messages To " + mobile_number + " !!!")



def test():
    import json
    from flask import jsonify, Response, json

    data = []  # or others
    return jsonify(ok=True, data=data)

    jsonp_callback = request.args.get('callback', '')
    if jsonp_callback:
        return Response(
            "%s(%s);" % (jsonp_callback, json.dumps({'ok': True, 'data': data})),
            mimetype="text/javascript"
        )
    return ok_jsonify(data)
'''
if __name__ == "__main__":
    app.run()
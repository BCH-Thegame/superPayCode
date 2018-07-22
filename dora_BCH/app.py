import time
from lxml import etree
from flask_apscheduler import APScheduler
import demjson as demjson
from flask import Flask, request
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from flask.json import jsonify
import requests

from util import getParams, sendTx, listTransactions, getToAddr, getBalanceByAddress, conv_dict

app = Flask(__name__)

rpc_user = 'root'
rpc_password = 'root'
# rpc_user and rpc_password are set in the bitcoin.conf file
# rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:18332" % (rpc_user, rpc_password))

class Config(object):  # 创建配置，用类
    JOBS = [  # 任务列表
        {  # 任务字典（细节）
            'id': 'indiana',
            'func': '__main__:indiana',
            'trigger': 'cron',
            'hour': "*/1",
            # 'minute': "*/1"
        }
    ]




app.config.from_object(Config())
@app.route('/')
def hello_world():
    return 'Hello World!'



#获取一个新的地址
@app.route('/newaddress',methods=['POST'])
def newaddress():
    # {"apiKey": "0000", "params": {"account":""}}
    result_data = "{'code':'%(code)s','data':%(data)s,'msg':'%(msg)s'}"
    rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:18332" % (rpc_user, rpc_password))

    try:
        form_data = request.json
        param = getParams(form_data,'post')
        if param ==None:
            raise Exception('入参异常')
        account = param['account']
        address_type = 'legacy'
        address = rpc_connection.getnewaddress (account,address_type)
        a = rpc_connection.walletpassphrase('admin', 30)
        address_pkey = rpc_connection.dumpprivkey(address)
        result_data = result_data % {"code":"0000","data":str({'address':address,'address_pkey':address_pkey}),"msg":'0'}
        result_data = demjson.decode(result_data)
    except BaseException as err:

        err = str(err).replace("'", "")
        result_data = result_data % ({"code": "0001", "data": "0", "msg": str(err)})

        # print(result_data)
        result_data = demjson.decode(result_data)
        # batch support : print timestamps of blocks 0 to 99 in 2 RPC round-trips:
    return jsonify(result_data)



#获取余额
@app.route('/getbalance')
def getbalance():
    # {"apiKey": "0000", "params": {"account":""}}
    result_data = "{'code':'%(code)s','data':%(data)s,'msg':'%(msg)s'}"
    rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:18332" % (rpc_user, rpc_password))
    try:
        form_data = request.args
        param = getParams(form_data,'get')
        if param == None:
            raise Exception('入参异常')
        address = param['address']
        amount,txs = getBalanceByAddress(address,rpc_connection)
        # account = rpc_connection.getaccount(address)
        # amount = rpc_connection.getbalance(account)
        result_data = result_data % {"code": "0000", "data": str({'amount': float(amount)}),
                                     "msg": '0'}
        result_data = demjson.decode(result_data)
    except BaseException as err:

        err = str(err).replace("'", "")
        result_data = result_data % ({"code": "0001", "data": "0", "msg": str(err)})

    # print(result_data)
        result_data = demjson.decode(result_data)
    # batch support : print timestamps of blocks 0 to 99 in 2 RPC round-trips:
    return jsonify(result_data)




#发送交易
@app.route('/sendrawtransaction',methods=['POST'])
def sendrawtransaction():
    # {"apiKey": "0000", "params": {"account":""}}
    result_data = "{'code':'%(code)s','data':%(data)s,'msg':'%(msg)s'}"
    rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:18332" % (rpc_user, rpc_password))

    try:
        form_data = request.json

        param = getParams(form_data,'post')
        if param == None:
            raise Exception('入参异常')

        # from_addr, from_prikey, to_addr, amount, fee_amount
        from_addr = param['from_addr']
        from_prikey = param['from_prikey']
        to_addr = param['to_addr']
        amount = param['amount']
        fee_amount = param['fee_amount']
        tx_data = None
        if 'tx_data' in param.keys():
            tx_data = param['tx_data']

        txhash = sendTx(rpc_connection,from_addr, from_prikey, to_addr, amount, fee_amount,tx_data)
        # print(txhash)
        result_data = result_data % {"code": "0000", "data": str({'txhash': txhash}),"msg": '0'}
        result_data = demjson.decode(result_data)
    except Exception as err:
        print(type(err))
        err = str(err).replace("'","")
        result_data = result_data % ({"code": "0001", "data": "0", "msg": str(err)})
        result_data = demjson.decode(result_data)
    # batch support : print timestamps of blocks 0 to 99 in 2 RPC round-trips:
    return jsonify(result_data)



#获取交易记录
@app.route('/listtransactions')
def listtransactions():
    rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:18332" % (rpc_user, rpc_password))
    # {"apiKey": "0000", "params": {"account":""}}
    result_data = "{'code':'%(code)s','data':%(data)s,'msg':'%(msg)s'}"
    try:
        form_data = request.args
        param = getParams(form_data,'get')
        if param == None:
            raise Exception('入参异常')
        # from_addr, from_prikey, to_addr, amount, fee_amount
        address = param['address']
        tx_list_result = []
        tx_list = rpc_connection.listtransactions()
        tx_list_result_temp = []
        for tx in tx_list:
            # print(tx)
            if ('address' in tx.keys() and address == tx['address']):
                tx['amount'] = float(tx['amount'])
                if 'fee' in tx.keys():
                    tx['fee'] = float(tx['fee'])

                if 'identifier' in tx.keys():
                    tx['identifier'] = 'true' if tx['identifier'] == True else 'false'

                if 'abandoned' in tx.keys():
                    tx['abandoned'] = 'true' if tx['abandoned'] == True else 'false'
                if 'trusted' in tx.keys():
                    tx['trusted'] = 'true' if tx['trusted'] == True else 'false'
                if 'blocktime' in tx.keys():
                    tx['blocktime_conv'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(tx['blocktime']))
                if 'time' in tx.keys():
                    tx['time_conv'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(tx['time']))
                if 'timereceived' in tx.keys():
                    tx['timereceived_conv'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(tx['timereceived']))

                to_add = getToAddr(tx['txid'], address, rpc_connection)
                if to_add != None:
                    tx['to_add'] = to_add

                tx_list_result_temp.append(tx)

        result_data = result_data % {"code": "0000", "data": str({'tx_list': tx_list_result_temp}),"msg": '0'}
        result_data = demjson.decode(result_data)
    except Exception as err:
        err = str(err).replace("'", "")
        result_data = result_data % ({"code": "0001", "data": "0", "msg": err})

    # print('result_data===',result_data)
        result_data = demjson.decode(result_data)
    # batch support : print timestamps of blocks 0 to 99 in 2 RPC round-trips:
    return jsonify(result_data)



#获取交易记录
@app.route('/listtransactionsByaddr')
def listtransactionsByaddr():
    rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:18332" % (rpc_user, rpc_password))
    # {"apiKey": "0000", "params": {"account":""}}
    result_data = "{'code':'%(code)s','data':%(data)s,'msg':%(msg)s}"
    try:
        form_data = request.args
        param = getParams(form_data,'get')
        if param == None:
            raise Exception('入参异常')

        address = param['address']
        to_address = None
        from_time = None
        to_time = None

        if 'to_address' in param.keys():
            to_address = param['to_address']

        if 'from_time' in param.keys():
            from_time = param['from_time']

        if 'to_time' in param.keys():
            to_time = param['to_time']


        to_add_list = listTransactions(rpc_connection,address,to_address,from_time,to_time)
        result_data = result_data % {"code": "0000", "data": str({'tx_list': to_add_list}), "msg": '0'}
        result_data = demjson.decode(result_data)
    except Exception as err:
        result_data = result_data % ({"code": "0001", "data": "0", "msg": str(err)})
        result_data = demjson.decode(result_data)


    return jsonify(result_data)

#发送交易
@app.route('/gettransaction',methods=['POST'])
def gettransaction():

    result_data = "{'code':'%(code)s','data':%(data)s,'msg':'%(msg)s'}"
    rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:18332" % (rpc_user, rpc_password))
    try:
        form_data = request.json
        param = getParams(form_data, 'post')
        if param == None:
            raise Exception('入参异常')
        txid = param['txid']
        print(txid)
        txinfo  = conv_dict(rpc_connection.gettransaction(txid))

        result_data = result_data % {"code": "0000", "data": str({'txinfo': txinfo}),
                                     "msg": '0'}
        print(result_data)
        result_data = demjson.decode(result_data)
    # e15b43f44f039a90fe0d15a5e62d721da9a98233a9f57fb932e966bc5f26c42d
    except BaseException as err:

        err = str(err).replace("'", "")
        result_data = result_data % ({"code": "0001", "data": "0", "msg": str(err)})
        result_data = demjson.decode(result_data)

    print(result_data)

    # batch support : print timestamps of blocks 0 to 99 in 2 RPC round-trips:
    return jsonify(result_data)


#获取交易记录
@app.route('/getEthPrice')
def getEthPrice():
    result_data = "{'code':'%(code)s','data':%(data)s,'msg':'%(msg)s'}"
    try:
        header = dict({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36'}
        )
        page = requests.get('https://coinmarketcap.com/currencies/bitcoin-cash/',headers=header)
        page.encoding = page.apparent_encoding
        html_tree = etree.HTML(page.text)
        # // *[ @ id = "quote_price"]
        price = html_tree.xpath('//*[@id="quote_price"]/@data-usd')[0]
        result_data = result_data % {"code": "0000", "data": str({'price': price}),"msg": '0'}

    except BaseException as err:

        err = str(err).replace("'", "")
        result_data = result_data % ({"code": "0001", "data": "0", "msg": str(err)})

    result_data = demjson.decode(result_data)
    return jsonify(result_data)



@app.route('/getTime')
def getTime():
    result_data = "{'code':'%(code)s','data':%(data)s,'msg':'%(msg)s'}"
    try:

        result_data = result_data % {"code": "0000", "data": str({'time': int(time.time())}), "msg": '0'}
    except BaseException as err:
        err = str(err).replace("'", "")
        result_data = result_data % ({"code": "0001", "data": "0", "msg": str(err)})

    result_data = demjson.decode(result_data)
    return jsonify(result_data)


#夺宝
def indiana():
    print('hello,world!')
    rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:18332" % (rpc_user, rpc_password))
    #获取现在时间点之前整点的发币的人
    #B账号地址
    address = 'mi5mCPh5fC2oykwJqgXvTejo63rPzrHKWp'

    from_time = int(time.time()-30000)
    to_time = int(time.time())

    tran = listTransactions(rpc_connection,address,None,from_time,to_time)
    toid_list = []
    for add in tran:
        if add['category'] == 'receive' and add['amount'] == 1:
            to_add = getToAddr(add['txid'], address, rpc_connection)
            if to_add not in toid_list:
                toid_list.append(to_add)

    header = dict({
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36'}
    )
    page = requests.get('https://coinmarketcap.com/currencies/bitcoin-cash/', headers=header)
    page.encoding = page.apparent_encoding
    html_tree = etree.HTML(page.text)
    # // *[ @ id = "quote_price"]
    price = html_tree.xpath('//*[@id="quote_price"]/@data-usd')[0]

    price = round(float(price))
    index = price % len(toid_list)

    # 获奖规则：当前coinmarketcap市场对应的bch的实时价格与当前参与人数的总数之间取余数，例如当前bch价格报价$772.76，
    # 取整数四舍五入773，当前参与人数为100，那么773 % 100 = 73，那么第73个参加的人获奖，如果余数为0则第一位参与人数的获奖，
    # 注：获奖为当前奖金池的80 %。
    print(index)
    winning_addr = toid_list[index]

    from_addr = 'mi5mCPh5fC2oykwJqgXvTejo63rPzrHKWp'
    from_prikey = 'cNjJR33xX1j5JchoaHhymMCpV5MKivC5jKZrtvDJCcVAxCAG35u2'
    amount = len(toid_list) * 0.8
    amount_A = len(toid_list) - amount -0.002

    addr_A = 'mtJBQnW7e2PNXsiPVfRLWAkRmkHxaaMgLx'
    print(winning_addr)
    txhash1 = sendTx(rpc_connection,from_addr, from_prikey, winning_addr, amount, 0.001,None)
    time.sleep(1800)
    rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:18332" % (rpc_user, rpc_password))
    txhash2 = sendTx(rpc_connection, from_addr, from_prikey, addr_A, amount_A, 0.001, None)
    print(from_addr, from_prikey, winning_addr, amount,txhash1,txhash2)



if __name__ == '__main__':
    scheduler = APScheduler()  # 实例化APScheduler
    scheduler.init_app(app)  # 把任务列表放进flask
    scheduler.start()
    app.run(host='0.0.0.0',port=5100)







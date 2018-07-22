import binascii
import time
import demjson


def listTransactions(rpc_connection,address,to_address,from_time,to_time):

    tx_list_result = []
    tx_list = rpc_connection.listtransactions()
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
            tx['to_add'] = to_add
            tx_list_result.append(tx)


    if to_address !=None:

        to_add_list = []
        for tx in tx_list_result:
            if to_address == tx['to_add']:
                to_add_list.append(tx)

        return to_add_list



    if from_time !=None and to_time !=None:
        to_add_list = []
        for tx in tx_list_result:
            if from_time <= tx['timereceived'] and to_time >= tx['timereceived']:
                to_add_list.append(tx)
        return to_add_list


    if from_time !=None:
        to_add_list = []
        for tx in tx_list_result:
            if from_time <= tx['timereceived']:
                to_add_list.append(tx)

        return to_add_list


    if to_time !=None:
        to_add_list = []
        for tx in tx_list_result:
            if to_time >= tx['timereceived']:
                to_add_list.append(tx)
        return to_add_list




def sendTx(rpc_connection,from_addr, from_prikey, to_addr, amount, fee_amount,tx_data):
    amount_sum, txs = getBalanceByAddress(from_addr,rpc_connection)
    if amount_sum < amount:
        raise Exception('金额异常')

    amount_tmp = 0
    txids = []
    txids_sign = []
    for tx in txs:
        if amount_tmp- fee_amount < amount :
            amount_tmp = amount_tmp + float(tx['amount'])
            txids.append({'txid': tx['txid'], "vout": tx['vout']})
            txids_sign.append({'txid': tx['txid'], "vout": tx['vout'], 'scriptPubKey': tx['scriptPubKey'],
                               'amount': float(tx['amount'])})

    price = '%8f' % (amount_tmp - amount - fee_amount)

    send_tx = {to_addr: amount, from_addr: float(price)}
    if tx_data !=None:
        data = binascii.b2a_hex(tx_data.encode())
        send_tx = {to_addr: amount, from_addr: (amount_tmp - amount - fee_amount), 'data': data.decode()}



    # 创建交易
    create_tea = rpc_connection.createrawtransaction(txids, send_tx)

    # 签名
    sugn_mess = rpc_connection.signrawtransaction(create_tea, txids_sign, [from_prikey])
    sugn_hex = sugn_mess['hex']
    txhash = rpc_connection.sendrawtransaction(sugn_hex)

    return txhash

def getParams(form_data,meth):

    if meth =='get':
        form_data = form_data['data']
        form_data = demjson.decode(form_data)

    apiKey = form_data['apiKey']
    if apiKey =='0000':
        params = form_data['params']
        return params
    return None



#获取
def getBalanceByAddress(address,rpc_connection):

    unspents = rpc_connection.listunspent(None, None, [address], True)
    amount = 0
    txs = []
    for pent in unspents:
        # print(pent)
        amount = amount + pent['amount']
        txs.append({'txid':pent['txid'],'scriptPubKey':pent['scriptPubKey'],'amount':pent['amount'],'vout':pent['vout']})
    return amount,txs




def conv_dict(dict_data):

    for key in dict_data.keys():
        # if(type(dict_data[key]) == 'bool'):
        #     dict_data[key] = 'true' if dict_data[key] ==True else 'false'
        if('decimal' in str(type(dict_data[key]))):
            dict_data[key] = float(dict_data[key])
        if ('bool' in str(type(dict_data[key]))):
            if dict_data[key]:
                dict_data[key] ='true'
            else:
                dict_data[key] = 'false'
        if('list' in str(type(dict_data[key]))):
            for dt in dict_data[key]:
                conv_dict(dt)

    return dict_data


def getToAddr(txid,address,rpc_connection):
    tx_info = rpc_connection.gettransaction(txid)
    if len(tx_info) == 0:
        return None
    details = tx_info['details']
    add_list = []
    for det in details:

        if 'address' not in det.keys() or det['address'] in add_list :
            continue
        add_list.append(det['address'])

    add_list.remove(address)
    if len(add_list) ==0:
        return None
    return add_list[0]



let API = "http://10.0.52.45:5100/"
// http://10.0.52.45:5100/listtransactions?data={"apiKey":"0000","params":{"address":"mypW6HydTuw8mHvbDihRu8MWJDdgjbbvNK"}}
function ajax(url,parmas,method){
    let _parmas = method ? '' : '?data=' + JSON.stringify({ "apiKey": "0000", "params": parmas })
    return new Promise((res, rej) =>{
        wx.request({
            url: API + url + _parmas,
            method: method || 'GET',
            data: method ? parmas : "",
            success:(data)=>{
                if(data.data.code == '0000'){
                    res(data.data)
                } else if (data.data.code == '0001'){
                    console.log(data)
                    wx.showModal({
                        title: 'error',
                        content: data.data.errMsg,
                    })
                }
            },
            fail:(error)=>{
                rej(error)
                console.log(error)
            }
        })
    })
}
// http://10.0.52.45:5100/getbalance?data={"apiKey":"0000","params":{"address":"mypW6HydTuw8mHvbDihRu8MWJDdgjbbvNK"}}

module.exports = {
    listtransactions: (parmas) =>  ajax('listtransactions', parmas),
    newaddress: (parmas) => ajax('newaddress', parmas,"POST"),
    getbalance: (parmas) => ajax('getbalance', parmas),
    getbonus: (parmas) => ajax('listtransactionsByaddr', parmas),
    sendrawtransaction: (parmas) => ajax('sendrawtransaction', parmas, "POST")
}
const app = getApp()
const api = require('../../api/api.js')
Page({
    data: {

    },

    scanPay: function(e) {

    },
    onLoad: function(options) {
        console.log(options)
        wx.setNavigationBarTitle({
            title: 'SuperPay',
        })
        wx.setBackgroundColor({
            backgroundColor: '#313541', // 窗口的背景色为白色
        })
        app.getLang()
        app.getAmount()
        let parmas = {
            "from_addr": "msNTLgN2rgaiXx66ZqG2juoi2j4cg3Qwue",
            "from_prikey": "cU3AcnGQKsiL1jM148w8s9AzWeDf3ztswV6CcYhMXk5DgPfa62hx",
            "to_addr": "mypW6HydTuw8mHvbDihRu8MWJDdgjbbvNK",
            "amount": 2,
            "fee_amount": 0.001,
            "tx_data": "hello,world!"
        }
        api.sendrawtransaction(parmas)
            .then(res => {
                console.log(res)
            })
    },
    adDetail:function(){
        wx.navigateTo({
            url: '/pages/adDetail/adDetail',
        })
    },
    toPay:function(){
        wx.navigateTo({
            url: `/pages/pay/pay?id=ad&address=n4KkZMS4FCNbHi2jkje6KSwEsDeDhzoXXL`,
        })
    },
    toPayment:function(){
        wx.navigateTo({
            url: `/pages/pay/pay?id=payment`,
        })
    },
    toWallet:function(e){
        wx.navigateTo({
            url: '/pages/creatWallet/creatWallet',
        })
    }
})
//app.js
const api = require('api/api.js')
App({
    onLaunch: function() {
        // 登录
        wx.login({
            success: res => {
                // 发送 res.code 到后台换取 openId, sessionKey, unionId
                console.log(res)
                wx.request({
                    url: 'https://opentest.liantuobank.com/api/wechatAppOpenId.htm?appid=wx96b8a0a79472de45&secret=84566bf29a77a174619bad4ee3f5664b&code=' + res.code,
                    success: data => {
                        console.log(data)
                        wx.setStorageSync("openId", data.data.wechatVo.openId)
                    }
                })
            }
        })
    },
    currPage: function () {
        let _curPageArr = getCurrentPages()
        return _curPageArr[_curPageArr.length - 1]
    },
    getAmount: function() {
        //获取钱包余额
        const currPage = this.currPage()
        let address = wx.getStorageSync("address")
        let parmas = {
            address: address.address
        }
        return api.getbalance(parmas)
            .then(res => {
                console.log(res)
                currPage.setData({
                    amount: res.data.amount
                })
            })
    },
    getLang:function(){
        const currPage = this.currPage()
        currPage.setData({
            en: this.globalData.en
        })
    },
    globalData: {
        userInfo: null,
        en:true
    }
})
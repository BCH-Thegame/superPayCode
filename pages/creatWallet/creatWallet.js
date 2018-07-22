const app = getApp()
const api = require('../../api/api.js')
const code = require("../../libs/qrCode/code.js")
Page({
    data: {
        pwd: true,
        pwdInput: ['', '', '', '', '', '']
    },

    onLoad: function(options) {
        wx.setNavigationBarTitle({
            title: 'BCH Wallet',
        })
        try {
            if (wx.getStorageSync("address")) {
                console.log("addres")
                let address = wx.getStorageSync("address")
                let size = code.size()
                this.setData({
                    address: address,
                    isReg: true,
                    qrSize: size.w,
                })
                code.qr(address.address_pkey, "qrcodecav", size.w, size.w)
                app.getAmount()
            } else {

            }
        } catch (error) {

        }
    },
    copyAddress: function(e) {
        wx.setClipboardData({
            data: this.data.address.address,
            success: function(res) {
                wx.getClipboardData({
                    success: function(res) {
                        console.log(res.data) // data
                    }
                })
            }
        })
    },
    passInput: function(e) {
        console.log(e)
        console.log(e.detail.value)
        let values = e.detail.value
        let vals = values.split("")
        console.log(vals)
        let pasLenght = vals.length
        let vs = vals.pop()

        let pwdInput = this.data.pwdInput
        pwdInput[pasLenght] = vals.pop()
        this.setData({
            pwdInput: pwdInput
        })
    },
    creatWallet: function(e) {
        console.log(e)
        wx.setStorageSync("walletName", e.detail.value.walletName)
        var openId = Date.parse(new Date());
        let parmas = { "apiKey": "0000", "params": { "account": "" + openId + "" } }
        api.newaddress(parmas)
            .then(res => {
                console.log("address::", res)
                wx.setStorageSync("address", res.data)
                this.setData({
                    isReg: true
                })
            })
    },
    onReady: function() {
        // 请求地址
        // http://10.0.52.45:5100/newaddress
        // data:
        // { "apiKey": "0000", "params": { "account": "openid" } }
    },

    onShow: function() {

    },

    onHide: function() {

    },

    onUnload: function() {

    },


    onPullDownRefresh: function() {

    },


    onReachBottom: function() {

    },

    /**
     * 用户点击右上角分享
     */
    onShareAppMessage: function() {

    }
})
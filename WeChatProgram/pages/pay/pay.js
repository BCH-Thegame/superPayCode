const app = getApp()
const api = require('../../api/api.js')
Page({

    data: {
        fee: 0.001,
        word: 100,
    },

    onLoad: function(options) {
        console.log(options)
        wx.setNavigationBarTitle({
            title: 'Payment',
        })
        if (options.id == 'ad') {
            this.setData({
                isAd: true
            })
        }
        if (options.id == 'payment') {
            this.setData({
                isPayment: true
            })
        }
        this.setData({
            options: options,

        })
        app.getAmount()
    },
    sendrawtransaction: function(e) {
        console.log(e)
        let address = wx.getStorageSync("address")
        let options = this.data.options
        let parmas = {
            "apiKey": "0000",
            "params": {
                "from_addr": address.address,
                "from_prikey": address.address_pkey,
                "fee_amount": 0.001,
                "amount":null,
                "to_addr":null
            }
        }

        if (options.id == 'ad' || options.id == 'bonus') {
            parmas.params.amount = 1
            parmas.params.to_addr = this.data.options.address

        } else {
            let formValue = e.detail.value
            console.log(formValue)
            let __parmas = parmas.parmas
            parmas.params.amount = formValue.amount
            parmas.params.to_addr = formValue.to_addr
            console.log(parmas)
            this.setData({
                payMent: true
            })
        }
        wx.showModal({
            title: 'Confirm?',
            content: 'confirm your payment?',
            success: res => {
                console.log(confirm)
                if (res.confirm) {
                    api.sendrawtransaction(parmas)
                        .then(res => {
                            console.log(res)
                            wx.showToast({
                                title: 'sucess',
                            })
                        })
                }
            }
        })
    },
    adinput: function(e) {
        console.log(e)
        this.setData({
            word: 100 - e.detail.value.length
        })
    },
    onReady: function() {

    },


    onShow: function() {

    },

    onHide: function() {

    },

    onUnload: function() {

    },

    /**
     * 页面相关事件处理函数--监听用户下拉动作
     */
    onPullDownRefresh: function() {

    },

    /**
     * 页面上拉触底事件的处理函数
     */
    onReachBottom: function() {

    },

    /**
     * 用户点击右上角分享
     */
    onShareAppMessage: function() {

    }
})
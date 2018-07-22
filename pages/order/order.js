// pages/order/order.js
const api = require('../../api/api.js')
Page({
    data: {
        currTab: 0
    },
    onLoad: function(options) {
        wx.setNavigationBarTitle({
            title: '账单明细',
        })
        let address = wx.getStorageSync("address")
        let parmas = {
            "address": address.address
        }
        console.log(api)
        api.listtransactions(parmas)
            .then(res => {
                console.log(res)
                this.setData({
                    order: res.data.tx_list
                })

            })
    },
    toDetail: function(e) {
        console.log(e)
        let order = this.data.order
        wx.setStorageSync("orderDetail", order[e.currentTarget.dataset.index])
        wx.navigateTo({
            url: '/pages/orderDetail/orderDetail',
        })
    },
    tabToggle: function(e) {
        this.setData({
            currTab: e.target.id
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

    onPullDownRefresh: function() {

    },

    onReachBottom: function() {

    },

    onShareAppMessage: function() {

    }
})
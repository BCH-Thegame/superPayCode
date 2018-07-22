const app = getApp()
Page({

    data: {
        userInfo: true
    },

    onLoad: function(options) {
        wx.setNavigationBarTitle({
            title: 'Wallet',
        })
        wx.setBackgroundColor({
            backgroundColor: '#313541', // 窗口的背景色为白色
        })
        
    },
    onShow:function(){
        if (wx.getStorageSync("address")) {
            this.setData({
                isReg: true
            })
            app.getAmount()
        } else {
            this.setData({
                isReg: false
            })
        }
    },
    getUserInfo: function(e) {
        console.log(e)
    },
    toOderDetail: function() {
        wx.navigateTo({
            url: '/pages/order/order',
        })
    },
    creatWallet: function() {
        wx.navigateTo({
            url: '/pages/creatWallet/creatWallet',
        })
    },
    onReady: function() {

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
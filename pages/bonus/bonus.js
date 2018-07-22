const app = getApp()
const api = require('../../api/api.js')
Page({
    data: {

    },
    onLoad: function(options) {
        wx.setNavigationBarTitle({
            title: "Bouns",
        })
        wx.setBackgroundColor({
            backgroundColor: '#ff4429', // 窗口的背景色为白色
        })
        wx.setNavigationBarColor({
            frontColor: '#ffffff',
            backgroundColor: '#ff4429',
        })
        let that = this
        var interValId = null;
        var timemsg = "";
        var endTime = new Date("2018/12/31 23:59:59");
        var intEndTime = endTime.getTime();
        // 开奖分钟
        var baseM = 59;
        // 开奖秒数
        var baseS = 59;
        var baseTime = baseM * 60 * 1000 + baseS * 1000;
        
        function cutDown() {
            var nowTime = new Date();
            var intNowTime = nowTime.getTime();
            var relayTime = intEndTime - intNowTime;
            if (relayTime > 0) {
                var m = nowTime.getMinutes();
                var s = nowTime.getSeconds();
                var currentTime = m * 60 * 1000 + s * 1000;
                var difTime;
                // 大于开奖时间，则在当前基础上加一个小时
                if (currentTime >= baseTime) {
                    difTime = baseTime + 1000 * 60 * 60 - currentTime;
                } else {
                    difTime = baseTime - currentTime;
                }
                var relayM = Math.floor(difTime / 1000 / 60 % 60);
                var relayS = Math.floor(difTime / 1000 % 60);
                timemsg = relayM + " min" + " " + relayS + " sec";
            } else {
                window.clearInterval(interValId);
                timemsg = "game over";
            }
            that.setData({
                timemsg: timemsg
            })
        }
        interValId = setInterval(cutDown, 1000)

        // 获取当前奖金池余额及参与人数
        var nowTime = new Date();
        var nowyear = nowTime.getFullYear(); //获取系统的年；
        var nowmonth = nowTime.getMonth() + 1; //获取系统月份，由于月份是从0开始计算，所以要加1
        var nowhours = nowTime.getHours(); //获取系统时，
        var nowdate = nowTime.getDate();
        if (nowhours < 10) {
            nowhours = "0" + nowhours;
        }
        var from_time = Date.parse(nowyear + "-" + nowmonth + "-" + nowdate + " " + nowhours + ":00:00") / 1000;
        console.log("from_time==" + from_time);
        var to_time = Date.parse(nowyear + "-" + nowmonth + "-" + nowdate + " " + nowhours + ":59:59") / 1000;
        console.log("to_time==" + to_time);
        let parmas = {
            "address": "mi5mCPh5fC2oykwJqgXvTejo63rPzrHKWp",
            "from_time": from_time,
            "to_time": to_time
        }
        let bonus = "0"; //奖金池
        let bonuspeo = "0"; //参与人数
        api.getbonus(parmas)
            .then(res => {
                console.log("params", res)
                var datalist = res.data.tx_list;
                for (var i = 0; i < datalist.length; i++) {
                    if (datalist[i].category == "receive" && datalist[i].amount == 1) {
                        bonus = parseInt(bonus) + parseInt(datalist[i].amount);
                        bonuspeo++;
                    }
                }
            })
        that.setData({
            bonus: bonus, //奖金池
            bonuspeo: bonuspeo //人数
        })

    },
    toPay: function(e) {
        wx.navigateTo({
            url: `/pages/pay/pay?id=${e.target.id}&address=mi5mCPh5fC2oykwJqgXvTejo63rPzrHKWp`,
        })
    },
    onReady: function() {

    },

    /**
     * 生命周期函数--监听页面显示
     */
    onShow: function() {

    },

    /**
     * 生命周期函数--监听页面隐藏
     */
    onHide: function() {

    },

    /**
     * 生命周期函数--监听页面卸载
     */
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
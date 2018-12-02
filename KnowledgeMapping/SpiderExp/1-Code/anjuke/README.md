# 运行方式
```python
python run.py
```
# 运行环境
```python3.6```

# 参考
1.其实以前也破解过,只是没有详细记录
2.参考 https://lengyue.me/index.php/2018/10/06/anjuke/

# 破解过程记录

## 准备
1. 破解url ```https://www.anjuke.com/captcha-verify/?callback=shield```

## 破解
1. 打开google F12,清除缓存,访问url,滑动一下试试
2. 会发现**checkV3**为验证码的请求接口
```
#请求数据为
callback: jQuery19108408108632218079_1543310767116  #估计用不到
responseId: ed3ce1892d6f4baa8e942e996a1553a7        #请求getV3接口获取的值(其实是图片的标识)
sessionId: fd3b3e22d056408cb898d357e585f4f6         #网页中有
data: 6E997EC058A756D97A00A3432F1300BDA8C611A531F7E17874673574FFC2A12BC99892D3D659513EEB726CA92F8F6F4DDB4308CDD24263C64EA4C1B70C1BFD17451F66255BF1953A1CB7B7F0AF64EA13CC1AB8652E5BDD8B58AE575935B855B399967A8780EB21A26F0A9F140B4FA0636B7280369622B4C40E20BC42B8274A61E86C1F60709C240710960B2A3E7F2C4EF9E97D2405F32B7854DE1373FE606C56E1B7469CA736FDF316DE2B73BD30618DCE511A2AB84396F860CE5E9CDD8C713CABD34B88713A6AA04AD3664654B30DF34FC0648417056EB56B6EADB17204A9145B779E4FD417E9BFFDDD1CAA3C1E1E9F6B4B27DBB3F5AF3F3EB7D99DE0BA9418D929CD90B5820735FB7E30199CD2E18448BFC62878E56A4B3A0307EC83D332BF5126956180282EC014C2E6B259E88EA0DFD533CAF71068E901609967B6E13EA149EAA2F468D530D9537E6FFB90740D1E75007DE644A9ACE3D6CFF8F20E8302EDD1CAE33A7FDC7E8C30705AE5C54A3AE2   #加密数据
_: 1543310767118     


#返回数据
jQuery19108408108632218079_1543310767116({
    "message": "校验失败",
    "data": {
        "ischange": false,
        "status": 1
    },
    "code": 0
})

```
3. 获取responseId
```
#请求链接

#请求数据
callback: jQuery19108408108632218079_1543310767116  #估计用不到
showType: embed     #固定值(验证码类型)
sessionId: fd3b3e22d056408cb898d357e585f4f6  #网页中的值
_: 1543310767117  #时间

#返回数据
jQuery19108408108632218079_1543310767116({
    "message": "成功",
    "data": {
        "responseId": "ed3ce1892d6f4baa8e942e996a1553a7",
        "level": 310,
        "status": 0,
        "puzzleImgUrl": "/captcha/captcha_img?rid=ed3ce1892d6f4baa8e942e996a1553a7&it=_puzzle",
        "tip": "请点击并将滑块拖动到指定位置",
        "bgImgUrl": "/captcha/captcha_img?rid=ed3ce1892d6f4baa8e942e996a1553a7&it=_big"
    },
    "code": 0
})

```

4. 破解加密数据
- 知识点1,如果是xhr的请求,可以在**XHR/fetch Breakpoints**中打断点,数据url的部分值
- 知识点2,如果是js的请求,可以直接点进那个js文件
- 知识点3,点进的js文件会定位到ajax的内部函数,Call Stack可以看堆栈(点checkVerifyResult函数),可以看到熟悉的ajax请求

5. 加密数据是由CryptoJS加密的
- 只是一段js 下载这个js就行了

6. 路径数组的获得
因为路径和时间滑动的距离都有关系,如果只是用加速度模拟,我试了好久都没有试出来
我的做法是 直接打开google调试工具,在验证码滑动的地方打断点,然后重复滑动了200次,得到200个轨迹数组,以后直接去路径数组中找到对应的路径就可以了

7. 图片的滑动的距离
简单的像素分析,很垃圾,但是正确率80%+把

8. js
以前的做法是打一个node.js,将js代码全部丢进去
现在使用execJs


'use strict';

function success(test) {
    var textarea = document.getElementById('test-response-text');
    textarea.value = text;
}

function fail(code) {
    var textarea = document.getElementById('test-response-text');
    textarea.value = 'Error code: ' + code;
}

// 新建XMLHttpRequest对象 --> onreadystatechange  回调，判断状态
//                      -->  open  构造
//                      -->  send  发送
var request = new XMLHttpRequest();
// 低版本的IE
// var request = new ActiveXObject('Microsoft.XMLHTTP');

// 状态发生变化时的回调函数
request.onreadystatechange = function () {
    // 成功完成请求
    if (request.readyState === 4) {
        if (request.status === 200) {
            // 拿到数据
            return success(request.responseText);
        } else {
            // 某些原因导致失败
            return fail(request.status)
        }
    } else {
        // 请求还未完成
    }
};

request.open("GET", "/api/cat");
request.send();
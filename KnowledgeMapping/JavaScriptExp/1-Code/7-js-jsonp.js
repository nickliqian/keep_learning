function refreshPrice(data) {
    var p = document.getElementById('test-jsonp');
    p.innerHTML = '当前价格：' +
        data['0000001'].name +': ' +
        data['0000001'].price + '；' +
        data['1399001'].name + ': ' +
        data['1399001'].price;
}

// 页面加载的时候执行以下函数
function getPrice() {
    var
        js = document.createElement('script'), // 创建一个script标签
        head = document.getElementsByTagName('head')[0]; // 把自己创建的script标签放到head里面
    js.src = 'http://api.money.126.net/data/feed/0000001,1399001?callback=refreshPrice'; // 想script标签中加入src
    // 由于浏览器加载的时候会允许get请求scr资源，这个请求是可以成功的
    // <script src="http://api.money.126.net/data/feed/0000001,1399001?callback=refreshPrice"></script>
    head.appendChild(js); // script资源请求加入head中
    // 这个标签请求的时候，返回的数据为 refreshPrice(data) 此时会回调 refreshPrice 函数 执行
}

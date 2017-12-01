function add(x, y, f) {
    return f(x) + f(y);
}

function string2int(s) {
    var arr = s.split('').map(function (x) {
        return x * 1;
    });
    return arr.reduce(function (x, y) {
        return x * 10 + y;
    })
}

function normalize(arr) {
    return arr.map(function (x) {
        var a = x[0].toUpperCase();
        var b = x[1].toLowerCase();
        x = a + b;
        return x;
    })
}

function normalize(arr) {
    return arr.map(function (x) {
        return x[0].toUpperCase() + x.substring(1,).toLowerCase();
    })
    }

var arr = ['1', '2', '3'];
var r;
r = arr.map(x => parseInt(x));
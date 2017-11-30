'use strict';
var arr = ['Bart', 'Lisa', 'Adam'];


for (var i in arr) {
    console.log(`Hello, ${arr[i]}!`)
}

for (var i in arr) {
    console.log('Hello, ' + arr[i] + '!')
}

for (var i=0; i<arr.length; i++) {
    console.log(`Hello, ${arr[i]}!`)
}

for (var i=arr.length; i>0; i--) {
    console.log(`Hello, ${arr[i-1]}!`);
}

var i = 0;
while (i < arr.length) {
    console.log(`Hello, ${arr[i]}!`)
    i ++
}

var i = arr.length;
while (i > 0) {
    console.log(`Hello, ${arr[i-1]}!`)
    i --
}
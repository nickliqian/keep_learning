[1 基础知识](#1)
[1.1 Number](#1.1)
[1.2 字符串](#1.2)
[1.3 布尔值](#1.3)
[1.4 比较运算符](#1.4)
[1.5 null和undefined](#1.5)
[1.6 数组](#1.6)
[1.7 对象](#1.7)
[1.8 变量](#1.8)
[1.9 strict模式](#1.9)
[1.10 条件判断](#1.10)
[1.11 循环](#1.11)
[1.12 Map](#1.12)
[1.13 Set](#1.13)
[1.14 iterable](#1.14)

## 1、基础知识
<h3 id="1.1">1.1 Number</h3>
```
123; // 整数123
0.456; // 浮点数0.456
1.2345e3; // 科学计数法表示1.2345x1000，等同于1234.5
-99; // 负数
NaN; // NaN表示Not a Number，当无法计算结果时用NaN表示
Infinity; // Infinity表示无限大，当数值超过了JavaScript的Number所能表示的最大值时，就表示为Infinity
0xff00，0xa5b4c3d2;//十六进制用0x前缀和0-9，a-f表示,和十进制表示的数值完全一样
```
```
1 + 2; // 3
(1 + 2) * 5 / 2; // 7.5
2 / 0; // Infinity
0 / 0; // NaN
10 % 3; // 1
10.5 % 3; // 1.5
```
<h3 id="1.2">1.2 字符串</h3>
```
"123"
'123'
"abc"
'abc'
```
```
"I'm OK"
// 如果字符串内既有'又有"，使用转义字符\来标示
'I\'m \"OK\"!';
// ASCII字符可以以\x##形式的十六进制表示，例如：
'\x41'; // 完全等同于 'A'
// 还可以用\u####表示一个Unicode字符：
'\u4e2d\u6587'; // 完全等同于 '中文'
```
```
// 多行字符串
`这是一个
多行
字符串`;
```
```
var name = '小明';
var age = 20;
var message = '你好, ' + name + ', 你今年' + age + '岁了!';
alert(message);
```
```
// 模板字符串
var message = `你好, ${name}, 你今年${age}岁了!`;
// 操作字符串
var s = 'Hello, world!';
s.length; // 13
var s = 'Hello, world!';

s[0]; // 'H'
s[6]; // ' '
s[7]; // 'w'
s[12]; // '!'
s[13]; // undefined 超出范围的索引不会报错，但一律返回undefined
// 字符串是不可变的，如果对字符串的某个索引赋值，不会有任何错误，但是，也没有任何效果
var s = 'Test';
s[0] = 'X';
alert(s); // s仍然为'Test'
```
```
// 字符串方法
toUpperCase()
toLowerCase()
indexOf()
substring() // 返回子字符串
```
<h3 id="1.3">1.3 布尔值</h3>
```
true; // 这是一个true值
false; // 这是一个false值
2 > 1; // 这是一个true值
2 >= 3; // 这是一个false值
// `&&`运算是与运算，只有所有都为true，&&运算结果才是true：
true && true; // 这个&&语句计算结果为true
true && false; // 这个&&语句计算结果为false
false && true && false; // 这个&&语句计算结果为false
// `||`运算是或运算，只要其中有一个为true，||运算结果就是true：
false || false; // 这个||语句计算结果为false
true || false; // 这个||语句计算结果为true
false || true || false; // 这个||语句计算结果为true
// `!`运算是非运算，它是一个单目运算符，把true变成false，false变成true：
! true; // 结果为false
! false; // 结果为true
! (2 > 5); // 结果为true
```
```
var age = 15;
if (age >= 18) {
    alert('adult');
} else {
    alert('teenager');
}
```
<h3 id="1.4">1.4 比较运算符</h3>
```
// 当我们对Number做比较时，可以通过比较运算符得到一个布尔值
2 > 5; // false
5 >= 2; // true
7 == 7; // true
```
```
// 实际上，JavaScript允许对任意数据类型做比较：
false == 0; // true
false === 0; // false,数据类型不一致 bool不等于number
```
```
要特别注意相等运算符==。JavaScript在设计时，有两种比较运算符：
第一种是==比较，它会自动转换数据类型再比较，很多时候，会得到非常诡异的结果；
第二种是===比较，它不会自动转换数据类型，如果数据类型不一致，返回false，如果一致，再比较。
由于JavaScript这个设计缺陷，不要使用==比较，始终坚持使用===比较。
```
```
NaN === NaN; // false
isNaN(NaN); // true
1/3; // 0.3333333333333333
(1-2/3); // 0.33333333333333337
1 / 3 === (1 - 2 / 3); // false,由于计算机精度的原因无法准确表示
// 计算绝对值是否小于某个阀值
Math.abs(1 / 3 - (1 - 2 / 3)) < 0.0000001; // true
```
<h3 id="1.5">1.5 null和undefined</h3>
```
null表示一个“空”的值，它和0以及空字符串''不同，0是一个数值，''表示长度为0的字符串，而null表示“空”。
在其他语言中，也有类似JavaScript的null的表示，例如Java也用null，Swift用nil，Python用None表示。但是，在JavaScript中，还有一个和null类似的undefined，它表示“未定义”。
JavaScript的设计者希望用null表示一个空的值，而undefined表示值未定义。事实证明，这并没有什么卵用，区分两者的意义不大。大多数情况下，我们都应该用null。undefined仅仅在判断函数参数是否传递的情况下有用。
```
<h3 id="1.6">1.6 数组</h3>
```
[1, 2, 3.14, 'Hello', null, true]; // 建议使用
new Array(1, 2, 3); // 创建了数组[1, 2, 3]
```
```
var arr = [1, 2, 3.14, 'Hello', null, true];
// 注意起始索引值为0
arr[0]; // 返回索引为0的元素，即1
arr[5]; // 返回索引为5的元素，即true
arr[6]; // 索引超出了范围，返回undefined
```
```
var arr = [1, 2, 3.14, 'Hello', null, true];
arr.length; // 6
// 请注意，直接给Array的length赋一个新的值会导致Array大小的变化：
var arr = [1, 2, 3];
arr.length; // 3
arr.length = 6;
arr; // arr变为[1, 2, 3, undefined, undefined, undefined]
arr.length = 2;
arr; // arr变为[1, 2]
// Array可以通过索引把对应的元素修改为新的值，因此，对Array的索引进行赋值会直接修改这个Array：
var arr = ['A', 'B', 'C'];
arr[1] = 99;
arr; // arr现在变为['A', 99, 'C']
// 请注意，如果通过索引赋值时，索引超过了范围，同样会引起Array大小的变化：
var arr = [1, 2, 3];
arr[5] = 'x';
arr; // arr变为[1, 2, 3, undefined, undefined, 'x']
```
```
indexOf()
slice()
arr.slice(0, 3); // 从索引0开始，到索引3结束，但不包括索引3: ['A', 'B', 'C']
arr.slice(3); // 从索引3开始到结束: ['D', 'E', 'F', 'G']
push()
arr.push('A', 'B'); // 可以添加多个
pop() // 删除最后一个元素
// 空数组继续pop不会报错，而是返回undefined
unshift() // 头部添加元素
shift() // 删除第一个元素
arr.shift(); // 空数组继续shift不会报错，而是返回undefined
sort() // 排序
reverse() // 反转
splice()
newarr = arr.concat(arr) // 连接数组
// 实际上，concat()方法可以接收任意个元素和Array，并且自动把Array拆开，然后全部添加到新的Array里：
var arr = ['A', 'B', 'C'];
arr.concat(1, 2, [3, 4]); // ['A', 'B', 'C', 1, 2, 3, 4]
join()
```
```
// 多维数组
var arr = [[1, 2, 3], [400, 500, 600], '-'];
```
<h3 id="1.7">1.7 对象</h3>
```
// JavaScript对象的键都是字符串类型，值可以是任意数据类型。
var person = {
    name: 'Bob',
    age: 20,
    tags: ['js', 'web', 'mobile'],
    city: 'Beijing',
    hasCar: true,
    zipcode: null
};
person.name; // 'Bob'
person.zipcode; // null
```
```
访问属性是通过.操作符完成的，但这要求属性名必须是一个有效的变量名。如果属性名包含特殊字符，就必须用''括起来：

var xiaohong = {
    name: '小红',
    'middle-school': 'No.1 Middle School'
};
xiaohong的属性名middle-school不是一个有效的变量，就需要用''括起来。访问这个属性也无法使用.操作符，必须用['xxx']来访问：

xiaohong['middle-school']; // 'No.1 Middle School'
xiaohong['name']; // '小红'
xiaohong.name; // '小红'

访问不存在的属性不报错，而是返回undefined
```
```
var xiaoming = {
    name: '小明'
};
xiaoming.age; // undefined
xiaoming.age = 18; // 新增一个age属性
xiaoming.age; // 18
delete xiaoming.age; // 删除age属性
xiaoming.age; // undefined
delete xiaoming['name']; // 删除name属性
xiaoming.name; // undefined
delete xiaoming.school; // 删除一个不存在的school属性也不会报错
```
```
如果我们要检测xiaoming是否拥有某一属性，可以用in操作符：
'name' in xiaoming; // true
'grade' in xiaoming; // false

不过要小心，如果in判断一个属性存在，这个属性不一定是xiaoming的，它可能是xiaoming继承得到的：
'toString' in xiaoming; // true

因为toString定义在object对象中，而所有对象最终都会在原型链上指向object，所以xiaoming也拥有toString属性。
要判断一个属性是否是xiaoming自身拥有的，而不是继承得到的，可以用hasOwnProperty()方法：
xiaoming.hasOwnProperty('name'); // true
xiaoming.hasOwnProperty('toString'); // false
```
<h3 id="1.8">1.8 变量</h3>
```
var a; // 申明了变量a，此时a的值为undefined
var $b = 1; // 申明了变量$b，同时给$b赋值，此时$b的值为1
var s_007 = '007'; // s_007是一个字符串
var Answer = true; // Answer是一个布尔值true
var t = null; // t的值是null
// 只能用var申明一次
var a = 123; // a的值是整数123
a = 'ABC'; // a变为字符串
```
<h3 id="1.9">1.9 strict模式</h3>
```
JavaScript在设计之初，为了方便初学者学习，并不强制要求用var申明变量。
这个设计错误带来了严重的后果：
如果一个变量没有通过var申明就被使用，那么该变量就自动被申明为全局变量：
i = 10; // i现在是全局变量
```
```
启用strict模式的方法是在JavaScript代码的第一行写上：
'use strict';
```
<h3 id="1.10">1.10 条件判断</h3>
```
var age = 20;
if (age >= 18) { // 如果age >= 18为true，则执行if语句块
    alert('adult');
} else { // 否则执行else语句块
    alert('teenager');
}
```
```
其中else语句是可选的。如果语句块只包含一条语句，那么可以省略{}：
// 不加大括号只能作用一条语句
var age = 20;
if (age >= 18)
    alert('adult');
else
    alert('teenager');
```
```
多行条件判断

var age = 3;
if (age >= 18) {
    alert('adult');
} else if (age >= 6) {
    alert('teenager');
} else {
    alert('kid');
}
```
```
JavaScript把null、undefined、0、NaN和空字符串''视为false，其他值一概视为true
```
<h3 id="1.11">1.11 循环</h3>
```
ar x = 0;
var i;
for (i=1; i<=10000; i++) {
    x = x + i;
}
x; // 50005000

i=1 这是初始条件，将变量i置为1；
i<=10000 这是判断条件，满足时就继续循环，不满足就退出循环；
i++ 这是每次循环后的递增条件，由于每次循环后变量i都会加1，因此它终将在若干次循环后不满足判断条件i<=10000而退出循环。
```
```
var arr = ['Apple', 'Google', 'Microsoft'];
var i, x;
for (i=0; i<arr.length; i++) {
    x = arr[i];
    console.log(x);
}
```
```
for循环的3个条件都是可以省略的，如果没有退出循环的判断条件，就必须使用break语句退出循环，否则就是死循环：

var x = 0;
for (;;) { // 将无限循环下去
    if (x > 100) {
        break; // 通过if判断来退出循环
    }
    x ++;
}
```
```
for ... in

for循环的一个变体是for ... in循环，它可以把一个对象的所有属性依次循环出来：

var o = {
    name: 'Jack',
    age: 20,
    city: 'Beijing'
};
for (var key in o) {
    console.log(key); // 'name', 'age', 'city'
}
for (var key in o) {
    if (o.hasOwnProperty(key)) {
        console.log(key); // 'name', 'age', 'city'
    }
}
```
```
由于Array也是对象，而它的每个元素的索引被视为对象的属性，因此，for ... in循环可以直接循环出Array的索引：

var a = ['A', 'B', 'C'];
for (var i in a) {
    console.log(i); // '0', '1', '2'
    console.log(a[i]); // 'A', 'B', 'C'
}
请注意，for ... in对Array的循环得到的是String而不是Number。
```
```
while循环只有一个判断条件，条件满足，就不断循环，条件不满足时则退出循环。

var x = 0;
var n = 99;
while (n > 0) {
    x = x + n;
    n = n - 2;
}
x; // 2500
```
```
最后一种循环是do { ... } while()循环，它和while循环的唯一区别在于，不是在每次循环开始的时候判断条件，而是在每次循环完成的时候判断条件：

var n = 0;
do {
    n = n + 1;
} while (n < 100);
n; // 100
用do { ... } while()循环要小心，循环体会至少执行1次，而for和while循环则可能一次都不执行。
```
<h3 id="1.12">1.12 Map</h3>
```
var m = new Map([['Michael', 95], ['Bob', 75], ['Tracy', 85]]);
m.get('Michael'); // 95

初始化Map需要一个二维数组，或者直接初始化一个空Map。Map具有以下方法：

var m = new Map(); // 空Map
m.set('Adam', 67); // 添加新的key-value
m.set('Bob', 59);
m.has('Adam'); // 是否存在key 'Adam': true
m.get('Adam'); // 67
m.delete('Adam'); // 删除key 'Adam'
m.get('Adam'); // undefined
```
<h3 id="1.13">1.13 Set</h3>
```
Set和Map类似，也是一组key的集合，但不存储value。由于key不能重复，所以，在Set中，没有重复的key。
var s1 = new Set(); // 空Set
var s2 = new Set([1, 2, 3]); // 含1, 2, 3
s.add(12)
s.delete(12)
```
<h3 id="1.14">1.14 iterable</h3>
```
遍历Array可以采用下标循环，遍历Map和Set就无法使用下标。
为了统一集合类型，ES6标准引入了新的iterable类型，
Array、Map和Set都属于iterable类型。
```
```
具有iterable类型的集合可以通过新的for ... of循环来遍历。
用for ... of循环遍历集合，用法如下：

var a = ['A', 'B', 'C'];
var s = new Set(['A', 'B', 'C']);
var m = new Map([[1, 'x'], [2, 'y'], [3, 'z']]);
for (var x of a) { // 遍历Array
    console.log(x);
}
for (var x of s) { // 遍历Set
    console.log(x);
}
for (var x of m) { // 遍历Map
    console.log(x[0] + '=' + x[1]);
}
```
```
a.forEach(function (element, index, array) {
    // element: 指向当前元素的值
    // index: 指向当前索引
    // array: 指向Array对象本身
    console.log(element + ', index = ' + index);
});
// a可以是 array map set
```
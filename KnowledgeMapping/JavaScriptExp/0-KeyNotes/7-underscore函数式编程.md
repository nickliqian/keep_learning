[7 underscore](#7)
[7.1 Collections](#7.1)
[7.2 Arrays](#7.2)
[7.3 Functions](#7.3)
[7.4 Objects](#7.4)
[7.5 Chaining](#7.5)


## 7 underscore
<h3 id="7.1">7.1 Collections</h3>
```
map/filter
var obj = {
    name: 'bob',
    school: 'No.1 middle school',
    address: 'xueyuan road'
};
// 如果使用_.mapObject，会返回字典
var upper = _.map(obj, function (value, key) {
    return key + '->' + value;
});
```
```
every / some
当集合的所有元素都满足条件时，_.every()函数返回true，当集合的至少一个元素满足条件时，_.some()函数返回true
'use strict';
// 所有元素都大于0？
_.every([1, 4, 7, -3, -9], (x) => x > 0); // false
// 至少一个元素大于0？
_.some([1, 4, 7, -3, -9], (x) => x > 0); // true
```
```
max / min
这两个函数直接返回集合中最大和最小的数：
'use strict';
var arr = [3, 5, 7, 9];
_.max(arr); // 9
_.min(arr); // 3

// 空集合会返回-Infinity和Infinity，所以要先判断集合不为空：
_.max([])
-Infinity
_.min([])
Infinity
注意，如果集合是Object，max()和min()只作用于value，忽略掉key：

'use strict';
_.max({ a: 1, b: 2, c: 3 }); // 3
```
```
groupBy

groupBy()把集合的元素按照key归类，key由传入的函数返回：

'use strict';

var scores = [20, 81, 75, 40, 91, 59, 77, 66, 72, 88, 99];
var groups = _.groupBy(scores, function (x) {
    if (x < 60) {
        return 'C';
    } else if (x < 80) {
        return 'B';
    } else {
        return 'A';
    }
});
// 结果:
// {
//   A: [81, 91, 88, 99],
//   B: [75, 77, 66, 72],
//   C: [20, 40, 59]
// }
可见groupBy()用来分组是非常方便的。
```
```
shuffle / sample

shuffle()用洗牌算法随机打乱一个集合：

'use strict';
// 注意每次结果都不一样：
_.shuffle([1, 2, 3, 4, 5, 6]); // [3, 5, 4, 6, 2, 1]
sample()则是随机选择一个或多个元素：

'use strict';
// 注意每次结果都不一样：
// 随机选1个：
_.sample([1, 2, 3, 4, 5, 6]); // 2
// 随机选3个：
_.sample([1, 2, 3, 4, 5, 6], 3); // [6, 1, 4]
```
<h3 id="7.2">7.2 Arrays</h3>
```
first / last
顾名思义，这两个函数分别取第一个和最后一个元素：
'use strict';
var arr = [2, 4, 6, 8];
_.first(arr); // 2
_.last(arr); // 8
```
```
flatten
flatten()接收一个Array，无论这个Array里面嵌套了多少个Array，flatten()最后都把它们变成一个一维数组：
'use strict';
_.flatten([1, [2], [3, [[4], [5]]]]); // [1, 2, 3, 4, 5]
```
```
zip / unzip
zip()把两个或多个数组的所有元素按索引对齐，然后按索引合并成新数组。例如，你有一个Array保存了名字，另一个Array保存了分数，现在，要把名字和分数给对上，用zip()轻松实现：
'use strict';
var names = ['Adam', 'Lisa', 'Bart'];
var scores = [85, 92, 59];
_.zip(names, scores);
// [['Adam', 85], ['Lisa', 92], ['Bart', 59]]
```
```
unzip()则是反过来：
'use strict';
var namesAndScores = [['Adam', 85], ['Lisa', 92], ['Bart', 59]];
_.unzip(namesAndScores);
// [['Adam', 'Lisa', 'Bart'], [85, 92, 59]]
```
```
object
有时候你会想，与其用zip()，为啥不把名字和分数直接对应成Object呢？别急，object()函数就是干这个的：
'use strict';
var names = ['Adam', 'Lisa', 'Bart'];
var scores = [85, 92, 59];
_.object(names, scores);
// {Adam: 85, Lisa: 92, Bart: 59}
注意_.object()是一个函数，不是JavaScript的Object对象。
```
```
range
range()让你快速生成一个序列，不再需要用for循环实现了：
'use strict';
// 从0开始小于10:
_.range(10); // [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
// 从1开始小于11：
_.range(1, 11); // [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
// 从0开始小于30，步长5:
_.range(0, 30, 5); // [0, 5, 10, 15, 20, 25]
// 从0开始大于-10，步长-1:
_.range(0, -10, -1); // [0, -1, -2, -3, -4, -5, -6, -7, -8, -9]
```
```
去重
var result = _.uniq(arr,false,(x)=>x.toUpperCase());
```
<h3 id="7.3">7.3 Functions</h3>
```
bind()
当用一个变量fn指向一个对象的方法时，直接调用fn()是不行的，因为丢失了this对象的引用。用bind可以修复这个问题。
var s = ' Hello  ';
var fn = _.bind(s.trim, s);
fn();
// 输出Hello
```
```
partial
Math.pow(x, y)
var pow2N = _.partial(Math.pow, 2); // 固定第一个参数为2
var cube = _.partial(Math.pow, _, 3); // 固定第二个参数为3
```
```
memoize
如果一个函数调用开销很大，我们就可能希望能把结果缓存下来，以便后续调用时直接获得结果。
var factorial = _.memoize(function(n) {
    console.log('start calculate ' + n + '!...');
    if (n < 2) {
        return 1;
    }
    return n * factorial(n - 1);
});
```
```
once
once 保证某个函数执行且仅一次
var register = _.once(function () {
    alert('Register ok!');
});
```
```
delay
_.delay(alert, 2000);
_.delay(console.log, 2000, 'Hello,', 'world!');
```
<h3 id="7.4">7.4 Objects</h3>
```
keys / allKeys /values
keys()可以非常方便地返回一个object自身所有的key，但不包含从原型链继承下来的
allKeys()除了object自身的key，还包含从原型链继承下来的
values
和keys()类似，values()返回object自身但不包含原型链继承的所有值
```
```
mapObject
mapObject()就是针对object的map版本：
'use strict';
var obj = { a: 1, b: 2, c: 3 };
// 注意传入的函数签名，value在前，key在后:
_.mapObject(obj, (v, k) => 100 + v); // { a: 101, b: 102, c: 103 }
```
```
invert
invert()把object的每个key-value来个交换，key变成value，value变成key：
'use strict';
_.invert(obj); // { '59': 'Bart', '85': 'Lisa', '90': 'Adam' }
```
```
extend / extendOwn
extend()把多个object的key-value合并到第一个object并返回
_.extend({name: 'Bob', age: 20}, {age: 15}, {age: 88, city: 'Beijing'});
注意：如果有相同的key，后面的object的value将覆盖前面的object的value。
extendOwn()和extend()类似，但获取属性时忽略从原型链继承下来的属性。
```
```
clone
浅复制
如果我们要复制一个object对象，就可以用clone()方法，它会把原有对象的所有属性都复制到新的对象中
var copied = _.clone(source);
指向同一个
```
```
isEqual
isEqual()对两个object进行深度比较，如果内容完全相同，则返回true
```
<h3 id="7.5">7.5 Chaining</h3>
```
链式调用
var r = _.chain([1, 4, 9, 16, 25])
         .map(Math.sqrt)
         .filter(x => x % 2 === 1)
         .value();

```


























# 判断js中的数据类型的几种方法
from https://www.cnblogs.com/dushao/p/5999563.html

判断js中的数据类型有一下几种方法：typeof、instanceof、 constructor、 prototype、 $.type()/jquery.type(),接下来主要比较一下这几种方法的异同。

### 0. 先举几个例子：
```
var a = "iamstring.";
var b = 222;
var c= [1,2,3];
var d = new Date();
var e = function(){alert(111);};
var f = function(){this.name="22";};
```
### 1. 最常见的判断方法：typeof
```
alert(typeof a)   ------------> string
alert(typeof b)   ------------> number
alert(typeof c)   ------------> object
alert(typeof d)   ------------> object
alert(typeof e)   ------------> function
alert(typeof f)   ------------> function
其中typeof返回的类型都是字符串形式，需注意，例如：
alert(typeof a == "string") -------------> true
alert(typeof a == String) ---------------> false
另外typeof 可以判断function的类型；在判断除Object类型的对象时比较方便。
```
### 2. 判断已知对象类型的方法： instanceof
```
alert(c instanceof Array) ---------------> true
alert(d instanceof Date)
alert(f instanceof Function) ------------> true
alert(f instanceof function) ------------> false
注意：instanceof 后面一定要是对象类型，并且大小写不能错，该方法适合一些条件选择或分支。
```
### 3. 根据对象的constructor判断： constructor
```
alert(c.constructor === Array) ----------> true
alert(d.constructor === Date) -----------> true
alert(e.constructor === Function) -------> true
注意： constructor 在类继承时会出错
eg：
      function A(){};
      function B(){};
      A.prototype = new B(); //A继承自B
      var aObj = new A();
      alert(aobj.constructor === B) -----------> true;
      alert(aobj.constructor === A) -----------> false;
而instanceof方法不会出现该问题，对象直接继承和间接继承的都会报true：
      alert(aobj instanceof B) ----------------> true;
      alert(aobj instanceof B) ----------------> true;
言归正传，解决construtor的问题通常是让对象的constructor手动指向自己：
      aobj.constructor = A; //将自己的类赋值给对象的constructor属性
      alert(aobj.constructor === A) -----------> true;
      alert(aobj.constructor === B) -----------> false; //基类不会报true了;
```
### 4. 通用但很繁琐的方法： prototype
```
alert(Object.prototype.toString.call(a) === ‘[object String]’) -------> true;
alert(Object.prototype.toString.call(b) === ‘[object Number]’) -------> true;
alert(Object.prototype.toString.call(c) === ‘[object Array]’) -------> true;
alert(Object.prototype.toString.call(d) === ‘[object Date]’) -------> true;
alert(Object.prototype.toString.call(e) === ‘[object Function]’) -------> true;
alert(Object.prototype.toString.call(f) === ‘[object Function]’) -------> true;
大小写不能写错，比较麻烦，但胜在通用。
```
### 5. 无敌万能的方法：jquery.type()
```
如果对象是undefined或null，则返回相应的“undefined”或“null”。
jQuery.type( undefined ) === "undefined"
jQuery.type() === "undefined"
jQuery.type( window.notDefined ) === "undefined"
jQuery.type( null ) === "null"
如果对象有一个内部的[[Class]]和一个浏览器的内置对象的 [[Class]] 相同，我们返回相应的 [[Class]] 名字。 (有关此技术的更多细节。 )
jQuery.type( true ) === "boolean"
jQuery.type( 3 ) === "number"
jQuery.type( "test" ) === "string"
jQuery.type( function(){} ) === "function"
jQuery.type( [] ) === "array"
jQuery.type( new Date() ) === "date"
jQuery.type( new Error() ) === "error" // as of jQuery 1.9
jQuery.type( /test/ ) === "regexp"
其他一切都将返回它的类型“object”。
```

>通常情况下用typeof 判断就可以了，遇到预知Object类型的情况可以选用instanceof或constructor方法,实在没辙就使用$.type()方法。
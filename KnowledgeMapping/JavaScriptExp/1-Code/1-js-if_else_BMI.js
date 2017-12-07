'use strict';

var height = parseFloat(prompt('请输入身高(m):'));
var weight = parseFloat(prompt('请输入体重(kg):'));
var bmi = weight/(height**2);
if (bmi < 18.5) {
    alert('过轻');
} else if (bmi >= 18.5 && bmi <= 25) {
    alert('正常');
} else if (bmi >= 25 && bmi <= 28) {
    alert('过重');
} else if (bmi >= 28 && bmi <= 32) {
    alert('肥胖');
} else {
    alert('严重肥胖');
}
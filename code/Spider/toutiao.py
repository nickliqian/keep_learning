import requests
import math
import hashlib


# 字符串按md5算法编码
def md5(string):
    return hashlib.md5(string.encode('utf-8')).hexdigest()

time_c = 1512375652000

t = math.floor(time_c/1000)

i = hex(int(t)).upper()[2:]
e = md5(str(t)).upper()

if len(i) != 8:
    as_ = "479BB4B7254C150"
    cp_ = "7E0AC8874BB0985"

s = e[0:5]
o = e[-5:]
print('i', i)
print('e', e)
print('s', s)
print('o', o)
n = ""
for a in range(5):
    n += s[a] + i[a]
print('n', n)

l = ""
for r in range(5):
    l += i[r + 3] + o[r]
print('l', l)

as_ = "A1" + n + i[-3:]
cp_ = i[0:3] + l + "E1"
print('as_', as_)
print('cp_', cp_)


user_id = "4540952864"


'''
!function(t) {
    var i = {};
    i.getHoney = function() {
        var t = Math.floor((new Date).getTime() / 1e3)
          , i = t.toString(16).toUpperCase()
          , e = md5(t).toString().toUpperCase();
        if (8 != i.length)
            return {
                as: "479BB4B7254C150",
                cp: "7E0AC8874BB0985"
            };
        for (var s = e.slice(0, 5), o = e.slice(-5), n = "", a = 0; 5 > a; a++)
            n += s[a] + i[a];
        for (var l = "", r = 0; 5 > r; r++)
            l += i[r + 3] + o[r];
        return {
            as: "A1" + n + i.slice(-3),
            cp: i.slice(0, 3) + l + "E1"
        }
    }
    ,
    t.ascp = i
}(window, document),


function o() {
    var t, i = ascp.getHoney(), e = "";
    return window.TAC && (e = TAC.sign(userInfo.id + "" + c.params.max_behot_time)),
    t = _.extend({}, c.params, {
        as: i.as,
        cp: i.cp,
        _signature: e
    })
}
'''
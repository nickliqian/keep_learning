import execjs


class jsReg():
    def __init__(self):
        self.ctx = execjs.compile("""
        function test(n, e, i) {
            t = "U;;=>99<??28U;:U8:U48261efeced332cc9f20413132c69381e96e4aafcc39a24366a39c806f2d8efa"
            e = e || 0,
            i = i || 10;
            for (var o = "_" + n + "_" + e + "_" + i + "_", a = "", c = 0; c < o.length; c++) {
                var r = 10 ^ o.charCodeAt(c);
                a += String.fromCharCode(r)
            }
            t = /^U.+?U.{1,3}U.{1,3}U/.test(t) ? t.replace(/^U.+?U.{1,3}U.{1,3}U/, a) : a + t,
            console.log("sptoken=" + encodeURIComponent(t) + ";domain=.yidianzixun.com;path=/;max-age=2592000")
        }
        """)

    def get_reg_text(self, c, e, i):
        return self.ctx.call(c, e, i)


ctx = execjs.compile("""
     function test(n, e, i) {
            t = "U;;=>99<??28U;:U8:U48261efeced332cc9f20413132c69381e96e4aafcc39a24366a39c806f2d8efa"
            e = e || 0,
            i = i || 10;
            for (var o = "_" + n + "_" + e + "_" + i + "_", a = "", c = 0; c < o.length; c++) {
                var r = 10 ^ o.charCodeAt(c);
                a += String.fromCharCode(r)
            }
            t = /^U.+?U.{1,3}U.{1,3}U/.test(t) ? t.replace(/^U.+?U.{1,3}U.{1,3}U/, a) : a + t,
            co = "sptoken=" + encodeURIComponent(t) + ";domain=.yidianzixun.com;path=/;max-age=2592000"
            co1 = encodeURIComponent(t)
            return co1;
        }
     """)
s = ctx.call("test", 11743365582, 10, 20)

print(s)
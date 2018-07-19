import execjs


# ctx = execjs.compile("""
#      function test(n, e, i) {
#             t = "U;;=>99<??28U;:U8:U48261efeced332cc9f20413132c69381e96e4aafcc39a24366a39c806f2d8efa"
#             e = e || 0,
#             i = i || 10;
#             for (var o = "_" + n + "_" + e + "_" + i + "_", a = "", c = 0; c < o.length; c++) {
#                 var r = 10 ^ o.charCodeAt(c);
#                 a += String.fromCharCode(r)
#             }
#             t = /^U.+?U.{1,3}U.{1,3}U/.test(t) ? t.replace(/^U.+?U.{1,3}U.{1,3}U/, a) : a + t,
#             co = "sptoken=" + encodeURIComponent(t) + ";domain=.yidianzixun.com;path=/;max-age=2592000"
#             co1 = encodeURIComponent(t)
#             return co1;
#         }
#      """)
#
# r = ctx.call("test", 2, 10, 20)
#
# print(r)


def import_js_file(path):
    with open(path, "r") as f:
        p = execjs.compile(f.read())
    return p


pwd = import_js_file("/home/nick/Desktop/bj/js/aes.js")
# import_js_file("/home/nick/Desktop/bj/js/jsencrypt.min.js")
# import_js_file("/home/nick/Desktop/bj/js/pbkdf2.js")
# import_js_file("/home/nick/Desktop/bj/js/encrypt.js")

# pwd = execjs.compile("""
#      function test(data) {
#             keyEncrypt(data);
#         }
# """)

r = pwd.call("keyEncrypt", "1qaz@WSX")

print(r)
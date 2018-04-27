import redis
import json


a = ["A - 安徽 ",
     "B - 北京 ",
     "C - 重庆 ",
     "F - 福建 ",
     "G - 甘肃 ",
     "G - 广东 ",
     "G - 广西 ",
     "G - 贵州 ",
     "H - 海南 ",
     "H - 河北 ",
     "H - 黑龙江 ",
     "H - 河南 ",
     "H - 湖北 ",
     "H - 湖南 ",
     "J - 江苏 ",
     "J - 江西 ",
     "J - 吉林 ",
     "L - 辽宁 ",
     "N - 内蒙古 ",
     "N - 宁夏 ",
     "Q - 青海 ",
     "S - 山东 ",
     "S - 上海 ",
     "S - 山西 ",
     "S - 陕西 ",
     "S - 四川 ",
     "T - 天津 ",
     "X - 新疆 ",
     "X - 西藏 ",
     "Y - 云南 ",
     "Z - 浙江 ",
     "Z - 总局", ]

b = [
    "/g_AH.html",
    "/g_BJ.html",
    "/g_CQ.html",
    "/g_FJ.html",
    "/g_GS.html",
    "/g_GD.html",
    "/g_GX.html",
    "/g_GZ.html",
    "/g_HAIN.html",
    "/g_HB.html",
    "/g_HLJ.html",
    "/g_HEN.html",
    "/g_HUB.html",
    "/g_HUN.html",
    "/g_JS.html",
    "/g_JX.html",
    "/g_JL.html",
    "/g_LN.html",
    "/g_NMG.html",
    "/g_NX.html",
    "/g_QH.html",
    "/g_SD.html",
    "/g_SH.html",
    "/g_SX.html",
    "/g_SAX.html",
    "/g_SC.html",
    "/g_TJ.html",
    "/g_XJ.html",
    "/g_XZ.html",
    "/g_YN.html",
    "/g_ZJ.html",
    "/g_CN.html",
]


citys = []
for i in a:
    city = i.split("-")[1].strip()
    citys.append(city)

print(citys)

codes = []
for j in b:
    code = j.strip("/").split(".")[0].split("_")[1]
    codes.append(code)

print(codes)


p = [{"city": citys[k], "code": codes[k]} for k in range(len(citys))]


redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
redis_conn = redis.Redis(connection_pool=redis_pool)

print(p)
for o in p:
    redis_conn.sadd("QCC:area_dict", o)
    print(o)

# data_b = redis_conn.spop("QCC:area_dict")
# print(data_b)
# data = data_b.decode("utf8")
# print(data)
# s = eval(data)
# print(type(s))
# print(s)
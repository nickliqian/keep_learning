import redis


# 连接redis
print("Connect to redis...")
r_pool = redis.ConnectionPool(host="192.168.70.40", port=6379)
r_conn = redis.Redis(connection_pool=r_pool)


"""
("北京", 3193.20, "beijing"),
("天津", 247382, "tianjin"),
"""

pro_list = [
("河北", 889070, "hebei"),
("内蒙古", 134518, "neimenggu"),
("山西", 183114, "shanxi"),
("上海", 736428, "shanghai"),
("安徽", 515414, "anhui"),
("江苏", 901205, "jiangsu"),
("浙江", 1371133, "zhejiang"),
("山东", 902085, "shandong"),
("江西", 307576, "jiangxi"),
("福建", 574749, "fujian"),
("广东", 1846066, "guangdong"),
("广西", 180793, "guangxi"),
("海南", 66684, "hainan"),
("河南", 657960, "henan"),
("湖北", 470454, "hubei"),
("湖南", 557812, "hunan"),
("黑龙江", 228890, "heilongjiang"),
("吉林", 174317, "jilin"),
("辽宁", 393191, "liaoning"),
("陕西", 353059, "shaanxi"),
("甘肃", 153848, "gansu"),
("宁夏", 51125, "ningxia"),
("青海", 42706, "qinghai"),
("新疆", 91278, "xinjiang"),
("重庆", 277941, "chongqing"),
("四川", 430483, "sichuan"),
("云南", 275368, "yunnan"),
("贵州", 191819, "guizhou"),
("西藏", 29303, "xizang")]

pro_pages_list = [['河北', 30435, 'hebei'],
                  ['内蒙古', 5283, 'neimenggu'],
                  ['山西', 6903, 'shanxi'],
                  ['上海', 25347, 'shanghai'],
                  ['安徽', 17980, 'anhui'],
                  ['江苏', 30840, 'jiangsu'],
                  ['浙江', 46504, 'zhejiang'],
                  ['山东', 30869, 'shandong'],
                  ['江西', 11052, 'jiangxi'],
                  ['福建', 19958, 'fujian'],
                  ['广东', 62335, 'guangdong'],
                  ['广西', 6826, 'guangxi'],
                  ['海南', 3022, 'hainan'],
                  ['河南', 22732, 'henan'],
                  ['湖北', 16481, 'hubei'],
                  ['湖南', 19393, 'hunan'],
                  ['黑龙江', 8429, 'heilongjiang'],
                  ['吉林', 6610, 'jilin'],
                  ['辽宁', 13906, 'liaoning'],
                  ['陕西', 12568, 'shaanxi'],
                  ['甘肃', 5928, 'gansu'],
                  ['宁夏', 2504, 'ningxia'],
                  ['青海', 2223, 'qinghai'],
                  ['新疆', 3842, 'xinjiang'],
                  ['重庆', 10064, 'chongqing'],
                  ['四川', 15149, 'sichuan'],
                  ['云南', 9978, 'yunnan'],
                  ['贵州', 7193, 'guizhou'],
                  ['西藏', 1776, 'xizang']]

if __name__ == '__main__':
    for pro in pro_pages_list:
        area = pro[0]
        number = pro[1]
        mark = pro[2]
        for i in range(number):
            tup = (area, str(i), mark)
            print(tup)
            r_conn.sadd("mingluji", tup)
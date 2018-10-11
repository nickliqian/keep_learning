import requests
from lxml import etree
import time


def crawl_list(page):
    url = "https://www.tianyancha.com/order/getOrderList.json"

    payload = "{\"pageNum\":" + str(page) + ",\"pageSize\":20,\"types\":\"20\"}"
    headers = {
        'accept': "*/*",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9",
        'cache-control': "no-cache",
        'connection': "keep-alive",
        'content-length': "40",
        'content-type': "application/json; charset=UTF-8",
        'cookie': "jsid=SEM-BD-GS-SY-28196; TYCID=c7eaade0ae7611e88d0c6df049ee76f0; undefined=c7eaade0ae7611e88d0c6df049ee76f0; ssuid=4227072815; aliyungf_tc=AQAAAE+ZZD0ISAsAD1Wwb4AOTTRZ0TTs; csrfToken=tha3vDcny5IW9VOAQHVlHqWp; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1535868584,1538228424,1538409730; _ga=GA1.2.1854989010.1538409731; _gid=GA1.2.1322157669.1538409731; RTYCID=dbb2321298f54a1885d9d6da380e7c08; CT_TYCID=1dfa05cdb6b746969e0e94d8a8375325; cloud_token=1cb238e5c365481486cebd96cdc6e06c; cloud_utm=63dd4acd55034da4bc60f5a20246edc5; _gat_gtag_UA_123487620_1=1; tyc-user-info=%257B%2522contactNumber%2522%253A%252215898896288%2522%252C%2522post%2522%253A%25223%2522%252C%2522claimDetailLevel%2522%253A%252220%2522%252C%2522nickname%2522%253A%2522%25E5%2585%25B1%25E7%2594%25A8%25E5%258F%258B%2520%25E7%259C%258B%25E8%25AF%25A6%25E7%25BB%2586%25E8%25B5%2584%25E6%2596%2599%2522%252C%2522integrity%2522%253A%252271%2525%2522%252C%2522state%2522%253A%25223%2522%252C%2522surday%2522%253A%252291%2522%252C%2522companyName%2522%253A%2522%25E5%25B1%25B1%25E4%25B8%259C%25E7%259C%2581%25E4%25BA%25BF%25E5%25BD%25A9%25E9%2592%25A2%25E9%2593%2581%25E6%259C%2589%25E9%2599%2590%25E5%2585%25AC%25E5%258F%25B8%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25220%2522%252C%2522onum%2522%253A%25222712%2522%252C%2522isExpired%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNzA0MDgzODQ2NCIsImlhdCI6MTUzODQxMTc0NCwiZXhwIjoxNTUzOTYzNzQ0fQ.gyNcfD8YIj7Er1_Enc__p8CLGDKA39FTr1nK8sc1TOTTrWHuLHx2MLqPF4VIOJpKUg-b8TxTk729u7QitF1UvQ%2522%252C%2522realName%2522%253A%2522%25E8%25AE%25B8%25E9%2587%2591%25E8%25B6%2585%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252217040838464%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNzA0MDgzODQ2NCIsImlhdCI6MTUzODQxMTc0NCwiZXhwIjoxNTUzOTYzNzQ0fQ.gyNcfD8YIj7Er1_Enc__p8CLGDKA39FTr1nK8sc1TOTTrWHuLHx2MLqPF4VIOJpKUg-b8TxTk729u7QitF1UvQ; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1538411755",
        'host': "www.tianyancha.com",
        'origin': "https://www.tianyancha.com",
        'pragma': "no-cache",
        'referer': "https://www.tianyancha.com/usercenter/myorder",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
        'x-requested-with': "XMLHttpRequest",
        }

    response = sess.request("POST", url, data=payload, headers=headers)
    print(response.text)
    html = etree.HTML(response.text)
    results = html.xpath("//a[@class='click pr20 ']/@href")
    print("[page {}] result count is {}".format(page, len(results)))
    if len(results) != 0:
        with open("./href.list", "a+") as f:
            for r in results:
                f.write("{}\n".format(r))
    return len(results)


if __name__ == '__main__':
    sess = requests.session()
    for i in range(1, 119):
        f = crawl_list(i)
        if f == 0:
            break
        time.sleep(1)

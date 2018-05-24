import requests
from lxml import etree


def get_company_touzi_data(unique, company_a_name, page_num):
    # 公司id
    querystring["unique"] = unique
    # 公司名称
    querystring["companyname"] = company_a_name
    # 页码
    querystring["p"] = str(page_num)

    response = requests.request("GET", url, headers=headers, params=querystring)

    if response.text.strip() == "":
        print("已经是最后一页...")
        return None

    html = etree.HTML(response.text)

    rs = html.xpath("//tr[position()>1]")

    items = []
    for r in rs:
        print("----------------->")
        # 投资企业名称
        company_a_name = company_a_name
        # 投资企业id
        company_a_id = "华为软件技术有限公司"

        # 被投资企业名称
        company_b_name = r.xpath("./td[1]/a/text()")[0].strip()
        # 被投资企业id
        company_b_id = r.xpath("./td[1]/a/@href")[0].strip()

        # 被投资法定代表人
        company_b_people = r.xpath("./td[2]/a[1]/text()")[0].strip()
        # 被投资法定代表人id
        company_b_people_id = r.xpath("./td[2]/a[1]/@href")[0].strip()
        # 对外投资与任职URL
        company_b_people_investment = r.xpath("./td[2]/a[2]/@href")[0].strip()

        # 注册资本
        company_b_investment = r.xpath("./td[3]/text()")[0].strip()
        # 出资比例
        company_a_money_percent = r.xpath("./td[4]/text()")[0].strip()
        # 成立日期
        company_b_invest_time = r.xpath("./td[5]/text()")[0].strip()
        # 状态
        company_b_status = r.xpath("./td[6]/span/text()")[0].strip()

        print("company_a_name: {}".format(company_a_name))
        print("company_a_id: {}".format(company_a_id))
        print("company_b_name: {}".format(company_b_name))
        print("company_b_id: {}".format(company_b_id))
        print("company_b_people: {}".format(company_b_people))
        print("company_b_people_id: {}".format(company_b_people_id))
        print("company_b_people_investment: {}".format(company_b_people_investment))
        print("company_b_investment: {}".format(company_b_investment))
        print("company_a_money_percent: {}".format(company_a_money_percent))
        print("company_b_invest_time: {}".format(company_b_invest_time))
        print("company_b_status: {}".format(company_b_status))

        print()


if __name__ == '__main__':
    url = "https://www.qichacha.com/company_getinfos"

    querystring = {"unique": "967bb69bdc8f5597c0df535ce0a62d3a",
                   "companyname": "华为软件技术有限公司",
                   "p": "1",
                   "tab": "base",
                   "box": "touzi"
                   }

    headers = {
        'referer': "https://www.qichacha.com/firm_CN_6b242b475738f45a4dd180564d029aa9.html",
        'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
        'x-requested-with': "XMLHttpRequest",
        'Cache-Control': "no-cache",
    }

    name_id = "f6608ad5de43e68ba1706655f4f9ae0a"
    name = "江苏华为工程物资有限公司"
    num = 1
    get_company_touzi_data(name_id, name, num)
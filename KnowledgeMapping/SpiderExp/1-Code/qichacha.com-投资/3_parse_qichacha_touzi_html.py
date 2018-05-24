from lxml import etree


with open("./qichacha_touzi.html", "r") as f:
    content = f.read()

html = etree.HTML(content)

rs = html.xpath("//tr[position()>1]")

for r in rs:
    print("----------------->")
    # 投资企业名称
    companyA_name = "华为软件技术有限公司"
    # 投资企业id
    companyA_id = "华为软件技术有限公司"

    # 被投资企业名称
    companyB_name = r.xpath("./td[1]/a/text()")[0].strip()
    # 被投资企业id
    companyB_id = r.xpath("./td[1]/a/@href")[0].strip()

    # 被投资法定代表人
    companyB_people = r.xpath("./td[2]/a[1]/text()")[0].strip()
    # 被投资法定代表人id
    companyB_people_id = r.xpath("./td[2]/a[1]/@href")[0].strip()
    # 对外投资与任职URL
    companyB_people_investment = r.xpath("./td[2]/a[2]/@href")[0].strip()

    # 注册资本
    companyB_investment = r.xpath("./td[3]/text()")[0].strip()
    # 出资比例
    companyA_money_percent = r.xpath("./td[4]/text()")[0].strip()
    # 成立日期
    companyB_invest_time = r.xpath("./td[5]/text()")[0].strip()
    # 状态
    companyB_status = r.xpath("./td[6]/span/text()")[0].strip()

    print("companyA_name: {}".format(companyA_name))
    print("companyA_id: {}".format(companyA_id))
    print("companyB_name: {}".format(companyB_name))
    print("companyB_id: {}".format(companyB_id))
    print("companyB_people: {}".format(companyB_people))
    print("companyB_people_id: {}".format(companyB_people_id))
    print("companyB_people_investment: {}".format(companyB_people_investment))
    print("companyB_investment: {}".format(companyB_investment))
    print("companyA_money_percent: {}".format(companyA_money_percent))
    print("companyB_invest_time: {}".format(companyB_invest_time))
    print("companyB_status: {}".format(companyB_status))

    print()



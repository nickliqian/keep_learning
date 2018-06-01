from lxml import etree


with open("my_file.csv", "w") as f:
    pass

j = 1
items = []
for i in range(1,5):
    with open("./yemian/{}.html".format(i), "r") as f:
        content = f.read()

    result = etree.HTML(content)

    rs = result.xpath("/html/body/div[@class='taptap-top-card']")

    for r in rs:
        item = {}
        item["rank"] = r.xpath("./span[@class='top-card-order-text']/text()")[0]
        item["name"] = r.xpath("./div[@class='top-card-middle']/a[@class='card-middle-title ']/h4/text()")
        if not item["name"]:
            item["name"] = r.xpath("./div[@class='top-card-middle']/a[@class='card-middle-title hasArea']/h4/text()")
        item["name"] = item["name"][0]

        item["company"] = r.xpath("./div[@class='top-card-middle']/p[@class='card-middle-author']/a/text()")[0]
        item["type"] = r.xpath("./div[@class='top-card-middle']/div[@class='card-middle-footer']/a/text()")[0]
        item["point"] = r.xpath("./div[@class='top-card-middle']/div[@class='card-middle-footer']/p[@class='middle-footer-rating']/span/text()")[0]

        print(item)
        with open("my_file.csv", "a+") as f:
            s = [str(j), item["name"], item["company"], item["type"], item["point"]]
            s = ",".join(s)
            f.write(s + "\n")
            j += 1

# with open("my_file.csv", "w") as f:
#     for item in items:
#         s = [item["rank"], item["name"], item["company"], item["type"], item["point"]]
#         s = ",".join(s)
#         print(s)
#         f.write(s+"\n")



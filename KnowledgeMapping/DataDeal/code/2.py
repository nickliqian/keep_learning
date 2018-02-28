
line = '3615433,"[""甘佰刚"", ""http://www.hljcredit.gov.cn/WebCreditQueryService.do?sxbzxrDetail&dsname=hlj&dt=1&icautiouid=1230610005741300666&srandRe=9X8V46W56HUSW4T5KG80S46B6F6WK6"", ""622323******** 675X"", ""1230610005741300666""]",1,"{""案号："": ""2015年阿执字第00294号"", ""企业法人/负责人姓名："": ""甘佰刚"", ""性别："": ""男性"", ""年龄："": ""31"", ""身份证号："": ""622323******** 675X"", ""企业法人/负责人姓名：-mark"": """", ""地域名称："": ""新疆"", ""执行法院："": ""阿图什市人民法院"", ""执行依据文号："": ""（2011）阿民初字第858号民事判决书"", ""作出执行依据单位："": """", ""被执行人的履行情况："": ""全部未履行"", ""失信被执行人具体情形："": ""其他有履行能力而拒不履行生效法律文书确定义务的"", ""已履行部分："": ""暂无"", ""未履行部分："": ""暂无"", ""立案时间："": ""2015年06月30日"", ""发布时间："": ""2015年10月28日""}",2018-02-27 15:36:39'

try:
    if "{}" in line:
        print("Data is empty -> {}".format(line))
    else:
        content = ("[" + f.readline() + "]").replace('""', '"') \
            .replace('"["', '["').replace('"]"', '"]') \
            .replace('"{"', '{"').replace('"}"', '"}').replace('\n', '')

        t = content.split('"},')
        print("分割长度：{} {}".format(len(t), content))

        s = t[0] + '"},' + '"' + t[1][:-1] + '"' + ']'

        print(s)
        data = json.loads(s)
        records.append(data)
except Exception as e:
    print("异常1 {}".format(line))
    content = ("[" + f.readline() + "]").replace('""', '"') \
        .replace('"["', '["').replace('"]"', '"]') \
        .replace('"{"', '{"').replace('"}"', '"}').replace('\n', '')

    t = content.split('"},')
    print("----", t)
    raise e
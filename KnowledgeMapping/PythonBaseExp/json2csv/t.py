# coding=utf-8
import json
import re

# origin = '{"priority": "1.0", "type": "失信被执行人名单", "age": "46", "sexy": "男", "lastmod": "2018-03-06T16:19:37", "StdStg": 6899, "loc": "http://shixin.court.gov.cn/detail?id=701170373", "duty": "一、	被申请执行人为杨思卫、毛友萍、曲宝庆。二、执行标的为借款本金人民币30万元及利息人民币10869.74元整（截止至2017年1月20日），2017年1月21日起，利息在原借款执行利率基础上上浮50%，按年利率15.66%计算，对应付未付利息记收复利。根据《中华人民共和国民事诉讼法》第二百三十九条的规定，申请执行的期间为二年。申请执行时效的中止、中断，适用法律有关诉讼时效中止、中断的规定。前款规定的期间，从法律文书规定履行期间的最后一日起计算；法律文书规定分期履行的，从规定的每次履行期间的最后一日起计算；法律文书未规定履行期间的，从法律文书生效之日起计算。", "caseCode": "(2017)鲁1302执791号", "partyTypeName": "0", "_version": 18330, "regDate": "20170209", "courtName": "临沂市兰山区人民法院", "cambrian_appid": "0", "performedPart": "暂无", "areaName": "山东", "performance": "全部未履行", "_select_time": 1520344724, "iname": "曲宝庆", "unperformPart": "暂无", "publishDateStamp": "1506441600", "publishDate": "2017年09月27日", "cardNum": "37280119701****7692", "StdStl": 8, "gistId": "（2017）临兰山证执字第76号", "_update_time": "1520345343", "changefreq": "always", "businessEntity": "", "gistUnit": "山东省临沂市兰山区公证处", "focusNumber": "0", "SiteId": 2004188, "sitelink": "http://shixin.court.gov.cn/", "disruptTypeName": "被执行人无正当理由拒不履行执行和解协议"}'
#
# old = origin.replace("	", "")
# print(old)
# new = json.loads(old)
# print(new)

# origin = '{"businessEntity": "", "duty": "一、解除原告中国邮政储蓄银行股份有限公司金乡县支行与被告葛红星于2014年11月17日签订的《小额贷款借款合同》;二、被告葛红星、毕素霞于本判决生效之日起十日内偿还原告中国邮政储蓄银行有限责任公司金乡县支行借款本金60000元、利息819.1元及自2015年8月18日起以本金60000元为基数至本判决确定的履行期限届满之日止按合同约定的利率支付贷款利息；　　三、被告陈卫国、周兰英、申凤芝对上述债务承担连带责任。如果被告未按本判决上述指定的期间履行给付金钱义务，应当依照《 HYPERLINK "javascript:SLC(98761,0)" 中华人民共和国民事诉讼法》第 HYPERLINK "javascript:SLC(98761,229)" 二百五十三条之规定，加倍支付迟延履行期间的债务利息。案件受理费1320元，减半收取660元，由被告葛红星、毕素霞、陈卫国、周兰英、申凤芝负担。", "cambrian_appid": "0", "StdStg": 6899, "loc": "http://shixin.court.gov.cn/detail?id=113489764", "cardNum": "37082819800****2324", "courtName": "金乡县人民法院", "areaName": "山东", "performance": "全部未履行", "_update_time": "1520302507", "_select_time": 1520301956, "gistId": "（2015）金商初字第654号民事判决书", "performedPart": "", "sexy": "女", "StdStl": 8, "lastmod": "2018-03-05T23:07:30", "iname": "周兰英", "SiteId": 2004188, "gistUnit": "金乡县人民法院", "priority": "1.0", "regDate": "20160118", "unperformPart": "", "type": "失信被执行人名单", "_version": 18328, "sitelink": "http://shixin.court.gov.cn/", "focusNumber": "0", "age": "36", "caseCode": "(2016)鲁0828执239号", "changefreq": "always", "disruptTypeName": "其他有履行能力而拒不履行生效法律文书确定义务", "publishDate": "2016年08月09日", "publishDateStamp": "1470672000", "partyTypeName": "0"}'
# pattern = r'"javascript:SLC\(.*?\)"'
# a = re.findall(pattern, origin)
# print(a)
# b = re.sub(pattern, "<test>", origin)
# print(b)
# new = json.loads(b)


origin = '{"businessEntity": "", "duty": ""一、被告浙江三象新材料科技有限公司于本判决生效之日起7日内，归还原告上海浦东发展银行股份有限公司金华分行借款本金500万元、支付利息5 746 611.84元（已计至2015年5月10日，此后利息另行按约定计至判决确定履行日止）。二、被告浙江三象新材料科技有限公司于本判决生效之日起7日内，给付原告上海浦东发展银行股份有限公司金华分行信用证垫款26 776 493.21元和按日万分之五计付的利息（其中本金14 875 963.78元自2013年12月13日起算，余款利息自2014年1月28日起算）。三、原告上海浦东发展银行股份有限公司金华分行对被告浙江三象新材料科技有限公司抵押担保的坐落于兰溪市兰江街道上黄村房屋（房产证号为兰房权证兰字第010045896号和第010045897号）折价、变卖或拍卖款享有优先受偿权。四、被告浙江加兰节能科技股份有限公司在2000万元的额度内对第一项、第二项款项承担连带责任。五、被告金华市圣尔达医疗器械有限公司、徐云夫、董伟琴、董建国、蔡忠丽均对第一项、第二项款项承担连带责任。如果被告未按本判决指定的期限履行给付金钱义务，应当依照《中华人民共和国民事诉讼法》第二百五十三条之规定，加倍支付迟延履行期间的债务利息。本案受理费204 416元（原告已预交），由七被告负担（各被告在履行时加付此款给原告）。"", "cambrian_appid": "0", "StdStg": 6899, "loc": "http://shixin.court.gov.cn/detail?id=111332775", "cardNum": "33062119620****4234", "courtName": "婺城法院", "areaName": "浙江", "performance": "全部未履行", "_update_time": "1520302174", "_select_time": 1520301956, "gistId": "(2015)金婺商初字第01851号", "performedPart": "", "sexy": "男", "StdStl": 8, "lastmod": "2018-03-05T22:19:06", "iname": "徐云夫", "SiteId": 2004188, "gistUnit": "金华婺城法院", "priority": "1.0", "regDate": "20151030", "unperformPart": "", "type": "失信被执行人名单", "_version": 18328, "sitelink": "http://shixin.court.gov.cn/", "focusNumber": "0", "age": "54", "caseCode": "(2015)金婺执民字第04665号", "changefreq": "always", "disruptTypeName": "其他有履行能力而拒不履行生效法律文书确定义务", "publishDate": "2016年03月09日", "publishDateStamp": "1457452800", "partyTypeName": "0"}'

pattern = r'"duty":\s("").+?("")'
# a = re.findall(pattern, origin)
# print(a)
new_data = re.sub(pattern, '>>>>>>>', origin)
print(new_data)
# new = json.loads(new_data)
# print(new)
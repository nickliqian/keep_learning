import json
import csv


path = "D://A//a鑫城国际润福宛.json"
with open(path, "r", encoding="utf-8") as f:
    d = json.load(f)

lis = d["data"]["list"]


with open('./result.csv', 'w', newline='') as csvfile:
    title = "house_code,title,frame_bedroom_num,frame_hall_num,frame_orientation,rent_area,price_total,tags,list_picture_url,ctime,decoration,appid,rent_type,community_id,community_name,subway_station,house_picture,house_picture_db,house_price_history,is_price_decrease,house_picture_count,is_ziroom,is_new_house_source".split(",")
    spamwriter = csv.writer(csvfile, delimiter=',')
    spamwriter.writerow(title)

    for item in lis:
        content = []
        for k in item:
            content.append(item[k])
        spamwriter.writerow(content)

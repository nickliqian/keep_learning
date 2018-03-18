import re

a = """
<dd class="job_bt">
        <h3 class="description">职位描述：</h3>
        <div>
        <p>岗位职责:</p>
<p>1、负责抓取各网站页面，分析链接，转码等；</p>
<p>2、负责一些优质号源发现，优质垂直站点发现等；</p>
<p>3、负责一些数据挖掘相关算法，做数据分析和处理。<br> <br></p>
<p>任职要求：</p>
<p>1、有扎实的数据结构和算法功底；</p>
<p>2、工作认真细致踏实，有较强的学习能力，熟悉常用爬虫工具；</p>
<p>3、熟悉linux开发环境，熟悉python等；</p>
<p>4、理解http，熟悉html, DOM, xpath, scrapy优先；</p>
<p>5、有爬虫，信息抽取，文本分类相关经验者优先；</p>
<p>6、了解Hadoop、Spark等大数据框架和流处理技术者优先。</p>
        </div>
    </dd>
"""

pattern = r'<dd\sclass="job_bt">(.*?)</dd>'
desc = re.findall(pattern, a, re.S)
if desc:
    data = desc[0].replace("\n", "")
    re_data = re.sub(r"<p>|</p>|<div>|</div>|<h3.*?>|</h3>|\s|<br>", "", data)

    print(re_data)
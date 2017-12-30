from selenium import webdriver
import time


driver = webdriver.PhantomJS(executable_path=r"D:\A\phantomjs-2.1.1-windows\bin\phantomjs.exe",)

# 利用DesiredCapabilities(代理设置)参数值，重新打开一个sessionId，我看意思就相当于浏览器清空缓存后，加上代理重新访问一次url
proxy=webdriver.Proxy()
proxy.proxy_type=ProxyType.MANUAL
proxy.http_proxy='1.9.171.51:800'
# 将代理设置添加到webdriver.DesiredCapabilities.PHANTOMJS中
proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
browser.start_session(webdriver.DesiredCapabilities.PHANTOMJS)
browser.get('http://1212.ip138.com/ic.asp')



url = "http://www.httpbin.org/ip"
driver.get(url)
time.sleep(3)
html = driver.page_source
print(html)
driver.quit()
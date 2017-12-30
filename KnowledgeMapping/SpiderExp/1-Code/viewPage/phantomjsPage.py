from selenium import webdriver
import time

service_args = [
    '--proxy=219.138.58.245:3128',
    '--proxy-type=http',
    ]

driver = webdriver.PhantomJS(
    executable_path=r"D:\A\phantomjs-2.1.1-windows\bin\phantomjs.exe",
    service_args=service_args
)
url = "http://www.httpbin.org/ip"
driver.get(url)
time.sleep(3)
html = driver.page_source
print(html)
driver.quit()
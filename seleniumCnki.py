#!/usr/bin/env python
# coding: utf-8
from selenium import webdriver
# from pyquery import PyQuery
from selenium.webdriver.common.action_chains import ActionChains    #模拟鼠标动作的类
import time

def per():
    for j in range(2,22):
        currXpath = '//*[@id="ctl00"]/table/tbody/tr[2]/td/table/tbody/tr['+str(j)+']'
        headerinfo = []
        for i in range(1, 7):
            headerinfo.append(browser.find_element_by_xpath(currXpath+ '/td['+str(i)+']').text)
        print(headerinfo)

        #进入论文详情页
        ActionChains(browser).double_click(browser.find_element_by_xpath(currXpath+ '/td[2]/a')).perform()

        #获取窗口句柄，切换窗口
        mainWindow = browser.current_window_handle
        windows =browser.window_handles

        #切换窗口
        browser.switch_to.window(windows[-1])

        #//*[@id="ChDivSummary"]
        #爬取摘要
        try:
            print(browser.find_element_by_xpath('//*[@id="ChDivSummary"]').text)
        except:
            pass

        #关键词//*[@id="mainArea"]/div[3]/div[3]/div[1]/p[2]
        #//*[@id="mainArea"]/div[3]/div[4]/div[1]/p[2]

        try:
           print(browser.find_element_by_xpath('//*[@class="wxBaseinfo"]/p[2]').text)
        except:
           pass
        #pdf下载链接
        try:
            print(browser.find_element_by_xpath('//*[@id="pdfDown"]').get_attribute("href"))
        except:
            pass
        browser.switch_to.window(mainWindow)
        browser.switch_to.frame('iframeResult')

# browser.current_url

if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    # 设置chrome不加载图片，提高速度
    options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})

    browser = webdriver.Chrome(options=options)
    browser.get('https://www.cnki.net/')
    # browser.get_attribute(key)#获取key属性名对应的属性值`

    # input搜索内容
    key_word = 'python'
    startPage = 1
    endPage = 1
    browser.find_element_by_xpath('//*[@id="txt_SearchText"]').send_keys(key_word)

    # 点击搜索/html/body/div[2]/div[2]/div/div[1]/input[2]
    ActionChains(browser).double_click(
        browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[1]/input[2]')).perform()

    time.sleep(3)
    # 跳转到frame框架中
    browser.switch_to.frame('iframeResult')

    # #将当前网页缓存到本地
    # with open('zw.html','w',encoding='utf-8') as f:
    #     f.write(browser.page_source)
    per()
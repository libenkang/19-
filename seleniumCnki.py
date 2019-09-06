from selenium import webdriver
import time
import pandas
from selenium.webdriver.common.action_chains import ActionChains  # 模拟鼠标动作的类


class spider:
    def __init__(self, keyword, endPage):
        self.keyword = keyword
        # self.startPage = start
        self.endPage = endPage
        self.browser = None
        self.data = []

    def setting(self):
        options = webdriver.ChromeOptions()
        # 设置chrome不加载图片，提高速度
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        # 指定下载目录
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': 'e:\\test'}
        options.add_experimental_option('prefs', prefs)
        #         options.add_argument('--no--sandbox')
        #         options.add_argument('--headless')
        self.browser = webdriver.Chrome(options=options)

        browser = webdriver.Chrome(options=options)

    def getCurrentPage(self, browser):
        for j in range(2, 22):
            currXpath = '//*[@id="ctl00"]/table/tbody/tr[2]/td/table/tbody/tr[' + str(j) + ']'
            info = []
            for i in range(1, 7):
                info.append(browser.find_element_by_xpath(currXpath + '/td[' + str(i) + ']').text)

            # 进入论文详情页
            ActionChains(browser).double_click(browser.find_element_by_xpath(currXpath + '/td[2]/a')).perform()

            # 获取窗口句柄，切换窗口
            mainWindow = browser.current_window_handle
            windows = browser.window_handles
            # 切换至最新打开的窗口
            browser.switch_to.window(windows[-1])

            # 爬取摘要
            try:
                info.append(browser.find_element_by_xpath('//*[@id="ChDivSummary"]').text)
            except:
                info.append('')
                pass

            # 爬取关键词//*[@id="mainArea"]/div[3]/div[3]/div[1]/p[2]
            try:
                info.append(browser.find_element_by_xpath('//*[@class="wxBaseinfo"]/p[2]').text)
            except:
                info.append('')
                pass

            # 爬取下载链接
            try:
                info.append(browser.find_element_by_xpath('//*[@id="pdfDown"]').get_attribute("href"))
            except:
                info.append('')
                pass

            browser.switch_to.window(mainWindow)
            browser.switch_to.frame('iframeResult')
            self.data.append(info)

    def nextPage(self, browser):
        ActionChains(browser).double_click(browser.find_element_by_xpath('//*[@id="ctl00"]/table/tbody/tr[3]/td/table/tbody/tr/td/div/a[last()]')).perform()

    def downLoad(self):
        urls = [self.data[i][-1] for i in range(len(self.data)) if self.data[i][-1] != '']
        self.browser.get(urls[i] for i in urls)

    def run(self):
        self.setting()
        browser = self.browser
        browser.get('https://www.cnki.net/')
        browser.find_element_by_xpath('//*[@id="txt_SearchText"]').send_keys(self.keyword)
        ActionChains(browser).double_click(
            browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[1]/input[2]')).perform()
        browser.switch_to.frame('iframeResult')
        for i in range(self.endPage):
            self.getCurrentPage(browser)
            if i != self.endPage - 1:
                self.nextPage()
        return self.data


# 输入关键词，起止页
key_wold = '大数据'
# startPage = 1
endPage = 2
sp = spider(key_wold, endPage)
data = sp.run()
sp.downLoad()
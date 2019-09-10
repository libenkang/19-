from selenium import webdriver
import time
import re
import pandas
from selenium.webdriver.common.action_chains import ActionChains  # 模拟鼠标动作的类
from samilarrate import samilarRate

class spider:
    def __init__(self, keyword, endPage):
        self.keyword = keyword
        # self.startPage = start
        self.endPage = endPage
        self.data = []
        self.savePath = ''

    def setting(self):
        self.savePath = "e:\\test\\" + self.keyword
        options = webdriver.ChromeOptions()

        # 设置chrome不加载图片，提高速度
        # 指定下载目录
        prefs = {"profile.managed_default_content_settings.images": 2, 'profile.default_content_settings.popups': 0,
                 'download.default_directory': self.savePath}
        options.add_experimental_option('prefs', prefs)
        #         options.add_argument('--no--sandbox')
        #         options.add_argument('--headless')
        browser = webdriver.Chrome(options=options)
        return browser

    def getCurrentPage(self, browser):
        for j in range(2, 22):
            currXpath = '//*[@id="ctl00"]/table/tbody/tr[2]/td/table/tbody/tr[' + str(j) + ']'
            info = [browser.find_element_by_xpath(currXpath + '/td[' + str(i) + ']').text for i in range(1, 7)]

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
                info.append(browser.find_element_by_xpath('//*[@id="catalog_KEYWORD"]/..').text)
            except:
                info.append('')
                pass

            # 爬取下载链接
            try:
                info.append(browser.find_element_by_xpath('//*[@id="pdfDown"]').get_attribute("href"))
            except:
                info.append('')
                pass

            browser.close()
            browser.switch_to.window(mainWindow)
            browser.switch_to.frame('iframeResult')
            self.data.append(info)

    def nextPage(self, browser):
        ActionChains(browser).double_click(browser.find_element_by_xpath(
            '//*[@id="ctl00"]/table/tbody/tr[3]/td/table/tbody/tr/td/div/a[last()]')).perform()

    def downLoad(self, browser, urls):
        time.sleep(2)
        [browser.get(urls[i]) for i in range(len(urls)) if urls[i] != None]
        print('files saved in ' + self.savePath)

    def myPage(self, data, sorft=None):
        df = pandas.DataFrame(data)
        pandas.set_option('display.max_columns', None)
        pandas.set_option('display.max_rows', None)
        pandas.set_option('display.max_colwidth', 1000)
        df.columns = ['序号', '题名', '作者', '来源', '发表时间', '数据库', '摘要', '关键词', '下载地址']
        if sorft is not None:
            keyword = list(df[df["序号"] == sorft]["摘要"])
            texts = list(df["摘要"])
            result,rate = samilarRate(df["摘要"],keyword[0])
            df["rate"] = rate
            df.sort_values("rate", ascending=False, inplace=True)
            df.index = [i + 1 for i in range(len(data))]

        html = df.to_html(index=True, justify='center')
        html = html.replace('class="dataframe"', 'class="dataframe" bgcolor=#F1E1FF ')
        row = re.findall('https(.*)</td>', html)
        for i in range(len(row)):
            html = html.replace('https' + row[i], '<a style="display:block" href="https' + row[i] + '">下载</a>')
        with open(self.savePath + "mypage.html", "w", encoding='utf-8') as file:
            file.write(html)
        return self.savePath + "mypage.html"

    def run(self):
        browser = self.setting()
        browser.get('https://www.cnki.net/')
        browser.find_element_by_xpath('//*[@id="txt_SearchText"]').send_keys(self.keyword)
        ActionChains(browser).double_click(
            browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[1]/input[2]')).perform()
        browser.switch_to.frame('iframeResult')
        time.sleep(1)
        for i in range(self.endPage):
            self.getCurrentPage(browser)
            if i != self.endPage - 1:
                self.nextPage(browser)

        browser.get(self.myPage(self.data))

        while(True):
            print("请输入论文序号，退出请按q")
            sorft = input("根据论文__内容的相似度进行排序： ")
            if sorft is 'q':
                break
            else:
                browser.get(self.myPage(self.data, sorft))

        chioce = input('Downloads all? Y/N: ')
        if chioce == 'Y':
            urls = [self.data[i][-1] for i in range(len(self.data)) if self.data[i][-1] != '']
            self.downLoad(browser, urls)
        browser.quit()


if __name__ == '__main__':
    # 输入关键词，起止页
    key_wold = input('请输入关键词：')
    # startPage = 1
    endPage = int(input('请输入页数：'))
    sp = spider(key_wold, endPage)
    sp.run()
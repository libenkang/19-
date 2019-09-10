## 知网论文爬取


### 使用说明
Python3 + selenium + Chrome浏览器 + chromedrive
确保将chromedrive.exe文件放置python3安装目录下

依赖的库有jieba,gensim,pandas，selenium(如未安装，可在命令行下 pip install xxx)

默认下载目录为E:/test/ 可在spider类的setting函数中修改

### 项目内容
使用selenium打开chrome浏览器访问知网主页（https://www.cnki.net） ,在输入框中自动输入关键词，点击搜索，
浏览器打开某一主题的论文库页面，程序爬取到第一条论文序号、标题、作者...，模拟点击标题，进入论文详情页，
程序定位到摘要及pdf下载链接，并爬取其内容，浏览器反回至论文库页面，继续爬取下一条论文信息...

每条论文信息存至一位数组，所有论文存入数组构成二维数组，使用pandas中dataframe方法将二维数组转成表格，
调用datafram中to_html方法生成本地html文件，并在chrome浏览器中打开展示数据。

程序提示“根据论文__内容的相似度进行排序：”，输入论文序号，程序将根据论文摘要匹配相似度并根据相似度对论文重新排序

程序提示“Downloads all? Y/N：”，输入Y，批量下载论文，N，程序运行完毕，关闭chrome浏览器

### 已知问题
selenium模拟人的动作操作浏览器，每次打开链接会在浏览器中打开新窗口，换言之，爬取n篇论文需要打开n个窗口......效率略低，setting函数中
设置浏览器不加载图片，效率仍然低。

setting中设置 headless, 可以不打开浏览器，浏览器后台运行，但是不能执行下载功能

### 作者邮箱
1577305478@qq.com

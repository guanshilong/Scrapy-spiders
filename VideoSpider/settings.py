# -*- coding: utf-8 -*-

# Scrapy settings for VideoSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

# Scrapy项目的名字,这将用来构造默认 User-Agent,同时也用来log使用startproject 命令创建项目时其也被自动赋值
BOT_NAME = 'VideoSpider'
DOWNLOAD_FAIL_ON_DATALOSS = False
# Scrapy搜索spider的模块列表
SPIDER_MODULES = ['VideoSpider.spiders']

# 使用 genspider 命令创建新spider的模块
NEWSPIDER_MODULE = 'VideoSpider.spiders'

# 爬取的默认User-Agent，除非被覆盖
# USER_AGENT = 'VideoSpider (+http://www.yourdomain.com)'

# 如果启用,Scrapy将会采用 robots.txt策略
ROBOTSTXT_OBEY = False

# 禁用Cookie（默认情况下启用）
COOKIES_ENABLED = False


# -----------------------concurrent--------------------------------------------------------------------------
# Scrapy downloader 并发请求(concurrent requests)的最大值,默认: 16, 说白了就是请求页面的并发, 并不是程序的并发
CONCURRENT_REQUESTS = 64
# 在项处理器（也称为项目管道）中并行处理的并发项目的最大数(每个响应),默认100
# CONCURRENT_ITEMS = 100

# 为同一网站的请求配置延迟（默认值：0）
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay

# 下载器在下载同一个网站下一个页面前需要等待的时间,该选项可以用来限制爬取速度
DOWNLOAD_DELAY = 1

# 下载延迟设置只有一个有效###
# 对单个网站进行并发请求的最大值
CONCURRENT_REQUESTS_PER_DOMAIN = 32
# 对单个IP进行并发请求的最大值。如果非0,则忽略 CONCURRENT_REQUESTS_PER_DOMAIN 设定,使用该设定。
# 也就是说,并发限制将针对IP,而不是网站。该设定也影响 DOWNLOAD_DELAY: 如果 CONCURRENT_REQUESTS_PER_IP 非0,
# 下载延迟应用在IP而不是网站上。
# CONCURRENT_REQUESTS_PER_IP = 16
# ------------------------------------------------------------------------------------------------------------


# -------------------------------Telnet控制台------------------------------------------------------------------
# 禁用Telnet控制台（默认启用）
# TELNETCONSOLE_ENABLED = False

# Telnet终端使用的端口范围。默认: [6023, 6073],如果设置为 None 或 0 ， 则使用动态分配的端口
# TELNETCONSOLE_PORT

# Telnet终端监听的接口(interface)。默认: '127.0.0.1'
# TELNETCONSOLE_HOST
# ------------------------------------------------------------------------------------------------------------


# 覆盖默认请求标头
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }


# 蜘蛛中间件 用来过滤出 URL 长度比 URLLENGTH_LIMIT 的 request | 过滤出所有失败(错误)的 HTTP response
SPIDER_MIDDLEWARES = {
    'scrapy_deltafetch.DeltaFetch': 100,
}
# 开启增量爬取
DELTAFETCH_ENABLED = True

# 下载中间件 例如增加http header信息，增加proxy信息 | 以对响应进行处理
# 如果您想要关闭user-agent中间间
DOWNLOADER_MIDDLEWARES = {
    'VideoSpider.middlewares.VideospiderDownloaderMiddleware': 543,
    # 禁用默认的获取useragent方法
    'scrapy.downloadermiddleware.useragent.UserAgentMiddleware': None,
    # 开启scrapy_fake_useragent插件
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
    # 'VideoSpider.middlewares.MyUserAgentMiddleware': 400,
    'VideoSpider.middlewares.MyProxyMiddleware': 401,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 500,
}

# 启用或禁用扩展程序
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
# 提供一个telnet控制台,该扩展默认为启用。用于进入当前执行的Scrapy进程的Python解析器
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }


# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'VideoSpider.pipelines.VideospiderPipeline': 300,
   # 'VideoSpider.pipelines.FilmPipeline': 200,
}

# 下载器超时时间(单位: 秒),默认: 180
DOWNLOAD_TIMEOUT = 30


# --------------------AUTOTHROTTLE------------------------------------
# 启用和配置AutoThrottle扩展（默认情况下禁用）
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True

# 开始下载时限速并延迟时间
AUTOTHROTTLE_START_DELAY = 0

# 高并发请求时最大延迟时间
# AUTOTHROTTLE_MAX_DELAY = 60

# Scrapy请求的平均数量应该并行发送每个远程服务器
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
#
# 启用显示所收到的每个响应的调节统计信息
# AUTOTHROTTLE_DEBUG = False
# ----------------------------------------------------------------------

# 启用和配置HTTP缓存（默认情况下禁用）
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


# -------------------------重试机制---------------------------------------
# #以下两项和中间件RetryMiddleware配合来控制同一IP重试次数
# 是否开启retry
RETRY_ENABLED = True
# 重试次数
RETRY_TIMES = 3
# 重试code
# RETRY_HTTP_CODECS
# -----------------------------------------------------------------------


# ----------------------------log----------------------------------------
# 是否启用logging, 默认: True
# LOG_ENABLED

# log的编码,默认为UTF-8
# LOG_ENCODING

# logging输出的文件名,默认为None。如果为None，则使用标准错误输出(standard error)
# LOG_FILE = './spider.log'

# 格式化:https://docs.python.org/2/library/logging.html#logrecord-attributes
# LOG_FORMAT

# log的最低级别。可选的级别有: CRITICAL、 ERROR、WARNING、INFO、DEBUG,默认为DEBUG
LOG_LEVEL = 'INFO'


# 默认为False,如果为 True ，进程所有的标准输出(及错误)将会被重定向到log中。例如,执行 print 'hello'，其将会在Scrapy log中显示
# LOG_STDOUT
# ----------------------------------------------------------------------

# -------------------------other----------------------------------------
# 开启重定向
# REDIRECT_ENABLED = False
#
# HTTPERROR_ALLOWED_CODES = [400]

# 设置单个爬虫暂停、恢复的状态保存,每个爬虫在每个代码中配置
# JOBDIR=filename

# 允许抓取任何网站的最大深度。如果为零，则不施加限制。
# scrapy.spidermiddlewares.depth.DepthMiddleware = 0

# 是否启用DNS内存缓存,默认为True
# DNSCACHE_ENABLED = False

# 允许抓取网址的最大网址长度,默认值：2083
# URLLENGTH_LIMIT
# ----------------------------------------------------------------------


# ------------------------MySQL配置--------------------------------------
MYSQL_HOST = '192.168.157.99'
MYSQL_DBNAME = 'scrapy'         #数据库名字，请修改
MYSQL_USER = 'root'             #数据库账号，请修改
MYSQL_PASSWD = 'root'         #数据库密码，请修改
MYSQL_PORT = 3306               #数据库端口，在dbhelper中使用
# ----------------------------------------------------------------------

ROBOTS_PATH = 'd:/robots.txt'
FILE_PATH = 'd:/'
XML_PATH = 'd:/sitemap.xml'

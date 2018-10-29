
# Organic wine data collection

## Biodynamic vineyards


```python
import parameters
```


```python
from selenium import webdriver
driver = webdriver.Chrome(parameters.chromedriver_location)
```


```python
from utilities.biodynamic_spiders import VineyardSpider
vineyard_spider = VineyardSpider(driver = driver, destination = parameters.vineyard_destination)
```


```python
from datetime import date
vineyard_spider.load_vineyards(link = 'http://www.biodynamicfood.org/', 
                               time = date(year=2018, month=10, day=29))
```

    Loading category "Crops" successful.
    Loading subcategory "Fruit" successful.
    Loading "Grapes For Wine" successful.
    Loading more vineyards.
    Loaded all vineyards.



```python
vineyard_links = vineyard_spider.get_vineyard_links()
print(vineyard_links)
```

    ['http://www.biodynamicfood.org/biodynamic/adamvs', 'http://www.biodynamicfood.org/biodynamic/ambyth-estate', 'http://www.biodynamicfood.org/biodynamic/ampelos-vineyards', 'http://www.biodynamicfood.org/biodynamic/Analemma-Wines', 'http://www.biodynamicfood.org/biodynamic/Annadel-Gap-Vineyard', 'http://www.biodynamicfood.org/biodynamic/araujo-estate', 'http://www.biodynamicfood.org/biodynamic/Bearg-Ranch-Vineyard', 'http://www.biodynamicfood.org/biodynamic/beaver-creek-vineyards', 'http://www.biodynamicfood.org/biodynamic/beckmen-purisima-vineyards', 'http://www.biodynamicfood.org/biodynamic/benziger-family-winery', 'http://www.biodynamicfood.org/biodynamic/bonterra-vineyards', 'http://www.biodynamicfood.org/biodynamic/brick-house-vineyards', 'http://www.biodynamicfood.org/biodynamic/brooks-vineyard', 'http://www.biodynamicfood.org/biodynamic/cooper-mountain-vineyards', 'http://www.biodynamicfood.org/biodynamic/cowhorn-vineyard-garden', 'http://www.biodynamicfood.org/biodynamic/dark-horse-vineyard', 'http://www.biodynamicfood.org/biodynamic/davero-sonoma-inc', 'http://www.biodynamicfood.org/biodynamic/deloach-vineyards', 'http://www.biodynamicfood.org/biodynamic/filigreen-farm', 'http://www.biodynamicfood.org/biodynamic/frey-vineyards-ltd', 'http://www.biodynamicfood.org/biodynamic/golden-vineyards', 'http://www.biodynamicfood.org/biodynamic/grimm-estates-llc', 'http://www.biodynamicfood.org/biodynamic/harms-vineyards-lavender-fields', 'http://www.biodynamicfood.org/biodynamic/hawk-horse-vineyards', 'http://www.biodynamicfood.org/biodynamic/hdd-llc', 'http://www.biodynamicfood.org/biodynamic/hedges-family-estate', 'http://www.biodynamicfood.org/biodynamic/jack-rabbit-hill-llc', 'http://www.biodynamicfood.org/biodynamic/jacob-hart-vineyard', 'http://www.biodynamicfood.org/biodynamic/johan-vineyards', 'http://www.biodynamicfood.org/biodynamic/keeler-estate-vineyard', 'http://www.biodynamicfood.org/biodynamic/maboroshi-vineyard', 'http://www.biodynamicfood.org/biodynamic/maha-estate', 'http://www.biodynamicfood.org/biodynamic/martian-ranch-vineyard', 'http://www.biodynamicfood.org/biodynamic/mattern-vineyards', 'http://www.biodynamicfood.org/biodynamic/Mineral-Springs-Ranch', 'http://www.biodynamicfood.org/biodynamic/montinore-estate', 'http://www.biodynamicfood.org/biodynamic/narrow-gate-vineyards', 'http://www.biodynamicfood.org/biodynamic/pearl-vineyard', 'http://www.biodynamicfood.org/biodynamic/pine-hawk-vineyards', 'http://www.biodynamicfood.org/biodynamic/porter-creek-vineyards', 'http://www.biodynamicfood.org/biodynamic/porter-bass-vineyards', 'http://www.biodynamicfood.org/biodynamic/preston-vineyards', 'http://www.biodynamicfood.org/biodynamic/puma-springs-vineyards', 'http://www.biodynamicfood.org/biodynamic/raymond-vineyard-and-cellar', 'http://www.biodynamicfood.org/biodynamic/Roederer-Estate-Domaine-Anderson', 'http://www.biodynamicfood.org/biodynamic/rose-ranch', 'http://www.biodynamicfood.org/biodynamic/Sea-Smoke-Cellars', 'http://www.biodynamicfood.org/biodynamic/sims-vineyard', 'http://www.biodynamicfood.org/biodynamic/sawyer-lindquist-vineyard', 'http://www.biodynamicfood.org/biodynamic/sun-hawk-farms', 'http://www.biodynamicfood.org/biodynamic/Tablas-Creek-Vineyard', 'http://www.biodynamicfood.org/biodynamic/Upper-Five-Vineyard', 'http://www.biodynamicfood.org/biodynamic/wilridge-vineyard']



```python
vineyard_spider.prepare_vineyard_parsing(links = vineyard_links)
```

    2018-10-29 16:48:31 [scrapy.utils.log] INFO: Scrapy 1.5.1 started (bot: scrapybot)
    2018-10-29 16:48:31 [scrapy.utils.log] INFO: Versions: lxml 4.2.5.0, libxml2 2.9.8, cssselect 1.0.3, parsel 1.5.1, w3lib 1.19.0, Twisted 18.9.0, Python 3.6.6 (default, Sep 12 2018, 18:26:19) - [GCC 8.0.1 20180414 (experimental) [trunk revision 259383]], pyOpenSSL 18.0.0 (OpenSSL 1.1.0i  14 Aug 2018), cryptography 2.3.1, Platform Linux-4.15.0-38-generic-x86_64-with-Ubuntu-18.04-bionic
    2018-10-29 16:48:31 [scrapy.crawler] INFO: Overridden settings: {'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'}
    2018-10-29 16:48:31 [scrapy.middleware] INFO: Enabled extensions:
    ['scrapy.extensions.corestats.CoreStats',
     'scrapy.extensions.telnet.TelnetConsole',
     'scrapy.extensions.memusage.MemoryUsage',
     'scrapy.extensions.logstats.LogStats']
    2018-10-29 16:48:31 [scrapy.middleware] INFO: Enabled downloader middlewares:
    ['scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware',
     'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware',
     'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware',
     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware',
     'scrapy.downloadermiddlewares.retry.RetryMiddleware',
     'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware',
     'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware',
     'scrapy.downloadermiddlewares.redirect.RedirectMiddleware',
     'scrapy.downloadermiddlewares.cookies.CookiesMiddleware',
     'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware',
     'scrapy.downloadermiddlewares.stats.DownloaderStats']
    2018-10-29 16:48:31 [scrapy.middleware] INFO: Enabled spider middlewares:
    ['scrapy.spidermiddlewares.httperror.HttpErrorMiddleware',
     'scrapy.spidermiddlewares.offsite.OffsiteMiddleware',
     'scrapy.spidermiddlewares.referer.RefererMiddleware',
     'scrapy.spidermiddlewares.urllength.UrlLengthMiddleware',
     'scrapy.spidermiddlewares.depth.DepthMiddleware']
    2018-10-29 16:48:31 [scrapy.middleware] INFO: Enabled item pipelines:
    []
    2018-10-29 16:48:31 [scrapy.core.engine] INFO: Spider opened
    2018-10-29 16:48:31 [scrapy.extensions.logstats] INFO: Crawled 0 pages (at 0 pages/min), scraped 0 items (at 0 items/min)
    2018-10-29 16:48:31 [scrapy.extensions.telnet] DEBUG: Telnet console listening on 127.0.0.1:6023



```python
vineyard_spider.parse_organizations()
```

    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/Analemma-Wines> (referer: None)
    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/ampelos-vineyards> (referer: None)
    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/adamvs> (referer: None)
    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/Bearg-Ranch-Vineyard> (referer: None)
    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/araujo-estate> (referer: None)
    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/beaver-creek-vineyards> (referer: None)
    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/Annadel-Gap-Vineyard> (referer: None)
    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/ambyth-estate> (referer: None)
    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/beckmen-purisima-vineyards> (referer: None)
    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/benziger-family-winery> (referer: None)
    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/cooper-mountain-vineyards> (referer: None)
    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/cowhorn-vineyard-garden> (referer: None)
    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/bonterra-vineyards> (referer: None)
    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/brick-house-vineyards> (referer: None)
    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/dark-horse-vineyard> (referer: None)
    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/brooks-vineyard> (referer: None)
    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/davero-sonoma-inc> (referer: None)
    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/deloach-vineyards> (referer: None)
    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/filigreen-farm> (referer: None)
    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/frey-vineyards-ltd> (referer: None)
    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/golden-vineyards> (referer: None)
    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/grimm-estates-llc> (referer: None)
    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/harms-vineyards-lavender-fields> (referer: None)


    Acreage not specified for one organization.
    Acreage not specified for one organization.
    Acreage not specified for one organization.
    Acreage not specified for one organization.
    Acreage not specified for one organization.
    Acreage not specified for one organization.
    Acreage not specified for one organization.


    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/hawk-horse-vineyards> (referer: None)
    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/hdd-llc> (referer: None)
    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/hedges-family-estate> (referer: None)
    2018-10-29 16:48:33 [scrapy.core.scraper] ERROR: Spider error processing <GET http://www.biodynamicfood.org/biodynamic/grimm-estates-llc> (referer: None)
    Traceback (most recent call last):
      File "/home/julian/PycharmProjects/organic_wine/venv/lib/python3.6/site-packages/twisted/internet/defer.py", line 654, in _runCallbacks
        current.result = callback(current.result, *args, **kw)
      File "/home/julian/PycharmProjects/organic_wine/utilities/biodynamic_spiders.py", line 124, in parse
        phone = [line for line in contact_info if line.startswith('Phone: ')][0]
    IndexError: list index out of range
    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/keeler-estate-vineyard> (referer: None)
    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/jacob-hart-vineyard> (referer: None)
    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/johan-vineyards> (referer: None)
    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/jack-rabbit-hill-llc> (referer: None)
    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/maboroshi-vineyard> (referer: None)
    2018-10-29 16:48:33 [scrapy.core.scraper] ERROR: Spider error processing <GET http://www.biodynamicfood.org/biodynamic/hdd-llc> (referer: None)
    Traceback (most recent call last):
      File "/home/julian/PycharmProjects/organic_wine/venv/lib/python3.6/site-packages/twisted/internet/defer.py", line 654, in _runCallbacks
        current.result = callback(current.result, *args, **kw)
      File "/home/julian/PycharmProjects/organic_wine/utilities/biodynamic_spiders.py", line 124, in parse
        phone = [line for line in contact_info if line.startswith('Phone: ')][0]
    IndexError: list index out of range
    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/maha-estate> (referer: None)
    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/martian-ranch-vineyard> (referer: None)
    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/mattern-vineyards> (referer: None)


    Acreage not specified for one organization.
    Acreage not specified for one organization.
    Acreage not specified for one organization.
    Acreage not specified for one organization.
    Acreage not specified for one organization.
    Acreage not specified for one organization.


    2018-10-29 16:48:33 [scrapy.core.scraper] ERROR: Spider error processing <GET http://www.biodynamicfood.org/biodynamic/maha-estate> (referer: None)
    Traceback (most recent call last):
      File "/home/julian/PycharmProjects/organic_wine/venv/lib/python3.6/site-packages/twisted/internet/defer.py", line 654, in _runCallbacks
        current.result = callback(current.result, *args, **kw)
      File "/home/julian/PycharmProjects/organic_wine/utilities/biodynamic_spiders.py", line 124, in parse
        phone = [line for line in contact_info if line.startswith('Phone: ')][0]
    IndexError: list index out of range
    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/Mineral-Springs-Ranch> (referer: None)
    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/pearl-vineyard> (referer: None)
    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/montinore-estate> (referer: None)
    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/porter-bass-vineyards> (referer: None)
    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/porter-creek-vineyards> (referer: None)
    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/pine-hawk-vineyards> (referer: None)
    2018-10-29 16:48:33 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/preston-vineyards> (referer: None)
    2018-10-29 16:48:34 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/narrow-gate-vineyards> (referer: None)
    2018-10-29 16:48:34 [scrapy.core.scraper] ERROR: Spider error processing <GET http://www.biodynamicfood.org/biodynamic/Mineral-Springs-Ranch> (referer: None)
    Traceback (most recent call last):
      File "/home/julian/PycharmProjects/organic_wine/venv/lib/python3.6/site-packages/twisted/internet/defer.py", line 654, in _runCallbacks
        current.result = callback(current.result, *args, **kw)
      File "/home/julian/PycharmProjects/organic_wine/utilities/biodynamic_spiders.py", line 124, in parse
        phone = [line for line in contact_info if line.startswith('Phone: ')][0]
    IndexError: list index out of range
    2018-10-29 16:48:34 [scrapy.core.scraper] ERROR: Spider error processing <GET http://www.biodynamicfood.org/biodynamic/pine-hawk-vineyards> (referer: None)
    Traceback (most recent call last):
      File "/home/julian/PycharmProjects/organic_wine/venv/lib/python3.6/site-packages/twisted/internet/defer.py", line 654, in _runCallbacks
        current.result = callback(current.result, *args, **kw)
      File "/home/julian/PycharmProjects/organic_wine/utilities/biodynamic_spiders.py", line 124, in parse
        phone = [line for line in contact_info if line.startswith('Phone: ')][0]
    IndexError: list index out of range
    2018-10-29 16:48:34 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/Roederer-Estate-Domaine-Anderson> (referer: None)
    2018-10-29 16:48:34 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/puma-springs-vineyards> (referer: None)
    2018-10-29 16:48:34 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/rose-ranch> (referer: None)
    2018-10-29 16:48:34 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/Sea-Smoke-Cellars> (referer: None)
    2018-10-29 16:48:34 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/raymond-vineyard-and-cellar> (referer: None)
    2018-10-29 16:48:34 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/sims-vineyard> (referer: None)
    2018-10-29 16:48:34 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/sun-hawk-farms> (referer: None)
    2018-10-29 16:48:34 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/sawyer-lindquist-vineyard> (referer: None)


    Acreage not specified for one organization.
    Acreage not specified for one organization.
    Acreage not specified for one organization.
    Acreage not specified for one organization.
    Acreage not specified for one organization.


    2018-10-29 16:48:34 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/Tablas-Creek-Vineyard> (referer: None)
    2018-10-29 16:48:34 [scrapy.core.scraper] ERROR: Spider error processing <GET http://www.biodynamicfood.org/biodynamic/puma-springs-vineyards> (referer: None)
    Traceback (most recent call last):
      File "/home/julian/PycharmProjects/organic_wine/venv/lib/python3.6/site-packages/twisted/internet/defer.py", line 654, in _runCallbacks
        current.result = callback(current.result, *args, **kw)
      File "/home/julian/PycharmProjects/organic_wine/utilities/biodynamic_spiders.py", line 124, in parse
        phone = [line for line in contact_info if line.startswith('Phone: ')][0]
    IndexError: list index out of range
    2018-10-29 16:48:34 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/wilridge-vineyard> (referer: None)
    2018-10-29 16:48:34 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.biodynamicfood.org/biodynamic/Upper-Five-Vineyard> (referer: None)
    2018-10-29 16:48:34 [scrapy.core.scraper] ERROR: Spider error processing <GET http://www.biodynamicfood.org/biodynamic/Upper-Five-Vineyard> (referer: None)
    Traceback (most recent call last):
      File "/home/julian/PycharmProjects/organic_wine/venv/lib/python3.6/site-packages/twisted/internet/defer.py", line 654, in _runCallbacks
        current.result = callback(current.result, *args, **kw)
      File "/home/julian/PycharmProjects/organic_wine/utilities/biodynamic_spiders.py", line 124, in parse
        phone = [line for line in contact_info if line.startswith('Phone: ')][0]
    IndexError: list index out of range


    Acreage not specified for one organization.
    Acreage not specified for one organization.
    Acreage not specified for one organization.
    Acreage not specified for one organization.
    Acreage not specified for one organization.


    2018-10-29 16:48:34 [scrapy.core.engine] INFO: Closing spider (finished)
    2018-10-29 16:48:34 [scrapy.statscollectors] INFO: Dumping Scrapy stats:
    {'downloader/request_bytes': 15163,
     'downloader/request_count': 53,
     'downloader/request_method_count/GET': 53,
     'downloader/response_bytes': 349527,
     'downloader/response_count': 53,
     'downloader/response_status_count/200': 53,
     'finish_reason': 'finished',
     'finish_time': datetime.datetime(2018, 10, 29, 20, 48, 34, 477625),
     'log_count/DEBUG': 54,
     'log_count/ERROR': 7,
     'log_count/INFO': 7,
     'memusage/max': 83271680,
     'memusage/startup': 83271680,
     'response_received_count': 53,
     'scheduler/dequeued': 53,
     'scheduler/dequeued/memory': 53,
     'scheduler/enqueued': 53,
     'scheduler/enqueued/memory': 53,
     'spider_exceptions/IndexError': 7,
     'start_time': datetime.datetime(2018, 10, 29, 20, 48, 31, 173019)}
    2018-10-29 16:48:34 [scrapy.core.engine] INFO: Spider closed (finished)



```python
vineyard_spider.close_parser()
```


```python

```

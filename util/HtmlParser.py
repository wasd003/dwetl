from entity.SecondMovie import SecondMovie
from entity.Movie import Movie
from Constants import *
from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup

class HtmlParser:
    pvCache = set() # 保存所有pv的productId
    soupList = [] # 所有电影页面的soup
    productIdList = [] # 所有电影页面的product id
    productIdSet = set() # 为了便于快速查询,通常存储所有id

    def __init__(self):
        self.soupList = self.getSoupList()
        cnt = 0
        for soup in self.soupList:
            print('读入页面: ' + str(cnt), flush=True)
            cnt = cnt + 1
            curId = self.getProductId(soup)
            print(curId)
            if curId == '0005019281':
                print('debug')
            self.productIdList.append(curId)
            if soup.find('a', {'class': 'av-retail-m-nav-text-logo'}) is not None:
                self.pvCache.add(curId)
        self.productIdSet = set(self.productIdList)

        # 不允许空值进入缓存
        self.productIdSet.discard(None)
        self.pvCache.discard(None)
    '''
    获取ROOT_DIR下所有的html的soup
    '''
    def getSoupList(self):
        movieList = []
        cnt = 0
        for f in listdir(ROOT_DIR):
            print('打开页面中: ' + str(cnt))
            cnt = cnt + 1
            if isfile(join(ROOT_DIR, f)):
                movieList.append(f)
        # movieList = [f for f in listdir(ROOT_DIR) if isfile(join(ROOT_DIR, f))]
        res = []
        cnt = 0
        for curMovieName in movieList:
            print('创建页面对应的soup中:' + str(cnt))
            cnt = cnt + 1
            url = ROOT_DIR + "\\" + curMovieName
            page = open(url, 'rb')
            res.append(BeautifulSoup(page.read(), 'html.parser'))
        return res

    def isMovie(self, idx):
        # 第一轮筛选，只保留电影或电视剧
        if self.isPrimeVideo(self.productIdList[idx]) is False and \
                self.getRootTagOfOldPage(self.soupList[idx]) != 'Movies & TV':
            return False

        # 第二轮筛选，去除电视剧
        movieName = self.getMovieName(self.soupList[idx])
        if movieName is None:
            return False
        movieName = movieName.lower()
        # 1. 判断标题关键字, 用于旧页面
        for keyword in TV_KEYWORD:
            if movieName.find(keyword) != -1:
                return False
        # 2. 剧集切换按钮判断， 用于PrimeVideo
        btn = self.soupList[idx].find('label', {'for': 'av-droplist-av-atf-season-selector'})
        if btn is not None:
            return False
        return True
    '''
    获得去重前的电影列表
    '''
    def getMovieList(self):
        res = []
        cnt = 0
        for i in range(len(self.soupList)):
            print('获取电影列表: ' + str(cnt))
            cnt = cnt + 1
            if self.isMovie(i):
                productId = self.productIdList[i]
                if productId == '0005019281':
                    print('debug')
                res.append(Movie(productId=self.productIdList[i],
                                 movieName=self.getMovieName(self.soupList[i]),
                                 nxt=self.getNxtList(self.soupList[i]),
                                 isPv=self.isPrimeVideo(self.productIdList[i])))
        return res
    '''
    利用pv缓存快速根据productId判断是否为pv
    '''
    def isPrimeVideo(self, productId):
        return productId in self.pvCache

    '''
    根据url提取product id
    '''
    def retrieveProductId(self, url):
        if url is None:
            return None
        # if not url.startswith('http'):
        #     return None
        idx = url.find('/dp/')
        if idx == -1:
            return None
        i = idx + 4
        res = ''
        while i < len(url) and url[i] != '/':
            res += url[i]
            i = i + 1
        return res

    '''
    获取当前页面product id
    '''
    def getProductId(self, soup):
        findRes = soup.find('link', {'rel': 'canonical'})
        if findRes is None:
            return None
        url = findRes.get('href')
        res = self.retrieveProductId(url)
        return res

    '''
    获取当前页面所指向的页面的二级电影列表
    '''
    def getNxtList(self, soup):
        res = []
        urls = soup.find_all('a', {'class': LINK_CLASS})
        for cur in urls:
            id = self.retrieveProductId(cur.get('href'))
            if id in self.productIdSet:
                res.append(SecondMovie(productId=id, movieName='', isPv=self.isPrimeVideo(id)))
        return res


    def getMovieName(self, soup):
        title = soup.find('h1', {'data-automation-id': 'title'})
        if title is not None:
            return self.getPureStr(title.getText())
        title = soup.find('span', {'id': 'productTitle'})
        if title is not None:
            return self.getPureStr(title.getText())
        return None

    '''
    对于老页面获得它的顶级tag，用以判断是否为电影
    '''
    def getRootTagOfOldPage(self, soup):
        findRes = soup.find('a', {'class': 'a-link-normal a-color-tertiary'})
        if findRes is None:
            return None
        rootTag = self.getPureStr(findRes.getText())
        return rootTag

    '''
    去掉头尾的不可见字符
    '''
    def getPureStr(self, str):
        s = {'\r', '\n', ' ', '\t'}
        i, j, n = 0, len(str) - 1, len(str)
        while i < n and str[i] in s:
            i = i + 1
        while j >= i and str[j] in s:
            j = j - 1
        return str[i:j + 1]


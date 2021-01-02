import os
import shutil
from util.HtmlParser import *
from Constants import *

'''
获取当前页面所指向的页面的二级电影列表
'''
def getNxtIdList(soup):
    res = []
    urls = soup.find_all('a', {'class': LINK_CLASS})
    for cur in urls:
        id = retrieveProductId(cur.get('href'))
        if id is not None:
            res.append(id)
    return res

def retrieveProductId(url):
    if url is None:
        return None
    idx = url.find('/dp/')
    if idx == -1:
        return None
    i = idx + 4
    res = ''
    while i < len(url) and url[i] != '/':
        res += url[i]
        i = i + 1
    return res

if __name__ == '__main__':
    fileList = os.listdir(FROM_PATH)
    for i in range(30):
        page = open(os.path.join(FROM_PATH, fileList[i]), 'rb')
        soup = BeautifulSoup(page.read(), 'html.parser')
        nxtListIdList = getNxtIdList(soup)
        for nxtid in nxtListIdList:
            try:
                fSrc = os.path.join(SRC_PATH, nxtid + '.html')
                fDes = os.path.join(TO_PATH, nxtid + '.html')
                shutil.copy(fSrc, fDes)
                print(fileList[i] + ':' + nxtid)
            except:
                # print('no such file')
                pass
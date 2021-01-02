from Constants import *
from entity.Movie import *
from entity.SecondMovie import *
class TxtParser():
    idToIdx = {}
    movieList = []

    def convertToBool(self, str):
        if str == 'True' or str == 'true':
            return True
        return False

    def getMovieList(self):
        # 1. 从pointId中读入productid，name和isPv
        cnt = 0
        with open(POINT_ID_DIR, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            productId, name, isPv = '', '', False
            for line in lines:
                print(cnt)
                cnt = cnt + 1
                if line.startswith('productId'):
                    productId = line[line.find(':') + 1: -1]
                elif line.startswith('name'):
                    name = line[line.find(':') + 1: -1]
                elif line.startswith('isPrime'):
                    isPv = self.convertToBool(line[line.find(':') + 1: -1])
                elif line == '\n':
                    self.movieList.append(Movie(productId=productId, movieName=name, isPv=isPv, nxt=[],
                                                releaseDate=None, url=None))
                    self.idToIdx[productId] = len(self.movieList) - 1
        # 2. 从release中读入releaseDate和url
        cnt = 0
        with open(RELEASE_DIR, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            productId, url, releaseDate = '', '', ''
            for line in lines:
                print(cnt)
                cnt = cnt + 1
                if line.startswith('productId'):
                    productId = line[line.find(':') + 1: -1]
                elif line.startswith('url'):
                    url = line[line.find(':') + 1: -1]
                elif line.startswith('time'):
                    releaseDate = line[line.find(':') + 1: -1]
                elif line == '\n':
                    if productId in self.idToIdx:
                        idx = self.idToIdx[productId]
                        self.movieList[idx].url = url
                        self.movieList[idx].releaseDate = releaseDate
        # 3. 读入nxt
        cnt = 0
        with open(POINT_ID_DIR, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            productId = ''
            try:
                for line in lines:
                    print(cnt)
                    cnt = cnt + 1
                    if line.startswith('productId'):
                        productId = line[line.find(':') + 1: -1]
                    elif line.startswith('pointIds'):
                        nxts = line[line.find(':') + 1: -1].split('@@@')
                        for i in range(1, len(nxts) - 1):
                            if nxts[i] in self.idToIdx:
                                rhs = self.movieList[self.idToIdx[nxts[i]]]
                                self.movieList[self.idToIdx[productId]].nxt.append(SecondMovie(
                                    productId=rhs.productId, movieName=rhs.movieName, isPv=rhs.isPv
                                ))
            except:
                print('exception')
        return self.movieList
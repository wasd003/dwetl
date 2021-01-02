from entity.Movie import Movie
from entity.SecondMovie import SecondMovie


class Distinct:
    movieList = []
    n = 0
    ufs = []
    idToIdx = {}  # productId映射到ufs下标

    def __init__(self, movieList):
        self.movieList = movieList
        self.n = len(movieList)
        self.ufs = [-1 for i in range(self.n)]
        for i in range(self.n):
            print('初始化去重数据结构: ' + str(i))
            self.idToIdx[movieList[i].productId] = i

    def find(self, i):
        if self.ufs[i] < 0:
            return i
        self.ufs[i] = self.find(self.ufs[i])
        return self.ufs[i]

    '''
    y合并到x上
    '''

    def union(self, x, y):
        x = self.find(x)
        y = self.find(y)
        if x == y:
            return
        self.ufs[x] += self.ufs[y]
        self.ufs[y] = x

    '''
    返回去重后的电影列表
    注意返回的Movie的nxt中的数据类型为Movie，不再是int
    '''

    def distinct(self):
        for i in range(self.n):
            print('并查集union: ' + str(i))
            for nxt in self.movieList[i].nxt:
                if nxt.productId in self.idToIdx:
                    if nxt.isPv:
                        self.union(self.idToIdx[nxt.productId], i)
                    else:
                        self.union(i, self.idToIdx[nxt.productId])
        res = []
        ufsToRes = {}  # ufs下标映射到res下标
        for i in range(self.n):
            print('构造root movie数组: ' + str(i))
            if self.ufs[i] < 0:
                res.append(Movie(productId=self.movieList[i].productId,
                                 movieName=self.movieList[i].movieName,
                                 nxt=[], isPv=self.movieList[i].isPv,
                                 releaseDate=self.movieList[i].releaseDate,
                                 url=self.movieList[i].url))
                ufsToRes[i] = len(res) - 1
        for i in range(self.n):
            print('为root movie填充儿子节点: ' + str(i))
            if self.ufs[i] >= 0:
                res[ufsToRes[self.find(i)]].nxt.append(SecondMovie(
                    productId=self.movieList[i].productId,
                    movieName=self.movieList[i].movieName,
                    isPv=self.movieList[i].isPv))
        return res

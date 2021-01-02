class Movie:
    productId = '',
    movieName = '',
    releaseDate = '',
    url = ''
    nxt = [], # ->SecondMovie
    isPv = False

    def __init__(self, productId, movieName, releaseDate, isPv, url, nxt):
        self.productId = productId
        self.movieName = movieName
        self.releaseDate = releaseDate
        self.isPv = isPv
        self.url = url
        self.nxt = nxt


    def __str__(self):
        res = ''
        res += '{\n'
        res += '\tmovieName: ' + self.movieName + '\n'
        res += '\tproductId: ' + self.productId + '\n'
        res += '\tisPv: ' + str(self.isPv) + '\n'
        res += '\tnxt: {' + '\n'
        for i in self.nxt:
            res += '\t\t' + str(i) + '\n'
        res += '\t}\n'
        res += '}'
        return res
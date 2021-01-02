class SecondMovie:
    productId = '',
    movieName = '',
    isPv = False

    def __init__(self, productId, movieName, isPv):
        self.productId = productId
        self.movieName = movieName
        self.isPv = isPv


    def __str__(self):
        res = '{movieName: ' + self.movieName + ', productId: ' + self.productId + ', isPv: ' + str(self.isPv) + '}'
        return res
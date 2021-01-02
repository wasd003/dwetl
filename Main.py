import sys

from util.HtmlParser import *
from util.Distinct import *
from Constants import *
import jsonpickle
from util.TxtParser import *
if __name__ == '__main__':
    # htmlParser = HtmlParser()
    # movieList = htmlParser.getMovieList()
    # dis = Distinct(movieList)
    # distinctMovieList = dis.distinct()
    # with open(EXPORT_PATH, 'a') as f:
    #     # f.write(json.dumps(distinctMovieList, sort_keys=True, indent=4, separators=(', ', ': ')))
    #     str = jsonpickle.encode(distinctMovieList, unpicklable=False)
    #     # print(str)
    #     f.write(str)

    txtParser = TxtParser()
    movieList = txtParser.getMovieList()
    dis = Distinct(movieList)
    distinctMovieList = dis.distinct()
    with open(EXPORT_PATH, 'a') as f:
        s = jsonpickle.encode(distinctMovieList, unpicklable=False)
        # print(str)
        f.write(s)
    print('去重前:' + str(len(movieList)))
    print('去重后' + str(len(distinctMovieList)))
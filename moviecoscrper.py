import requests


class MovieCo:
    def __init__(self):
        self.url='https://yts.mx/api/v2/list_movies.json?query_term='
    def getdata(self,search):
        url=self.url+search
        req=requests.get(url)
        #data=self.extractinfo(req.json())
        return req.json()['data']['movies']

    def moviedata(self,ID):
        url='https://yts.mx/api/v2/movie_details.json?movie_id='+ID
        req=requests.get(url)
        return req.json()['data']['movie']
'''
    def extractinfo(self,data):
        movies=data['data']['movies']
        alldata=[]
        for i in movies:
            data={'title_english':i['title_english'],'year':i['year'],i['rating'],i['runtime'],i['genres'],i['summary'],i['language'],i['background_image'], i['torrents']}
            alldata.append(data)
        return alldata

'''
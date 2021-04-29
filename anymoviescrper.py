
import requests
from bs4 import BeautifulSoup
from concurrent import futures




class anymoviesdownload:
    def movielisted(self):
        url='https://www.downloads-anymovies.com/movies.html'





    def textreplace(self,text):
        s='full movie online free'.split()
        text=text.lower()
        for i in s:
            if i in text:
                text=text.replace(i,'').strip()
        s2='watch '
        if text[:6] ==s2:
            return text[6:]
        return text

    def finddata(self,res):
        d=[]
        for i in res:
            try:
                img=i.find('div',{'class':'result_image'}).find('img')['src']
            except:
                img=''
            try:
                link=i.find('div',{'class':'result_title'}).find('a')['href']
            except:
                link=''
            try:
                title=i.find('div',{'class':'result_title'}).text
                title=self.textreplace(title)
            except:
                title=''
            d.append({'medium_cover_image':img,'id':link,'title':title,'tran':'غير مترجم'})
        return d
        
    def extractmovies(self,movie):

        d=[]
        movie=movie.replace(' ','+')
        url=f'https://www.downloads-anymovies.com/search.php?zoom_query={movie}'
        req=requests.get(url,timeout=1)
        soup = BeautifulSoup(req.text, 'html.parser')
        results=soup.find('div',{'class':'results'})
        results1=soup.findAll('div',{'class':'result_block'})
        results2=soup.findAll('div',{'class':'result_altblock'})
        total=results1+results2
        with futures.ThreadPoolExecutor(12) as executor:
            task1=executor.submit(self.finddata,total)
        res=task1.result()
        
        return res



    def findlinks(self,link):
        l=[]
        req=requests.get(link)
        soup = BeautifulSoup(req.text, 'html.parser')
        downloadurl=[i['href'] for i in soup.findAll('a',{'target':"_blank"})]
        try:
            text=soup.find('div',{'id':'e11'})
            text=str(text)
            data=text.split('br/')
            date=data[1][1:-1]
            minu=data[2][1:-1]
            rating=data[0][-10:-1]
        except:
            date=''
            minu=''
            rating=''
        try:
            summry=soup.find('div',{'id':'e12'}).text
        except:
            summry=''
        try:
            name=soup.find('div',{'id':'e13'}).text
        except:
            name=''
        try:
            img=soup.find('div',{'id':'e9'}).find('img')['src']
            image='https://www.downloads-anymovies.com'+img[2:]
        except:
            image=''

        if len(downloadurl)>1:
            l=list(set(downloadurl))
            l=[{'url':i,'quality':'HD'} for i in l]
            return {'title_english':name,'rating':rating,'runtime':minu,'year':date,'description_intro':summry,'torrents':l,'medium_cover_image':image,'watching':l}
        
        try:
            l=[{'url':i,'quality':'HD'} for i in downloadurl]
        except:
            l=[{'url':'#','quality':'HD'}]

        return {'title_english':name,'rating':rating,'runtime':minu,'year':date,'description_intro':summry,'torrents':l,'medium_cover_image':image,'watching':l}

def main(search):
    try:
        movielab=anymoviesdownload()
        anymoives=movielab.extractmovies(search)
        return anymoives
    except:
        return []

def main2(url):
    try:
        movielab=anymoviesdownload()
        anymoives=movielab.findlinks(url)
        return anymoives
    except:
        return []

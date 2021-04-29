from flask import Flask, request, jsonify,render_template,redirect, url_for
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS
from anymoviescrper import main,main2
from moviecoscrper import MovieCo
from flask_sqlalchemy import SQLAlchemy
import os
import xxhash
import decimal
import ast

def hashcode(text):
    xcode=xxhash.xxh64(text).intdigest()
    return(decimal.Decimal(xcode))

def stripNonAlphaNum(text):

	import re
	year=re.findall('[(]\d{4}[)]',text)
	if year:
		year=int(year[0][1:-1])
	else:
		year=re.findall('\d{4}',text)
		if year:
			year=int(year[0][1:-1])
		else:
			year=0
	name=''
	if re.findall('[(]\d{4}[)]',text):
		name=' '.join(re.compile('[(]\d{4}[)]',re.UNICODE).split(text)).strip()
	else:
		name=' '.join(re.compile('\d{4}',re.UNICODE).split(text)).strip()
	return name,year

################################################################
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'movie.db')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db=SQLAlchemy(app)
CORS(app)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

def saveinbestmovies(name):
	hashcoded=hashcode(name)
	by_title=BestmovieDB.query.filter_by(hachcoded=str(hashcoded)).first()
	if by_title:
		new=by_title.times+1
		by_title.times=new
		db.session.commit() 
	else:
		new_movie=BestmovieDB(str(hashcoded),1)
		db.session.add(new_movie)
		db.session.commit()
		



class BestmovieDB(db.Model):
	_id=db.Column("id",db.Integer,primary_key=True)
	hachcoded=db.Column(db.String(50))
	times=db.Column(db.Integer)
	def __init__(self,hachcoded,times):
		self.hachcoded=hachcoded
		self.times=times

class MovieDB(db.Model):
	_id=db.Column("id",db.Integer,primary_key=True)
	title=db.Column(db.String(50))
	hachcoded=db.Column(db.String(50))
	english_title=db.Column(db.String(50))
	arabic_title=db.Column(db.String(50))
	alies=db.Column(db.String(50))
	year=db.Column(db.Integer)
	img=db.Column(db.String(100))
	link=db.Column(db.String(100))
	date=db.Column(db.String(20))
	rating=db.Column(db.String(10))
	runtime=db.Column(db.String(10))
	summry=db.Column(db.String(500))
	downloadlinks=db.Column(db.String(200))
	watchinglinks=db.Column(db.String(200))
	def __init__(self,title,hachcoded,english_title,arabic_title,alies,year,img,link,date,rating,runtime,summry,downloadlinks,watchinglinks):
		self.title=title
		self.hachcoded=hachcoded
		self.english_title=english_title
		self.arabic_title=arabic_title
		self.alies=alies
		self.year=year
		self.img=img
		self.link=link
		self.date=date
		self.rating=rating
		self.runtime=runtime
		self.summry=summry
		self.downloadlinks=downloadlinks
		self.watchinglinks=watchinglinks


class backupDB(db.Model):
	_id=db.Column("id",db.Integer,primary_key=True)
	title=db.Column(db.String(50))
	hachcoded=db.Column(db.String(50))
	english_title=db.Column(db.String(50))
	arabic_title=db.Column(db.String(50))
	alies=db.Column(db.String(50))
	year=db.Column(db.Integer)
	img=db.Column(db.String(100))
	link=db.Column(db.String(100))
	date=db.Column(db.String(20))
	rating=db.Column(db.String(10))
	runtime=db.Column(db.String(10))
	summry=db.Column(db.String(500))
	downloadlinks=db.Column(db.String(200))
	watchinglinks=db.Column(db.String(200))
	def __init__(self,title,hachcoded,english_title,arabic_title,alies,year,img,link,date,rating,runtime,summry,downloadlinks,watchinglinks):
		self.title=title
		self.hachcoded=hachcoded
		self.english_title=english_title
		self.arabic_title=arabic_title
		self.alies=alies
		self.year=year
		self.img=img
		self.link=link
		self.date=date
		self.rating=rating
		self.runtime=runtime
		self.summry=summry
		self.downloadlinks=downloadlinks
		self.watchinglinks=watchinglinks
def saveinbackup(result,source):
	english_title,year=stripNonAlphaNum(result['title_english'])
	new_movie=backupDB(result['title_english'],str(hashcode(result['title_english'])),english_title,english_title,english_title,year, result['medium_cover_image'],str(source), str(result['year']), str(result['rating']), str(result['runtime']), str(result['description_intro']), str(result['torrents']),str(result['torrents']))
	db.session.add(new_movie)
	db.session.commit()

def get_from_backup(movie_id,x):
	result={}
	if x==1:
		result['id']=movie_id.link
		result['tran']='غير مترجم'
	else:
		result['id']=movie_id._id
		result['tran']='مترجم'

	
	result['title_english']=movie_id.title
	result['medium_cover_image']=movie_id.img
	
	
	return result
def compatableresult(movie_id):
	result={}
	result['title_english']=movie_id.english_title
	result['medium_cover_image']=movie_id.img
	result['year']=movie_id.year
	result['rating']=movie_id.rating
	result['runtime']=movie_id.runtime
	result['tran']='مترجم'
	result['description_intro']=movie_id.summry
	downloadlinks=ast.literal_eval(movie_id.downloadlinks)
	result['torrents']=[{'url':i,'quality':'HD'} for i in downloadlinks]

	watching=ast.literal_eval(movie_id.watchinglinks)
	result['watching']=[{'url':i,'quality':'HD'} for i in watching if 'https://mycima.wine/' not in i]

	return result	


def semantic(Query):
	result=[]
	by_title=MovieDB.query.filter_by(english_title=Query).first()
	if by_title:
		if result:
			if by_title._id in [i['id'] for i in result]:
				pass
			else:
				result.append({'id':by_title._id,'title':by_title.english_title,'medium_cover_image':by_title.img,'tran':'مترجم'})
		else:
			result.append({'id':by_title._id,'title':by_title.english_title,'medium_cover_image':by_title.img,'tran':'مترجم'})
	
	in_title=MovieDB.query.filter(MovieDB.english_title.like('%'+Query+'%')).all()
	if in_title:
		if result:
			for found_movie in in_title:
				if found_movie._id in [i['id'] for i in result]:
					pass
				else:
					result.append({'id':found_movie._id,'title':found_movie.english_title,'medium_cover_image':found_movie.img,'tran':'مترجم'})		
		else:
			for found_movie in in_title:
				result.append({'id':found_movie._id,'title':found_movie.english_title,'medium_cover_image':found_movie.img,'tran':'مترجم'})
	
	in_summry=MovieDB.query.filter(MovieDB.summry.like('%'+Query+'%')).all()
	
	if in_summry:
		if result:
			for found_movie in in_summry:
				if found_movie._id in [i['id'] for i in result]:
					pass
				else:
					result.append({'id':found_movie._id,'title':found_movie.english_title,'medium_cover_image':found_movie.img,'tran':'مترجم'})		
		else:
			for found_movie in in_summry:
				result.append({'id':found_movie._id,'title':found_movie.english_title,'medium_cover_image':found_movie.img,'tran':'مترجم'})

	return result

@app.route('/',methods=['GET','POST'])
def home():
	result=''
	if request.method == 'POST':
		result = request.form
		Query=result['newsearch']
		result1=main(Query)
		#movie=MovieCo()
		#result2=movie.getdata(Query)
		#result=result1+result2
		result2=semantic(Query)
		result=result2+result1
		return render_template('index2.html',result=result)

	if request.method == 'GET':
		result=[]
		found=BestmovieDB.query.order_by(BestmovieDB.times.desc()).limit(10).all()
		if found:
			for f in found:
				found_movie=backupDB.query.filter_by(hachcoded=f.hachcoded).first()
				found_movie2=MovieDB.query.filter_by(hachcoded=f.hachcoded).first()
				if found_movie:
					result.append(get_from_backup(found_movie,1))
				if found_movie2:
					result.append(get_from_backup(found_movie2,0))
			return render_template('index.html',result=result)
		else:
			return render_template('index.html',result=[{}])

@app.route('/movie', methods=['GET'])
def profile():
	source = str(request.args['source'])
	if len(source)>5:
		if source[0:4]=='http':
			
			result=main2(source)
			
			############
			if result:
				found_movie=backupDB.query.filter_by(title=result['title_english']).first()
				if found_movie:
					pass
				else:
					try:
						saveinbackup(result,source)
					except:
						pass
			
			########################3
		else:
			movie_id=MovieDB.query.filter_by(_id=source).first()
			result=compatableresult(movie_id)
	else:
		movie_id=MovieDB.query.filter_by(_id=source).first()
		result=compatableresult(movie_id)
	if result:
		saveinbestmovies(result['title_english'])
		return render_template('downloadpage.html',result=result)
	if  result==[]:
		return redirect(url_for('home'))


if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0',debug=False)
	

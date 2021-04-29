from movieapi import db,MovieDB
import pandas as pd
import xxhash
import decimal


#delete all record
'''
num=db.session.query(MovieDB).delete()
db.session.commit()

#for specific value
db.session.query(Model).filter(Model.id==123).delete()
db.session.commit()
'''
def hashcode(text):
    xcode=xxhash.xxh64(text).intdigest()
    return(decimal.Decimal(xcode))

data=pd.read_csv('updeted_mazika2day.csv')
for i in range(len(data)):
    print(i)
    title=data['title'].iloc[i]
    hcode=str(hashcode(data['english_title'].iloc[i]))
    english_title=data['english_title'].iloc[i]
    arabic_title=data['arabic_name'].iloc[i]
    alies=data['alies'].iloc[i]
    year=data['year'].iloc[i]
    link=data['link'].iloc[i]

    
    image=data['image'].iloc[i]
    year=data['qulity'].iloc[i]
    rating=data['cat'].iloc[i]
    runtime=data['runtime'].iloc[i]
    description=data['summry'].iloc[i]
    downloadlinks=data['links'].iloc[i]
    watchinglinks=data['watching'].iloc[i]
    found_movie=MovieDB.query.filter_by(hachcoded=str(hcode)).first()
    if found_movie:
        pass
    else:
        new_movie=MovieDB(title,hcode,english_title,arabic_title,alies,year, image,link, year, rating, runtime, description, downloadlinks,watchinglinks)
        db.session.add(new_movie)
        db.session.commit()
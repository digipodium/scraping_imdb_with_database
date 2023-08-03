from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, Float
from sqlalchemy.orm import mapper, sessionmaker, declarative_base
import pandas as pd
import numpy as np
import pandas as pd
from dputils.scrape import Scraper, Tag, Browser
from dputils.scrape import BeautifulSoup, requests
import time
import streamlit as st
from db import Movie


# config
st.set_page_config(
    page_title='IMDB Scraping using Database',
    page_icon='🎬',
    layout='wide',
    initial_sidebar_state='auto'
)
# title
st.title('IMDB Scraping using Database')

st.sidebar.subheader('About')
st.sidebar.markdown("""
This app scrapes the Popular movies from IMDB and stores them in a database.
The user can view the collected data in the form of dataframe.  
""")

st.sidebar.subheader('Requirements')
st.sidebar.markdown("""
            **Python libraries:** 
            - `dptuils`,
            - `pandas`,
            - `streamlit`,
            - `numpy`,
            - `sqlalchemy`,
            - `requests`,
            - `beautifulsoup4`
""")

st.sidebar.info("https://www.imdb.com/chart/moviemeter is used to scrape the data")

BASE_URL = 'https://www.imdb.com'
IMDB_URL = f'{BASE_URL}/chart/moviemeter'
sc = Scraper(IMDB_URL)
target = Tag('div', cls='sc-9bf20411-3 khhOiz ipc-page-grid__item ipc-page-grid__item--span-2')
items =Tag('li')
img = Tag('img', output='src')
rank = Tag(cls='sc-94da5b1b-0 kaCAvv meter-const-ranking sc-14dd939d-4 iuctsm cli-meter-title-header')
title = Tag(cls='ipc-title ipc-title--base ipc-title--title ipc-title-link-no-icon ipc-title--on-textPrimary sc-14dd939d-7 fjdYTb cli-title')
metadata = Tag(cls='sc-14dd939d-5 cPiUKY cli-title-metadata')
rating = Tag('span', cls='ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating')
engine = create_engine('sqlite:///movies.db')
db = sessionmaker(bind=engine)()
age_rating_list = ['R', 'PG-13','TV-MA','PG','UA']

if st.button('Scrape Live Data'):
    with st.spinner('Scraping...'):
        popular_movies = sc.get_all(
            target,
            items, 
            img=img, 
            rank=rank, 
            title=title, 
            metadata=metadata, 
            rating=rating
        )
        st.success('Scraping Completed')
    
    with st.spinner('Saving to Database...'):
        for idx,record in enumerate(popular_movies):
            metadata= record['metadata']
            year = metadata[:4]
            for rl in age_rating_list:
                if rl in metadata:
                    age_rating = rl
                    break
            else:
                age_rating = 'U'
            title = record['title'].strip().capitalize()
            runtime = metadata.replace(year,'').replace(age_rating,'').strip()
            rating = record['rating']
            if rating and '.' in rating:
                rating = float(rating)
            else:
                try:rating = int(rating)
                except:rating = 0
            print(metadata, '--->',year, age_rating, title, runtime, rating)
            m = Movie(
                title=title,
                img_url=record['img'],
                rating=rating,
                rank=record['rank'],
                year=year,
                age_rating=age_rating,
                runtime=runtime)
            db.add(m)
        db.commit()
        st.success('Saved to Database')

if st.checkbox('View Data'):
    df = pd.read_sql('select * from movies', engine, index_col='id')
    st.dataframe(df,
                 column_config={
                    'img_url': st.column_config.ImageColumn(
                        label="Thumbnail",
                        width="small", 
                        help="The image"),
                    "rating": st.column_config.NumberColumn(
                        label="Rating",
                        format="%.2f ⭐",
                    ),
                       
                 },
                 use_container_width=True)
    

# to run the app
# streamlit run app.py  
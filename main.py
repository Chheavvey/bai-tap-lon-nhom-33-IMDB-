import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import numpy as np

HEADERS ={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", 
        "Accept-Encoding":"gzip, deflate", 
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
        "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

genres = [
    "Adventure",
    "Animation",
    "Biography",
    "Comedy",
    "Crime",
    "Drama",
    "Family",
    "Fantasy",
    "Film-Noir",
    "History",
    "Horror",
    "Music",
    "Musical",
    "Mystery",
    "Romance",
    "Sci-Fi",
    "Sport",
    "Thriller",
    "War",
    "Western"
]

movie_name = []
year = []
time = []
rating = []
metascore = []
votes = []
gross = []
description = []
Director = []
Stars = []

url_dict = {}

for genre in genres:
    url = "https://www.imdb.com/search/title/?genres={}&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=5aab685f-35eb-40f3-95f7-c53f09d542c3&pf_rd_r=N97GEQS6R7J9EV7V770D&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_16"
    formated_url = url.format(genre)
    url_dict[genre] = formated_url
    
print(url_dict)

def get_movies(url, interval):
    resp = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(resp.content, 'html.parser')

    movie_data = soup.findAll('div', attrs= {'class': 'lister-item mode-advanced'})
    try:
        for store in movie_data:
            name = store.h3.a.text
            movie_name.append(name)
    
            year_of_release = store.h3.find('span', class_ = 'lister-item-year text-muted unbold').text.replace('(', '').replace(')', '')
            year.append(year_of_release)
    
            runtime = store.p.find('span', class_ = 'runtime').text.replace(' min', '')
            time.append(runtime)
    
            rate = store.find('div', class_ = 'inline-block ratings-imdb-rating').text.replace('\n', '')
            rating.append(rate)
    
            meta  = store.find('span', class_ = 'metascore').text.replace(' ', '') if store.find('span', class_ = 'metascore') else '^^^^^^'
            metascore.append(meta)
    
            value = store.find_all('span', attrs = {'name': 'nv'})
    
            vote = value[0].text
            votes.append(vote)
    
            grosses = value[1].text if len(value) >1 else '*****'
            gross.append(grosses)
     
            describe = store.find_all('p', class_ = 'text-muted')
            description_ = describe[1].text.replace('\n', '') if len(describe) >1 else '*****'
            description.append(description_)
    
            cast = store.find("p", class_ = '')
            cast = cast.text.replace('\n', '').split('|')
            cast = [x.strip() for x in cast]
            cast = [cast[i].replace(j, "") for i,j in enumerate(["Director:", "Stars:"])]
            Director.append(cast[0])
            Stars.append([x.strip() for x in cast[1].split(",")])
    except IndexError:
        print("Error")

for genre, url in url_dict.items():
    get_movies(url, 1)

movie_DF = pd.DataFrame({'Name of movie': movie_name, 
    'Year of relase': year, 'Watchtime': time, 
    'Movie Rating': rating, 'Metascore': metascore,
    'Vote': votes, 'Gross': gross, 'Description': description, 'Director': Director, 'Stars': Stars
})

movie_DF.to_csv("Film.csv")
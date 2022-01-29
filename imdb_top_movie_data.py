from bs4 import BeautifulSoup
import requests 
import re

# download data from IMDB website 
url = "https://www.imdb.com/chart/top"
response = requests.get(url)
movie_list_html = BeautifulSoup(response.text, 'html.parser')

# scrape for the required data from the HTML file downloaded 
movies = movie_list_html.select('td.titleColumn')
links = [a.attrs.get('href') for a in movie_list_html.select('td.titleColumn a')]
crew = [a.attrs.get('title') for a in movie_list_html.select('td.titleColumn a')]
ratings_and_votes = [a.attrs.get('title') for a in movie_list_html.select('td.ratingColumn.imdbRating strong')]

ratings = []
votes = []

for rating_and_vote_string in ratings_and_votes:
    rating_and_vote = re.sub('[a-zA-Z ]', '', rating_and_vote_string) 
    ratings.append(rating_and_vote[:3])
    votes.append(rating_and_vote[3:]) 

top_movies_data = []

for index in range(0, len(movies)):
    movie_string = movies[index].get_text()
    movie = ' '.join(movie_string.split()).replace('.', '')
    movie_title = movie[len(str(index))+1:-7]
    year = re.search('\((.*?)\)', movie_string).group(1)
    rank = movie.split()[0]
    movie_data = {
        'movie_title' : movie_title,
        'rank': rank,
        'year': year,
        'star_cast' : crew[index],
        'rating' : ratings[index],
        'votes' : votes[index],
        'link' : links[index]} 
    top_movies_data.append(movie_data)

for movie_data in top_movies_data: 
    print('{} : {} ({}), Starring : {}, Rating: {}'.format(movie_data['rank'], movie_data['movie_title'],
    movie_data['year'], movie_data['star_cast'], movie_data['rating']))



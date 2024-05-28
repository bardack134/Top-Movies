from pprint import pprint
import requests 
from constants import API_KEY, API_TOKEN

url = "https://api.themoviedb.org/3/search/movie?api_key=" + API_KEY



parameters={
    'query':"titanic"
}

# Making a GET request 
r = requests.get(url,  params=parameters).json() 


# for debugging proccess 
# pprint(r) 

# title_list=[]
# year_list=[]

# for data in r['results']:
    
#     title_list.append(data['title'])
#     year_list.append(data['release_date'])
    
# pprint(title_list)
# pprint(year_list)
data_list=[]

for movie in r['results']:
    data={}
    
    data['release_date'] = movie['release_date']
    data['title'] = movie['title']
    data_list.append(data)
    
pprint(data_list)

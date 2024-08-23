from dotenv import load_dotenv
import requests
import os

load_dotenv()

TMDB_API_KEY=os.environ['TMDB_API_KEY']
LANGUAGE = 'en-US'
MAX_CAST_SIZE = 6

movie_id = 1163194

# Get the movie details from the TMDB API
movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language={LANGUAGE}"
response = requests.get(movie_url)
movie = response.json()

credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={TMDB_API_KEY}&language={LANGUAGE}"
response = requests.get(credits_url)
credits = response.json()

keywords_url = f"https://api.themoviedb.org/3/movie/{movie_id}/keywords?api_key={TMDB_API_KEY}"
response = requests.get(keywords_url)
keywords = response.json()

cast = []
for person in credits['cast'][:MAX_CAST_SIZE]:
    cast.append(person['name'])
cast = ", ".join(cast)

genres = []
for genre in movie['genres']:
    genres.append(genre['name'])
genres = ", ".join(genres)

spoken_languages = []
for language in movie['spoken_languages']:
    spoken_languages.append(language['english_name'])
spoken_languages = ", ".join(spoken_languages)

kw = []
for keyword in keywords['keywords']:
    kw.append(keyword['name'])
keywords = ", ".join(kw)




llm_instructions = [
    "Help me in creating a collection of tags for the following movie.",
    "The tags are intended to be used for SEO purposes in youtube.",
    "Include infomration such as the movie title, overview, cast, genres, languages, tagline, and keywords.",
    "Please provide the information in a single string separated by commas without hashtags or quotes.",
    "Please respond only with the tags and no other information.",
    "The information of the movie is as follows:"
]

instructions = []
instructions.append("\n".join(llm_instructions))
instructions.append("\n")
instructions.append(f"Movie: {movie['title']}")
instructions.append(f"Overview: {movie['overview']}")
instructions.append(f"Cast: {cast}")
instructions.append(f"Genres: {genres}")
instructions.append(f"Languages: {spoken_languages}")
instructions.append(f"Tagline: {movie['tagline']}")
instructions.append(f"Keywords: {keywords}")



import os
from anthropic import Anthropic

client = Anthropic(
    # This is the default and can be omitted
    api_key=os.environ["ANTHROPIC_API_KEY"],
)

message = client.messages.create(
    max_tokens=2048,
    messages=[
        {
            "role": "user",
            "content": "\n".join(instructions),
        }
    ],
    model="claude-3-5-sonnet-20240620",
)

[message] = message.content
print(message.text)
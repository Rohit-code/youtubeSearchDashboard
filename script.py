import os
import aiohttp
import asyncio
from elasticsearch import Elasticsearch, helpers
from datetime import datetime
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

load_dotenv()
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
# Predefined YouTube search query
SEARCH_QUERY = 'Hello'
#es = Elasticsearch()

es = Elasticsearch("http://localhost:9200",
    http_auth=('elastic', 'Mt-i5zkzBtcy*RXEYmtJ'),)

# Elasticsearch index setup
# Elasticsearch index setup
INDEX_NAME = 'youtube_videos'
if not es.indices.exists(index=INDEX_NAME):
    es.indices.create(index=INDEX_NAME, body={
        'mappings': {
            'properties': {
                'video_title': {'type': 'text'},
                'description': {'type': 'text'},
                'publishing_datetime': {'type': 'date'},
                'video_id': {'type': 'keyword'},
                # Add more fields as necessary
            }
        }
    })


async def fetch_videos():
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&order=date&type=video&q={SEARCH_QUERY}&key={YOUTUBE_API_KEY}"
    async with aiohttp.ClientSession() as session:
        while True:
            async with session.get(url) as response:
                data = await response.json()
                
                data = extract_video_data(data)
                
                actions = [
                    {
                        '_index': INDEX_NAME,
                        '_source': {
                            'video_title': video['video_title'],
                            'description': video['description'],
                            'publishing_datetime': video['published_datetime'],
                            'video_id':video["video_id"]
                            # Map more fields as required
                        },
                    }
                    for video in data
                ]
                helpers.bulk(es, actions)
                await asyncio.sleep(10)  # Wait for 10 seconds before the next API call

def extract_video_data(response):
    videos = []
    for item in response['items']:
        video_data = {
            'video_title': item['snippet']['title'],
            'description': item['snippet']['description'],
            'publish_datetime': item['snippet']['publishedAt'],
            'video_id': item['id']['videoId']
        }
        videos.append(video_data)
    return videos

# Extract data

es.indices.create(index=INDEX_NAME, body={}) #, headers={'Content-Type': 'application/json'})


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch_videos())

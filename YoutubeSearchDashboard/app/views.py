from django.shortcuts import render
from rest_framework.decorators import APIView
from rest_framework.response import Response
import os
import aiohttp
import asyncio
from elasticsearch import Elasticsearch, helpers
from datetime import datetime
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

# Initialize the Elasticsearch client
es = Elasticsearch("http://localhost:9200")

load_dotenv()
# The API key should be stored in an environment variable for security reasons

# Your search view
class SearchView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize the Elasticsearch client
        self.es = Elasticsearch("http://localhost:9200")

    def get(self, request):
        # Your search query
        search_query = 'tea how'

        # Formulate the search request
        search_body = {
            'query': {
                'multi_match': {
                    'query': search_query,
                    'fields': ['video_title', 'description'],
                    'type': 'best_fields',  # Finds documents which match any field, but uses the _score from the best field
                    'fuzziness': 'AUTO'  # Allows for fuzzy matching on the search query
                }
            }
        }

        # Execute the search query
        response = es.search(index='youtube_videos', body=search_body, headers={'Content-Type': 'application/json'})

        # Print out the response or process it according to your application's needs
        return Response(response)



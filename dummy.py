# Sample response from YouTube API
response = {
    "kind": "youtube#searchListResponse",
    "etag": "yIj93I_GgTUD-8v4EfgqgmPH8Js",
    "nextPageToken": "CAUQAA",
    "regionCode": "IN",
    "pageInfo": {
        "totalResults": 1000000,
        "resultsPerPage": 5
    },
    "items": [
        {
            "kind": "youtube#searchResult",
            "etag": "REchy8NZtV4TxuA27XF463MhiGg",
            "id": {
                "kind": "youtube#video",
                "videoId": "MXBj9Fror5c"
            },
            "snippet": {
                "publishedAt": "2024-03-13T10:59:44Z",
                "channelId": "UCZE7PZ4TOBFs4iU-9lMczHw",
                "title": "NIK BỊ ĐÃNG TRÍ HAY QUÊN 😱| Hello Nikki #shorts",
                "description": "",
                "thumbnails": {
                    "default": {
                        "url": "https://i.ytimg.com/vi/MXBj9Fror5c/default.jpg",
                        "width": 120,
                        "height": 90
                    },
                    "medium": {
                        "url": "https://i.ytimg.com/vi/MXBj9Fror5c/mqdefault.jpg",
                        "width": 320,
                        "height": 180
                    },
                    "high": {
                        "url": "https://i.ytimg.com/vi/MXBj9Fror5c/hqdefault.jpg",
                        "width": 480,
                        "height": 360
                    }
                },
                "channelTitle": "Hello Nikki",
                "liveBroadcastContent": "none",
                "publishTime": "2024-03-13T10:59:44Z"
            }
        },
    ]
}

# Function to extract required fields from the response
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
extracted_videos = extract_video_data(response)

# Display extracted data
for video in extracted_videos:
    print(f"Video Title: {video['video_title']}")
    print(f"Description: {video['description']}")
    print(f"Publish Datetime: {video['publish_datetime']}")
    print(f"Video ID: {video['video_id']}\n")
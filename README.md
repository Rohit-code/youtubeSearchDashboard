# YouTube Analytics Django Application

This Django application provides endpoints to fetch and store data from the YouTube Data API, specifically channel information, video data, and video statistics. It also offers endpoints for querying and retrieving this data.

## Installation

1. Clone this repository to your local machine.
2. Create a virtual environment for the project.
3. Install the dependencies from the `requirements.txt` file:
4. Set up the necessary environment variables:
- `api_key_channel_and_videos`: Your YouTube Data API key for accessing channel and video data.
- `api_key_video_statistics`: Your YouTube Data API key for accessing video statistics.

## Usage

1. Run migrations to create the necessary database tables:

2. Start the Django development server:

3. Access the API endpoints using the provided URLs:

- Endpoint for fetching and storing channel data:
  ```
  /fetch_and_store_channels/
  ```

- Endpoint for fetching and storing video data:
  ```
  /fetch_and_store_videos/
  ```

- Endpoint for fetching and storing video statistics:
  ```
  /fetch_and_store_video_statistics/
  ```

- Endpoint for querying channel data by name:
  ```
  /channel_by_name/<channel_name>/
  ```

- Endpoint for searching video by title:
  ```
  /api/search_video_by_title/<search_query>/
  ```

- Endpoint for getting total views for a channel within a time range:
  ```
  /total_views/<channel_id>/<start_timestamp>/<end_timestamp>/
  ```

- Endpoint for getting all video statistics for a specific video:
  ```
  /get_all_video_stats/<video_id>/
  ```

- Endpoint for getting video statistics for a specific video:
  ```
  /get_video_stats_by_id/<video_id>/
  ```

## Notes

- Make sure to replace the API keys with your own keys obtained from the Google Developer Console.
- Ensure that your Django application has appropriate permissions to access the YouTube Data API.
- This README assumes basic knowledge of Django and RESTful API concepts.


![Image Description](images\Screenshot 2024-03-13 221717.png)

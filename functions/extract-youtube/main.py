import re
from googleapiclient.discovery import build
import pandas as pd
from google.cloud import storage
import json
import datetime
import uuid
from io import BytesIO
import functions_framework

# storage client
storage_client = storage.Client()

# storage bucket
bucket_name = "ba882-team05"

# my api key created
api_key = 'AIzaSyAmJ7u9TgHN8-nTpHzrQxya5sdvwdflrK8'

# Netflix's YouTube Channel ID
channel_id = 'UCWOA1ZGywLbqmigxE4Qlvuw'

# Function to clean the description
def clean_description(description):
    cleaned_desc = re.split(r'\n\nSUBSCRIBE|\n\nWatch on Netflix|\r\n\r\nAbout Netflix|\n\nAbout Netflix', description, 1)[0]
    return cleaned_desc.strip()  # Remove leading and trailing whitespace

# Function to extract the real title
def extract_title(title):
    # Find the index of the first occurrence of ' | '
    index = title.find(' | ')
    
    # If ' | ' is found, return the part before it
    if index != -1:
        return title[:index]
    else:
        # If ' | ' is not found, return the original title
        return title

# Function to convert duration to required format
def format_duration(duration):
    duration = duration.replace('PT', '')
    hours = minutes = seconds = 0

    if 'H' in duration:
        hours, duration = duration.split('H')
        hours = int(hours)
    if 'M' in duration:
        minutes, duration = duration.split('M')
        minutes = int(minutes)
    if 'S' in duration:
        seconds = int(duration.replace('S', ''))

    # Format overall time as HH:MM:SS
    overall_time = f"{hours:02}:{minutes:02}:{seconds:02}"

    return overall_time, hours, minutes, seconds  # Return four values

# Function to fetch category name using categoryId
def get_category_name(yt, category_id):
    """
    This function gets the category name from YouTube Data API using the categoryId.
    """
    try:
        # Fetch category name using categoryId (e.g., '1' for Film & Animation)
        categories_request = yt.videoCategories().list(
            part='snippet',
            id=category_id
        )
        categories_response = categories_request.execute()
        category_name = categories_response['items'][0]['snippet']['title']  # Get the category name
        return category_name
    except Exception as e:
        print(f"Error fetching category for id {category_id}: {e}")
        return 'Unknown'  # Return 'Unknown' if category not found or an error occurs

# Main function to fetch video information
def main(request):
    yt = build('youtube', 'v3', developerKey=api_key)

    # Save the information of each video
    videos_info = []

    # Initialize request for search API to get video details
    request = yt.search().list(
        channelId=channel_id,
        part='snippet',  # Get snippet info including title, description, etc.
        maxResults=50,   # Max results for each page
        order='date'     # Sort by date
    )

    # # Loop until you get enough data (max 400 videos)
    # while len(videos_info) < 400:
    # CHANGED HERE!!!
    # Loop until no more pages are available (no limit on number of videos)
    while request is not None:
        response = request.execute()

        for item in response['items']:
            video_id = item['id'].get('videoId')
            if video_id:  # Make sure video id exists
                # Get video statistics and details
                stats_request = yt.videos().list(
                    part='statistics, snippet, contentDetails',
                    id=video_id
                )
                stats_response = stats_request.execute()
                video_info = stats_response['items'][0]

                # Extract relevant information
                views = video_info['statistics'].get('viewCount')
                likes = video_info['statistics'].get('likeCount')
                favorites = video_info['statistics'].get('favoriteCount')
                comments_cnt = video_info['statistics'].get('commentCount')

                # Get snippet information
                title = video_info['snippet'].get('title')
                extracted_title = extract_title(title)  # Extract the real title
                description = video_info['snippet'].get('description')
                cleaned_description = clean_description(description)  # Clean the description
                published_at = video_info['snippet'].get('publishedAt')
                thumbnail_url = video_info['snippet']['thumbnails']['default']['url']
                video_duration = video_info['contentDetails'].get('duration')
                overall_time, hours, minutes, seconds = format_duration(video_duration)  # Format the duration
                category_id = video_info['snippet'].get('categoryId')  # Get the categoryId

                # Fetch the category name using categoryId
                category_name = get_category_name(yt, category_id)

                video_data = {
                    'video_id': video_id,
                    'title': title,
                    'extracted_title': extracted_title,
                    'description': cleaned_description,
                    'category': category_name,  # Use the category name here
                    'published_at': published_at,
                    'views': views,
                    'likes': likes,
                    'favorites': favorites,
                    'comments_count': comments_cnt,
                    'comments': [],
                    'thumbnail_url': thumbnail_url,
                    'overall_time': overall_time,   # Overall time in HH:MM:SS format
                    'hours': hours,                 # Hours
                    'minutes': minutes,             # Minutes
                    'seconds': seconds              # Seconds
                }

                # Turn comment counts as an integer (if exists)
                comments_cnt = int(comments_cnt) if comments_cnt else 0

                # Only when comments exist
                if comments_cnt > 0:
                    comments_request = yt.commentThreads().list(
                        part='snippet',
                        videoId=video_id,
                        maxResults=5
                    )
                    comments_response = comments_request.execute()

                    # Extract comment texts
                    for comment_item in comments_response['items']:
                        comment_text = comment_item['snippet']['topLevelComment']['snippet']['textDisplay']
                        video_data['comments'].append(comment_text)  # Add comment texts to video_data list

                videos_info.append(video_data)  # Add a complete video information to the list

        # # Check if there are more pages
        # if 'nextPageToken' in response:
        #     request = yt.search().list_next(request, response)  # Request to get more pages
        # else:
        #     break
        # CHANGED HERE!!!
        # Check for nextPageToken and continue fetching more pages if available
        request = yt.search().list_next(request, response)

    data = []
    for item in videos_info:
      data.append(dict(item))

    videos_info = pd.DataFrame(data)
    videos_info.shape

    # flatten back to a list of dictionaries 
    videos_info = videos_info.to_dict('records')

    # Generate job ID
    JOB_ID = datetime.datetime.now().strftime("%Y%m%d%H%M") + "-" + str(uuid.uuid4())

    # Prepare data for GCS
    blob_name = f"jobs/youtube_api/{JOB_ID}/youtube_api.json"

    # Save the data as a json file in memory
    json_buffer = BytesIO()
    for record in videos_info:
      json_buffer.write((json.dumps(record) + "\n").encode('utf-8'))
    json_buffer.seek(0)

    # Upload the JSON file to GCS
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_file(json_buffer, content_type="application/json")

    # Prepare results
    file_path = f"gs://{bucket_name}/{blob_name}"
    
    results = {
        'filepath': file_path,
        'jobid': JOB_ID,
        'bucket_id': bucket_name,
        'blob_name': blob_name
    }
    
    print(results)
    return results
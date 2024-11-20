import os
import sys
import argparse
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

def get_youtube_service(api_key):
    """Builds the YouTube service object."""
    return build('youtube', 'v3', developerKey=api_key)

def search_videos(youtube, query, max_results):
    """Searches for videos based on a query and returns their video IDs and titles."""
    request = youtube.search().list(
        q=query,
        part='id,snippet',
        type='video',
        maxResults=max_results
    )
    response = request.execute()
    videos = []
    for item in response.get('items', []):
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        videos.append({'id': video_id, 'title': title})
    return videos

def get_transcript(video_id):
    """Fetches the transcript for a given video ID."""
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        if transcript_list.find_transcript(['en']):
            transcript = transcript_list.find_transcript(['en']).fetch()
        else:
            return "No English transcripts found for this video."
        # Combine all transcript pieces into one string
        full_transcript = ' '.join([entry['text'] for entry in transcript])
        return full_transcript
    except TranscriptsDisabled:
        return "Transcripts are disabled for this video."
    except NoTranscriptFound:
        return "No transcripts found for this video."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="Search YouTube videos and retrieve their transcripts.")
    parser.add_argument('query', type=str, help='Topic to search for')
    parser.add_argument('n', type=int, help='Number of videos to retrieve')
    parser.add_argument('--api_key', type=str, help='YouTube Data API key', required=True)
    
    args = parser.parse_args()
    
    youtube = get_youtube_service(args.api_key)
    print(f"Searching for '{args.query}' on YouTube...")
    videos = search_videos(youtube, args.query, args.n)
    
    if not videos:
        print("No videos found.")
        sys.exit(0)
    
    for idx, video in enumerate(videos, start=1):
        print(f"\nVideo {idx}: {video['title']}")
        print(f"Video ID: {video['id']}")
        transcript = get_transcript(video['id'])
        print(f"Transcript:\n{transcript}\n{'-'*80}")

if __name__ == "__main__":
    main()

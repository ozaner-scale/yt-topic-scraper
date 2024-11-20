import os
import sys
import argparse
import json
from dotenv import load_dotenv
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

def get_youtube_service(api_key):
    """Builds the YouTube service object."""
    return build('youtube', 'v3', developerKey=api_key)

def search_videos(youtube, query, max_results):
    """
    Searches for videos based on a query and returns their video IDs and titles.
    Handles pagination to retrieve up to max_results videos.
    """
    videos = []
    next_page_token = None

    while len(videos) < max_results:
        request = youtube.search().list(
            q=query,
            part='id,snippet',
            type='video',
            maxResults=min(max_results - len(videos), 50),  # YouTube API allows max 50 per request
            pageToken=next_page_token
        )
        try:
            response = request.execute()
        except Exception as e:
            print(f"An error occurred while searching for videos: {str(e)}")
            break

        for item in response.get('items', []):
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            videos.append({'id': video_id, 'title': title})
            if len(videos) >= max_results:
                break

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break  # No more pages

    return videos

def get_transcript(video_id):
    """Fetches the transcript for a given video ID."""
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript(['en']).fetch()
        # Combine all transcript pieces into one string
        full_transcript = ' '.join([entry['text'] for entry in transcript])
        return full_transcript
    except TranscriptsDisabled:
        return None  # Indicate that transcripts are disabled
    except NoTranscriptFound:
        return None  # Indicate that no transcripts are found
    except Exception:
        return None  # Any other exception treated as no transcript

def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Search YouTube videos and retrieve their transcripts.")
    parser.add_argument('query', type=str, help='Topic to search for')
    parser.add_argument('n', type=int, help='Number of videos to retrieve with transcripts')
    parser.add_argument('--api_key', type=str, help='YouTube Data API key')
    parser.add_argument('-j', '--json', action='store_true', help='Output results in JSON format')
    parser.add_argument('-o', '--out', type=str, help='Output file path')

    args = parser.parse_args()

    # Retrieve API key from argument or environment variable
    api_key = args.api_key or os.getenv('YT_API_KEY')
    if not api_key:
        print("Error: You must provide a YouTube Data API key either via the --api_key argument or the YT_API_KEY environment variable.")
        sys.exit(1)

    youtube = get_youtube_service(api_key)
    print(f"Searching for '{args.query}' on YouTube...")

    # Set max_attempts to n + 10
    desired_count = args.n
    max_additional_attempts = 10
    max_search_results = desired_count + max_additional_attempts

    # Search for more videos to account for those without transcripts
    videos = search_videos(youtube, args.query, max_search_results)

    if not videos:
        print("No videos found.")
        sys.exit(0)

    results = []
    attempts = 0

    for video in videos:
        if len(results) >= desired_count:
            break  # Desired number of results achieved

        transcript = get_transcript(video['id'])
        if transcript:
            video_info = {
                'video_number': len(results) + 1,
                'title': video['title'],
                'video_id': video['id'],
                'transcript': transcript
            }
            results.append(video_info)
        else:
            attempts += 1
            if attempts >= max_additional_attempts:
                break  # Reached maximum additional attempts

    if len(results) < desired_count:
        print(f"Only found {len(results)} videos with transcripts after {attempts} unsuccessful attempts.")
    else:
        print(f"Successfully retrieved {len(results)} videos with transcripts.")

    if results:
        if args.out:
            try:
                with open(args.out, 'w', encoding='utf-8') as f:
                    if args.json:
                        # Output as JSON
                        json.dump(results, f, indent=4, ensure_ascii=False)
                    else:
                        # Pretty console output
                        for video in results:
                            f.write(f"\nVideo {video['video_number']}: {video['title']}\n")
                            f.write(f"Video ID: {video['video_id']}\n")
                            f.write(f"Transcript:\n{video['transcript']}\n{'-'*80}\n")
                print(f"Output successfully saved to '{args.out}'.")
            except Exception as e:
                print(f"An error occurred while writing to the file: {str(e)}")
        else:
            # Pretty console output
            for video in results:
                print(f"\nVideo {video['video_number']}: {video['title']}")
                print(f"Video ID: {video['video_id']}")
                print(f"Transcript:\n{video['transcript']}\n{'-'*80}")

if __name__ == "__main__":
    main()
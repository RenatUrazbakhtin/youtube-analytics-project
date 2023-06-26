
from googleapiclient.discovery import build
from datetime import timedelta
import isodate


class PlayList:
    api_key = "AIzaSyAq81ppMIiD0BIY6rX9iYS51HmrEHq31Ho"
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.title = self.get_playlist_title()
        self.url = ''.join(['https://www.youtube.com/playlist?list=', self.playlist_id])

    def get_info(self):
        playlist = self.youtube.playlistItems().list(part='snippet,contentDetails', playlistId=self.playlist_id).execute()
        return playlist

    def get_playlist_title(self):
        playlists = self.youtube.playlists().list(channelId=self.get_info()['items'][0]['snippet']['channelId'], part='contentDetails,snippet', maxResults=50,).execute()

        for playlist in playlists['items']:
            if playlist['id'] == self.playlist_id:
                return playlist['snippet']['title']


    def get_video_ids(self):
        return [video['contentDetails']['videoId'] for video in self.get_info()['items']]

    @property
    def total_duration(self):

        total_duration = timedelta(hours=0, minutes=0, seconds=0)

        for video_id in self.get_video_ids():
            video = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails', id=video_id).execute()
            duration = video['items'][0]['contentDetails']['duration']

            iso_duration = isodate.parse_duration(duration)
            duration_split = str(iso_duration).split(':')
            duration = timedelta(hours=int(duration_split[0]), minutes=int(duration_split[1]),
                                 seconds=int(duration_split[2]))
            total_duration += duration

        return total_duration

    def show_best_video(self):
        best_video_likes = 0
        best_video_url = ''

        for video_id in self.get_video_ids():
            video = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails', id=video_id).execute()
            likes = int(video['items'][0]['statistics']['likeCount'])
            if likes > best_video_likes:
                best_video_likes = likes
                best_video_url = ''.join(['https://youtu.be/', video_id])
            else:
                continue

        return best_video_url
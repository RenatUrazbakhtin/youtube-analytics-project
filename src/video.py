from src.channel import Channel
from googleapiclient.discovery import build
import json
class Video():
    api_key = "AIzaSyAq81ppMIiD0BIY6rX9iYS51HmrEHq31Ho"
    youtube = build('youtube', 'v3', developerKey=api_key)
    def __init__(self, video_id):
        self.video_id = video_id
        self.title = self.get_video()['items'][0]['snippet']['title']
        self.url = self.url = ''.join(['https://www.youtube.com/watch/', self.video_id])
        self.view_count = self.get_video()['items'][0]['statistics']['viewCount']
        self.likes_count = self.get_video()['items'][0]['statistics']['likeCount']
    def get_video(self):
        video = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails', id=self.video_id).execute()
        return video
    def __str__(self):
        return self.title

class PLVideo(Video):
    def __init__(self, video_id, pl_id):
        super().__init__(video_id)
        self.pl_id = pl_id






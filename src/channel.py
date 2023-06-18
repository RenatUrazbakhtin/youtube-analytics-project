import os
from googleapiclient.discovery import build
import json

class Channel:
    """Класс для ютуб-канала"""
    api_key = "AIzaSyAq81ppMIiD0BIY6rX9iYS51HmrEHq31Ho"
    youtube = build('youtube', 'v3', developerKey=api_key)
    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.title = self.get_info()['items'][0]['snippet']['title']
        self.description = self.get_info()['items'][0]['snippet']['localized']['description']
        self.url = ''.join(['https://www.youtube.com/channel/', self.channel_id])
        self.subscriber_count = self.get_info()['items'][0]['statistics']['subscriberCount']
        self.video_count = self.get_info()['items'][0]['statistics']['videoCount']
        self.view_count = self.get_info()['items'][0]['statistics']['viewCount']

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __ge__(self, other):
        if int(self.subscriber_count) >= int(other.subscriber_count):
            return True
        else:
            return False
    def __gt__(self, other):
        if int(self.subscriber_count) > int(other.subscriber_count):
            return True
        else:
            return False
    def __lt__(self, other):
        if int(self.subscriber_count) < int(other.subscriber_count):
            return True
        else:
            return False
    def __le__(self, other):
        if int(self.subscriber_count) <= int(other.subscriber_count):
            return True
        else:
            return False
    def get_info(self):
        channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        return channel

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(channel)

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)

    def to_json(self, filename):
        with open(filename, "w") as file:
            data = {
            'channel_id': self.channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count
        }
            json.dump(data, file, indent=2, ensure_ascii=False)

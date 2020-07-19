import time
from typing import List, Any

import click
import progressbar

from .scope import Scope


class Video(Scope):
    def fetch(self, user_id: str, *args) -> List[Any]:
        user_videos_response = self._collection_api.get(user_id=user_id, count=200)
        user_videos = user_videos_response['items']
        click.echo("User has %s videos. Received %s" % (user_videos_response['count'], len(user_videos)))
        return user_videos

    def remove(self, user_id, vk_collection) -> None:
        click.echo('Deleting...')
        time.sleep(1)
        deleted_per_second = 0
        for video in progressbar.progressbar(vk_collection):
            self._collection_api.delete(video_id=video['id'], owner_id=video['owner_id'], target_id=user_id)
            deleted_per_second += 1
            if deleted_per_second == 5:
                time.sleep(1.2)
                deleted_per_second = 0

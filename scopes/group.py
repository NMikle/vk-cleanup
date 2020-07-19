import time
from typing import List, Any

import click
import progressbar

from .scope import Scope


class Group(Scope):
    def fetch(self, user_id: str, *args) -> List[Any]:
        user_groups = self._collection_api.get(user_id=user_id)['items']
        click.echo("Received %s groups" % (len(user_groups)))
        return user_groups

    def remove(self, user_id: str, vk_collection: List[Any]) -> None:
        click.echo('Leaving...')
        time.sleep(1)
        deleted_per_second = 0
        for group_id in progressbar.progressbar(vk_collection):
            self._collection_api.leave(group_id=group_id)
            deleted_per_second += 1
            if deleted_per_second == 5:
                time.sleep(1.2)
                deleted_per_second = 0

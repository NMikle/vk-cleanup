from typing import List, Any


class Scope:
    def __init__(self, vk_collection_api) -> None:
        self._collection_api = vk_collection_api

    def fetch(self, user_id: str, *args) -> List[Any]:
        raise NotImplementedError

    def remove(self, user_id: str, vk_collection: List[Any]) -> None:
        raise NotImplementedError

from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.model import AbstractModel
from mipac.models.user import UserDetailed
from mipac.types.mute import IMuteUser

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class MuteUser(AbstractModel):
    def __init__(self, data: IMuteUser, *, client: ClientManager) -> None:
        self.__data: IMuteUser = data
        self.__client: ClientManager = client

    @property
    def id(self) -> str:
        return self.__data["id"]

    @property
    def created_at(self) -> str:
        return self.__data["created_at"]

    @property
    def mutee_id(self) -> str:
        return self.__data["mutee_id"]

    @property
    def mutee(self) -> UserDetailed:
        return UserDetailed(self.__data["mutee"], client=self.__client)

    def __eq__(self, __value: MuteUser) -> bool:
        return isinstance(__value, IMuteUser) and self.id == __value.id

    def __ne__(self, __value: MuteUser) -> bool:
        return not self.__eq__(__value)
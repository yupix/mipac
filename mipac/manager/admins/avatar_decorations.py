
from __future__ import annotations
from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.http import HTTPClient
from mipac.actions.admins.avatar_decorations import AvatarDecorationActions

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class AvatarDecorationManager(AbstractManager):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__action: AvatarDecorationActions = AvatarDecorationActions(session=session, client=client)

    @property
    def action(self) -> AvatarDecorationActions:
        return self.__action

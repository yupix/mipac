from __future__ import annotations
from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.http import HTTPClient
from mipac.actions.admins.avatar_decorations import (
    AdminAvatarDecorationActions,
    ClientAdminAvatarDecorationActions,
)

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class ClientAdminAvatarDecorationManager(AbstractManager):
    def __init__(self, avatar_decoration_id: str, *, session: HTTPClient, client: ClientManager):
        self.__action: ClientAdminAvatarDecorationActions = ClientAdminAvatarDecorationActions(
            avatar_decoration_id, session=session, client=client
        )

    @property
    def action(self) -> ClientAdminAvatarDecorationActions:
        return self.__action


class AdminAvatarDecorationManager(AbstractManager):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__action: AdminAvatarDecorationActions = AdminAvatarDecorationActions(
            session=session, client=client
        )

    @property
    def action(self) -> AdminAvatarDecorationActions:
        return self.__action

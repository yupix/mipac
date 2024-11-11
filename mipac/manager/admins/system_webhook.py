from __future__ import annotations
from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.http import HTTPClient
from mipac.actions.admins.system_webhook import SystemWebhookActions, ClientSystemWebhookActions

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class ClientSystemWebhookManager(AbstractManager):
    def __init__(self, webhook_id: str, *, session: HTTPClient, client: ClientManager):
        self.__action: ClientSystemWebhookActions = ClientSystemWebhookActions(
            webhook_id, session=session, client=client
        )

    @property
    def action(self) -> ClientSystemWebhookActions:
        return self.__action


class SystemWebhookManager(AbstractManager):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__action: SystemWebhookActions = SystemWebhookActions(session=session, client=client)

    @property
    def action(self) -> SystemWebhookActions:
        return self.__action

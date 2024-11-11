from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from mipac.utils.format import str_to_datetime
from mipac.types.system_webhook import ISystemWebhook, SystemWebhookEventTypes

if TYPE_CHECKING:
    from mipac.client import ClientManager


class SystemWebhook:
    def __init__(self, raw_system_webhook: ISystemWebhook, *, client: ClientManager):
        self.__raw_system_webhook: ISystemWebhook = raw_system_webhook
        self.___client: ClientManager = client

    @property
    def id(self) -> str:
        return self.__raw_system_webhook["id"]

    @property
    def is_active(self) -> bool:
        return self.__raw_system_webhook["is_active"]

    @property
    def updated_at(self) -> datetime:
        return str_to_datetime(self.__raw_system_webhook["updated_at"])

    @property
    def latest_sent_at(self) -> datetime | None:
        return (
            str_to_datetime(self.__raw_system_webhook["latest_sent_at"])
            if self.__raw_system_webhook["latest_sent_at"]
            else None
        )

    @property
    def latest_status(self) -> str | None:
        return self.__raw_system_webhook["latest_status"]

    @property
    def name(self) -> str:
        return self.__raw_system_webhook["name"]

    @property
    def on(self) -> SystemWebhookEventTypes:
        return self.__raw_system_webhook["on"]

    @property
    def url(self) -> str:
        return self.__raw_system_webhook["url"]

    @property
    def secret(self) -> str:
        return self.__raw_system_webhook["secret"]

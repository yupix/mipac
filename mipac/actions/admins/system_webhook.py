from __future__ import annotations

from typing import TYPE_CHECKING, Literal, override

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.system_webhook import SystemWebhook
from mipac.types.system_webhook import ISystemWebhook, SystemWebhookEventTypes

if TYPE_CHECKING:
    from mipac.client import ClientManager


class SharedSystemWebhookActions(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self._session: HTTPClient = session
        self._client: ClientManager = client

    async def delete(self, *, webhook_id: str) -> bool:
        is_success: bool = await self._session.request(
            Route("POST", "/api/admin/system-webhook/delete"), json={"id": webhook_id}
        )
        return is_success

    async def update(
        self,
        is_active: bool,
        name: str,
        on: SystemWebhookEventTypes,
        url: str,
        secret: str,
        *,
        webhook_id: str,
    ) -> SystemWebhook:
        body = {"isActive": is_active, "name": name, "on": on, "url": url, "secret": secret}
        system_webhook_payload: ISystemWebhook = await self._session.request(
            Route("POST", "/api/admin/system-webhook/update"), json={"id": webhook_id, **body}
        )

        return SystemWebhook(system_webhook_payload, client=self._client)


class ClientSystemWebhookActions(SharedSystemWebhookActions):
    def __init__(self, webhook_id: str, *, session: HTTPClient, client: ClientManager):
        super().__init__(session=session, client=client)
        self.__webhook_id: str = webhook_id

    @override
    async def delete(self, *, webhook_id: str | None = None) -> bool:
        webhook_id = webhook_id or self.__webhook_id
        return await super().delete(webhook_id=webhook_id)

    @override
    async def update(
        self,
        is_active: bool,
        name: str,
        on: SystemWebhookEventTypes,
        url: str,
        secret: str,
        *,
        webhook_id: str | None = None,
    ) -> SystemWebhook:
        webhook_id = webhook_id or self.__webhook_id
        return await super().update(is_active, name, on, url, secret, webhook_id=webhook_id)


class SystemWebhookActions(SharedSystemWebhookActions):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        super().__init__(session=session, client=client)

    async def create(
        self,
        is_active: bool,
        name: str,
        on: list[Literal["abuseReport", "abuseReportResolved", "userCreated"]],
        url: str,
        secret: str,
    ):
        body = {"isActive": is_active, "name": name, "on": on, "url": url, "secret": secret}

        system_webhook_payload: ISystemWebhook = await self._session.request(
            Route("POST", "/api/admin/system-webhook/create"), json=body
        )
        return SystemWebhook(system_webhook_payload, client=self._client)

    async def get_list(
        self,
        is_active: bool | None = None,
        abuse_report: bool | None = None,
        abuse_report_resolved: bool | None = None,
        user_created: bool | None = None,
    ):
        body = {
            "isActive": is_active,
            "abuseReport": abuse_report,
            "abuseReportResolved": abuse_report_resolved,
            "userCreated": user_created,
        }
        system_webhook_payload: list[ISystemWebhook] = await self._session.request(
            Route("POST", "/api/admin/system-webhook/list"), json=body
        )
        return [
            SystemWebhook(system_webhook, client=self._client)
            for system_webhook in system_webhook_payload
        ]

    async def show(self, *, webhook_id: str):
        system_webhook_payload: ISystemWebhook = await self._session.request(
            Route("POST", "/api/admin/system-webhook/show"), json={"id": webhook_id}
        )
        return SystemWebhook(system_webhook_payload, client=self._client)

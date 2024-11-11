from typing import TypedDict, Literal

SystemWebhookEventTypes = Literal[
    "abuseReport",
    "abuseReportResolved",
    "userCreated",
    "inactiveModeratorsWarning",
    "inactiveModeratorsInvitationOnlyChanged",
]


class ISystemWebhook(TypedDict):
    id: str
    is_active: bool
    updated_at: str
    latest_sent_at: str | None
    latest_status: str | None
    name: str
    on: SystemWebhookEventTypes
    url: str
    secret: str

from typing import Literal, NotRequired, TypedDict

from mipac.types.ads import IPartialAd
from mipac.types.roles import IRolePolicies

ISensitiveMediaDetectionSentivity = Literal["medium", "low", "high", "veryLow", "veryHigh"]
ISensitiveMediaDetection = Literal["none", "all", "local", "remote"]


class IFeatures(TypedDict):
    registration: bool
    email_required_for_signup: bool
    local_timeline: bool
    global_timeline: bool
    hcaptcha: bool
    turnstile: bool
    recaptcha: bool
    object_storage: bool
    service_worker: bool
    miauth: bool


class IPartialMeta(TypedDict):
    maintainer_name: str | None
    maintainer_email: str | None
    version: str
    provides_tar_ball: bool
    name: str | None
    short_name: str | None
    uri: str
    description: str | None
    langs: list[str]
    tos_url: str | None
    repository_url: str | None
    feedback_url: str | None
    default_dark_theme: str | None
    default_light_theme: str | None
    disable_registration: bool
    email_required_for_signup: bool
    enable_hcaptcha: bool
    hcaptcha_site_key: str | None
    enable_mcaptcha: bool
    mcaptcha_site_key: str | None
    mcaptcha_instance_url: str | None
    enable_recaptcha: bool
    recaptcha_site_key: str | None
    enable_turnstile: bool
    turnstile_site_key: str | None
    enable_testcaptcha: bool
    sw_publickey: str | None
    mascot_image_url: str
    banner_url: str | None
    server_error_image_url: str | None
    info_image_url: str | None
    not_found_image_url: str | None
    icon_url: str | None
    max_note_text_length: int
    ads: list[IPartialAd]
    notes_per_one_ad: int
    enable_email: bool
    enable_service_worker: bool
    translator_available: bool
    media_proxy: bool
    enable_url_preview: bool
    background_image_url: str | None
    impressum_url: str | None
    logo_image_url: str | None
    privacy_policy_url: str | None
    inquiry_url: str | None
    server_rules: list[str]
    theme_color: str | None
    policies: IRolePolicies
    note_searchable_scope: Literal["local", "global"]
    max_file_size: int


class IMetaDetailedOnly(TypedDict):
    features: IFeatures
    proxy_account_name: str | None
    require_setup: bool
    cache_remote_files: bool
    cache_remote_sensitive_files: bool


class IMetaDetailed(IPartialMeta, IMetaDetailedOnly):
    pass


class IMetaDetailedOnly(TypedDict):
    features: IFeatures
    proxy_account_name: str
    require_setup: bool
    cache_remote_files: bool
    cache_remote_sensitive_files: bool


class IMeta(IPartialMeta, TypedDict): ...


class IAdminMeta(TypedDict):
    cache_remote_files: bool
    cache_remote_sensitive_files: bool
    email_required_for_signup: bool
    enable_hcaptcha: bool
    hcaptcha_site_key: str | None
    enable_mcaptcha: bool
    mcaptcha_site_key: str | None
    mcaptcha_instance_url: str | None
    enable_recaptcha: bool
    recaptcha_site_key: str | None
    enable_turnstile: bool
    turnstile_site_key: str | None
    enable_testcaptcha: bool
    sw_publickey: str | None
    mascot_image_url: str | None
    banner_url: str | None
    server_error_image_url: str | None
    info_image_url: str | None
    not_found_image_url: str | None
    icon_url: str | None
    app192_icon_url: str | None
    app512_icon_url: str | None
    enable_email: bool
    enable_service_worker: bool
    translator_available: bool
    silenced_hosts: NotRequired[list[str]]
    media_silenced_hosts: list[str]
    pinned_users: list[str]
    hidden_tags: list[str]
    blocked_hosts: list[str]
    sensitive_words: list[str]
    prohibited_words: list[str]
    prohibited_words_for_name_of_user: list[str]
    banned_email_domains: NotRequired[list[str]]
    preserved_usernames: list[str]
    hcaptcha_secret_key: str | None
    mcaptcha_secret_key: str | None
    recaptcha_secret_key: str | None
    turnstile_secret_key: str | None
    sensitive_media_detection: str
    sensitive_media_detection_sensitivity: str
    set_sensitive_flag_automatically: bool
    enable_sensitive_media_detection_for_videos: bool
    proxy_account_id: str | None
    email: str | None
    smtp_secure: bool
    smtp_host: str | None
    smtp_port: float | None
    smtp_user: str | None
    smtp_pass: str | None
    sw_private_key: str | None
    use_object_storage: bool
    object_storage_base_url: str | None
    object_storage_bucket: str | None
    object_storage_prefix: str | None
    object_storage_endpoint: str | None
    object_storage_region: str | None
    object_storage_port: float | None
    object_storage_access_key: str | None
    object_storage_secret_key: str | None
    object_storage_use_ssl: bool
    object_storage_use_proxy: bool
    object_storage_set_public_read: bool
    enable_ip_logging: bool
    enable_active_email_validation: bool
    enable_verifymail_api: bool
    verifymail_auth_key: str | None
    enable_truemail_api: bool
    truemail_instance: str | None
    truemail_auth_key: str | None
    enable_charts_for_remote_user: bool
    enable_charts_for_federated_instances: bool
    enable_stats_for_federated_instances: bool
    enable_server_machine_stats: bool
    enable_identicon_generation: bool
    manifest_json_override: str
    policies: dict
    enable_fanout_timeline: bool
    enable_fanout_timeline_db_fallback: bool
    per_local_user_user_timeline_cache_max: float
    per_remote_user_user_timeline_cache_max: float
    per_user_home_timeline_cache_max: float
    per_user_list_timeline_cache_max: float
    enable_reactions_buffering: bool
    notes_per_one_ad: float
    background_image_url: str | None
    deepl_auth_key: str | None
    deepl_is_pro: bool
    default_dark_theme: str | None
    default_light_theme: str | None
    description: str | None
    disable_registration: bool
    impressum_url: str | None
    maintainer_email: str | None
    maintainer_name: str | None
    name: str | None
    short_name: str | None
    object_storage_s3_force_path_style: bool
    privacy_policy_url: str | None
    inquiry_url: str | None
    repository_url: str | None
    summaly_proxy: str | None
    theme_color: str | None
    tos_url: str | None
    uri: str
    version: str
    url_preview_enabled: bool
    url_preview_timeout: float
    url_preview_maximum_content_length: float
    url_preview_require_content_length: bool
    url_preview_user_agent: str | None
    url_preview_summary_proxy_url: str | None
    federation: str
    federation_hosts: list[str]


class IUpdateMetaBody(TypedDict, total=False):
    announcements: list
    disable_registration: bool
    disable_local_timeline: bool
    disable_global_timeline: bool
    enable_emoji_reaction: bool
    use_star_for_reaction_fallback: bool
    pinned_users: list[str]
    hidden_tags: list[str]
    blocked_hosts: list[str]
    mascot_image_url: str | None
    banner_url: str | None
    error_image_url: str | None
    icon_url: str | None
    name: str | None
    description: str | None
    max_note_text_length: int
    local_drive_capacity_mb: int
    remote_drive_capacity_mb: int
    cache_remote_files: bool
    proxy_remote_files: bool
    enable_recaptcha: bool
    recaptcha_site_key: str
    recaptcha_secret_key: str
    enable_turnstile: bool
    turnstile_site_key: str
    turnstile_secret_key: str
    proxy_account_id: str | None
    proxy_account: str
    maintainer_name: str | None
    maintainer_email: str | None
    langs: str
    summaly_proxy: str | None
    enable_twitter_integration: bool
    twitter_consumer_key: str | None
    twitter_consumer_secret: str | None
    enable_github_integration: bool
    github_client_id: str | None
    github_client_secret: str | None
    enable_discord_integration: bool
    discord_client_id: str | None
    discord_client_secret: str | None
    enable_email: bool
    email: str
    smtp_secure: bool
    smtp_host: str | None
    smtp_port: int | None
    smtp_user: str | None
    smtp_pass: str | None
    enable_service_worker: bool
    sw_public_key: str
    sw_private_key: str
    tos_url: str | None
    tos_text_url: str
    repository_url: str
    feedback_url: str
    use_object_storage: bool
    object_storage_base_url: str | None
    object_storage_bucket: str | None
    object_storage_prefix: str | None
    object_storage_endpoint: str | None
    object_storage_region: str | None
    object_storage_port: int | None
    object_storage_access_key: str | None
    object_storage_secret_key: str | None
    object_storage_use_s_s_l: bool
    object_storage_use_proxy: bool
    object_storage_set_public_read: bool
    object_storage_s3_force_path_style: bool
    server_rules: NotRequired[
        list[str]
    ]  # v13.11.3以降のバージョンから追加。その場合は使わないとエラー出るかも

from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator, Literal, Optional, TypeVar, Union, overload

from mipac.config import config
from mipac.errors.base import (
    NotExistRequiredData,
    NotSupportVersion,
    NotSupportVersionText,
    ParameterError,
)
from mipac.http import HTTPClient, Route
from mipac.models.clip import Clip
from mipac.models.note import Note
from mipac.models.user import Achievement, LiteUser, UserDetailed
from mipac.types.clip import IClip
from mipac.types.note import INote
from mipac.types.user import ILiteUser, IUserDetailed
from mipac.utils.cache import cache
from mipac.utils.format import remove_dict_empty
from mipac.utils.pagination import Pagination, pagination_iterator
from mipac.utils.util import check_multi_arg

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager

__all__ = ["UserActions"]

T = TypeVar("T", bound=Union[LiteUser, UserDetailed])


class UserActions:
    def __init__(
        self,
        session: HTTPClient,
        client: ClientManager,
        user: Optional[LiteUser] = None,
    ):
        self.__session: HTTPClient = session
        self.__user: Optional[LiteUser] = user
        self.__client: ClientManager = client

    async def get_me(self) -> UserDetailed:
        """
        ログインしているユーザーの情報を取得します
        """

        res = await self.__session.request(
            Route("POST", "/api/i"),
            auth=True,
            lower=True,
        )
        return UserDetailed(res, client=self.__client)  # TODO: 自分用のクラスに変更する

    def get_profile_link(
        self,
        external: bool = True,
        protocol: Literal["http", "https"] = "https",
    ):
        if not self.__user:
            return None
        host = (
            f"{protocol}://{self.__user.host}"
            if external and self.__user.host
            else self.__session._url
        )
        path = (
            f"/@{self.__user.username}" if external else f"/{self.__user.api.action.get_mention()}"
        )
        return host + path

    @cache(group="get_user")
    async def get(
        self,
        user_id: str | None = None,
        username: str | None = None,
        host: str | None = None,
        **kwargs,
    ) -> UserDetailed:
        """
        Retrieve user information from the user ID using the cache.
        If there is no cache, `fetch` is automatically used.
        The `fetch` method is recommended if you want up-to-date user information.

        Parameters
        ----------
        user_id : str
            target user id
        username : str
            target username
        host : str, default=None
            Hosts with target users

        Returns
        -------
        UserDetailed
            user information
        """

        field = remove_dict_empty({"userId": user_id, "username": username, "host": host})
        data = await self.__session.request(
            Route("POST", "/api/users/show"), json=field, auth=True, lower=True
        )
        return UserDetailed(data, client=self.__client)

    async def fetch(
        self,
        user_id: str | None = None,
        username: str | None = None,
        host: str | None = None,
    ) -> UserDetailed:
        """
        Retrieve the latest user information using the target user ID or username.
        If you do not need the latest information, you should basically use the `get` method.
        This method accesses the server each time,
        which may increase the number of server accesses.

        Parameters
        ----------
        user_id : str
            target user id
        username : str
            target username
        host : str, default=None
            Hosts with target users

        Returns
        -------
        UserDetailed
            ユーザー情報
        """
        return await self.get(user_id=user_id, username=username, host=host, cache_override=True)

    async def get_notes(
        self,
        user_id: str | None = None,
        include_replies: bool = True,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        since_date: int = 0,
        until_date: int = 0,
        include_my_renotes: bool = True,
        with_files: bool = False,
        file_type: Optional[list[str]] = None,
        exclude_nsfw: bool = True,
        get_all: bool = False,
    ) -> AsyncGenerator[Note, None]:
        if check_multi_arg(user_id, self.__user) is False:
            raise ParameterError("missing required argument: user_id", user_id, self.__user)

        user_id = user_id or self.__user and self.__user.id
        data = {
            "userId": user_id,
            "includeReplies": include_replies,
            "limit": limit,
            "sinceId": since_id,
            "untilId": until_id,
            "sinceDate": since_date,
            "untilDate": until_date,
            "includeMyRenotes": include_my_renotes,
            "withFiles": with_files,
            "fileType": file_type,
            "excludeNsfw": exclude_nsfw,
        }

        if get_all:
            data["limit"] = 100
            limit = 100

        pagination = Pagination[INote](
            self.__session, Route("POST", "/api/users/notes"), json=data, limit=limit
        )

        while True:
            res_notes = await pagination.next()
            for note in res_notes:
                yield Note(note, client=self.__client)
            if get_all is False or pagination.is_final:
                break

    def get_mention(self, user: Optional[LiteUser] = None) -> str:
        """
        Get mention name of user.

        Parameters
        ----------
        user : Optional[User], default=None
            The object of the user whose mentions you want to retrieve

        Returns
        -------
        str
            メンション
        """

        user = user or self.__user

        if user is None:
            raise NotExistRequiredData("Required parameters: user")
        return f"@{user.username}@{user.host}" if user.instance else f"@{user.username}"

    @overload
    async def search(
        self,
        query: str,
        limit: int = 100,
        offset: int = 0,
        origin: Literal["local", "remote", "combined"] = "combined",
        detail: Literal[False] = ...,
        *,
        get_all: bool = False,
    ) -> AsyncGenerator[LiteUser, None]:
        ...

    @overload
    async def search(
        self,
        query: str,
        limit: int = 100,
        offset: int = 0,
        origin: Literal["local", "remote", "combined"] = "combined",
        detail: Literal[True] = True,
        *,
        get_all: bool = False,
    ) -> AsyncGenerator[UserDetailed, None]:
        ...

    async def search(
        self,
        query: str,
        limit: int = 100,
        offset: int = 0,
        origin: Literal["local", "remote", "combined"] = "combined",
        detail: Literal[True, False] = True,
        *,
        get_all: bool = False,
    ) -> AsyncGenerator[UserDetailed | LiteUser, None]:
        """
        Search users by keyword.

        Parameters
        ----------
        query : str
            Keyword to search.
        limit : int, default=100
            The maximum number of users to return.
        offset : int, default=0
            The number of users to skip.
        origin : Literal['local', 'remote', 'combined'], default='combined'
            The origin of users to search.
        detail : Literal[True, False], default=True
            Whether to return detailed user information.
        get_all : bool, default=False
            Whether to return all users.

        Returns
        -------
        AsyncGenerator[Union[LiteUser, UserDetailed], None]
            A AsyncGenerator of users.
        """

        if limit > 100:
            raise ParameterError("limit は100以下である必要があります")

        if get_all:
            limit = 100

        body = remove_dict_empty(
            {"query": query, "limit": limit, "offset": offset, "origin": origin, "detail": detail}
        )

        if detail:
            pagination = Pagination[IUserDetailed](
                self.__session,
                Route("POST", "/api/users/search"),
                json=body,
                pagination_type="count",
            )
            iterator = pagination_iterator(
                pagination, get_all, model=UserDetailed, client=self.__client
            )
        else:
            pagination = Pagination[ILiteUser](
                self.__session,
                Route("POST", "/api/users/search"),
                json=body,
                pagination_type="count",
            )

            iterator = pagination_iterator(
                pagination, get_all=get_all, model=LiteUser, client=self.__client
            )
        async for user in iterator:
            yield user

    async def search_by_username_and_host(
        self,
        username: str,
        host: str,
        limit: int = 100,
        detail: bool = True,
    ) -> list[UserDetailed | LiteUser]:
        """
        Search users by username and host.

        Parameters
        ----------
        username : str
            Username of user.
        host : str
            Host of user.
        limit : int, default=100
            The maximum number of users to return.
        detail : bool, default=True
            Weather to get detailed user information.

        Returns
        -------
        list[UserDetailed | LiteUser]
            A list of users.
        """

        if limit > 100:
            raise ParameterError("limit は100以下である必要があります")

        body = remove_dict_empty(
            {"username": username, "host": host, "limit": limit, "detail": detail}
        )
        res = await self.__session.request(
            Route("POST", "/api/users/search-by-username-and-host"),
            lower=True,
            auth=True,
            json=body,
        )
        return [
            UserDetailed(user, client=self.__client)
            if detail
            else LiteUser(user, client=self.__client)
            for user in res
        ]

    async def get_achievements(self, user_id: str | None = None) -> list[Achievement]:
        """Get achievements of user."""
        user_id = user_id or self.__user and self.__user.id

        if not user_id:
            raise ParameterError("user_id is required")

        data = {
            "userId": user_id,
        }
        res = await self.__session.request(
            Route("POST", "/api/users/achievements"),
            json=data,
            auth=True,
            lower=True,
        )
        return [Achievement(i) for i in res]

    async def get_clips(
        self,
        user_id: str | None = None,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        get_all: bool = False,
    ):
        user_id = user_id or self.__user and self.__user.id

        if not user_id:
            raise ParameterError("user_id is required")

        if limit > 100:
            raise ParameterError("limit must be less than 100")

        if get_all:
            limit = 100

        body = {"userId": user_id, "limit": limit, "sinceId": since_id, "untilId": until_id}

        pagination = Pagination[IClip](
            self.__session, Route("POST", "/api/users/clips"), json=body, auth=True
        )

        while True:
            clips: list[IClip] = await pagination.next()
            for clip in clips:
                yield Clip(clip, client=self.__client)
            if get_all is False or pagination.is_final:
                break

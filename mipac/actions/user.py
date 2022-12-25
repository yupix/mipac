from __future__ import annotations

from typing import TYPE_CHECKING, Literal, Optional, AsyncIterator

from mipac.errors.base import NotExistRequiredData, ParameterError
from mipac.http import HTTPClient, Route
from mipac.models.user import UserDetailed, LiteUser
from mipac.util import cache, check_multi_arg, remove_dict_empty

if TYPE_CHECKING:
    from mipac.manager.client import ClientActions
    from mipac.models.note import Note

__all__ = ['UserActions']


class UserActions:
    def __init__(
        self,
        session: HTTPClient,
        client: ClientActions,
        user: Optional[LiteUser] = None,
    ):
        self.__session: HTTPClient = session
        self.__user: Optional[LiteUser] = user
        self.__client: ClientActions = client

    async def get_me(self) -> UserDetailed:
        """
        ログインしているユーザーの情報を取得します
        """

        res = await self.__session.request(Route('POST', '/api/i'), auth=True)
        return UserDetailed(res, client=self.__client)  # TODO: 自分用のクラスに変更する

    def get_profile_link(
        self,
        external: bool = True,
        protocol: Literal['http', 'https'] = 'https',
    ):
        if not self.__user:
            return None
        host = (
            f'{protocol}://{self.__user.host}'
            if external and self.__user.host
            else self.__session._url
        )
        path = (
            f'/@{self.__user.username}'
            if external
            else f'/{self.__user.action.get_mention()}'
        )
        return host + path

    @cache(group='get_user')
    async def get(
        self,
        user_id: Optional[str] = None,
        username: Optional[str] = None,
        host: Optional[str] = None,
    ) -> UserDetailed:
        """
        ユーザーのプロフィールを取得します。一度のみサーバーにアクセスしキャッシュをその後は使います。
        fetch_userを使った場合はキャッシュが廃棄され再度サーバーにアクセスします。

        Parameters
        ----------
        user_id : str
            取得したいユーザーのユーザーID
        username : str
            取得したいユーザーのユーザー名
        host : str, default=None
            取得したいユーザーがいるインスタンスのhost

        Returns
        -------
        UserDetailed
            ユーザー情報
        """

        field = remove_dict_empty(
            {'userId': user_id, 'username': username, 'host': host}
        )
        data = await self.__session.request(
            Route('POST', '/api/users/show'), json=field, auth=True, lower=True
        )
        return UserDetailed(data, client=self.__client)

    @cache
    async def fetch(
        self,
        user_id: Optional[str] = None,
        username: Optional[str] = None,
        host: Optional[str] = None,
    ) -> UserDetailed:
        """
        サーバーにアクセスし、ユーザーのプロフィールを取得します。基本的には get_userをお使いください。

        Parameters
        ----------
        user_id : str
            取得したいユーザーのユーザーID
        username : str
            取得したいユーザーのユーザー名
        host : str, default=None
            取得したいユーザーがいるインスタンスのhost

        Returns
        -------
        UserDetailed
            ユーザー情報
        """
        if not check_multi_arg(user_id, username):
            raise ParameterError('user_id, usernameどちらかは必須です')

        field = remove_dict_empty(
            {'userId': user_id, 'username': username, 'host': host}
        )
        data = await self.__session.request(
            Route('POST', '/api/users/show'), json=field, auth=True, lower=True
        )
        return UserDetailed(data, client=self.__client)

    async def get_notes(
        self,
        user_id: Optional[str] = None,
        include_replies: bool = True,
        limit: int = 10,
        since_id: Optional[str] = None,
        until_id: Optional[str] = None,
        since_date: int = 0,
        until_date: int = 0,
        include_my_renotes: bool = True,
        with_files: bool = False,
        file_type: Optional[list[str]] = None,
        exclude_nsfw: bool = True,
    ) -> list[Note]:

        if check_multi_arg(user_id, self.__user):
            raise ParameterError('user_idがありません')

        user_id = user_id or self.__user and self.__user.id
        data = {
            'userId': user_id,
            'includeReplies': include_replies,
            'limit': limit,
            'sinceId': since_id,
            'untilId': until_id,
            'sinceDate': since_date,
            'untilDate': until_date,
            'includeMyRenotes': include_my_renotes,
            'withFiles': with_files,
            'fileType': file_type,
            'excludeNsfw': exclude_nsfw,
        }
        res = await self.__session.request(
            Route('POST', '/api/users/notes'), json=data, auth=True, lower=True
        )
        return [Note(i, client=self.__client) for i in res]

    def get_mention(self, user: Optional[LiteUser] = None) -> str:
        """
        Get mention name of user.

        Parameters
        ----------
        user : Optional[User], default=None
            メンションを取得したいユーザーのオブジェクト

        Returns
        -------
        str
            メンション
        """

        user = user or self.__user

        if user is None:
            raise NotExistRequiredData('Required parameters: user')
        return (
            f'@{user.username}@{user.host}'
            if user.instance
            else f'@{user.username}'
        )

    async def search(
        self,
        query: str,
        limit: int = 100,
        offset: int = 0,
        origin: Literal['local', 'remote', 'combined'] = 'combined',
        detail: bool = True,
        *,
        all: bool = False
    ) -> AsyncIterator[UserDetailed | LiteUser]:
        """
        ユーザーを検索します。

        Parameters
        ----------
        query : str
            検索クエリ
        limit : int, default=100
            取得するユーザーの数
        offset : int, default=0
            取得するユーザーのオフセット
        origin : Literal['local', 'remote', 'combined'], default='combined'
            取得するユーザーのインスタンスの種類
        detail : bool, default=True
            ユーザーの詳細情報を取得するかどうか
        all : bool, default=False
            全てのユーザーを取得するかどうか

        Returns
        -------
        AsyncIterator[UserDetailed | LiteUser]
            ユーザーのリスト
        """

        if limit > 100:
            raise ParameterError('limit は100以下である必要があります')

        async def request(body) -> list[UserDetailed | LiteUser]:
            res = await self.__session.request(
                Route('POST', '/api/users/search'), lower=True, auth=True, json=body
            )
            return [UserDetailed(user, client=self.__client) if detail
                    else LiteUser(user, client=self.__client) for user in res]

        body = remove_dict_empty(
            {
                'query': query,
                'limit': limit,
                'offset': offset,
                'origin': origin,
                'detail': detail,
            }
        )

        if all:
            body['limit'] = 100
        first_req = await request(body)

        for user in first_req:
            yield user

        if all and len(first_req) == 100:
            times = 1
            while True:
                body['offset'] = times * 100
                res = await request(body)
                if len(res) <= 100:
                    for user in res:
                        yield user
                if len(res) == 0:
                    break
                times += 1

    async def search_by_username_and_host(
        self,
        username: str,
        host: str,
        limit: int = 100,
        detail: bool = True,
    ) -> list[UserDetailed | LiteUser]:
        """
        ユーザーをユーザー名とインスタンスのホストで検索します。

        Parameters
        ----------
        username : str
            ユーザー名
        host : str
            インスタンスのホスト
        limit : int, default=100
            取得するユーザーの数
        detail : bool, default=True
            ユーザーの詳細情報を取得するかどうか

        Returns
        -------
        list[UserDetailed | LiteUser]
            ユーザーのリスト
        """

        if limit > 100:
            raise ParameterError('limit は100以下である必要があります')

        body = remove_dict_empty(
            {
                'username': username,
                'host': host,
                'limit': limit,
                'detail': detail,
            }
        )
        res = await self.__session.request(
            Route('POST', '/api/users/search-by-username-and-host'), lower=True, auth=True, json=body
        )
        return [UserDetailed(user, client=self.__client) if detail
                else LiteUser(user, client=self.__client) for user in res]

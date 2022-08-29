from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Literal, Optional

from typing_extensions import Self

from mipac.core.models.poll import RawPoll
from mipac.exception import NotExistRequiredData
from mipac.models.lite.user import UserLite

if TYPE_CHECKING:
    from mipac.actions.note import NoteActions
    from mipac.manager.client import ClientActions
    from mipac.models.user import UserDetailed
    from mipac.types.drive import IDriveFile
    from mipac.types.emoji import ICustomEmojiLite
    from mipac.types.note import INote, INoteReaction, IPoll

__all__ = (
    'Note',
    'Poll',
    'Follow',
    'Header',
    'NoteReaction',
)


class Follow:
    def __init__(self, data):
        self.id: Optional[str] = data.get('id')
        self.created_at: Optional[datetime] = datetime.strptime(
            data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ'
        ) if data.get('created_at') else None
        self.type: Optional[str] = data.get('type')
        self.user: Optional[UserDetailed] = data.get('user')

    async def follow(self) -> tuple[bool, Optional[str]]:
        """
        ユーザーをフォローします
        Returns
        -------
        bool
            成功ならTrue, 失敗ならFalse
        str
            実行に失敗した際のエラーコード
        """

        if self.id:
            raise NotExistRequiredData('user_idがありません')
        return await self._state.user.follow.add(user_id=self.id)

    async def unfollow(self, user_id: Optional[str] = None) -> bool:
        """
        与えられたIDのユーザーのフォローを解除します

        Parameters
        ----------
        user_id : Optional[str] = None
            フォローを解除したいユーザーのID

        Returns
        -------
        status
            成功ならTrue, 失敗ならFalse
        """

        if user_id is None:
            user_id = self.user.id
        return await self._state.user.follow.remove(user_id)


class Header:
    def __init__(self, data):
        self.id = data.get('id')
        self.type = data.get('type')


class Poll:
    def __init__(self, raw_data: RawPoll):
        self.__raw_data = raw_data

    @property
    def multiple(self) -> bool | None:
        return self.__raw_data.multiple

    @property
    def expires_at(self) -> Optional[int]:
        return self.__raw_data.expires_at

    @property
    def choices(self):
        return self.__raw_data.choices

    @property
    def expired_after(self) -> Optional[int]:
        return self.__raw_data.expired_after


class NoteReaction:
    """
    Attributes
    ----------
    id : Optional[str], default=None
    created_at : Optional[datetime], default=None
    type : Optional[str], default=None
    user : Optional[RawUser], default=None
    """

    __slots__ = (
        '__reaction',
    )

    def __init__(self, reaction: INoteReaction):
        self.__reaction: INoteReaction = reaction

    @property
    def id(self) -> str | None:
        return self.__reaction['id']

    @property
    def created_at(self) -> datetime | None:
        return (
            datetime.strptime(
                self.__reaction['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ'
            )
            if 'created_at' in self.__reaction
            else None
        )

    @property
    def type(self) -> str | None:
        return self.__reaction['type']

    @property
    def user(self) -> UserLite:
        return UserLite(self.__reaction['user'])


class Note:
    """
    Noteモデル

    Parameters
    ----------
    note: INote
        アクションを持たないNoteクラス
    client: ClientActions
    """

    def __init__(self, note: INote, client: ClientActions):
        self.__note = note
        self._client: ClientActions = client

    @property
    def id(self) -> str:
        """
        ユーザーのID

        Returns
        -------
        str
            ユーザーのID
        """
        return self.__note['id']

    @property
    def created_at(self) -> datetime:
        return datetime.strptime(
            self.__note['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ'
        )

    @property
    def content(self) -> str | None:
        return self.__note['text']

    @property
    def cw(self) -> str | None:
        return self.__note['cw']

    @property
    def user_id(self) -> str:
        return self.__note['user_id']

    @property
    def author(self) -> UserLite:
        return UserLite(self.__note['user'])

    @property
    def reply_id(self) -> str:
        return self.__note['reply_id']

    @property
    def renote_id(self) -> str:
        return self.__note['renote_id']

    @property
    def files(self) -> list[IDriveFile]:  # TODO: モデルに
        return self.__note['files']

    @property
    def file_ids(self) -> list[str]:
        return self.__note['file_ids']

    @property
    def visibility(
        self,
    ) -> Literal['public', 'home', 'followers', 'specified']:
        return self.__note['visibility']

    @property
    def reactions(self) -> dict[str, int]:
        return self.__note['reactions']

    @property
    def renote_count(self) -> int:
        return self.__note['renote_count']

    @property
    def replies_count(self) -> int:
        return self.__note['replies_count']

    @property
    def emojis(self) -> list[ICustomEmojiLite]:  # TODO: モデルに
        return self.__note['emojis']

    @property
    def renote(self) -> Self | None:
        return (
            Note(note=self.__note['renote'], client=self._client)
            if 'renote' in self.__note
            else None
        )

    @property
    def reply(self) -> Self | None:
        return (
            Note(note=self.__note['renote'], client=self._client)
            if 'renote' in self.__note
            else None
        )

    @property
    def visible_user_ids(self) -> list[str]:
        return (
            self.__note['visible_user_ids']
            if 'visible_user_ids' in self.__note
            else []
        )

    @property
    def local_only(self) -> bool:
        return (
            self.__note['local_only'] if 'local_only' in self.__note else False
        )

    @property
    def my_reaction(self) -> str | None:
        return (
            self.__note['my_reaction']
            if 'my_reaction' in self.__note
            else None
        )

    @property
    def uri(self) -> str | None:
        return self.__note['uri'] if 'uri' in self.__note else None

    @property
    def url(self) -> str | None:
        return self.__note['url'] if 'url' in self.__note else None

    @property
    def is_hidden(self) -> bool:
        return (
            self.__note['is_hidden'] if 'is_hidden' in self.__note else False
        )

    @property
    def poll(self) -> IPoll | None:
        return self.__note['poll'] if 'poll' in self.__note else None

    @property
    def action(self) -> NoteActions:
        """
        ノートに対するアクション

        Returns
        -------
        NoteActions
        """
        return self._client._create_note_instance(self.id).action

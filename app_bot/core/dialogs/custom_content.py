from aiogram.types import InlineKeyboardButton
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import ScrollingGroup, Group, Keyboard
from core.utils.texts import _
from itertools import zip_longest, chain
from typing import List, Optional
from aiogram_dialog.widgets.common import WhenCondition


class CustomPager(ScrollingGroup):
    async def _render_page(
            self,
            page: int,
            keyboard: list[list[InlineKeyboardButton]],
    ) -> list[list[InlineKeyboardButton]]:
        pages = self._get_page_count(keyboard)
        last_page = pages - 1
        current_page = min(last_page, page)
        page_offset = current_page * self.height

        return keyboard[page_offset: page_offset + self.height]

    async def _render_pager(
            self,
            pages: int,
            manager: DialogManager,
    ):
        if self.hide_pager:
            return []
        if pages == 0 or (pages == 1 and self.hide_on_single_page):
            return []

        last_page = pages - 1
        current_page = min(last_page, await self.get_page(manager))
        next_page = min(last_page, current_page + 1)
        prev_page = max(0, current_page - 1)

        if current_page == pages - 1:
            next_page = 0
        elif current_page == 0:
            prev_page = pages - 1

        return [
            [
                InlineKeyboardButton(
                    text=_('BACK_PAGER'),
                    callback_data=self._item_callback_data(prev_page),
                ),
                InlineKeyboardButton(
                    text=_('FORWARD_PAGER'),
                    callback_data=self._item_callback_data(next_page),
                ),
            ],
        ]


class Multicolumn(Group):
    def __init__(self, *buttons: Keyboard, id: Optional[str] = None,
                 when: WhenCondition = None):
        super().__init__(*buttons, id=id, when=when)

    async def _render_keyboard(
            self, data, manager: DialogManager,
    ) -> List[List[InlineKeyboardButton]]:
        columns = []
        for button in self.buttons:
            subkbd = await button.render_keyboard(data, manager)
            columns.append(list(chain.from_iterable(subkbd)))
        return [
            list(filter(None, row))
            for row in zip_longest(*columns)
        ]

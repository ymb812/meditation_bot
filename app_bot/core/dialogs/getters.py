from aiogram_dialog import DialogManager
from aiogram.enums import ContentType
from aiogram_dialog.api.entities import MediaAttachment
from core.database.models import Post, Card


async def get_input_data(dialog_manager: DialogManager, **kwargs):
    return {'data': dialog_manager.dialog_data}


async def get_reg_states_content(dialog_manager: DialogManager, **kwargs):
    post_1 = await Post.get(id=1003)
    post_2 = await Post.get(id=1004)
    post_3 = await Post.get(id=1005)

    media_content_1, media_content_2, media_content_3 = None, None, None
    if post_1.photo_file_id:
        media_content_1 = MediaAttachment(ContentType.PHOTO, url=post_1.photo_file_id)
    if post_2.photo_file_id:
        media_content_2 = MediaAttachment(ContentType.PHOTO, url=post_1.photo_file_id)
    if post_3.photo_file_id:
        media_content_3 = MediaAttachment(ContentType.PHOTO, url=post_1.photo_file_id)

    return {
        'msg_text': [post_1.text, post_2.text, post_3.text],
        'media_content_1': media_content_1,
        'media_content_2': media_content_2,
        'media_content_3': media_content_3,
    }


async def get_main_media_content(dialog_manager: DialogManager, **kwargs):
    post_1 = await Post.get(id=1006)
    post_2 = await Post.get(id=1007)
    post_3 = await Post.get(id=1008)
    post_4 = await Post.get(id=1009)
    post_5 = await Post.get(id=1010)

    media_content_1, media_content_2, media_content_3, media_content_4, media_content_5 = None, None, None, None, None
    if post_1.photo_file_id:
        media_content_1 = MediaAttachment(ContentType.PHOTO, url=post_1.photo_file_id)
    if post_2.photo_file_id:
        media_content_2 = MediaAttachment(ContentType.PHOTO, url=post_2.photo_file_id)
    if post_3.photo_file_id:
        media_content_3 = MediaAttachment(ContentType.PHOTO, url=post_3.photo_file_id)
    if post_4.photo_file_id:
        media_content_4 = MediaAttachment(ContentType.PHOTO, url=post_4.photo_file_id)
    if post_5.photo_file_id:
        media_content_5 = MediaAttachment(ContentType.PHOTO, url=post_5.photo_file_id)

    return {
        'msg_text': [post_1.text, post_2.text, post_3.text, post_4.text, post_5.text],
        'media_content_1': media_content_1,
        'media_content_2': media_content_2,
        'media_content_3': media_content_3,
        'media_content_4': media_content_4,
        'media_content_5': media_content_5,
        'cards': await Card.all().order_by('order_priority'),
    }


async def get_card(dialog_manager: DialogManager, **kwargs):
    card = await Card.get(id=dialog_manager.dialog_data['card_id'])
    media_content = MediaAttachment(ContentType.PHOTO, url=card.photo_file_id) if card.photo_file_id else None

    return {
        'msg_text': card.text,
        'media_content': media_content,
    }

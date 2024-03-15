import asyncio
import logging
from datetime import datetime
from aiogram import Bot, types
from aiogram.utils.i18n import I18n
from core.database import init
from core.database.models import User, Dispatcher, Post
from settings import settings


logger = logging.getLogger(__name__)
bot = Bot(settings.bot_token.get_secret_value(), parse_mode='HTML')
i18n = I18n(path='locales', default_locale='ru', domain='messages')
i18n.set_current(i18n)


class Broadcaster(object):
    @staticmethod
    async def __send_mailing_msg_to_user(user_id: int, message: types.Message, bot: Bot):
        if message.photo:
            await bot.send_photo(chat_id=user_id, photo=message.photo[-1].file_id, caption=message.caption)

        elif message.text:
            await bot.send_message(chat_id=user_id, text=message.text)


    @staticmethod
    async def __send_content_message(post: Post, user_id: int):
        try:
            if not post.photo_file_id and not post.video_file_id and not post.sticker_file_id \
                    and not post.video_note_id and not post.document_file_id and post.text:
                await bot.send_message(chat_id=user_id, text=post.text)

            elif post.sticker_file_id:  # sticker
                await bot.send_sticker(chat_id=user_id, sticker=post.sticker_file_id)

            elif post.photo_file_id:  # photo
                await bot.send_photo(chat_id=user_id, photo=post.photo_file_id, caption=post.text)

            elif post.video_file_id:  # video
                await bot.send_video(chat_id=user_id, video=post.video_file_id, caption=post.text)

            elif post.video_note_id:  # video_note
                if post.text:
                    await bot.send_message(chat_id=user_id, text=post.text)
                await bot.send_video_note(chat_id=user_id, video_note=post.video_note_id)

            elif post.document_file_id:  # document
                await bot.send_document(chat_id=user_id, document=post.document_file_id, caption=post.text)
            else:
                logger.error(f'Unexpected content type: post_id={post.id}')

        except Exception as e:
            logger.error(f'Content sending error: user_id={user_id}, post_id={post.id}', exc_info=e)


    @classmethod
    async def send_content_to_users(
            cls,
            bot: Bot,
            is_for_registered_only: bool = True,
            is_for_all_users: bool = False,
            message: types.Message | None = None,
            broadcaster_post: Post | None = None
    ):
        sent_amount = 0

        if is_for_all_users:
            users_ids = await User.all()
        else:
            users_ids = await User.filter(is_registered=is_for_registered_only).all()

        if not users_ids:
            return sent_amount

        for i in range(0, len(users_ids), settings.mailing_batch_size):
            user_batch = users_ids[i:i + settings.mailing_batch_size]
            for user in user_batch:
                # send mailing from admin panel
                if broadcaster_post:
                    try:
                        await cls.__send_content_message(post=broadcaster_post, user_id=user.user_id)
                    except Exception as e:
                        logger.error(f'Error in mailing from admin panel, user_id={user.user_id}', exc_info=e)

                # send mailing via /send
                else:
                    try:
                        await cls.__send_mailing_msg_to_user(user_id=user.user_id, message=message, bot=bot)
                        sent_amount += 1
                    except Exception as e:
                        logger.error(f'Error in mailing via /send, user_id={user.user_id}', exc_info=e)

        return sent_amount


    # send mailing from admin panel
    @classmethod
    async def order_work(cls, order: Dispatcher):
        try:
            post = await Post.filter(id=(await order.post).id).first()
        except Exception as e:
            logger.error(f'Get post error', exc_info=e)
            return

        # sending
        if order.user_id:  # for notifications
            try:
                await cls.__send_content_message(post=post, user_id=order.user_id)
            except Exception as e:
                logger.error(f'Error in mailing from admin panel, user_id={order.user_id}', exc_info=e)

        else:  # mailing
            await cls.send_content_to_users(
                bot=bot,
                broadcaster_post=post,
                is_for_registered_only=order.is_for_registered_only,
                is_for_all_users=order.is_for_all_users,
            )

        # delete order
        try:
            await Dispatcher.filter(id=order.id).delete()
        except Exception as e:
            logger.critical(f'Delete order error', exc_info=e)
            return

        logger.info(f'order_id={order.id} has been sent to users')


    @classmethod
    async def start_event_loop(cls):
        logger.info('Broadcaster started')
        while True:
            try:
                active_orders = await Dispatcher.filter(send_at__lte=datetime.now()).all()
                logger.info(f'active_orders: {active_orders}')

            except Exception as e:
                logger.error(f'get active orders error', exc_info=e)
                continue

            index = 0
            futures = []
            try:
                if active_orders:
                    async with asyncio.TaskGroup() as tg:
                        while index < len(active_orders) or futures:
                            # start order work
                            if (len(futures) < settings.mailing_batch_size) and (index < len(active_orders)):
                                futures.append(tg.create_task(cls.order_work(active_orders[index])))
                                logger.info(
                                    f'Create order: '
                                    f'order_id={active_orders[index].id} '
                                    f'post_id={active_orders[index].post_id} '
                                )
                                index += 1

                            ind_x = 0
                            for i, _f in enumerate(reversed(futures)):
                                if _f.done():
                                    _f.cancel()
                                    del futures[len(futures) - i - 1 + ind_x]
                                    ind_x += 1
                            await asyncio.sleep(0.5)
                await asyncio.sleep(0.5)

            except Exception as e:
                logger.error(f'Broadcaster main loop async creating tasks error', exc_info=e)
                continue

            await asyncio.sleep(settings.broadcaster_sleep)


async def main():
    await init()
    await Broadcaster.start_event_loop()


if __name__ == '__main__':
    asyncio.run(main())

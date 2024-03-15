from aiogram.utils.i18n import I18n, FSMI18nMiddleware


i18n = FSMI18nMiddleware(I18n(path='locales', default_locale='ru', domain='messages'))

from aiogram import Dispatcher

from .is_admin import IsAdminFilter

def register_all_filters(dp: Dispatcher):
    # сюда прописывать фильтры
    filters = (
        IsAdminFilter,
    )

    for fltr in filters:
        dp.filters_factory.bind(fltr)

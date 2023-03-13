from aiogram.utils import executor
from Handlers.admin import register_admin_handlers
from Handlers.client import register_client_handlers
from Handlers.general import register_general_handlers
from Handlers.create_bot import dp


async def on_startup(_) -> None:
    print('Бот вышел в онлайн')
    return


def main():
    register_admin_handlers(dp)
    register_client_handlers(dp)
    register_general_handlers(dp)
    executor.start_polling(dp, skip_updates=True,
                           on_startup=on_startup)


if __name__ == "__main__":
    main()

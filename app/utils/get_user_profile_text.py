from aiogram.types import Message, CallbackQuery

from app.database.models import User


def get_user_profile_text(message: Message | None = None, callback: CallbackQuery | None = None):
    if message:
        user: User = User.get(
            telegram_id=message.from_user.id
        )

    if callback:
        user: User = User.get(
            telegram_id=callback.from_user.id
        )

    if message:
        match user.lang:
            case "RU":
                return f"Данные пользователя <b>{message.from_user.first_name}</b> 👤" + \
                    f"\n\n<em>ID</em>: <code><b>{user.telegram_id}</b></code> 🪪" + \
                    f"\n<em>Баланс</em>: <b>{user.balance} RUB</b> 💸" + \
                    f"\n<em>Дата регистрации</em>: <b>{user.date}</b> 🗓" + \
                    f"\n<em>Подписка</em>: <b>{'Активна ✅' if user.subscribe_status else 'Не активна ❌'}</b>" + \
                    f"\n<em>Реферальная скидка</em>: <b>{user.discount}%</b>"

            case "ENG":
                return f"User data <b>{message.from_user.first_name}</b> 👤" + \
                    f"\n\n<em>ID</em>: <code><b>{user.telegram_id}</b></code> 🪪" + \
                    f"\n<em>Balance</em>: <b>{user.balance} RUB</b> 💸" + \
                    f"\n<em>Registration date</em>: <b>{user.date}</b> 🗓" + \
                    f"\n<em>Subscribe</em>: <b>{'Active ✅' if user.subscribe_status else 'Inactive ❌'}</b>" + \
                    f"\n<em>Referral discount</em>: <b>{user.discount}%</b>"

    if callback:
        match user.lang:
            case "RU":
                return f"Данные пользователя <b>{callback.from_user.first_name}</b> 👤" + \
                    f"\n\n<em>ID</em>: <code><b>{user.telegram_id}</b></code> 🪪" + \
                    f"\n<em>Баланс</em>: <b>{user.balance} RUB</b> 💸" + \
                    f"\n<em>Дата регистрации</em>: <b>{user.date}</b> 🗓" + \
                    f"\n<em>Подписка</em>: <b>{'Активна ✅' if user.subscribe_status else 'Не активна ❌'}</b>" + \
                    f"\n<em>Реферальная скидка</em>: <b>{user.discount}%</b>"

            case "ENG":
                return f"User data <b>{callback.from_user.first_name}</b> 👤" + \
                    f"\n\n<em>ID</em>: <code><b>{user.telegram_id}</b></code> 🪪" + \
                    f"\n<em>Balance</em>: <b>{user.balance} RUB</b> 💸" + \
                    f"\n<em>Registration date</em>: <b>{user.date}</b> 🗓" + \
                    f"\n<em>Subscribe</em>: <b>{'Active ✅' if user.subscribe_status else 'Inactive ❌'}</b>" + \
                    f"\n<em>Referral discount</em>: <b>{user.discount}%</b>"    
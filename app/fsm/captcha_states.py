from aiogram.fsm.state import StatesGroup, State


class CaptchaStates(StatesGroup):
    captcha_text = State()
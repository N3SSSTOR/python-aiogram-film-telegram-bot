from aiogram.fsm.state import StatesGroup, State


class TokenStates(StatesGroup):
    token = State()
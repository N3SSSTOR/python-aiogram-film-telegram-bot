from aiogram.fsm.state import StatesGroup, State


class AdminStates(StatesGroup):
    send = State()
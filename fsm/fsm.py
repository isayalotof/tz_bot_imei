from aiogram.fsm.state import StatesGroup, State


class UserInWL(StatesGroup):
    waiting_for_the_imei = State()
    work_with_api = State()
    add_user = State()

class UserNotInWL(StatesGroup):
    denial_of_access = State()
from turtledemo.sorting_animate import instructions1

from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import fsm.fsm
from app import keyboards as kb
from tool.IMEI import real_check_imei
from tool.functions import is_user, check_imei, get_token, add_user

router = Router()

instruct = """ Инструкция по использованию API для проверки IMEI

 Эндпоинт
`POST /api/check-imei`

 Формат запроса
{
    "imei": "строка_IMEI",
    "token": "строка_токена"
}


## Параметры
- imei: (строка) IMEI-номер для проверки.
- token: (строка) Токен для авторизации.

## Ответы
- 200 OK:
    json
    {
        "status": "success",
        "imei": "результат_проверки"
    }
    

- 403 Forbidden: Неверный токен.
    json
    {
        "detail": "Unauthorized token"
    }
    

- 400 Bad Request: Неверный формат IMEI.
    json
    {
        "detail": "Invalid IMEI format"
    }"""

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f'Здравствуйте,{message.from_user.first_name.capitalize()}!')
    if is_user(message.from_user.id):
        await message.answer(f'У вас есть доступ. Пришлите мне ваш IMEI', reply_markup=kb.main)
        await state.set_state(fsm.fsm.UserInWL.waiting_for_the_imei)
    else:
        await message.answer(f'В доступе отказано.')
        await state.set_state(fsm.fsm.UserNotInWL.denial_of_access)


@router.message(F.text == 'Проверить IMEI')
async def imei(message: Message, state: FSMContext):
    if is_user(message.from_user.id):
        await message.answer(f'У вас есть доступ. Пришлите мне ваш IMEI', reply_markup=kb.main)
        await state.set_state(fsm.fsm.UserInWL.waiting_for_the_imei)
    else:
        await message.answer(f'В доступе отказано.')
        await state.set_state(fsm.fsm.UserNotInWL.denial_of_access)


@router.message(F.text == 'API')
async def imei(message: Message, state: FSMContext):
    if is_user(message.from_user.id):
        await message.answer(f'Ваш token - {get_token(message.from_user.id)}\n'
                                f'{instruct}', reply_markup=kb.main)
    else:
        await message.answer(f'В доступе отказано.')
        await state.set_state(fsm.fsm.UserNotInWL.denial_of_access)

@router.message(F.text == 'Добавить пользователя')
async def imei(message: Message, state: FSMContext):
    if is_user(message.from_user.id):
        await message.answer(f'Пришлите user_id пользователя, только цифры\n'
                                f'Можно узнать в @getmyid_bot')
        await state.set_state(fsm.fsm.UserInWL.add_user)
    else:
        await message.answer(f'В доступе отказано.')
        await state.set_state(fsm.fsm.UserNotInWL.denial_of_access)


@router.message(F.text, fsm.fsm.UserInWL.waiting_for_the_imei)
async def check_user_imei(message: Message):
    if check_imei(message.text):
        properties = real_check_imei(message.text)
        await message.answer(f'Имя устройства: {properties.get('deviceName', 'Unknown')}\n'
                             f'IMEI: {properties.get('imei', 'Unknown')}\n'
                             f'Серия: {properties.get('serial', 'Unknown')}\n'
                             f'Описание модели: {properties.get('modelDesc', 'Unknown')}\n'
                             )
        await message.answer_photo(f'{properties.get('image', '')}')
    else:
        await message.answer(f'Пришлите валидный IMEI')


@router.message(F.text, fsm.fsm.UserNotInWL.denial_of_access)
async def denial_access(message: Message):
    await message.answer('В доступе отказано.\n'
                         'Если вы получили доступ используйте /start')

@router.message(F.text, fsm.fsm.UserInWL.add_user)
async def denial_access(message: Message):
    if message.text.isdigit():
        add_user(int(message.text))
        await message.answer('Пользователь добавлен\n'
                             'Для выхода в главное меню используйте /start')
    else:
        await message.answer('Пришлите валидный id или используйте /start')

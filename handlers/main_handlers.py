from aiogram import types
from aiogram.utils.exceptions import MessageNotModified

from bot import (
    bot, Dispatcher, InlineKeyboards
)

from db import Database

db = Database()


async def start_command_handler(message: types.Message):
    """Срабатывает при старте бота"""
    await message.answer("Привет! Этот бот позволяет смотреть погоду. Главное меню:",
                         reply_markup=InlineKeyboards.main_keyboard())
    await message.delete()


async def profile(callback_query: types.CallbackQuery):
    """Профиль"""
    user_id = callback_query.from_user.id
    city = await db.get_city_by_user_id(user_id=user_id)

    try:
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text=f"""
<b>{callback_query.from_user.full_name}</b>, вот вот ваш профиль:

<i>Статус</i>: {'Не зарегистрирован ❌' if not city
                                    else 'Зарегистрирован ✅'}
                                    
<i>Город</i>: {'Отсутствует ❌' if not city else city}""",
                                    reply_markup=InlineKeyboards.transition_to_main_keyboard(),
                                    parse_mode="HTML")
    except MessageNotModified:
        await callback_query.answer('Вы уже нажали на кнопку Профиль')


async def return_to_main_menu(callback_query: types.CallbackQuery):
    try:
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text='Главное меню:',
            reply_markup=InlineKeyboards.main_keyboard()
        )
    except MessageNotModified:
        await callback_query.answer('Вы уже нажали на кнопку В главное меню')


async def transition_to_change_city(callback_query: types.CallbackQuery):
    """Срабатывает при выборе города"""
    try:
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text='🏙️ Выберите город из списка ниже: ',
            reply_markup=InlineKeyboards.first_30_cities_keyboard()
        )
    except MessageNotModified:
        await callback_query.answer('Вы уже нажали на кнопку')


async def change_city(callback_query: types.CallbackQuery):
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text="Ожидайте... 🔎",
        reply_markup=InlineKeyboards.transition_to_main_keyboard(),
    )
    city = callback_query.data[4:]
    try:
        result = await db.update_city_by_user_id(
            user_id=callback_query.from_user.id,
            new_city=city)
        if not result:
            await db.insert_user(user_id=callback_query.from_user.id, city=city)
    except Exception as exc:
        await callback_query.answer(f'Что-то пошло не так: {exc}')

    else:
        try:
            await bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text='Главное меню:',
                reply_markup=InlineKeyboards.main_keyboard()
            )
            await callback_query.answer('Город успешно установлен')
        except MessageNotModified:
            await callback_query.answer('Вы уже нажали на кнопку В главное меню')


async def transition_to_change_city2(callback_query: types.CallbackQuery):
    try:
        await bot.edit_message_reply_markup(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            reply_markup=InlineKeyboards.second_20_cities_keyboard()
        )
    except MessageNotModified:
        await callback_query.answer('Вы уже нажали на кнопку')


def register_main_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(start_command_handler, commands=['start'])
    dispatcher.register_callback_query_handler(profile, lambda cb: cb.data == 'profile')
    dispatcher.register_callback_query_handler(return_to_main_menu, lambda cb: cb.data == 'main_menu')
    dispatcher.register_callback_query_handler(transition_to_change_city, lambda cb: cb.data == 'change_city')
    dispatcher.register_callback_query_handler(change_city, lambda cb: cb.data.startswith('гор_'))
    dispatcher.register_callback_query_handler(transition_to_change_city2, lambda cb: cb.data == 'next_cities')
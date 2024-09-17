from datetime import datetime, timedelta

from aiogram import types
from aiogram.utils.exceptions import MessageNotModified

from bot import (
    bot, Dispatcher, InlineKeyboards
)

from db import Database, CitiesScheme

from weatherbitAPI import (
    WeatherAPI, WeatherHandler, WeatherSchemeData, WeatherSchemeDataToday, AirQualityScheme
)

from typing import Optional

db = Database()
api = WeatherAPI()

handler = WeatherHandler()


async def get_1_day_forecast(callback_query: types.CallbackQuery):
    user: Optional[CitiesScheme] = await db.get_user_info(callback_query.from_user.id)

    if not user:
        await callback_query.answer('Вы не выбрали город!', show_alert=True)
    else:
        current_date = datetime.now().date()
        date_2_day = (current_date + timedelta(days=2)).strftime("%Y-%m-%d")
        date_3_day = (current_date + timedelta(days=3)).strftime("%Y-%m-%d")
        date_4_day = (current_date + timedelta(days=4)).strftime("%Y-%m-%d")

        is_updated_today: bool = user.days_4_update_on.strftime("%Y-%m-%d") == current_date.strftime("%Y-%m-%d")

        if is_updated_today and user.weather_forecast_for_1_day:
            try:
                await bot.edit_message_text(
                    chat_id=callback_query.message.chat.id,
                    message_id=callback_query.message.message_id,
                    text=user.weather_forecast_for_1_day,
                    reply_markup=InlineKeyboards.change_days_forecasts_keyboard(
                        day_2=2, day_3=3, day_4=4,
                        date_of_2_day=date_2_day, date_of_3_day=date_3_day, date_of_4_day=date_4_day
                    ),
                    parse_mode='HTML'
                )
            except MessageNotModified:
                await callback_query.answer('Вы уже нажали на кнопку')

        else:
            try:
                await bot.edit_message_text(
                    chat_id=callback_query.message.chat.id,
                    message_id=callback_query.message.message_id,
                    text="Ожидайте... 🔎",
                    reply_markup=InlineKeyboards.transition_to_main_keyboard(),
                )
            except MessageNotModified:
                await callback_query.answer('Вы уже нажали на кнопку')

            forecast_json = await api.get_4_days_forecasts(city=user.city)
            parsed_json = handler.parse_json_forecasts_for_4_days(forecast_json)

            weather: list[list[WeatherSchemeData]] = handler.get_4_days_forecasts(parsed_json).data

            days: list[str] = []

            for day in weather:
                day: list[WeatherSchemeData]

                lst = []

                for time in day:
                    lst.append([*time.weather.description.items()])
                lst = [sorted(sublist, key=lambda x: x[1], reverse=True) for sublist in lst]

                text_weather = f"""
<u><b>Число - {day[0].datetime[:10]}</b></u> 📆


<i><b>Ночь (с 00 по {day[0].datetime[-2:]})</b></i> 🌙
Направление ветра - {day[0].wind_cdir_full} 💨
Температура - {round(day[0].temp, 1)}°C 🌡
Кажущаяся температура - {round(day[0].app_temp, 1)}°C
Вероятность выпадения осадков - {day[0].pop}%
Давление - {round(day[0].pres * 0.75006)} мм рт. ст.
Относительная влажность воздуха - {day[0].rh}%
Облачность - {day[0].clouds}% ☁️
УФ-индекс - {day[0].uv}
<b>Статус погоды: 
{lst[0][0][0]} - {round(lst[0][0][1] * (100 / 6))}%
{f'{lst[0][1][0]} - {round(lst[0][1][1] * (100 / 6))}%' if len(lst[0]) > 1 else ''}</b>

<i><b>Утро (с 06 по {day[1].datetime[-2:]})</b></i> 🌅
Направление ветра - {day[1].wind_cdir_full} 💨
Температура - {round(day[1].temp, 1)}°C 🌡
Кажущаяся температура - {round(day[1].app_temp, 1)}°C
Вероятность выпадения осадков - {day[1].pop}%
Давление - {round(day[1].pres * 0.75006)} мм рт. ст.
Относительная влажность воздуха - {day[1].rh}%
Облачность - {day[1].clouds}% ☁️
УФ-индекс - {day[1].uv}
<b>Статус погоды: 
{lst[1][0][0]} - {round(lst[1][0][1] * (100 / 6))}%
{f'{lst[1][1][0]} - {round(lst[1][1][1] * (100 / 6))}%' if len(lst[1]) > 1 else ''}</b>
         
<i><b>День (с 12 по {day[2].datetime[-2:]})</b></i> 🌞
Направление ветра - {day[2].wind_cdir_full} 💨
Температура - {round(day[2].temp, 1)}°C 🌡
Кажущаяся температура - {round(day[2].app_temp, 1)}°C
Вероятность выпадения осадков - {day[2].pop}%
Давление - {round(day[2].pres * 0.75006)} мм рт. ст.
Относительная влажность воздуха - {day[2].rh}%
Облачность - {day[2].clouds}% ☁️
УФ-индекс - {day[2].uv}
<b>Статус погоды: 
{lst[2][0][0]} - {round(lst[2][0][1] * (100 / 6))}%
{f'{lst[2][1][0]} - {round(lst[2][1][1] * (100 / 6))}%' if len(lst[2]) > 1 else ''}</b>

<i><b>Вечер (с 18 по {day[3].datetime[-2:]})</b></i> 🌆
Направление ветра - {day[3].wind_cdir_full} 💨
Температура - {round(day[3].temp, 1)}°C 🌡
Кажущаяся температура - {round(day[3].app_temp, 1)}°C
Вероятность выпадения осадков - {day[3].pop}%
Давление - {round(day[3].pres * 0.75006)} мм рт. ст.
Относительная влажность воздуха - {day[3].rh}%
Облачность - {day[3].clouds}% ☁️
УФ-индекс - {day[3].uv}
<b>Статус погоды: 
{lst[3][0][0]} - {round(lst[3][0][1] * (100 / 6))}%
{f'{lst[3][1][0]} - {round(lst[3][1][1] * (100 / 6))}%' if len(lst[3]) > 1 else ''}</b>"""

                if not days:
                    try:
                        await bot.edit_message_text(
                            chat_id=callback_query.message.chat.id,
                            message_id=callback_query.message.message_id,
                            text=text_weather,
                            reply_markup=InlineKeyboards.change_days_forecasts_keyboard(
                                day_2=2, day_3=3, day_4=4,
                                date_of_2_day=date_2_day, date_of_3_day=date_3_day, date_of_4_day=date_4_day
                            ),
                            parse_mode="HTML"
                        )
                    except MessageNotModified:
                        await callback_query.answer('Вы уже нажали на кнопку')

                days.append(text_weather)

            await db.update_weather_info_forecasts_by_city(
                city=user.city,
                day1=days[0],
                day2=days[1],
                day3=days[2],
                day4=days[3]
            )


async def get_4_days_forecasts(callback_query: types.CallbackQuery):
    user: Optional[CitiesScheme] = await db.get_user_info(callback_query.from_user.id)

    if not user:
        try:
            await callback_query.answer('Неактуально...', show_alert=True)
            await bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text="Главное меню:  ",
                reply_markup=InlineKeyboards.main_keyboard(),
            )
        except MessageNotModified:
            await callback_query.answer('Вы уже нажали на кнопку')
    else:
        current_date = datetime.now().date()
        date_1_day = (current_date + timedelta(days=1)).strftime("%Y-%m-%d")
        date_2_day = (current_date + timedelta(days=2)).strftime("%Y-%m-%d")
        date_3_day = (current_date + timedelta(days=3)).strftime("%Y-%m-%d")
        date_4_day = (current_date + timedelta(days=4)).strftime("%Y-%m-%d")

        day = callback_query.data[0]

        data = {
            'day_1': 1,
            'day_2': 2,
            'day_3': 3,
            'day_4': 4,

            'date_of_1_day': date_1_day,
            'date_of_2_day': date_2_day,
            'date_of_3_day': date_3_day,
            'date_of_4_day': date_4_day,
        }

        del data[f'day_{day}']
        del data[f'date_of_{day}_day']

        is_updated_today = user.days_4_update_on.strftime("%Y-%m-%d") == current_date.strftime("%Y-%m-%d")

        if is_updated_today and user.weather_forecast_for_2_day:
            try:
                await bot.edit_message_text(
                    chat_id=callback_query.message.chat.id,
                    message_id=callback_query.message.message_id,
                    text=getattr(user, f'weather_forecast_for_{day}_day'),
                    reply_markup=InlineKeyboards.change_days_forecasts_keyboard(**data),
                    parse_mode='HTML'
                )
            except MessageNotModified:
                await callback_query.answer('Вы уже нажали на кнопку')

        else:
            try:
                await callback_query.answer('Неактуально...', show_alert=True)
                await bot.edit_message_text(
                    chat_id=callback_query.message.chat.id,
                    message_id=callback_query.message.message_id,
                    text="Главное меню:  ",
                    reply_markup=InlineKeyboards.main_keyboard(),
                )
            except MessageNotModified:
                await callback_query.answer('Вы уже нажали на кнопку')


async def get_today_forecast(callback_query: types.CallbackQuery):
    user: Optional[CitiesScheme] = await db.get_user_info(callback_query.from_user.id)

    if not user:
        await callback_query.answer('Вы не выбрали город!', show_alert=True)
    else:
        is_updated_now = user.today_update_on.strftime("%Y-%m-%d-%H") == datetime.now().strftime("%Y-%m-%d-%H")

        if is_updated_now and user.weather_info_today:
            try:
                await bot.edit_message_text(
                    chat_id=callback_query.message.chat.id,
                    message_id=callback_query.message.message_id,
                    text=user.weather_info_today,
                    reply_markup=InlineKeyboards.transition_to_main_keyboard(),
                    parse_mode='HTML'
                )
            except MessageNotModified:
                await callback_query.answer('Вы уже нажали на кнопку')

        else:
            try:
                await bot.edit_message_text(
                    chat_id=callback_query.message.chat.id,
                    message_id=callback_query.message.message_id,
                    text="Ожидайте... 🔎",
                    reply_markup=InlineKeyboards.transition_to_main_keyboard(),
                )

            except MessageNotModified:
                await callback_query.answer('Вы уже нажали на кнопку')

            else:
                try:
                    json = await api.get_weather_for_today(city=user.city)

                    data: WeatherSchemeDataToday = handler.parse_json_forecasts_for_today(json)

                    text = f"""
<i><b>Дата - {datetime.now().strftime("%Y-%m-%d  %H")} часов</b></i> 📆

Время восхода солнца - {data.sunrise} (UTC +3:00) 🌇
Время заката - {data.sunset} (UTC +3:00) 🏙

Давление - {round(data.pres * 0.75006)}

Скорость ветра - {data.wind_spd} м/с 💨
{f'Скорость порыва ветра - {data.gust} м/с' if data.gust else ''} 
Направление ветра - {data.wind_cdir_full}

Температура - {data.temp}°C 🌡
Кажущаяся температура - {data.app_temp}°C 

Относительная влажность воздуха - {data.rh} % 💧
Облачность - {data.clouds} % ☁️
Видимость - {data.vis} км 👁
УФ-индекс - {data.uv}
Индекс качества воздуха - {data.aqi}


<b>Статус: {data.weather.description}</b>"""

                    await bot.edit_message_text(
                        chat_id=callback_query.message.chat.id,
                        message_id=callback_query.message.message_id,
                        text=text,
                        reply_markup=InlineKeyboards.transition_to_main_keyboard(),
                        parse_mode='HTML'
                    )
                except MessageNotModified:
                    await callback_query.answer('Что-то пошло не так!')
                else:
                    await db.update_weather_info_today_by_city(
                        city=user.city,
                        new_weather_info_today=text
                    )


async def get_today_air_quality_forecast(callback_query: types.CallbackQuery):
    user: Optional[CitiesScheme] = await db.get_user_info(callback_query.from_user.id)

    if not user:
        await callback_query.answer('Вы не выбрали город!', show_alert=True)
    else:
        is_updated_now = user.air_quality_update_on.strftime("%Y-%m-%d") == datetime.now().strftime("%Y-%m-%d")

        if is_updated_now and user.weather_info_today:
            try:
                await bot.edit_message_text(
                    chat_id=callback_query.message.chat.id,
                    message_id=callback_query.message.message_id,
                    text=user.air_quality_today,
                    reply_markup=InlineKeyboards.transition_to_main_keyboard(),
                    parse_mode='HTML'
                )
            except MessageNotModified:
                await callback_query.answer('Вы уже нажали на кнопку')

        else:
            try:
                await bot.edit_message_text(
                    chat_id=callback_query.message.chat.id,
                    message_id=callback_query.message.message_id,
                    text="Ожидайте... 🔎",
                    reply_markup=InlineKeyboards.transition_to_main_keyboard(),
                )

            except MessageNotModified:
                await callback_query.answer('Вы уже нажали на кнопку')

            else:
                try:
                    json = await api.get_air_quality_for_today(city=user.city)

                    data: AirQualityScheme = handler.parse_json_air_quality_forecast_for_today(json)
                    levels = {0: 'Нет', 1: 'Низкий', 2: 'Умеренный', 3: 'Высокий', 4: 'Очень высокий'}

                    predominant_pollens = {
                        'Trees': 'Пыльца от цветения деревьев 🌳',
                        'Weeds': 'Пыльца от цветения различных видов сорняков 🌾',
                        'Molds': 'Споры плесени 🦠',
                        'Grasses': 'Пыльца от цветения трав 🌿'
                    }

                    text = f"""
<i><b>Дата - {datetime.now().strftime("%Y-%m-%d")}</b></i> 🕒

Индекс качества воздуха: {data.aqi} 🌬️


<b>Концентрация озона</b> (O3) на поверхности - {round(data.o3, 1)} (µг/м³) 🌫️

<b>Концентрация диоксида серы</b> (SO2) на поверхности - {round(data.so2, 1)} (µг/м³) 🏭

<b>Концентрация диоксида азота</b> (NO2) на поверхности - {round(data.no2, 1)} (µг/м³) 🚗

<b>Концентрация угарного газа (CO)</b> - {round(data.co, 1)} (µг/м³) 🔥


<b>Уровень пыльцы деревьев - {levels[data.pollen_level_tree]}</b> 🌳
<b>Уровень пыльцы трав - {levels[data.pollen_level_grass]}</b> 🌿
<b>Уровень пыльцы сорняков - {levels[data.pollen_level_weed]}</b> 🌾
<b>Уровень плесени - {levels[data.mold_level]}</b> 🦠


<i>Преобладающий тип пыльцы</i> - {predominant_pollens[data.predominant_pollen_type]}
"""
                    await bot.edit_message_text(
                        chat_id=callback_query.message.chat.id,
                        message_id=callback_query.message.message_id,
                        text=text,
                        reply_markup=InlineKeyboards.transition_to_main_keyboard(),
                        parse_mode='HTML'
                    )
                except MessageNotModified:
                    await callback_query.answer('Что-то пошло не так!')
                else:
                    await db.update_air_quality_info_today_by_city(
                        city=user.city,
                        new_air_quality_info_today=text
                    )


def register_weather_handlers(dispatcher: Dispatcher):
    dispatcher.register_callback_query_handler(get_1_day_forecast, lambda cb: cb.data == '1_day')
    dispatcher.register_callback_query_handler(get_4_days_forecasts, lambda cb: cb.data in ('2_day', '3_day', '4_day'))
    dispatcher.register_callback_query_handler(get_today_forecast, lambda cb: cb.data == 'forecast_for_today')
    dispatcher.register_callback_query_handler(get_today_air_quality_forecast, lambda cb: cb.data == 'air_quality')
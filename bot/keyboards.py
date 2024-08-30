from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton
)


class InlineKeyboards:

    @staticmethod
    def main_keyboard() -> InlineKeyboardMarkup:
        """Инлайн клавиатура в главном меню"""
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Профиль ⚙️', callback_data='profile'),
                 InlineKeyboardButton(text='Выбрать город 🗺️', callback_data='change_city')],
                [InlineKeyboardButton(text='Прогноз каждый час 🌥️', callback_data='forecast_for_today')],
                [InlineKeyboardButton(text='Прогноз на след. 3 дня 🌥️', callback_data='3_day_forecast')],
                [InlineKeyboardButton(text='Другое', callback_data='other')]
            ], row_width=2)
        return kb

    @staticmethod
    def transition_to_main_keyboard() -> InlineKeyboardMarkup:
        """Инлайн клавиатура при показе погоды"""
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='В главное меню', callback_data='main_menu')]
            ], row_width=1)
        return kb

    @staticmethod
    def first_30_cities_keyboard() -> InlineKeyboardMarkup:
        """Первая инлайн клавиатура для выбора города"""
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Москва", callback_data="гор_Москва"),
                InlineKeyboardButton(text="Санкт-Петербург", callback_data="гор_Санкт-Петербург"),
                InlineKeyboardButton(text="Новосибирск", callback_data="гор_Новосибирск")
            ],
            [
                InlineKeyboardButton(text="Екатеринбург", callback_data="гор_Екатеринбург"),
                InlineKeyboardButton(text="Казань", callback_data="гор_Казань"),
                InlineKeyboardButton(text="Нижний Новгород", callback_data="гор_Нижний Новгород")
            ],
            [
                InlineKeyboardButton(text="Челябинск", callback_data="гор_Челябинск"),
                InlineKeyboardButton(text="Самара", callback_data="гор_Самара"),
                InlineKeyboardButton(text="Омск", callback_data="гор_Омск")
            ],
            [
                InlineKeyboardButton(text="Ростов-на-Дону", callback_data="гор_Ростов-на-Дону"),
                InlineKeyboardButton(text="Уфа", callback_data="гор_Уфа"),
                InlineKeyboardButton(text="Красноярск", callback_data="гор_Красноярск")
            ],
            [
                InlineKeyboardButton(text="Пермь", callback_data="гор_Пермь"),
                InlineKeyboardButton(text="Воронеж", callback_data="гор_Воронеж"),
                InlineKeyboardButton(text="Волгоград", callback_data="гор_Волгоград")
            ],
            [
                InlineKeyboardButton(text="Краснодар", callback_data="гор_Краснодар"),
                InlineKeyboardButton(text="Саратов", callback_data="гор_Саратов"),
                InlineKeyboardButton(text="Тюмень", callback_data="гор_Тюмень")
            ],
            [
                InlineKeyboardButton(text="Тольятти", callback_data="гор_Тольятти"),
                InlineKeyboardButton(text="Ижевск", callback_data="гор_Ижевск"),
                InlineKeyboardButton(text="Барнаул", callback_data="гор_Барнаул")
            ],
            [
                InlineKeyboardButton(text="Ульяновск", callback_data="гор_Ульяновск"),
                InlineKeyboardButton(text="Иркутск", callback_data="гор_Иркутск"),
                InlineKeyboardButton(text="Хабаровск", callback_data="гор_Хабаровск")
            ],
            [
                InlineKeyboardButton(text="Махачкала", callback_data="гор_Махачкала"),
                InlineKeyboardButton(text="Ярославль", callback_data="гор_Ярославль"),
                InlineKeyboardButton(text="Владивосток", callback_data="гор_Владивосток")
            ],
            [
                InlineKeyboardButton(text="Оренбург", callback_data="гор_Оренбург"),
                InlineKeyboardButton(text="Томск", callback_data="гор_Томск"),
                InlineKeyboardButton(text="Кемерово", callback_data="гор_Кемерово")
            ],
            [
                InlineKeyboardButton(text="Другие 20 городов ➡️", callback_data="next_cities")
            ],
            [
                InlineKeyboardButton(text='В главное меню', callback_data='main_menu')
            ]
        ], row_width=3)
        return kb

    @staticmethod
    def second_20_cities_keyboard() -> InlineKeyboardMarkup:
        """Вторая инлайн клавиатура для выбора города"""
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Владикавказ", callback_data="гор_Владикавказ"),
                InlineKeyboardButton(text="Новороссийск", callback_data="гор_Новороссийск"),
                InlineKeyboardButton(text="Пятигорск", callback_data="гор_Пятигорск")
            ],
            [
                InlineKeyboardButton(text="Сочи", callback_data="гор_Сочи"),
                InlineKeyboardButton(text="Ставрополь", callback_data="гор_Ставрополь"),
                InlineKeyboardButton(text="Тверь", callback_data="гор_Тверь")
            ],
            [
                InlineKeyboardButton(text="Тула", callback_data="гор_Тула"),
                InlineKeyboardButton(text="Калуга", callback_data="гор_Калуга"),
                InlineKeyboardButton(text="Кострома", callback_data="гор_Кострома")
            ],
            [
                InlineKeyboardButton(text="Курск", callback_data="гор_Курск"),
                InlineKeyboardButton(text="Липецк", callback_data="гор_Липецк"),
                InlineKeyboardButton(text="Мурманск", callback_data="гор_Мурманск")
            ],
            [
                InlineKeyboardButton(text="Пенза", callback_data="гор_Пенза"),
                InlineKeyboardButton(text="Псков", callback_data="гор_Псков"),
                InlineKeyboardButton(text="Рязань", callback_data="гор_Рязань")
            ],
            [
                InlineKeyboardButton(text="Смоленск", callback_data="гор_Смоленск"),
                InlineKeyboardButton(text="Сургут", callback_data="гор_Сургут"),
                InlineKeyboardButton(text="Тамбов", callback_data="гор_Тамбов")
            ],
            [
                InlineKeyboardButton(text="Саранск", callback_data="гор_Саранск"),
                InlineKeyboardButton(text="Чебоксары", callback_data="гор_Чебоксары")
            ],
            [
                InlineKeyboardButton(text="Назад ⬅️", callback_data="past_cities")
            ]
        ])
        return kb

    @staticmethod
    def other_keyboard() -> InlineKeyboardMarkup:
        """Инлайн клавиатура в меню 'Другое'"""
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Связь 📞', callback_data='dev')],
                [InlineKeyboardButton(text='Незнакомые термины', callback_data='terms')],
                [InlineKeyboardButton(text='В главное меню', callback_data='main_menu')]
            ], row_width=1)
        return kb

    @staticmethod
    def back_keyboard() -> InlineKeyboardMarkup:
        """Инлайн клавиатура при показе автора (чтобы вернутся в меню 'Другое')"""
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Назад', callback_data='back')]
            ], row_width=1)
        return kb

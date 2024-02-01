import requests
import sqlite3
from kivy.app import App
from kivy.uix.button import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

Window.size = (500, 500)
Window.clearcolor = (95/255, 158/255, 160/255)
Window.title = "Конвертер денег"
API_URL = "https://v6.exchangerate-api.com/v6/aa1030f7347eda99fa082ed3/latest"


class CurrencyConverter:
    def __init__(self, base_currency):
        self.base_currency = base_currency

    def get_exchange_rates(self):
        response = requests.get(f"{API_URL}/{self.base_currency}")
        response.raise_for_status()
        exchange_rates = response.json()
        return exchange_rates

class CurrencyApp(App):
    def __init__(self):
        super().__init__()
        self.label = Label(text='Конвертер')
        self.first = Label(text="Перша валюта: ")
        self.second = Label(text="Друга валюта: ")
        self.text_input = TextInput(hint_text = f"Виберіть валюту ", multiline = False)   
        self.input_data = TextInput(hint_text=f"Введіте значення в Евро", multiline=False)
        self.input_data.bind(text=self.on_text)  
        

    def on_text(self, *args):
        data = self.input_data.text
        selected_currency = self.text_input.text.lower()

        currency_mapping = {
            "евро": ("EUR","UAH", "USD", "Гривні", "Доллар"),
            "доллар": ("USD", "UAH","EUR", "Гривні", "Евро"),
            "гривні": ("UAH","EUR", "USD", "Евро", "Доллар"),
            "крони": ("CZK","EUR", "UAH", "Евро", "Гривні"),
        }

        try:
            currency_code, first_value, second_value, text_1, text_2 = currency_mapping[selected_currency]
            self.currency_converter = CurrencyConverter(currency_code)

            data = float(data)
            exchange_rates = self.currency_converter.get_exchange_rates()

            if exchange_rates and "conversion_rates" in exchange_rates:
                rate_first = exchange_rates["conversion_rates"].get(first_value, 0)
                rate_second = exchange_rates["conversion_rates"].get(second_value, 0)

                self.first.text = f"{text_1}: {data * rate_first}"
                self.second.text = f"{text_2}: {data * rate_second}"
            else:
                print(f"Не вдалося отримати курси обміну або неправильний формат відповіді. Відповідь: {exchange_rates}")

        except Exception as e:
            print(f"Ошибка: {e}")


    def build(self):
        box = BoxLayout(orientation='vertical')
        box.add_widget(self.label)
        box.add_widget(self.text_input)
        box.add_widget(self.input_data)
        box.add_widget(self.first)
        box.add_widget(self.second)
        return box

if __name__ == '__main__':
    # Запуск Kivy-приложения
    CurrencyApp().run()

import asyncio
import json
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from android import LibreLinkUp
from config import TOKEN, PATIENT_ID, COUNTRY, HEADERS

Libre_link_up = LibreLinkUp(TOKEN, PATIENT_ID, COUNTRY, HEADERS)

class ColoredLabel(BoxLayout):
    def __init__(self, glucose_value, time_value, trend, bg_color, **kwargs):
        super(ColoredLabel, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.padding = 10

        with self.canvas.before:
            Color(*bg_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(pos=self._update_rect, size=self._update_rect)

        glucose_label = Label(
            text=f"{float(glucose_value)}",
            font_size='35sp',
            size_hint_x=0.6,
            halign='left',
            valign='middle',
            color=(0, 0, 0, 1)
        )
        glucose_label.bind(size=self._update_text_size)

        trend_label = Label(
            text=trend,
            font_size='30sp',
            size_hint_x=4.8,
            font_name="seguiemj",
            halign='left',
            valign='middle',
            color=(0, 0, 0, 1)
        )
        trend_label.bind(size=self._update_text_size)

        time_label = Label(
            text=f"{time_value}",
            font_size='20sp',
            size_hint_x=0.7,
            halign='right',
            valign='middle',
            color=(0, 0, 0, 1)
        )
        time_label.bind(size=self._update_text_size)

        self.add_widget(glucose_label)
        self.add_widget(trend_label)
        self.add_widget(time_label)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def _update_text_size(self, label, value):
        label.text_size = label.size



class GlucoseApp(App):
    async def fetch_data(self):
        return await asyncio.to_thread(Libre_link_up.return_data_for_app)

    async def update_data(self, dt):
        self.grid_layout.clear_widgets()

        glucose_data = await self.fetch_data()

        with open("glucose_data.json", 'r', encoding='utf-8') as file:
            glucose_data = reversed(list(json.loads(file.read())))


        for data in glucose_data:
            data = dict(data)
            glucose_value = float(data["value"])
            time_value = data["current_time"]
            trend = data["trend"]
            if glucose_value > 13.5:
                bg_color = get_color_from_hex('#FFA500')  # Оранжевый
            elif 10 <= glucose_value <= 13.5:
                bg_color = get_color_from_hex('#FFFF00')  # Желтый
            elif 4 <= glucose_value < 10:
                bg_color = get_color_from_hex('#00FF00')  # Зеленый
            else:
                bg_color = get_color_from_hex('#FF0000')  # Красный

    #         self.update_display(glucose_value, time_value, trend, bg_color)

    # def update_display(self, glucose_value, time_value, trend, bg_color):
        #self.grid_layout.clear_widgets()
            glucose_item = ColoredLabel(
                glucose_value=glucose_value,
                time_value=time_value,
                trend=trend,
                bg_color=bg_color,
                size_hint_y=None,
                height=100
            )
            self.grid_layout.add_widget(glucose_item, index=0)

    def get_current_time(self):
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def build(self):
        Window.clearcolor = get_color_from_hex('#FFFFFF')

        main_layout = BoxLayout(orientation='vertical')


        scroll_view = ScrollView()
        self.grid_layout = GridLayout(cols=1, size_hint_y=None)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))
        scroll_view.add_widget(self.grid_layout)
        main_layout.add_widget(scroll_view)

        Clock.schedule_interval(self.async_update_wrapper, 120) 

        return main_layout

    def async_update_wrapper(self, dt):
        asyncio.run(self.update_data(dt))

if __name__ == '__main__':
    GlucoseApp().run()

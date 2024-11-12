from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock

class ImageButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(ImageButton, self).__init__(**kwargs)

class LandingPage(Screen):
    def __init__(self, **kwargs):
        super(LandingPage, self).__init__(**kwargs)

        self.layout = FloatLayout()

        self.background = Image(source='backgroundLanding.png', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(self.background)

        with self.layout.canvas.before:
            Color(1, 1, 1)  
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)

        self.layout.bind(size=self._update_rect, pos=self._update_rect)

        # Menggunakan ImageButton dengan ukuran fleksibel
        self.start_button = ImageButton(
            source='images/button_landing.png',
            size_hint=(0.4, 0.3),  # Tentukan size_hint yang diinginkan untuk fleksibilitas
            pos_hint={'center_x': 0.53, 'center_y': 0.25}
        )
        self.start_button.bind(on_press=self.go_to_menu)

        self.layout.add_widget(self.start_button)

        self.add_widget(self.layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def go_to_menu(self, instance):
        self.manager.current = 'menu'

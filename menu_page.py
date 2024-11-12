from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Rectangle, RoundedRectangle, Color
from kivy.core.audio import SoundLoader
from kivy.uix.button import ButtonBehavior
from kivy.metrics import dp
from kivy.core.window import Window

class RoundedButton(Button):
    def __init__(self, image_source='', **kwargs):
        super(RoundedButton, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (1, 1, 1, 0)

        # Draw rounded rectangle
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rounded_rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[20])

        # Draw image
        with self.canvas:
            self.rect = Rectangle(source=image_source, size=self.size, pos=self.pos)

        # Bind for updates
        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        self.rounded_rect.pos = self.pos
        self.rounded_rect.size = self.size
        self.rect.pos = self.pos
        self.rect.size = self.size

class ImageButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(ImageButton, self).__init__(**kwargs)

class MenuPage(Screen):
    def __init__(self, **kwargs):
        super(MenuPage, self).__init__(**kwargs)

        layout = FloatLayout()
        background = Image(source='background.png', allow_stretch=True, keep_ratio=False)
        layout.add_widget(background)

        # Back button
        back_button = ImageButton(source='images/back.png', size_hint=(None, None), size=(dp(150), dp(70)), pos_hint={'x': 0.05, 'top': 0.95})
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        # Music toggle button
        self.music_button = ImageButton(source='images/mute.png', size_hint=(None, None), size=(dp(150), dp(70)), pos_hint={'right': 0.95, 'top': 0.95})
        self.music_button.bind(on_press=self.toggle_music)
        layout.add_widget(self.music_button)

        scroll_view = ScrollView(size_hint=(1, 0.6), do_scroll_x=True, do_scroll_y=False)
        scroll_view.pos_hint = {'center_x': 0.5, 'y': 0.0}

        # Mengatur menu_grid dengan size_hint agar ukuran fleksibel
        menu_grid = GridLayout(cols=6, padding=20, spacing=20, size_hint_x=None, height=dp(100), size_hint_y=1)
        menu_grid.bind(minimum_width=menu_grid.setter('width'))

        buttons = [
            ('lowercase_letter', self.go_to_lowercase, 'images/image1.png'),
            ('Instructions', self.show_instructions, 'images/image2.png'),
            ('Settings', self.show_settings, 'images/image3.png'),
            ('Exit', self.exit_game, 'images/image4.png'),
            ('High Scores', self.show_high_scores, 'images/image5.png'),
            ('Help', self.show_help, 'images/image6.png'),
            ('Profile', self.show_profile, 'images/image6.png'),
            ('Credits', self.show_credits, 'images/image7.png'),
            ('Level 1', self.start_level_1, 'images/image8.png'),
            ('Level 2', self.start_level_2, 'images/image9.png'),
            ('Level 3', self.start_level_3, 'images/image10.png'),
            ('Level 4', self.start_level_4, 'images/level4_icon.png')
        ]

        # Menggunakan size_hint agar ukuran button relatif
        for text, action, image_source in buttons:
            button = RoundedButton(image_source=image_source, size_hint_x=None, width=dp(2000) / 6, height=dp(100))
            button.bind(on_press=action)
            menu_grid.add_widget(button)

        scroll_view.add_widget(menu_grid)
        layout.add_widget(scroll_view)

        self.add_widget(layout)

        # Pengaturan musik
        self.is_music_muted = False
        self.music = SoundLoader.load('background_music.mp3')
        if self.music:
            self.music.loop = True
            self.music.play()

    def go_back(self, instance):
        self.manager.current = 'landing'
        if self.music and not self.is_music_muted:
            self.music.play()

    def toggle_music(self, instance):
        self.is_music_muted = not self.is_music_muted
        if self.is_music_muted:
            self.music.stop()
            self.music_button.source = 'images/unmute.png'
            print("Music muted")
        else:
            self.music.play()
            self.music_button.source = 'images/mute.png'
            print("Music unmuted")

    def go_to_lowercase(self, instance):
        self.manager.current = 'lowercase_letter_screen'

    def start_game(self, instance):
        print("Game Started!")

    def show_instructions(self, instance):
        self.manager.current = 'LearnNumber'

    def show_settings(self, instance):
        print("Open settings here")

    def exit_game(self, instance):
        print("Exiting game...")

    def show_high_scores(self, instance):
        print("Show high scores")

    def show_help(self, instance):
        print("Show help")

    def show_profile(self, instance):
        print("Show profile")

    def show_credits(self, instance):
        print("Show credits")

    def start_level_1(self, instance):
        print("Starting Level 1")

    def start_level_2(self, instance):
        print("Starting Level 2")

    def start_level_3(self, instance):
        print("Starting Level 3")

    def start_level_4(self, instance):
        print("Starting Level 4")

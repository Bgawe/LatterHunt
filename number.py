from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import ButtonBehavior
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.metrics import dp


class ImageButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(ImageButton, self).__init__(**kwargs)

class NumberScreen(Screen):
    def __init__(self, **kwargs):
        super(NumberScreen, self).__init__(**kwargs)
        self.current_index = 0
        self.alphabet_images = {
            '1': 'images/AbcAlphabet/1.png',
            '2': 'images/AbcAlphabet/2.png',
            '3': 'images/AbcAlphabet/3.png',
            '4': 'images/AbcAlphabet/4.png',
            '5': 'images/AbcAlphabet/5.png',
            '6': 'images/AbcAlphabet/6.png',
            '7': 'images/AbcAlphabet/7.png',
            '8': 'images/AbcAlphabet/8.png',
            '9': 'images/AbcAlphabet/9.png',
            '10': 'images/AbcAlphabet/10.png',
            '11': 'images/AbcAlphabet/11.png',
            '12': 'images/AbcAlphabet/12.png',
            '13': 'images/AbcAlphabet/13.png',
            '14': 'images/AbcAlphabet/14.png',
            '15': 'images/AbcAlphabet/15.png',
            '16': 'images/AbcAlphabet/16.png',
            '17': 'images/AbcAlphabet/17.png',
            '18': 'images/AbcAlphabet/18.png',
            '19': 'images/AbcAlphabet/19.png',
            '20': 'images/AbcAlphabet/20.png',
        }
        
        # Musik untuk setiap huruf
        self.alphabet_sounds = {
            '1': 'sounds/1.mp3',
            '2': 'sounds/2.mp3',
            '3': 'sounds/3.mp3',
            '4': 'sounds/4.mp3',
            '5': 'sounds/5.mp3',
            '6': 'sounds/6.mp3',
            '7': 'sounds/7.mp3',
            '8': 'sounds/8.mp3',
            '9': 'sounds/9.mp3',
            '10': 'sounds/10.mp3',
            '11': 'sounds/11.mp3',
            '12': 'sounds/12.mp3',
            '13': 'sounds/13.mp3',
            '14': 'sounds/14.mp3',
            '15': 'sounds/15.mp3',
            '16': 'sounds/16.mp3',
            '17': 'sounds/17.mp3',
            '18': 'sounds/18.mp3',
            '19': 'sounds/19.mp3',
            '20': 'sounds/20.mp3',
        }

        # Layout utama
        self.layout = FloatLayout()

        # Gambar latar belakang
        self.background = Image(source='backgroundAbcAlpha.png', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(self.background)

        # Tombol kembali ke menu
        self.back_to_menu_button = ImageButton(source='images/back.png',size_hint=(None, None), size=(dp(150), dp(70)), pos_hint={'x': 0.05, 'top': 0.95})
        self.back_to_menu_button.bind(on_press=self.go_to_menu)
        self.layout.add_widget(self.back_to_menu_button)

        # Tombol kembali untuk navigasi
        self.back_button = ImageButton(source='images/AbcAlphabet/back_arrow.png', size_hint=(None, None), size=(100, 100), pos_hint={'x': 0.1, 'y': 0.5})
        self.back_button.bind(on_press=self.previous_letter)
        self.back_button.disabled = True  # Nonaktifkan tombol kembali di huruf A

        # Gambar flashcard
        self.flashcard_image = ImageButton(
            source=self.alphabet_images['1'],
            size=(1000, 1000),
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            size_hint=(None, None)
        )
        self.flashcard_image.bind(on_press=self.animate_flashcard)  # Mengikat flashcard untuk animasi dan suara

        # Tombol berikutnya untuk navigasi
        self.next_button = ImageButton(source='images/AbcAlphabet/next_arrow.png', size_hint=(None, None), size=(100, 100), pos_hint={'x': 0.8, 'y': 0.5})
        self.next_button.bind(on_press=self.next_letter)

        # Menambahkan tombol dan gambar ke layout
        self.layout.add_widget(self.back_button)
        self.layout.add_widget(self.flashcard_image)
        self.layout.add_widget(self.next_button)

        self.add_widget(self.layout)

        self.current_sound = None  # Untuk menyimpan sound yang sedang diputar

    def on_enter(self):
        # Jalankan animasi saat layar dimasuki
        self.animate_flashcard(initial=True)

    def next_letter(self, instance):
        if self.current_index < len(self.alphabet_images) - 1:
            self.current_index += 1
            self.update_flashcard()

    def previous_letter(self, instance):
        if self.current_index > 0:
            self.current_index -= 1
            self.update_flashcard()

    def update_flashcard(self):
        current_letter = list(self.alphabet_images.keys())[self.current_index]
        self.animate_flashcard()

    def animate_flashcard(self, instance=None, initial=False):
        # Putar musik saat animasi dimulai
        current_letter = list(self.alphabet_images.keys())[self.current_index]
        self.play_sound(current_letter)

        # Buat animasi untuk mengubah ukuran gambar
        scale_up = Animation(size=(600, 600), duration=0.3)
        scale_down = Animation(size=(200, 200), duration=0.2)

        # Gabungkan animasi
        animation_sequence = scale_up + scale_down

        if not initial:
            # Callback untuk memperbarui sumber gambar setelah animasi selesai
            animation_sequence.bind(on_complete=lambda *args: self.update_image_source(current_letter))

        animation_sequence.start(self.flashcard_image)

        if initial:
            # Untuk animasi awal, langsung update gambar setelah animasi
            self.update_image_source(current_letter)

    def update_image_source(self, current_letter):
        # Memperbarui sumber gambar
        self.flashcard_image.source = self.alphabet_images[current_letter]
        self.flashcard_image.reload()  # Memuat ulang gambar untuk memperbarui tampilan

        # Mengaktifkan/nonaktifkan tombol berdasarkan indeks saat ini
        self.back_button.disabled = (self.current_index == 0)
        self.next_button.disabled = (self.current_index == len(self.alphabet_images) - 1)

        # Hentikan musik setelah animasi selesai
        if self.current_sound:
            self.current_sound.stop()

    def play_sound(self, current_letter):
        # Jika ada suara yang sedang diputar, hentikan
        if self.current_sound:
            self.current_sound.stop()
        
        # Muat dan mainkan suara yang sesuai
        sound_path = self.alphabet_sounds.get(current_letter)
        if sound_path:
            self.current_sound = SoundLoader.load(sound_path)
            if self.current_sound:
                self.current_sound.play()

    def go_to_menu(self, instance):
        self.manager.current = 'lowercase_letter_screen'  # Ganti dengan nama layar menu Anda
            
        
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

class FlashCardScreen(Screen):
    def __init__(self, **kwargs):
        super(FlashCardScreen, self).__init__(**kwargs)
        self.current_index = 0
        self.alphabet_images = {
            'A': 'images/AbcAlphabet/a.png',
            'B': 'images/AbcAlphabet/b.png',
            'C': 'images/AbcAlphabet/c.png',
            'D': 'images/AbcAlphabet/d.png',
            'E': 'images/AbcAlphabet/e.png',
            'F': 'images/AbcAlphabet/f.png',
            'G': 'images/AbcAlphabet/g.png',
            'H': 'images/AbcAlphabet/h.png',
            'I': 'images/AbcAlphabet/i.png',
            'J': 'images/AbcAlphabet/j.png',
            'K': 'images/AbcAlphabet/k.png',
            'L': 'images/AbcAlphabet/l.png',
            'M': 'images/AbcAlphabet/m.png',
            'N': 'images/AbcAlphabet/n.png',
            'O': 'images/AbcAlphabet/o.png',
            'P': 'images/AbcAlphabet/p.png',
            'Q': 'images/AbcAlphabet/q.png',
            'R': 'images/AbcAlphabet/r.png',
            'S': 'images/AbcAlphabet/s.png',
            'T': 'images/AbcAlphabet/t.png',
            'U': 'images/AbcAlphabet/u.png',
            'V': 'images/AbcAlphabet/v.png',
            'W': 'images/AbcAlphabet/w.png',
            'X': 'images/AbcAlphabet/x.png',
            'Y': 'images/AbcAlphabet/y.png',
            'Z': 'images/AbcAlphabet/z.png'
        }
        
        # Musik untuk setiap huruf
        self.alphabet_sounds = {
            'A': 'sounds/a.mp3',
            'B': 'sounds/b.mp3',
            'C': 'sounds/c.mp3',
            'D': 'sounds/d.mp3',
            'E': 'sounds/e.mp3',
            'F': 'sounds/f.mp3',
            'G': 'sounds/g.mp3',
            'H': 'sounds/h.mp3',
            'I': 'sounds/i.mp3',
            'J': 'sounds/j.mp3',
            'K': 'sounds/k.mp3',
            'L': 'sounds/l.mp3',
            'M': 'sounds/m.mp3',
            'N': 'sounds/n.mp3',
            'O': 'sounds/o.mp3',
            'P': 'sounds/p.mp3',
            'Q': 'sounds/q.mp3',
            'R': 'sounds/r.mp3',
            'S': 'sounds/s.mp3',
            'T': 'sounds/t.mp3',
            'U': 'sounds/u.mp3',
            'V': 'sounds/v.mp3',
            'W': 'sounds/w.mp3',
            'X': 'sounds/x.mp3',
            'Y': 'sounds/y.mp3',
            'Z': 'sounds/z.mp3'
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
            source=self.alphabet_images['A'],
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
            
        
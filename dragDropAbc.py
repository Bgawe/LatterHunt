from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
import random
from kivy.uix.screenmanager import Screen


# Kivy Builder untuk UI
Builder.load_string('''
<DragImage>:
    size_hint: None, None
    size: 150, 150
    canvas.before:
        PushMatrix
        Rotate:
            angle: self.angle
            origin: self.center
    canvas.after:
        PopMatrix

<DropArea>:
    image_source: ''
    sound_source: ''
    opacity_value: 0.5
    Image:
        id: image
        source: root.image_source
        size_hint: 0.4, 0.4  # Ukuran relatif terhadap ukuran layar
        pos: root.pos
        opacity: root.opacity_value


<GameLayout>:
    drag_image: drag_image
    completed_image_widget: completed_image_widget

    Image:
        source: "images/matchCard.png"
        allow_stretch: True
        keep_ratio: False
        size_hint: 1, 1

    ImageButton:
        source: "images/back.png"
        size_hint: None, None
        size: 250,100
        pos_hint: {"x": 0.05, "y": 0.85}
        on_release: root.go_back()

    # Baris 1
    DropArea:
        id: drop_area1
        pos_hint: {"x": 0.25, "y": 0.75}
        size_hint: 0.3, 0.25
        image_source: "images/AbcAlphabet/a.png"
        sound_source: "sounds/a.mp3"

    DropArea:
        id: drop_area2
        pos_hint: {"x": 0.45, "y": 0.75}
        size_hint: 0.3, 0.25
        image_source: "images/AbcAlphabet/b.png"
        sound_source: "sounds/b.mp3"

    DropArea:
        id: drop_area3
        pos_hint: {"x": 0.65, "y": 0.75}
        size_hint: 0.3, 0.25
        image_source: "images/AbcAlphabet/c.png"
        sound_source: "sounds/c.mp3"

    DropArea:
        id: drop_area4
        pos_hint: {"x": 0.85, "y": 0.75}
        size_hint: 0.3, 0.25
        image_source: "images/AbcAlphabet/d.png"
        sound_source: "sounds/d.mp3"

    # Baris 2
    DropArea:
        id: drop_area5
        pos_hint: {"x": 0.25, "y": 0.45}
        size_hint: 0.3, 0.25
        image_source: "images/AbcAlphabet/e.png"
        sound_source: "sounds/e.mp3"

    DropArea:
        id: drop_area6
        pos_hint: {"x": 0.45, "y": 0.45}
        size_hint: 0.3, 0.25
        image_source: "images/AbcAlphabet/f.png"
        sound_source: "sounds/f.mp3"

    DropArea:
        id: drop_area7
        pos_hint: {"x": 0.65, "y": 0.45}
        size_hint: 0.3, 0.25
        image_source: "images/AbcAlphabet/g.png"
        sound_source: "sounds/g.mp3"

    DropArea:
        id: drop_area8
        pos_hint: {"x": 0.85, "y": 0.45}
        size_hint: 0.3, 0.25
        image_source: "images/AbcAlphabet/h.png"
        sound_source: "sounds/h.mp3"

    # Baris 3
    DropArea:
        id: drop_area9
        pos_hint: {"x": 0.25, "y": 0.2}
        size_hint: 0.3, 0.25
        image_source: "images/AbcAlphabet/i.png"
        sound_source: "sounds/i.mp3"

    DropArea:
        id: drop_area10
        pos_hint: {"x": 0.45, "y": 0.2}
        size_hint: 0.3, 0.25
        image_source: "images/AbcAlphabet/j.png"
        sound_source: "sounds/j.mp3"

    DropArea:
        id: drop_area11
        pos_hint: {"x": 0.65, "y": 0.2}
        size_hint: 0.3, 0.25
        image_source: "images/AbcAlphabet/k.png"
        sound_source: "sounds/k.mp3"

    DropArea:
        id: drop_area12
        pos_hint: {"x": 0.85, "y": 0.2}
        size_hint: 0.3, 0.25
        image_source: "images/AbcAlphabet/l.png"
        sound_source: "sounds/l.mp3"

    DragImage:
        id: drag_image
        source: root.current_image
        pos: 100, 300

    Image:
        id: completed_image_widget
        source: root.completed_image
        size_hint: None, None
        size: 150, 150
        opacity: 0  # Ini disembunyikan hingga permainan selesai
        pos: root.center_pos
''')

# Kelas DragImage untuk gambar yang bisa digeser
class DragImage(Image):
    angle = NumericProperty(0)
    scale = NumericProperty(1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dragging = False
        self.initial_pos = (self.x, self.y)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.dragging = True
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.dragging:
            self.pos = (touch.x - self.width / 2, touch.y - self.height / 2)
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.dragging:
            self.dragging = False
            app = App.get_running_app()
            # Ambil layar aktif untuk memastikan kita mengakses GameLayout
            screen = app.root.get_screen('dragdrop')  # Sesuaikan dengan nama screen Anda
            game_layout = screen.game_layout  # Ambil GameLayout dari screen
            for drop_area in game_layout.get_drop_areas():
                if drop_area.collide_point(*touch.pos) and drop_area.image_source == self.source:
                    game_layout.complete_drag(drop_area)
                    self.animate_success()
                    return True
            self.animate_failure()
            return True
        return super().on_touch_up(touch)

    def animate_failure(self):
        animation = Animation(angle=15, duration=0.2) + Animation(angle=-15, duration=0.2)
        animation += Animation(angle=0, duration=0.2)
        animation.bind(on_complete=lambda *args: self.reset_position())
        animation.start(self)

    def animate_success(self):
        scale_animation = Animation(scale=1.5, duration=0.2) + Animation(scale=1.0, duration=0.2)
        return_animation = Animation(pos=self.initial_pos, duration=0.5)
        scale_animation.bind(on_complete=lambda *args: return_animation.start(self))
        scale_animation.start(self)

    def reset_position(self):
        animation = Animation(pos=self.initial_pos, duration=0.2)
        animation.start(self)

# Kelas DropArea untuk area penempatan gambar
class DropArea(Widget):
    image_source = StringProperty("")
    opacity_value = NumericProperty(0.5)
    sound_source = StringProperty("")

# Kelas GameLayout untuk menyusun game
# Kelas GameLayout untuk menyusun game
class GameLayout(FloatLayout):
    drag_image = ObjectProperty(None)
    completed_image_widget = ObjectProperty(None)
    images = ListProperty([
        "images/AbcAlphabet/a.png",
        "images/AbcAlphabet/b.png",
        "images/AbcAlphabet/c.png",
        "images/AbcAlphabet/d.png",
        "images/AbcAlphabet/e.png",
        "images/AbcAlphabet/f.png",
        "images/AbcAlphabet/g.png",
        "images/AbcAlphabet/h.png",
        "images/AbcAlphabet/i.png",
        "images/AbcAlphabet/j.png",
        "images/AbcAlphabet/k.png",
        "images/AbcAlphabet/l.png"
    ])
    current_image = StringProperty("")
    completed_image = StringProperty("images/berhasil.png")
    completed_sound = StringProperty("sounds/berhasil.mp3")
    center_pos = ListProperty([0, 0])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.completed_images = []
        self.load_next_image()

    def get_drop_areas(self):
        return [child for child in self.children if isinstance(child, DropArea)]

    def load_next_image(self):
        available_images = [img for img in self.images if img not in self.completed_images]
        if available_images:
            self.current_image = random.choice(available_images)
            # Set ukuran drop area sesuai dengan ukuran drag image
            for drop_area in self.get_drop_areas():
                drop_area.size = self.drag_image.size  # Menyamakan ukuran drop area dengan drag image

            # Tampilkan drag image kembali setelah selesai
            self.drag_image.opacity = 1
        else:
            # Jika permainan selesai, sembunyikan drag_image dan tampilkan completed_image_widget
            self.drag_image.opacity = 0  # Sembunyikan gambar drag
            self.completed_image_widget.opacity = 1
            
            # Perbesar ukuran gambar selesai
            self.completed_image_widget.size = (500, 500)  # Ubah ukuran sesuai keinginan

            # Posisikan gambar selesai di tengah
            self.completed_image_widget.pos = (
                self.width / 2 - self.completed_image_widget.width / 2,
                self.height / 2 - self.completed_image_widget.height / 2
            )

            # Menyembunyikan semua DropArea
            for drop_area in self.get_drop_areas():
                drop_area.opacity = 0

            # Memutar suara selesai
            sound = SoundLoader.load(self.completed_sound)
            if sound:
                sound.play()

            print("Permainan Selesai!")

    def complete_drag(self, drop_area):
        drop_area.opacity_value = 1
        self.completed_images.append(self.current_image)

        if drop_area.sound_source:
            sound = SoundLoader.load(drop_area.sound_source)
            if sound:
                sound.play()

        self.load_next_image()
    
    def go_back(self):
        app = App.get_running_app()
        app.root.current = 'lowercase_letter_screen'

# Kelas DragDropScreen untuk menampilkan permainan
class DragDropScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_layout = GameLayout()  # Menggunakan GameLayout dari test.py
        self.add_widget(self.game_layout)

if __name__ == '__main__':
    class DragDropApp(App):
        def build(self):
            return DragDropScreen()

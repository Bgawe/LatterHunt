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
        size_hint: None, None
        size: 150, 150
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
        size: 150, 70
        pos_hint: {"x": 0.05, "y": 0.85}
        on_release: root.go_back()

    # Baris 1
    DropArea:
        id: drop_area1
        pos: 450, 550
        image_source: "images/Numbers/1.png"
        sound_source: "sounds/1.mp3"

    DropArea:
        id: drop_area2
        pos: 650, 550
        image_source: "images/Numbers/2.png"
        sound_source: "sounds/2.mp3"

    DropArea:
        id: drop_area3
        pos: 850, 550
        image_source: "images/Numbers/3.png"
        sound_source: "sounds/3.mp3"

    DropArea:
        id: drop_area4
        pos: 1050, 550
        image_source: "images/Numbers/4.png"
        sound_source: "sounds/4.mp3"

    # Baris 2
    DropArea:
        id: drop_area5
        pos: 450, 350
        image_source: "images/Numbers/5.png"
        sound_source: "sounds/5.mp3"

    DropArea:
        id: drop_area6
        pos: 650, 350
        image_source: "images/Numbers/6.png"
        sound_source: "sounds/6.mp3"

    DropArea:
        id: drop_area7
        pos: 850, 350
        image_source: "images/Numbers/7.png"
        sound_source: "sounds/7.mp3"

    DropArea:
        id: drop_area8
        pos: 1050, 350
        image_source: "images/Numbers/8.png"
        sound_source: "sounds/8.mp3"

    # Baris 3
    DropArea:
        id: drop_area9
        pos: 450, 150
        image_source: "images/Numbers/9.png"
        sound_source: "sounds/9.mp3"

    DropArea:
        id: drop_area10
        pos: 650, 150
        image_source: "images/Numbers/10.png"
        sound_source: "sounds/10.mp3"

    DragImage:
        id: drag_image
        source: root.current_image
        pos: 100, 300

    Image:
        id: completed_image_widget
        source: root.completed_image
        size_hint: None, None
        size: 150, 150
        opacity: 0
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
            screen = app.root.get_screen('numbers')
            game_layout = screen.game_layout
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

# Kelas DropArea
class DropArea(Widget):
    image_source = StringProperty("")
    opacity_value = NumericProperty(0.5)
    sound_source = StringProperty("")

# Kelas GameLayout
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
    center_pos = ListProperty([0, 0])  # Tambahkan properti ini

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.completed_images = []
        self.center_pos = [self.width / 2, self.height / 2]  # Mengatur posisi di tengah
        self.load_next_image()


    def load_next_image(self):
        available_images = [img for img in self.images if img not in self.completed_images]
        if available_images:
            self.current_image = random.choice(available_images)

# Kelas DragDropScreen untuk numerik
class NumbersScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_layout = GameLayout()
        self.add_widget(self.game_layout)

if __name__ == '__main__':
    class NumbersApp(App):
        def build(self):
            return NumbersScreen()

    NumbersApp().run()

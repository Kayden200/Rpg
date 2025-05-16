from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.properties import NumericProperty, ObjectProperty
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.vector import Vector

Window.clearcolor = (0.2, 0.2, 0.2, 1)

class Player(Image):
    health = NumericProperty(100)
    xp = NumericProperty(0)
    level = NumericProperty(1)

    def move(self, direction):
        self.pos = Vector(*self.pos) + Vector(*direction)

class Enemy(Image):
    health = NumericProperty(50)

class Joystick(Widget):
    knob = ObjectProperty(None)
    base = ObjectProperty(None)
    touch_active = False

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.touch_active = True
            self.move_knob(touch.pos)
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.touch_active:
            self.move_knob(touch.pos)

    def on_touch_up(self, touch):
        if self.touch_active:
            self.knob.center = self.center
            self.touch_active = False

    def move_knob(self, pos):
        dx = pos[0] - self.center_x
        dy = pos[1] - self.center_y
        distance = min((dx ** 2 + dy ** 2) ** 0.5, self.width / 2)
        angle = Vector(dx, dy).angle((1, 0))
        self.knob.center = (
            self.center_x + distance * Vector(1, 0).rotate(angle)[0],
            self.center_y + distance * Vector(1, 0).rotate(angle)[1],
        )

class GameScreen(Widget):
    player = ObjectProperty(None)
    enemy = ObjectProperty(None)
    joystick = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1/60)

    def update(self, dt):
        if self.joystick.touch_active:
            dx = self.joystick.knob.center_x - self.joystick.center_x
            dy = self.joystick.knob.center_y - self.joystick.center_y
            direction = Vector(dx, dy).normalize() * 3 if dx or dy else Vector(0, 0)
            self.player.move(direction)

class RPGApp(App):
    def build(self):
        return GameScreen()

if __name__ == '__main__':
    RPGApp().run()

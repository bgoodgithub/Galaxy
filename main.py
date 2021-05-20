from kivy.config import Config

Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')

from kivy import platform
from kivy.core.window import Window
from kivy.app import App
from kivy.graphics import Line, Color
from kivy.properties import NumericProperty, Clock
from kivy.uix.widget import Widget


class MainWidget(Widget):
    from transforms import transform, transform_2d, transform_perspective
    from user_actions import keyboard_closed, on_keyboard_up, on_keyboard_down, on_touch_down, on_touch_up
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    v_nb_lines = 10
    v_lines_spacing = .25  # percentage of screen width
    vertical_lines = []

    h_nb_lines = 15
    h_lines_spacing = .1
    horizontal_lines = []

    speed = 4
    current_offset_y = 0

    speed_x = 12
    current_speed_x = 0
    current_offset_x = 0

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        # print("INIT W: " + str(self.width) + " H: " + str(self.height))
        self.init_vertical_lines()
        self.init_horizontal_lines()

        if self.is_dektop():
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)

        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def is_dektop(self):
        if platform in ("linux", "win", "macosx"):
            return True
        else:
            return False

    def init_vertical_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            # self.line = Line(points=[100, 0, 100, 100])
            for i in range(0, self.v_nb_lines):
                self.vertical_lines.append(Line())

    def update_vertical_lines(self):
        central_line_x = int(self.width / 2)
        # self.line.points = [center_x, 0, center_x, 100]
        spacing = self.v_lines_spacing * self.width
        offset = -int(self.v_nb_lines / 2) + 0.5  # 0.5 term makes so empty space in middle instead of line
        for i in range(0, self.v_nb_lines):
            line_x = int(central_line_x + offset * spacing + self.current_offset_x)
            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)
            self.vertical_lines[i].points = [x1, y1, x2, y2]
            offset += 1

    def init_horizontal_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.h_nb_lines):
                self.horizontal_lines.append(Line())

    def update_horizontal_lines(self):
        central_line_x = int(self.width / 2)
        spacing = self.v_lines_spacing * self.width
        offset = int(self.v_nb_lines / 2) - 0.5

        xmin = central_line_x - offset * spacing + self.current_offset_x
        xmax = central_line_x + offset * spacing + self.current_offset_x
        spacing_y = self.h_lines_spacing * self.height

        for i in range(0, self.h_nb_lines):
            line_y = i * spacing_y - self.current_offset_y
            x1, y1 = self.transform(xmin, line_y)
            x2, y2 = self.transform(xmax, line_y)
            self.horizontal_lines[i].points = [x1, y1, x2, y2]

    def update(self, dt):
        # print(str(dt*60))
        time_factor = dt*60
        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.current_offset_y += self.speed * time_factor

        spacing_y = self.h_lines_spacing * self.height
        if self.current_offset_y >= spacing_y:
            self.current_offset_y -= spacing_y

        self.current_offset_x += self.current_speed_x * time_factor


class GalaxyApp(App):
    pass


GalaxyApp().run()

from kivy.config import Config

Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')

from kivy import platform
from kivy.core.window import Window
from kivy.app import App
from kivy.graphics import Line, Color, Quad
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

    tile = None
    ti_x = 0
    ti_y = 0

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        # print("INIT W: " + str(self.width) + " H: " + str(self.height))
        self.init_vertical_lines()
        self.init_horizontal_lines()
        self.init_tiles()

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

    def init_tiles(self):
        with self.canvas:
            Color(1, .5, 1)
            self.tile = Quad()

    def init_vertical_lines(self):
        with self.canvas:
            Color(1, .5, 1)
            # self.line = Line(points=[100, 0, 100, 100])
            for i in range(0, self.v_nb_lines):
                self.vertical_lines.append(Line())

    def get_line_x_from_index(self, index):
        central_line_x = self.perspective_point_x
        spacing = self.v_lines_spacing * self.width
        offset = index - 0.5
        line_x = central_line_x + offset * spacing + self.current_offset_x
        return line_x

    def get_line_y_from_index(self, index):
        spacing_y = self.h_lines_spacing * self.height
        line_y = index * spacing_y - self.current_offset_y
        return line_y

    def get_tile_coordinates(self, ti_x, ti_y):
        x = self.get_line_x_from_index(ti_x)
        y = self.get_line_y_from_index(ti_y)
        return x, y

    def update_tiles(self):
        xmin, ymin = self.get_tile_coordinates(self.ti_x, self. ti_y)
        xmax, ymax = self.get_tile_coordinates(self.ti_x + 1, self. ti_y + 1)

        x1, y1 = self.transform(xmin, ymin)
        x2, y2 = self.transform(xmin, ymax)
        x3, y3 = self.transform(xmax, ymax)
        x4, y4 = self.transform(xmax, ymin)

        self.tile.points = [x1, y1, x2, y2, x3, y3, x4, y4]

    def update_vertical_lines(self):
        start_index = -int(self.v_nb_lines/2) + 1
        for i in range(start_index, start_index + self.v_nb_lines):
            line_x = self.get_line_x_from_index(i)
            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)
            self.vertical_lines[i].points = [x1, y1, x2, y2]

    def init_horizontal_lines(self):
        with self.canvas:
            Color(1, .5, 1)
            for i in range(0, self.h_nb_lines):
                self.horizontal_lines.append(Line())

    def update_horizontal_lines(self):
        start_index = -int(self.v_nb_lines/2) + 1
        end_index = start_index + self.v_nb_lines - 1
        xmin = self.get_line_x_from_index(start_index)
        xmax = self.get_line_x_from_index(end_index)
        for i in range(0, self.h_nb_lines):
            line_y = self.get_line_y_from_index(i)
            x1, y1 = self.transform(xmin, line_y)
            x2, y2 = self.transform(xmax, line_y)
            self.horizontal_lines[i].points = [x1, y1, x2, y2]

    def update(self, dt):
        # print(str(dt*60))
        time_factor = dt*60
        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.update_tiles()
        self.current_offset_y += self.speed * time_factor

        spacing_y = self.h_lines_spacing * self.height
        if self.current_offset_y >= spacing_y:
            self.current_offset_y -= spacing_y

        self.current_offset_x += self.current_speed_x * time_factor


class GalaxyApp(App):
    pass


GalaxyApp().run()

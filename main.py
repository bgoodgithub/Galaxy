from kivy.app import App
from kivy.graphics import Line, Color
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget


class MainWidget(Widget):
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    v_nb_lines = 10
    v_lines_spacing = .25  # percentage of screen width
    vertical_lines = []

    h_nb_lines = 15
    h_lines_spacing = .1
    horizontal_lines = []

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        # print("INIT W: " + str(self.width) + " H: " + str(self.height))
        self.init_vertical_lines()
        self.init_horizontal_lines()

    def on_parent(self, widget, parent):
        # print("ON PARENT W: " + str(self.width) + " H: " + str(self.height))
        pass

    def on_size(self, *args):
        # print("ON SIZE W: " + str(self.width) + " H: " + str(self.height))
        # self.perspective_point_x = self.width/2
        # self.perspective_point_y = self.height * 0.75
        self.update_vertical_lines()
        self.update_horizontal_lines()

    def on_perspective_point_x(self, widget, value):
        # print("PX: " + str(value))
        pass

    def on_perspective_point_y(self, widget, value):
        # print("PY: " + str(value))
        pass

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
            line_x = int(central_line_x + offset * spacing)
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

        xmin = central_line_x - offset * spacing
        xmax = central_line_x + offset * spacing
        spacing_y = self.h_lines_spacing * self.height

        for i in range(0, self.h_nb_lines):
            line_y = i * spacing_y
            x1, y1 = self.transform(xmin, line_y)
            x2, y2 = self.transform(xmax, line_y)
            self.horizontal_lines[i].points = [x1, y1, x2, y2]

    def transform(self, x, y):
        # return self.transform_2d(x, y)
        return self.transform_perspective(x, y)

    def transform_2d(self, x, y):
        return int(x), int(y)

    def transform_perspective(self, x, y):
        lin_y = y * self.perspective_point_y / self.height
        if lin_y > self.perspective_point_y:
            lin_y = self.perspective_point_y

        diff_x = x - self.perspective_point_x
        diff_y = self.perspective_point_y - lin_y
        factor_y = diff_y / self.perspective_point_y
        factor_y = pow(factor_y, 2)  # increasing the power gives the illusion of moving faster

        tr_x = self.perspective_point_x + diff_x * factor_y
        tr_y = (1 - factor_y) * self.perspective_point_y

        return int(tr_x), int(tr_y)


class GalaxyApp(App):
    pass


GalaxyApp().run()

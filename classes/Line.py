from classes.Point import Point


class Line:

    def __init__(self, point_0: Point, point_1: Point, id_=None):
        self.id = id_
        self.point_0 = point_0
        self.point_1 = point_1

    def __str__(self):
        return f"{self.__class__.__name__} " \
               f"[id: {self.id},\tp0: {self.point_0} p1: {self.point_1}]"

    def __repr__(self):
        return f"{self.__class__.__name__} [id: {self.id}]"

    def get_distance(self):
        return ((self.point_0.X - self.point_1.X) ** 2 +
                (self.point_0.Y - self.point_1.Y) ** 2 +
                (self.point_0.Z - self.point_1.Z) ** 2) ** 0.5

    def __get_y_by_x(self, x):
        x1, x2 = self.point_0.X, self.point_1.X
        y1, y2 = self.point_0.Y, self.point_1.Y
        y = ((x - x1)*(y2 - y1)) / (x2 - x1) + y1
        return y

    def __get_x_by_y(self, y):
        x1, x2 = self.point_0.X, self.point_1.X
        y1, y2 = self.point_0.Y, self.point_1.Y
        x = ((y - y1) * (x2 - x1)) / (y2 - y1) + x1
        return x

    def get_grid_cross_points_list(self, grid_step):
        points = set()
        x1, x2 = self.point_0.X, self.point_1.X
        y1, y2 = self.point_0.Y, self.point_1.Y
        points.add((x1, y1))
        points.add((x2, y2))
        x, y = min(x1, x2), min(y1, y2)
        x_max, y_max = max(x1, x2), max(y1, y2)
        while True:
            x += grid_step
            grid_x = x // grid_step * grid_step
            if grid_x < x_max:
                grid_y = self.__get_y_by_x(grid_x)
                points.add((grid_x, grid_y))
            else:
                break
        while True:
            y += grid_step
            grid_y = y // grid_step * grid_step
            if grid_y < y_max:
                grid_x = self.__get_x_by_y(grid_y)
                points.add((grid_x, grid_y))
            else:
                break
        points = sorted(list(points), key=lambda x: (x[0], x[1]))
        points = [Point(X=point[0], Y=point[1], Z=0,
                        R=0, G=0, B=0) for point in points]
        return points


if __name__ == "__main__":
    p0 = Point(-10, 0, 0, 0, 0, 0)
    p1 = Point(10, 0, 0, 0, 0, 0)
    p2 = Point(0, 10, 0, 0, 0, 0)
    p3 = Point(10, 9, 0, 0, 0, 0)

    l1 = Line(p0, p3)
    print(l1)
    points = l1.get_grid_cross_points_list(2)
    print(points)

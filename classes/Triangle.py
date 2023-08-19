from classes.Point import Point


class Triangle:

    __slots__ = ["id", "point_0", "point_1", "point_2", "r", "mse", "vv"]

    def __init__(self, point_0: Point, point_1: Point, point_2: Point, r=None, mse=None, id_=None):
        self.id = id_
        self.point_0 = point_0
        self.point_1 = point_1
        self.point_2 = point_2
        self.r = r
        self.mse = mse

    def __str__(self):
        return f"{self.__class__.__name__} " \
               f"[id: {self.id}\t[[Point_0: [id: {self.point_0.id},\t" \
               f"x: {self.point_0.X} y: {self.point_0.Y} z: {self.point_0.Z}]\t" \
               f"\t\t [Point_1: [id: {self.point_1.id},\t" \
               f"x: {self.point_1.X} y: {self.point_1.Y} z: {self.point_1.Z}]\t" \
               f"\t\t [Point_2: [id: {self.point_2.id},\t" \
               f"x: {self.point_2.X} y: {self.point_2.Y} z: {self.point_2.Z}]\t" \
               f"r: {self.r},\tmse: {self.mse}"
    # def __str__(self):
    #     return f"{self.__class__.__name__} " \
    #            f"[id: {self.id}\t[[Point_0: [id: {self.point_0.id},\t" \
    #            f"x: {self.point_0.X} y: {self.point_0.Y} z: {self.point_0.Z},\t" \
    #            f"RGB: ({self.point_0.R},{self.point_0.G},{self.point_0.B})]\n" \
    #            f"\t\t [Point_1: [id: {self.point_1.id},\t" \
    #            f"x: {self.point_1.X} y: {self.point_1.Y} z: {self.point_1.Z},\t" \
    #            f"RGB: ({self.point_1.R},{self.point_1.G},{self.point_1.B})]\n" \
    #            f"\t\t [Point_2: [id: {self.point_2.id},\t" \
    #            f"x: {self.point_2.X} y: {self.point_2.Y} z: {self.point_2.Z},\t" \
    #            f"RGB: ({self.point_2.R},{self.point_2.G},{self.point_2.B})]]]"

    def __repr__(self):
        return f"{self.__class__.__name__} [id={self.id}, points=[{self.point_0.id}-" \
               f"{self.point_1.id}-{self.point_2.id}]]"

    def __iter__(self):
        point_lst = [self.point_0, self.point_1, self.point_2]
        return iter(point_lst)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if not isinstance(other, Triangle):
            raise TypeError("Операнд справа должен иметь тип Triangle")
        if hash(self) == hash(other) or self.id is None or other.id is None:
            return (self.point_0 == other.point_0) and \
                   (self.point_1 == other.point_1) and \
                   (self.point_2 == other.point_2)
        return False

    def get_z_from_xy(self, x, y):
        """
        Рассчитывает отметку точки (x, y) в плоскости треугольника
        :param x: координата x
        :param y: координата y
        :return: координата z для точки (x, y)
        """
        a = -((self.point_1.Y - self.point_0.Y) * (self.point_2.Z - self.point_0.Z) -
              (self.point_2.Y - self.point_0.Y) * (self.point_1.Z - self.point_0.Z))
        b = ((self.point_1.X - self.point_0.X) * (self.point_2.Z - self.point_0.Z) -
             (self.point_2.X - self.point_0.X) * (self.point_1.Z - self.point_0.Z))
        c = -((self.point_1.X - self.point_0.X) * (self.point_2.Y - self.point_0.Y) -
              (self.point_2.X - self.point_0.X) * (self.point_1.Y - self.point_0.Y))
        d = -(self.point_0.X * a + self.point_0.Y * b + self.point_0.Z * c)
        z = (a * x + b * y + d) / -c
        return z

    def get_area(self):
        a = ((self.point_1.X - self.point_0.X)**2 + (self.point_1.Y - self.point_0.Y)**2) ** 0.5
        b = ((self.point_2.X - self.point_1.X)**2 + (self.point_2.Y - self.point_1.Y)**2) ** 0.5
        c = ((self.point_0.X - self.point_2.X)**2 + (self.point_0.Y - self.point_2.Y)**2) ** 0.5
        p = (a + b + c) / 2
        s = (p * (p - a) * (p - b) * (p - c)) ** 0.5
        return s

    def is_point_in_triangle(self, point: Point):
        s_abc = self.get_area()
        if s_abc == 0:
            return False
        s_ab_p = Triangle(self.point_0, self.point_1, point).get_area()
        s_bc_p = Triangle(self.point_1, self.point_2, point).get_area()
        s_ca_p = Triangle(self.point_2, self.point_0, point).get_area()
        delta_s = abs(s_abc - (s_ab_p + s_bc_p + s_ca_p))
        if delta_s < 1e-6:
            return True
        return False

    # def is_point_in_triangle(self, point: Point):
    #     x1 = self.point_1.X - self.point_0.X
    #     y1 = self.point_1.Y - self.point_0.Y
    #     x2 = self.point_2.X - self.point_0.X
    #     y2 = self.point_2.Y - self.point_0.Y
    #     p_x = point.X - self.point_0.X
    #     p_y = point.Y - self.point_0.Y
    #     mu = (p_x*y1 - p_y*x1) / (x2*y1 - x1*y2)
    #     if 0 <= mu <= 1:
    #         lambda_ = (p_x - mu * x2) / x1
    #         if (lambda_ >= 0) and ((mu + lambda_) <= 1):
    #             return True
    #     return False

    # def is_point_in_triangle(self, point: Point):
    #     ab_x = self.point_1.X - self.point_0.X
    #     ab_y = self.point_1.Y - self.point_0.Y
    #     ac_x = self.point_2.X - self.point_0.X
    #     ac_y = self.point_2.Y - self.point_0.Y
    #     ap_x = point.X - self.point_0.X
    #     ap_y = point.Y - self.point_0.Y
    #
    #     u = (ap_x*ab_x + ap_y*ab_y) / (ab_x**2 + ab_y**2)
    #     v = (ap_x*ac_x + ap_y*ac_y) / (ac_x**2 + ac_y**2)
    #     print(u, v)
    #     if (0 <= u <= 1) and (0 <= v <= 1) and (u + v <= 1):
    #         return True
    #     return False

    @classmethod
    def parse_triangle_from_db_row(cls, row: tuple):
        """
        Метод который создает и возвращает объект Triangle по данным читаемым из БД
        :param row: кортеж данных читаемых из БД
        :return: объект класса Triangle
        """
        id_ = row[0]
        r = row[1]
        mse = row[2]
        point_0 = Point.parse_point_from_db_row(row[3:10])
        point_1 = Point.parse_point_from_db_row(row[10:17])
        point_2 = Point.parse_point_from_db_row(row[17:])
        return cls(id_=id_, r=r, mse=mse, point_0=point_0, point_1=point_1, point_2=point_2)

    def get_dict(self):
        return {"id": self.id,
                "r": self.r,
                "mse": self.mse,
                "point_0": self.point_0.get_dict(),
                "point_1": self.point_1.get_dict(),
                "point_2": self.point_2.get_dict()}


if __name__ == "__main__":
    p0 = Point(0, 0, 1, 0, 0, 0)
    p1 = Point(10, 0, 0, 0, 0, 0)
    p2 = Point(0, 10, 28.01, 0, 0, 0)
    p3 = Point(20, 0, 0, 0, 0, 0)
    p4 = Point(5, 5, 5, 0, 0, 0)
    p = Point(1, -0.001, 5, 0, 0, 0)
    tri = Triangle(p0, p1, p2)
    print(tri.get_z_from_xy(1, 1))
    print(tri.is_point_in_triangle(p))

from classes.DemTypeEnum import DemTypeEnum
from classes.Point import Point
from classes.Polynomial2CellDB import Polynomial2CellDB
from classes.Polynomial2ModelDB import Polynomial2ModelDB
from classes.abc_classes.SegmentedModelABC import SegmentedModelABC


class Polynomial2Model3x3DB(Polynomial2ModelDB):

    def __init__(self, voxel_model, buffer_zone=None):
        self.buffer_zone = buffer_zone
        self.model_type = f"{DemTypeEnum.POLYNOMIAL_2.name}_3x3_buffer_zone_{self.buffer_zone}"
        self.model_name = f"{self.model_type}_from_{voxel_model.vm_name}"
        self.mse_data = None
        self.cell_type = Polynomial2CellDB
        SegmentedModelABC.__init__(self, voxel_model, self.cell_type)

    def _find_cells_for_point(self, point):
        points = self.__find_points_for_cells_search(point)
        cells = []
        for point in points:
            cell = self.get_model_element_for_point(point)
            if cell is not None:
                cells.append(cell)
        return cells

    def __find_points_for_cells_search(self, point):
        if self.buffer_zone is None:
            return self.__points_for_3x3_zone(point)
        else:
            return self.__points_for_custom_buffer_zone(point)

    def __points_for_3x3_zone(self, point):
        x, y, z = point.X, point.Y, point.Z
        step = self.voxel_model.step
        points = [Point(X=x - step, Y=y - step, Z=z, R=1, G=1, B=1),
                  Point(X=x, Y=y - step, Z=z, R=1, G=1, B=1),
                  Point(X=x + step, Y=y - step, Z=z, R=1, G=1, B=1),
                  Point(X=x - step, Y=y, Z=z, R=1, G=1, B=1),
                  point,
                  Point(X=x + step, Y=y, Z=z, R=1, G=1, B=1),
                  Point(X=x - step, Y=y + step, Z=z, R=1, G=1, B=1),
                  Point(X=x, Y=y + step, Z=z, R=1, G=1, B=1),
                  Point(X=x + step, Y=y + step, Z=z, R=1, G=1, B=1)]
        return points

    def __points_for_custom_buffer_zone(self, point):
        if self.buffer_zone < 0 or self.buffer_zone > 1:
            raise ValueError(f"Значение buffer_zone должно быть в пределах от 0 до 1 переданно ({self.buffer_zone})")
        x, y, z = point.X, point.Y, point.Z
        step = self.voxel_model.step
        x0 = x // step * step
        y0 = y // step * step
        buffer = self.buffer_zone * step
        points = [point]
        d_left, d_right = x - x0, x0 + step - x
        d_down, d_up = y - y0, y0 + step - y
        r_left_down = (d_left ** 2 + d_down ** 2) ** 0.5
        r_left_up = (d_left ** 2 + d_up ** 2) ** 0.5
        r_right_down = (d_right ** 2 + d_down ** 2) ** 0.5
        r_right_up = (d_right ** 2 + d_up ** 2) ** 0.5
        if r_left_down <= buffer:
            points.append(Point(X=x - step, Y=y - step, Z=z, R=1, G=1, B=1))
        if d_down <= buffer:
            points.append(Point(X=x, Y=y - step, Z=z, R=1, G=1, B=1))
        if r_right_down <= buffer:
            points.append(Point(X=x + step, Y=y - step, Z=z, R=1, G=1, B=1))
        if d_left <= buffer:
            points.append(Point(X=x - step, Y=y, Z=z, R=1, G=1, B=1))
        if d_right <= buffer:
            points.append(Point(X=x + step, Y=y, Z=z, R=1, G=1, B=1))
        if r_left_up <= buffer:
            points.append(Point(X=x - step, Y=y + step, Z=z, R=1, G=1, B=1))
        if d_up <= buffer:
            points.append(Point(X=x, Y=y + step, Z=z, R=1, G=1, B=1))
        if r_right_up <= buffer:
            points.append(Point(X=x + step, Y=y + step, Z=z, R=1, G=1, B=1))
        return points

    def _calk_matrix_params(self, base_scan):
        """
        Расчитывает коэфициенты матрицы нормальных уравнений
        :param base_scan: базовый скан воксельной модели
        :return: None
        """
        for point in base_scan:
            cells = self._find_cells_for_point(point)
            for cell in cells:
                x = point.X - (cell.voxel.X + cell.voxel.step / 2)
                y = point.Y - (cell.voxel.Y + cell.voxel.step / 2)
                a, b = x ** 2, y ** 2
                c = x * y
                d, e, f = x, y, 1
                try:
                    cell.aa += a * a
                    cell.ab += a * b
                    cell.ac += a * c
                    cell.ad += a * d
                    cell.ae += a * e
                    cell.af += a * f
                    cell.bb += b * b
                    cell.bc += b * c
                    cell.bd += b * d
                    cell.be += b * e
                    cell.bf += b * f
                    cell.cc += c * c
                    cell.cd += c * d
                    cell.ce += c * e
                    cell.cf += c * f
                    cell.dd += d * d
                    cell.de += d * e
                    cell.df += d * f
                    cell.ee += e * e
                    cell.ef += e * f
                    cell.ff += f * f

                    cell.az += a * point.Z
                    cell.bz += b * point.Z
                    cell.cz += c * point.Z
                    cell.dz += d * point.Z
                    cell.ez += e * point.Z
                    cell.fz += f * point.Z
                except AttributeError:
                    cell.aa = a * a
                    cell.ab = a * b
                    cell.ac = a * c
                    cell.ad = a * d
                    cell.ae = a * e
                    cell.af = a * f
                    cell.bb = b * b
                    cell.bc = b * c
                    cell.bd = b * d
                    cell.be = b * e
                    cell.bf = b * f
                    cell.cc = c * c
                    cell.cd = c * d
                    cell.ce = c * e
                    cell.cf = c * f
                    cell.dd = d * d
                    cell.de = d * e
                    cell.df = d * f
                    cell.ee = e * e
                    cell.ef = e * f
                    cell.ff = f * f

                    cell.az = a * point.Z
                    cell.bz = b * point.Z
                    cell.cz = c * point.Z
                    cell.dz = d * point.Z
                    cell.ez = e * point.Z
                    cell.fz = f * point.Z
        self.logger.info(f"Рассчет элементов матрицы нормальных коэфициентов модели {self.model_name} завершен")

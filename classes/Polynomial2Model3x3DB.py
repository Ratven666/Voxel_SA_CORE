from classes.DemTypeEnum import DemTypeEnum
from classes.Point import Point
from classes.Polynomial2CellDB import Polynomial2CellDB
from classes.Polynomial2ModelDB import Polynomial2ModelDB
from classes.abc_classes.SegmentedModelABC import SegmentedModelABC


class Polynomial2Model3x3DB(Polynomial2ModelDB):

    def __init__(self, voxel_model):
        self.model_type = DemTypeEnum.POLYNOMIAL_2_3x3
        self.model_name = f"{self.model_type.name}_from_{voxel_model.vm_name}"
        self.mse_data = None
        self.cell_type = Polynomial2CellDB
        SegmentedModelABC.__init__(self, voxel_model, self.cell_type)

    def _find_cells_for_point(self, point):
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
        cells = []
        for point in points:
            cell = self.get_model_element_for_point(point)
            if cell is not None:
                cells.append(cell)
        return cells

    def _calk_matrix_params(self, base_scan):
        """
        Расчитывает коэфициенты матрицы нормальных уравнений
        :param base_scan: базовый скан воксельной модели
        :return: None
        """
        for point in base_scan:
            cells = self._find_cells_for_point(point)
            for cell in cells:
                X = point.X - (cell.voxel.X + cell.voxel.step / 2)
                Y = point.Y - (cell.voxel.Y + cell.voxel.step / 2)
                a, b = X ** 2, Y ** 2
                c = X * Y
                d, e, f = X, Y, 1
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
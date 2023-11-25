import numpy as np

from classes.DemTypeEnum import DemTypeEnum
from classes.Polynomial2CellDB import Polynomial2CellDB
from classes.ScanDB import ScanDB
from classes.abc_classes.SegmentedModelABC import SegmentedModelABC


class Polynomial2ModelDB(SegmentedModelABC):
    """
    Polynomial2  модель связанная с базой данных
    """

    def __init__(self, voxel_model):
        self.model_type = DemTypeEnum.POLYNOMIAL_2.name
        self.model_name = f"{self.model_type}_from_{voxel_model.vm_name}"
        self.mse_data = None
        self.cell_type = Polynomial2CellDB
        super().__init__(voxel_model, self.cell_type)

    def _calk_segment_model(self):
        """
        Метод определяющий логику создания плоскостной модели
        :return: None
        """
        self.logger.info(f"Начат расчет модели {self.model_name}")
        base_scan = ScanDB.get_scan_from_id(self.voxel_model.base_scan_id)
        self.__fit_polynomials(base_scan)
        self.logger.info(f"Рассчитаны плоскости в модели {self.model_name}")
        self._calk_cell_mse(base_scan)
        self.__calk_abcdef_mse()
        self.logger.info(f"Рассчитаны СКП модели {self.model_name}")

    def __fit_polynomials(self, base_scan):
        self._calk_matrix_params(base_scan)
        for cell in self:
            try:
                m_n = np.array([[cell.aa, cell.ab, cell.ac, cell.ad, cell.ae, cell.af],
                                [cell.ab, cell.bb, cell.bc, cell.bd, cell.be, cell.bf],
                                [cell.ac, cell.bc, cell.cc, cell.cd, cell.ce, cell.cf],
                                [cell.ad, cell.bd, cell.cd, cell.dd, cell.de, cell.df],
                                [cell.ae, cell.be, cell.ce, cell.de, cell.ee, cell.ef],
                                [cell.af, cell.bf, cell.cf, cell.df, cell.ef, cell.ff]])
                m_d = np.array([cell.az, cell.bz, cell.cz, cell.dz, cell.ez, cell.fz])
            except AttributeError:
                continue
            try:
                abc = np.linalg.solve(m_n, m_d)
            except np.linalg.LinAlgError:
                cell.r = -1
                continue
            cell.a = float(abc[0])
            cell.b = float(abc[1])
            cell.c = float(abc[2])
            cell.d = float(abc[3])
            cell.e = float(abc[4])
            cell.f = float(abc[5])
            cell.Q = np.linalg.inv(m_n)
        self.logger.info(f"Расчет параметров вписываемых плоскостей модели {self.model_name} завершен")

    def __calk_abcdef_mse(self):
        for cell in self:
            if cell.r <= 0:
                continue
            try:
                D = np.diagonal(cell.Q)
                abcdef_mse = np.sqrt(D) * cell.mse
                cell.m_a, cell.m_b, cell.m_c = float(abcdef_mse[0]), float(abcdef_mse[1]), float(abcdef_mse[2])
                cell.m_d, cell.m_e, cell.m_f = float(abcdef_mse[3]), float(abcdef_mse[4]), float(abcdef_mse[5])
            except AttributeError:
                continue

    def _calk_matrix_params(self, base_scan):
        """
        Расчитывает коэфициенты матрицы нормальных уравнений
        :param base_scan: базовый скан воксельной модели
        :return: None
        """
        for point in base_scan:
            cell = self.get_model_element_for_point(point)
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

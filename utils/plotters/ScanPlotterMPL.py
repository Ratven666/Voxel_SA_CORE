import logging

import matplotlib.pyplot as plt

from CONFIG import MAX_POINT_SCAN_PLOT, LOGGER
from utils.plotters.PlotterABC import PlotterABC
from utils.scan_utils.scan_samplers.TotalPointCountScanSampler import TotalPointCountScanSampler


class ScanPlotterMPL(PlotterABC):
    """
    Отрисовка скана в 3D через библиотеку matplotlib
    """

    __logger = logging.getLogger(LOGGER)

    def __init__(self, sampler=TotalPointCountScanSampler(MAX_POINT_SCAN_PLOT)):
        super().__init__()
        self.__fig = None
        self.__ax = None
        self.__sampler = sampler

    def __calk_plot_limits(self, scan):
        """
        Рассчитывает область построения скана для сохранения пропорций вдоль осей
        :param scan: скан который будет отрисовываться
        :return: Словарь с пределами построения модель вдоль трех осей
        """
        min_x, min_y, min_z = scan.min_X, scan.min_Y, scan.min_Z
        max_x, max_y, max_z = scan.max_X, scan.max_Y, scan.max_Z
        try:
            limits = [max_x - min_x,
                      max_y - min_y,
                      max_z - min_z]
        except TypeError:
            self.__logger.critical(f"Не рассчитаны значения границ в скане \"{scan.scan_name}\". "
                                   f"Невозможно рассчитать область построения модели.")
            return
        length = max(limits) / 2
        x_lim = [((min_x + max_x) / 2) - length, ((min_x + max_x) / 2) + length]
        y_lim = [((min_y + max_y) / 2) - length, ((min_y + max_y) / 2) + length]
        z_lim = [((min_z + max_z) / 2) - length, ((min_z + max_z) / 2) + length]
        return {"X_lim": x_lim, "Y_lim": y_lim, "Z_lim": z_lim}

    def __set_plot_limits(self, plot_limits):
        """
        Устанавливает в графике области построения в соответствии с переданными значениями
        :param plot_limits: словарь с границами области построения
        :return: None
        """
        try:
            self.__ax.set_xlim(*plot_limits["X_lim"])
            self.__ax.set_ylim(*plot_limits["Y_lim"])
            self.__ax.set_zlim(*plot_limits["Z_lim"])
        except TypeError:
            self.__logger.critical(f"Переданны некорректные лимиты области модели.")

    def plot(self, scan):
        """
        Отрисовка скана в 3D
        :param scan: скан который будет отрисовываться
        :return: None
        """
        self.__fig = plt.figure()
        self.__ax = self.__fig.add_subplot(projection="3d")
        if self.__sampler is not None:
            scan = self.__sampler.do_sampling(scan)
        x_lst, y_lst, z_lst, c_lst = [], [], [], []
        for point in scan:
            x_lst.append(point.X)
            y_lst.append(point.Y)
            z_lst.append(point.Z)
            c_lst.append([point.R / 255.0, point.G / 255.0, point.B / 255.0])
        self.__set_plot_limits(self.__calk_plot_limits(scan))
        self.__ax.scatter(x_lst, y_lst, z_lst, c=c_lst, marker="+", s=2)
        plt.show()

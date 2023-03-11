import logging

import plotly.express as px
import plotly.graph_objects as go

from CONFIG import LOGGER, MAX_POINT_SCAN_PLOT
from utils.plotters.PlotterABC import PlotterABC
from utils.scan_utils.scan_samplers.TotalPointCountScanSampler import TotalPointCountScanSampler


class _ScanPlotterMeshPlotly(PlotterABC):
    # __logger = logging.getLogger(LOGGER)

    def __init__(self, sampler=TotalPointCountScanSampler(MAX_POINT_SCAN_PLOT)):
        super().__init__(sampler)
        # self.__sampler = sampler

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

    def plot(self, scan):
        if self.__sampler is not None:
            scan = self.__sampler.do_sampling(scan)
        x_lst, y_lst, z_lst, c_lst = [], [], [], []
        for point in scan:
            x_lst.append(point.X)
            y_lst.append(point.Y)
            z_lst.append(point.Z)
        fig = go.Figure(data=[go.Mesh3d(x=x_lst,
                                        y=y_lst,
                                        z=z_lst,
                                        opacity=0.7,
                                        cmin=scan.min_Z,
                                        cmax=scan.max_Z,
                                        colorscale="Earth",
                                        contour=go.mesh3d.Contour(color="red", show=True, width=5)
                                        )])

        pl = self.__calk_plot_limits(scan)
        fig.update_layout(
            scene=dict(
                xaxis=dict(range=pl["X_lim"], ),
                yaxis=dict(range=pl["Y_lim"], ),
                zaxis=dict(range=pl["Z_lim"], ), ),
            margin=dict(r=10, l=10, b=10, t=10))

        fig.show()

from abc import abstractmethod

import plotly.graph_objects as go
import numpy as np
from scipy.spatial import Delaunay

from CONFIG import MAX_POINT_SCAN_PLOT
from utils.plotters.PlotterABC import PlotterABC
from utils.scan_utils.scan_samplers.TotalPointCountScanSampler import TotalPointCountScanSampler


class ScanPlotterPlotly(PlotterABC):
    def __init__(self, sampler=TotalPointCountScanSampler(MAX_POINT_SCAN_PLOT)):
        super().__init__(sampler)

    def set_plot_limits(self, scan, fig):
        pl = self.calk_plot_limits(scan)
        fig.update_layout(
            scene=dict(
                xaxis=dict(range=pl["X_lim"]),
                yaxis=dict(range=pl["Y_lim"]),
                zaxis=dict(range=pl["Z_lim"])),
            margin=dict(r=10, l=10, b=10, t=10))

    @abstractmethod
    def plot(self, scan):
        pass


class ScanPlotterPointsPlotly(ScanPlotterPlotly):
    def __init__(self, sampler=TotalPointCountScanSampler(MAX_POINT_SCAN_PLOT), point_size=5):
        super().__init__(sampler)
        self.__point_size = point_size

    def plot(self, scan):
        plot_data = self.sample_data(scan)
        fig = go.Figure(data=[go.Scatter3d(x=plot_data["x"],
                                           y=plot_data["y"],
                                           z=plot_data["z"],
                                           mode="markers",
                                           marker=dict(
                                               size=self.__point_size,
                                               color=plot_data["z"],
                                               opacity=1,
                                               colorscale="Rainbow"
                                           )
                                           )])
        self.set_plot_limits(scan, fig)
        fig.show()


class ScanPlotterMeshPlotly(ScanPlotterPlotly):
    def __init__(self, sampler=TotalPointCountScanSampler(MAX_POINT_SCAN_PLOT)):
        super().__init__(sampler)

    @staticmethod
    def __calk_delone_triangulation(plot_data):
        points2D = np.vstack([plot_data["x"], plot_data["y"]]).T
        tri = Delaunay(points2D)
        i_lst, j_lst, k_lst = ([triplet[c] for triplet in tri.simplices] for c in range(3))
        return {"i_lst": i_lst, "j_lst": j_lst, "k_lst": k_lst}

    @staticmethod
    def __calk_faces_colors(ijk_dict, plot_data):
        c_lst = []
        for idx in range(len(ijk_dict["i_lst"])):
            c_i = plot_data["color"][ijk_dict["i_lst"][idx]]
            c_j = plot_data["color"][ijk_dict["j_lst"][idx]]
            c_k = plot_data["color"][ijk_dict["k_lst"][idx]]
            r = round((c_i[0] + c_j[0] + c_k[0]) / 3)
            g = round((c_i[1] + c_j[1] + c_k[1]) / 3)
            b = round((c_i[2] + c_j[2] + c_k[2]) / 3)
            c_lst.append(f"rgb({r}, {g}, {b})")
        return c_lst

    def plot(self, scan):
        plot_data = self.sample_data(scan)

        ijk_dict = self.__calk_delone_triangulation(plot_data)
        c_lst = self.__calk_faces_colors(ijk_dict, plot_data)

        fig = go.Figure(data=[go.Mesh3d(x=plot_data["x"],
                                        y=plot_data["y"],
                                        z=plot_data["z"],
                                        i=ijk_dict["i_lst"],
                                        j=ijk_dict["j_lst"],
                                        k=ijk_dict["k_lst"],
                                        opacity=1,
                                        facecolor=c_lst,
                                        )])
        self.set_plot_limits(scan, fig)
        fig.show()

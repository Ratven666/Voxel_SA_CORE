import numpy as np
import plotly.graph_objects as go


class SubsidenceModelPlotlyPlotter:

    def __init__(self):
        self.model = None

    def plot(self, model):
        self.model = model

        x = np.full((self.model.voxel_model.X_count * 2), None)
        y = np.full((self.model.voxel_model.Y_count * 2), None)
        z = np.full((self.model.voxel_model.Y_count * 2,
                     self.model.voxel_model.X_count * 2), None)
        mse = np.full((self.model.voxel_model.Y_count * 2,
                       self.model.voxel_model.X_count * 2), None)
        subs = np.full((self.model.voxel_model.Y_count * 2,
                       self.model.voxel_model.X_count * 2), None)
        slope = np.full((self.model.voxel_model.Y_count * 2,
                       self.model.voxel_model.X_count * 2), None)
        curvature = np.full((self.model.voxel_model.Y_count * 2,
                            self.model.voxel_model.X_count * 2), None)
        subsidence_class = np.full((self.model.voxel_model.Y_count * 2,
                                   self.model.voxel_model.X_count * 2), None)

        for cell in self.model:
            x0 = cell.voxel.X
            y0 = cell.voxel.Y
            step = cell.voxel.step

            try:
                i, j = self.__calk_indexes(cell)
            except TypeError:
                continue
            z[j][i] = cell.get_ref_z_from_xy(x0 + 1e-9, y0 + 1e-9)
            z[j + 1][i] = cell.get_ref_z_from_xy(x0 + 1e-9, y0 + step - 1e-9)
            z[j][i + 1] = cell.get_ref_z_from_xy(x0 + step - 1e-9, y0 + 1e-9)
            z[j + 1][i + 1] = cell.get_ref_z_from_xy(x0 + step - 1e-9, y0 + step - 1e-9)
            mse[j][i] = cell.subsidence_mse
            mse[j + 1][i] = cell.subsidence_mse
            mse[j][i + 1] = cell.subsidence_mse
            mse[j + 1][i + 1] = cell.subsidence_mse
            subs[j][i] = cell.subsidence
            subs[j + 1][i] = cell.subsidence
            subs[j][i + 1] = cell.subsidence
            subs[j + 1][i + 1] = cell.subsidence
            slope[j][i] = cell.slope
            slope[j + 1][i] = cell.slope
            slope[j][i + 1] = cell.slope
            slope[j + 1][i + 1] = cell.slope
            curvature[j][i] = cell.curvature
            curvature[j + 1][i] = cell.curvature
            curvature[j][i + 1] = cell.curvature
            curvature[j + 1][i + 1] = cell.curvature
            subsidence_class[j][i] = cell.subsidence_class
            subsidence_class[j + 1][i] = cell.subsidence_class
            subsidence_class[j][i + 1] = cell.subsidence_class
            subsidence_class[j + 1][i + 1] = cell.subsidence_class

            x[i], x[i + 1] = x0, x0 + step
            y[j], y[j + 1] = y0, y0 + step
        fig = go.Figure()

        fig.add_trace(go.Surface(x=x,
                                 y=y,
                                 z=z,
                                 surfacecolor=subs,
                                 colorscale="RdYlGn_r"))

        fig.add_trace(go.Surface(x=x,
                                 y=y,
                                 z=z,
                                 surfacecolor=slope,
                                 colorscale="RdYlGn_r"))

        fig.add_trace(go.Surface(x=x,
                                 y=y,
                                 z=z,
                                 surfacecolor=curvature,
                                 colorscale="RdYlGn_r"))

        fig.add_trace(go.Surface(x=x,
                                 y=y,
                                 z=z,
                                 surfacecolor=mse,
                                 colorscale="Rainbow_r"))

        fig.add_trace(go.Surface(x=x,
                                 y=y,
                                 z=z,
                                 surfacecolor=subsidence_class,
                                 colorscale=[[0, "red"], [0.5, "green"], [1, "blue"]]))
                                 # colorscale="Rainbow_r"))

        button_layer_1_height = 1.02
        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=[{"visible": [True, False, False, False, False]}],
                            label="subsidence",
                            method="update"
                        ),
                        dict(
                            args=[{"visible": [False, True, False, False, False]}],
                            label="slope",
                            method="update"
                        ),
                        dict(
                            args=[{"visible": [False, False, True, False, False]}],
                            label="curvature",
                            method="update"
                        ),
                        dict(
                            args=[{"visible": [False, False, False, True, False]}],
                            label="MSE",
                            method="update"
                        ),
                        dict(
                            args=[{"visible": [False, False, False, False, True]}],
                            label="Class",
                            method="update"
                        ),
                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.37,
                    xanchor="left",
                    y=button_layer_1_height,
                    yanchor="top"
                ),
            ]
        )
        width, height = self.__calk_sizes()
        fig.update_layout(
            width=width,
            height=height,
            autosize=False,
            margin=dict(t=100, b=0, l=0, r=0),
        )

        pl = self.__calk_plot_limits()
        fig.update_layout(
            scene=dict(
                xaxis=dict(range=pl["X_lim"]),
                yaxis=dict(range=pl["Y_lim"]),
                # zaxis=dict(range=pl["Z_lim"]),
            ),
            margin=dict(r=10, l=10, b=10, t=10))

        fig.update_layout(title_text=f"Model {self.model.model_name}")

        fig.update_layout(
            annotations=[
                dict(text="Texture<br>Type", x=0.25, xref="paper", y=1.01,
                     yref="paper", showarrow=False),
            ])

        fig.update_layout(
            scene={
                'camera_eye': {"x": 0, "y": -2, "z": 1},
            })

        fig.show()

    def __calk_indexes(self, cell):
        """
        Рассчитывает индексы вокселя внутри модели по трем осям
        на основании координат вокселя, его размера и области модели
        :param cell: ячейка для которой выполняется расчет индекса
        :return: кортеж с индексами ячейки модели
        """
        try:
            voxel = cell.voxel
        except AttributeError:
            return None
        x0 = self.model.voxel_model.min_X
        y0 = self.model.voxel_model.min_Y
        i = (int((voxel.X - x0 + 1e-9) / self.model.voxel_model.step)) * 2
        j = (int((voxel.Y - y0 + 1e-9) / self.model.voxel_model.step)) * 2
        return i, j

    def __calk_sizes(self, width=1600):
        c = self.model.voxel_model.Y_count / self.model.voxel_model.X_count
        height = round(width * c)
        return width, height

    def __calk_plot_limits(self):
        """
        Рассчитывает область построения скана для сохранения пропорций вдоль осей
        :return: Словарь с пределами построения модель вдоль трех осей
        """
        model = self.model.voxel_model
        min_x, min_y, min_z = model.min_X, model.min_Y, model.min_Z
        max_x, max_y, max_z = model.max_X, model.max_Y, model.max_Z
        limits = [max_x - min_x,
                  max_y - min_y,
                  max_z - min_z]
        length = max(limits) / 2
        x_lim = [((min_x + max_x) / 2) - length, ((min_x + max_x) / 2) + length]
        y_lim = [((min_y + max_y) / 2) - length, ((min_y + max_y) / 2) + length]
        z_lim = [((min_z + max_z) / 2) - length, ((min_z + max_z) / 2) + length]
        return {"X_lim": x_lim, "Y_lim": y_lim, "Z_lim": z_lim}
import plotly.graph_objects as go


class DEMIndexPlotterPlotly:

    def __init__(self):
        self.model = None

    def plot(self, model):
        self.model = model
        ax_ticks = self.__calk_ax_ticks()
        fig = go.Figure()
        fig.add_trace(go.Heatmap(x=ax_ticks["x_ticks"],
                                 y=ax_ticks["y_ticks"],
                                 z=self.model.model_indexes,
                                 colorscale="RdYlGn_r"
                                 )
                      )
        width, height = self.__calk_sizes()
        fig.update_layout(
            width=width,
            height=height,
            autosize=False,
            margin=dict(t=100, b=0, l=0, r=0),
        )
        fig.update_scenes(
            aspectratio=dict(x=1, y=1, z=1),
            aspectmode="manual"
        )
        button_layer_1_height = 1.05
        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=["type", "heatmap"],
                            label="Heatmap",
                            method="restyle"
                        ),
                        dict(
                            args=[{"contours.showlabels": True, "type": "contour"}],
                            label="Contours",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "surface"],
                            label="3D Surface",
                            method="restyle"
                        )
                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.1,
                    xanchor="left",
                    y=button_layer_1_height,
                    yanchor="top"
                ),
            ]
        )
        fig.update_layout(
            annotations=[
                dict(text="Graph<br>Type", x=0, xref="paper", y=1.04,
                     yref="paper", showarrow=False),
            ])
        fig.update_layout(title_text=f"DEM_Index \"{self.model.__class__.__name__}\"")
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
        i = int((voxel.X - x0 + 1e-9) / self.model.voxel_model.step)
        j = int((voxel.Y - y0 + 1e-9) / self.model.voxel_model.step)
        return i, j

    def __calk_ax_ticks(self):
        """
        Рассчитывает корректные подписи по осям модели на основе координат вокселя
        :return: словарь с полдписями для осей
        """
        x_ticks = [self.model.dem_model.voxel_model.min_X + (idx + 0.5) * self.model.dem_model.voxel_model.step
                   for idx in range(self.model.dem_model.voxel_model.X_count)]
        y_ticks = [self.model.dem_model.voxel_model.min_Y + (idx + 0.5) * self.model.dem_model.voxel_model.step
                   for idx in range(self.model.dem_model.voxel_model.Y_count)]
        return {"x_ticks": x_ticks, "y_ticks": y_ticks}

    def __calk_sizes(self, width=800):
        c = self.model.dem_model.voxel_model.Y_count / self.model.dem_model.voxel_model.X_count
        height = round(width * c)
        return width, height

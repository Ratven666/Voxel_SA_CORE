from classes.Point import Point
from classes.branch_classes.deformation_classes.SubsidanсeCellDB import SubsidenceCellDB
from classes.branch_classes.deformation_classes.SubsidenceModelDB import SubsidenceModelDB
from classes.branch_classes.deformation_classes.plotters.SubsidenceHeatMapPlotlyPlotter import \
    SubsidenceHeatMapPlotlyPlotter
from classes.branch_classes.deformation_classes.plotters.SubsidenceHistSeabornPlotter import \
    SubsidenceHistSeabornPlotter
from classes.branch_classes.deformation_classes.plotters.SubsidenceModelPlotlyPlotter import \
    SubsidenceModelPlotlyPlotter


class SubsidenceModelWindowFilter:

    def __init__(self, subsidence_model: SubsidenceModelDB, window_size: int):
        self.subsidence_model = subsidence_model
        self.voxel_model = subsidence_model.voxel_model
        self.model_name = f"{self.subsidence_model.model_name}_w{window_size}"
        self.window_size = self._check_windows_size(window_size)
        self._model_structure = {}
        self._init_model()

    def __iter__(self):
        return iter(self._model_structure.values())

    def get_model_element_for_point(self, point):
        """
        Возвращает ячейку содержащую точку point
        :param point: точка для которой нужна соответствующая ячейка
        :return: объект ячейки модели, содержащая точку point
        """
        vxl_md_X = int((point.X - self.voxel_model.min_X) // self.voxel_model.step)
        vxl_md_Y = int((point.Y - self.voxel_model.min_Y) // self.voxel_model.step)
        X = self.voxel_model.min_X + vxl_md_X * self.voxel_model.step
        Y = self.voxel_model.min_Y + vxl_md_Y * self.voxel_model.step
        if self.voxel_model.is_2d_vxl_mdl is False:
            vxl_md_Z = int((point.Z - self.voxel_model.min_Z) // self.voxel_model.step)
            Z = self.voxel_model.min_Z + vxl_md_Z * self.voxel_model.step
        else:
            Z = self.voxel_model.min_Z
        model_key = f"{X:.5f}_{Y:.5f}_{Z:.5f}"
        return self._model_structure.get(model_key, None)

    # def get_model_element_for_point(self, point):
    #     return self.subsidence_model.get_model_element_for_point(point)

    def _init_model(self):
        for cell in self.subsidence_model:
            cells = self._get_cells_in_window(cell)
            filtered_cell = self._calk_filtered_cell(cell, self._mean_cell_filter)
            cell_key = self.subsidence_model.get_key_for_voxel(filtered_cell.voxel)
            self._model_structure[cell_key] = filtered_cell

    def _calk_filtered_cell(self, cell: SubsidenceCellDB, filter_func):
        new_cell = SubsidenceCellDB(cell.voxel, self)
        new_cell.voxel_id = cell.voxel_id
        new_cell.subsidence = cell.subsidence
        new_cell.subsidence_mse = cell.subsidence_mse
        cells = self._get_cells_in_window(new_cell)
        filtered_cell = filter_func(new_cell, cells)
        return filtered_cell

    @staticmethod
    def _mean_cell_filter(center_cell, cells):
        mean_subsidence = 0
        counter = 0
        for cell in cells:
            try:
                mean_subsidence += cell.subsidence
                counter += 1
            except TypeError:
                continue
        mean_subsidence = mean_subsidence / counter if counter > 0 else None
        center_cell.subsidence = mean_subsidence
        return center_cell

    def _get_cells_in_window(self, central_cell: SubsidenceCellDB):
        step = central_cell.voxel.step
        c_point = Point(X=central_cell.voxel.X + step / 2,
                        Y=central_cell.voxel.Y + step / 2,
                        Z=0, R=0, G=0, B=0)
        cells = []
        x0 = c_point.X - (self.window_size // 2) * step
        y0 = c_point.Y - (self.window_size // 2) * step
        for i in range(self.window_size):
            y = y0 + step * i
            for j in range(self.window_size):
                x = x0 + step * j
                cell = (self.subsidence_model.
                        get_model_element_for_point(Point(X=x, Y=y, Z=0, R=0, G=0, B=0)))
                if cell is not None:
                    cells.append(cell)
        return cells

    @staticmethod
    def _check_windows_size(window_size):
        if window_size % 2 == 1:
            return window_size
        raise ValueError(f"Window_size должен быть нечетным числом. Переданно - {window_size}")

    def plot_surface(self, plotter=SubsidenceModelPlotlyPlotter()):
        """
        Вывод отображения сегментированной модели
        :param plotter: объект определяющий логику отображения модели
        :return: None
        """
        plotter.plot(self)

    def plot_heat_map(self, plotter=SubsidenceHeatMapPlotlyPlotter()):
        plotter.plot(self)

    def plot_subsidence_hist(self, plotter=SubsidenceHistSeabornPlotter()):
        plotter.plot(self)

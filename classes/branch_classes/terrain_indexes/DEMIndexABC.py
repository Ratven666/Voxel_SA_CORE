from abc import ABC, abstractmethod

import numpy as np

from classes.Point import Point
from classes.branch_classes.terrain_indexes.DEMIndexPlotterPlotly import DEMIndexPlotterPlotly


class DEMIndexABC(ABC):

    def __init__(self, dem_model, full_neighbours):
        self.dem_model = dem_model
        self.full_neighbours = full_neighbours
        self.model_indexes = np.full((self.dem_model.voxel_model.Y_count,
                                      self.dem_model.voxel_model.X_count), None)
        self.__calk_model_indexes()
        self.i, self.j = 0, 0

    def __iter__(self):
        return self

    def __next__(self):
        for _ in range(self.dem_model.voxel_model.Y_count - 1):
            if self.i < self.dem_model.voxel_model.X_count:
                self.i += 1
                if self.j < self.dem_model.voxel_model.Y_count:
                    return self.model_indexes[self.j][self.i - 1]
            else:
                self.i = 0
                self.j += 1
        self.i, self.j = 0, 0
        raise StopIteration

    def __get_cell_neighbour_structure(self, cell):
        """
        Создает структуру соседних ячеек относительно ячейки cell
        :param cell: чентральная ячейка относительно которой ищутся соседи
        :return: 3х3 масив с ячейками относительно ячейки cell
        """
        step = cell.voxel.step
        x0, y0 = (cell.voxel.X + step / 2,
                  cell.voxel.Y + step / 2)
        neighbour_structure = [[(-step, -step), (-step, 0), (-step, step)],
                               [(0, -step), (0, 0), (0, step)],
                               [(step, -step), (step, 0), (step, step)]]
        for x in range(3):
            for y in range(3):
                dx, dy = neighbour_structure[x][y]
                point = Point(X=x0 + dx, Y=y0 + dy, Z=0, R=0, G=0, B=0)
                try:
                    cell = self.dem_model.get_model_element_for_point(point)
                    if cell is not None:
                        neighbour_structure[x][y] = cell.get_z_from_xy(point.X, point.Y)
                    else:
                        neighbour_structure[x][y] = None
                except KeyError:
                    neighbour_structure[x][y] = None
        return neighbour_structure

    def __get_indexes(self, cell):
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
        x0 = self.dem_model.voxel_model.min_X
        y0 = self.dem_model.voxel_model.min_Y
        i = int((voxel.X - x0 + 1e-9) / self.dem_model.voxel_model.step)
        j = int((voxel.Y - y0 + 1e-9) / self.dem_model.voxel_model.step)
        return i, j

    def __calk_model_indexes(self):
        for cell in self.dem_model:
            cell_index = self.calk_index_value(self.__get_cell_neighbour_structure(cell))
            i, j = self.__get_indexes(cell)
            self.model_indexes[j][i] = cell_index

    def get_index_for_point(self, point):
        cell = self.dem_model.get_model_element_for_point(point)
        try:
            i, j = self.__get_indexes(cell)
        except TypeError:
            return None
        return self.model_indexes[j][i]

    @abstractmethod
    def calk_index_value(self, cell_neighbour_structure):
        pass

    def plot(self, plotter=DEMIndexPlotterPlotly()):
        """
        Вывод распределения карты индексов
        :param plotter: объект определяющий логику отображения
        :return: None
        """
        plotter.plot(self)

import matplotlib.pyplot as plt
import numpy as np


class VoxelModelPlotter:

    def __init__(self):
        self.voxel_model = None

    def plot(self, voxel_model):
        self.voxel_model = voxel_model
        area = np.full((self.voxel_model.X_count,
                        self.voxel_model.Y_count,
                        self.voxel_model.Z_count), False)

        colors = np.zeros(area.shape + (3,))

        for voxel in self.voxel_model:
            i, j, k = self.__calk_indexes(voxel)
            area[i][j][k] = True
            colors[i][j][k][0] = voxel.R / 255.0
            colors[i][j][k][1] = voxel.G / 255.0
            colors[i][j][k][2] = voxel.B / 255.0

        ax = plt.figure().add_subplot(projection='3d')
        self.__set_plot_limits(ax, self.__calk_plot_limits(self.voxel_model))
        ax.voxels(area, facecolors=colors)

        plt.show()

    def __calk_indexes(self, voxel):
        x0 = self.voxel_model.min_X
        y0 = self.voxel_model.min_Y
        z0 = self.voxel_model.min_Z
        i = int((voxel.X - x0) / self.voxel_model.step)
        j = int((voxel.Y - y0) / self.voxel_model.step)
        k = int((voxel.Z - z0) / self.voxel_model.step)
        return i, j, k

    def __calk_plot_limits(self, vxl_mdl):
        """
        Рассчитывает область построения скана для сохранения пропорций вдоль осей
        :param scan: скан который будет отрисовываться
        :return: Словарь с пределами построения модель вдоль трех осей
        """
        min_x, min_y, min_z = vxl_mdl.min_X, vxl_mdl.min_Y, vxl_mdl.min_Z
        max_x, max_y, max_z = vxl_mdl.max_X, vxl_mdl.max_Y, vxl_mdl.max_Z

        limits = [vxl_mdl.X_count,
                  vxl_mdl.Y_count,
                  vxl_mdl.Z_count]
        length = max(limits)
        x_lim = [0, length]
        y_lim = [0, length]
        z_lim = [0, length]
        return {"X_lim": x_lim, "Y_lim": y_lim, "Z_lim": z_lim}

    # def __calk_plot_limits(self, vxl_mdl):
    #     """
    #     Рассчитывает область построения скана для сохранения пропорций вдоль осей
    #     :param scan: скан который будет отрисовываться
    #     :return: Словарь с пределами построения модель вдоль трех осей
    #     """
    #     min_x, min_y, min_z = vxl_mdl.min_X, vxl_mdl.min_Y, vxl_mdl.min_Z
    #     max_x, max_y, max_z = vxl_mdl.max_X, vxl_mdl.max_Y, vxl_mdl.max_Z
    #     try:
    #         limits = [max_x - min_x,
    #                   max_y - min_y,
    #                   max_z - min_z]
    #     except TypeError:
    #         self.logger.critical(f"Не рассчитаны значения границ в скане \"{vxl_mdl.vm_name}\". "
    #                                f"Невозможно рассчитать область построения модели.")
    #         return
    #     length = max(limits) / 2
    #     x_lim = [((min_x + max_x) / 2) - length - self.voxel_model.min_X,
    #              ((min_x + max_x) / 2) + length - self.voxel_model.min_X]
    #     y_lim = [((min_y + max_y) / 2) - length - self.voxel_model.min_Y,
    #              ((min_y + max_y) / 2) + length - self.voxel_model.min_Y]
    #     z_lim = [((min_z + max_z) / 2) - length - self.voxel_model.min_Z,
    #              ((min_z + max_z) / 2) + length - self.voxel_model.min_Z]
    #     return {"X_lim": x_lim, "Y_lim": y_lim, "Z_lim": z_lim}

    def __set_plot_limits(self, ax, plot_limits):
        """
        Устанавливает в графике области построения в соответствии с переданными значениями
        :param plot_limits: словарь с границами области построения
        :return: None
        """
        try:
            ax.set_xlim(*plot_limits["X_lim"])
            ax.set_ylim(*plot_limits["Y_lim"])
            ax.set_zlim(*plot_limits["Z_lim"])
        except TypeError:
            self.logger.critical(f"Переданны некорректные лимиты области модели.")

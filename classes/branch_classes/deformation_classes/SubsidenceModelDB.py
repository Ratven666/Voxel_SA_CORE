from sqlalchemy import select, insert

from classes.DemTypeEnum import DemTypeEnum
from classes.Point import Point
from classes.ScanDB import ScanDB
from classes.VoxelModelDB import VoxelModelDB
from classes.abc_classes.SegmentedModelABC import SegmentedModelABC
from classes.branch_classes.deformation_classes.SubsidanсeCellDB import SubsidenceCellDB
from classes.branch_classes.deformation_classes.plotters.SubsidenceHeatMapPlotlyPlotter import SubsidenceHeatMapPlotlyPlotter
from classes.branch_classes.deformation_classes.plotters.SubsidenceHistSeabornPlotter import SubsidenceHistSeabornPlotter
from classes.branch_classes.deformation_classes.plotters.SubsidenceModelPlotlyPlotter import SubsidenceModelPlotlyPlotter
from utils.start_db import engine


class SubsidenceModelDB(SegmentedModelABC):

    def __init__(self, reference_model: SegmentedModelABC,
                 comparable_model: SegmentedModelABC,
                 resolution_m=None,
                 border_subsidence=1
                 ):
        self.reference_model = reference_model
        self.comparable_model = comparable_model
        self.voxel_model = reference_model.voxel_model \
            if resolution_m is None or resolution_m == reference_model.voxel_model.step \
            else VoxelModelDB(scan=ScanDB.get_scan_from_id(reference_model.voxel_model.base_scan_id),
                              step=resolution_m,
                              is_2d_vxl_mdl=reference_model.voxel_model.is_2d_vxl_mdl,
                              )
        self.resolution = resolution_m if resolution_m is not None else reference_model.voxel_model.step
        self.border_subsidence = border_subsidence
        self.model_type = DemTypeEnum.SUBSIDENCE.name
        self.model_name = (f"{self.model_type}_ref_{reference_model.model_name}_{comparable_model.model_name}_"
                           f"res_{self.resolution}")
        self.mse_data = None
        self.cell_type = SubsidenceCellDB
        super().__init__(self.voxel_model, self.cell_type)

    def _calk_segment_model(self):
        """
        Метод определяющий логику создания стандартной DEM модели
        :return: None
        """
        self.logger.info(f"Начат расчет модели {self.model_name}")
        self._calk_subsidence()
        # base_scan = ScanDB.get_scan_from_id(self.voxel_model.base_scan_id)
        # self.__calk_average_z(base_scan)
        # self._calk_cell_mse(base_scan)

    def _calk_subsidence(self):
        for cell in self:
            x, y = cell.voxel.X + cell.voxel.step / 2, \
                   cell.voxel.Y + cell.voxel.step / 2
            center_point = Point(X=x, Y=y, Z=0, R=0, G=0, B=0)
            ref_cell = self.reference_model.get_model_element_for_point(point=center_point)
            comp_cell = self.comparable_model.get_model_element_for_point(point=center_point)
            if ref_cell is not None and comp_cell is not None:
                ref_z = ref_cell.get_z_from_xy(x, y)
                comp_z = comp_cell.get_z_from_xy(x, y)
                if ref_z is not None and comp_z is not None:
                    subsidence = ref_z - comp_z
                    if abs(subsidence) <= self.border_subsidence:
                        cell.subsidence = subsidence
                    else:
                        cell.subsidence = None
                ref_mse_z = ref_cell.get_mse_z_from_xy(x, y)
                comp_mse_z = comp_cell.get_mse_z_from_xy(x, y)
                if ref_mse_z is not None and comp_mse_z is not None:
                    cell.subsidence_mse = (ref_mse_z ** 2 + comp_mse_z ** 2) ** 0.5

            # ref_z = self.reference_model.get_z_from_point(point=center_point)
            # comp_z = self.comparable_model.get_z_from_point(point=center_point)
            # if ref_z is not None and comp_z is not None:
            #     cell.subsidence = ref_z - comp_z
            # ref_mse_z = (self.reference_model.get_model_element_for_point(point=center_point).
            #              get_mse_z_from_xy(x, y))
            # comp_mse_z = (self.comparable_model.get_model_element_for_point(point=center_point).
            #               get_mse_z_from_xy(x, y))
            # if ref_mse_z is not None and comp_mse_z is not None:
            #     cell.subsidence_mse = (ref_mse_z ** 2 + comp_mse_z ** 2) ** 0.5

    def _init_model(self):
        """
        Инициализирует сегментированную модель при запуске
        Если модель для воксельной модели нужного типа уже есть в БД - запускает
        копирование данных из БД в атрибуты модели
        Если такой модели нет - создает новую модели и запись в БД
        :return: None
        """
        select_ = select(self.db_table) \
            .where(self.db_table.c.model_name == self.model_name)

        with engine.connect() as db_connection:
            db_model_data = db_connection.execute(select_).mappings().first()
            if db_model_data is not None:
                self._copy_model_data(db_model_data)
                self._load_cell_data_from_db(db_connection)
                self.logger.info(f"Загрузка {self.model_name} модели завершена")
            else:
                stmt = insert(self.db_table).values(base_voxel_model_id=self.voxel_model.id,
                                                    model_type=self.model_type,
                                                    model_name=self.model_name,
                                                    MSE_data=self.mse_data
                                                    )
                db_connection.execute(stmt)
                db_connection.commit()
                self.id = self._get_last_model_id()
                self._calk_segment_model()
                self._save_cell_data_in_db(db_connection)
                db_connection.commit()
                self.logger.info(f"Расчет модели {self.model_name} завершен и загружен в БД\n")

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

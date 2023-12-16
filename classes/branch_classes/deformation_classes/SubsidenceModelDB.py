import logging

from sqlalchemy import select, insert, desc

from CONFIG import LOGGER
from classes.Point import Point
from classes.VoxelModelDB import VoxelModelDB
from classes.abc_classes.SegmentedModelABC import SegmentedModelABC
from classes.branch_classes.deformation_classes.SubsidenceCellDB import SubsidenceCellDB
from classes.branch_classes.deformation_classes.plotters.SubsidenceHeatMapPlotlyPlotter import \
    SubsidenceHeatMapPlotlyPlotter
from utils.start_db import Tables, engine


class SubsidenceModelDB:
    logger = logging.getLogger(LOGGER)
    db_table = Tables.subsidence_models_db_table

    def __init__(self, id_:int = None,
                 voxel_model: VoxelModelDB = None,
                 window_size=1,
                 border_subsidence=1,
                 reference_model: SegmentedModelABC = None,
                 comparable_model: SegmentedModelABC = None,
                 ):
        self.id_ = id_
        self.voxel_model = voxel_model
        self.window_size = window_size
        self.border_subsidence = border_subsidence
        self.reference_model = reference_model
        self.comparable_model = comparable_model
        self.base_voxel_model_id = None
        self.reference_model_id = None
        self.comparable_model_id = None
        self.subsidence_offset = 0
        self.model_name = self._init_subsidence_model_name()
        self._model_structure = {}
        self._init_model()

    def __iter__(self):
        return iter(SubsidenceModelWindowIterator(subsidence_model=self,
                                                  filter_function=None))

    def __str__(self):
        return f"{self.__class__.__name__} [ID: {self.id_},\tmodel_name: {self.model_name}]"

    def __repr__(self):
        return f"{self.__class__.__name__} [ID: {self.id_}]"

    def _init_subsidence_model_name(self):
        if self.reference_model is not None and self.comparable_model is not None:
            return (f"Subsidence_mdl_ref_{self.reference_model.model_name}_"
                    f"{self.comparable_model.model_name}_window_size_{self.window_size}")
        return None

    def get_model_element_for_point(self, point: Point):
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

    def _calk_subsidence_model(self):
        self.logger.info(f"Начат расчет модели {self.model_name}")
        self._calk_subsidence()
        self.logger.info(f"Завершен расчет модели {self.model_name}")

    def _calk_subsidence(self):
        for cell in self._model_structure.values():
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

    def _create_model_structure(self, element_class):
        """
        Создание структуры сегментированной модели
        :param element_class: Класс ячейки конкретной модели
        :return: None
        """
        for voxel in self.voxel_model:
            model_key = self._get_key_for_voxel(voxel)
            self._model_structure[model_key] = element_class(voxel, self)

    @staticmethod
    def _get_key_for_voxel(voxel):
        return f"{voxel.X:.5f}_{voxel.Y:.5f}_{voxel.Z:.5f}"

    def _init_model(self):
        """
        Инициализирует сегментированную модель при запуске
        Если модель для воксельной модели нужного типа уже есть в БД - запускает
        копирование данных из БД в атрибуты модели
        Если такой модели нет - создает новую модели и запись в БД
        :return: None
        """
        if (self.voxel_model is not None and
            self.reference_model is not None and
                self.comparable_model is not None):
            select_ = select(self.db_table) \
                .where(self.db_table.c.model_name == self.model_name)
            with engine.connect() as db_connection:
                db_model_data = db_connection.execute(select_).mappings().first()
                if db_model_data is not None:
                    self._create_model_structure(SubsidenceCellDB)
                    self._copy_model_data(db_model_data)
                    self._load_cell_data_from_db(db_connection)
                    self.logger.info(f"Загрузка {self.model_name} модели завершена")
                else:
                    self._create_model_structure(SubsidenceCellDB)
                    stmt = insert(self.db_table).values(base_voxel_model_id=self.voxel_model.id,
                                                        reference_model_id=self.reference_model.id,
                                                        comparable_model_id=self.comparable_model.id,
                                                        model_name=self.model_name,
                                                        subsidence_offset=self.subsidence_offset,
                                                        )
                    db_connection.execute(stmt)
                    db_connection.commit()
                    self.id_ = self._get_last_model_id()
                    self._calk_subsidence_model()
                    self._save_cell_data_in_db(db_connection)
                    db_connection.commit()
                    self.logger.info(f"Расчет модели {self.model_name} завершен и загружен в БД\n")
        elif self.id_ is not None:
            select_ = select(self.db_table) \
                .where(self.db_table.c.id == self.id_)
            with engine.connect() as db_connection:
                db_model_data = db_connection.execute(select_).mappings().first()
                if db_model_data is None:
                    raise ValueError(f"SubsidenceModelDB с id={self.id_} нет в базе данных!")
                if db_model_data is not None:
                    if self.voxel_model is None:
                        self.voxel_model = VoxelModelDB.get_voxel_model_by_id(id_=db_model_data["base_voxel_model_id"])
                    self._create_model_structure(SubsidenceCellDB)
                    self._copy_model_data(db_model_data)
                    self._load_cell_data_from_db(db_connection)
                    self.logger.info(f"Загрузка {self.model_name} модели завершена")
        if len(self._model_structure) == 0:
            raise ValueError("Модель оседаний не инициализирована!")

    def _copy_model_data(self, db_model_data: dict):
        """
        Копирует данные из записи БД в атрибуты сегментированной модели
        :param db_model_data: Данные записи из БД
        :return: None
        """
        self.id_ = db_model_data["id"]
        self.base_voxel_model_id = db_model_data["base_voxel_model_id"]
        self.reference_model_id = db_model_data["reference_model_id"]
        self.comparable_model_id = db_model_data["comparable_model_id"]
        self.model_name = db_model_data["model_name"]
        self.subsidence_offset = db_model_data["subsidence_offset"]

    def _save_cell_data_in_db(self, db_connection):
        """
        Сохраняет данные из всех ячеек модели в БД
        :param db_connection: открытое соединение с БД
        :return: None
        """
        for cell in self._model_structure.values():
            cell._save_cell_data_in_db(db_connection)

    def _load_cell_data_from_db(self, db_connection):
        """
        Загружает данные всех ячеек модели из БД
        :param db_connection: открытое соединение с БД
        :return: None
        """
        for cell in self._model_structure.values():
            cell._load_cell_data_from_db(db_connection)

    def _get_last_model_id(self):
        """
        Возвращает последний id для сегментированной модели в таблице БД dem_models
        :return: последний id для сегментированной модели в таблице БД dem_models
        """
        with engine.connect() as db_connection:
            stmt = (select(self.db_table.c.id).order_by(desc("id")))
            last_model_id = db_connection.execute(stmt).first()
            if last_model_id:
                return last_model_id[0]
            else:
                return 0

    def plot_heat_map(self, plotter=SubsidenceHeatMapPlotlyPlotter()):
        plotter.plot(self)


class SubsidenceModelWindowIterator:

    def __init__(self, subsidence_model: SubsidenceModelDB, filter_function=None):
        self.subsidence_model = subsidence_model
        self.window_size = self._check_windows_size(subsidence_model.window_size)
        self.filter_function = self._mean_cell_filter if filter_function is None else filter_function
        self.__iterator = None

    def __iter__(self):
        self.__iterator = iter(self.subsidence_model._model_structure.values())
        return self

    def __next__(self):
        try:
            cell = next(self.__iterator)
            new_cell = self._get_cell_copy(cell)
            cells = self._get_cells_in_window(central_cell=cell)
            filtered_cell = self.filter_function(new_cell, cells)
            return filtered_cell
        except StopIteration:
            raise StopIteration
        finally:
            pass

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

    def _get_cell_copy(self, cell):
        new_cell = SubsidenceCellDB(cell.voxel, self.subsidence_model)
        new_cell.voxel_id = cell.voxel_id
        new_cell.subsidence = cell.subsidence
        new_cell.subsidence_mse = cell.subsidence_mse
        return new_cell

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


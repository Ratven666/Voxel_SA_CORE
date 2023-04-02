from abc import ABC, abstractmethod


class CellABC(ABC):

    @abstractmethod
    def get_z_from_xy(self, x, y):
        pass

    @abstractmethod
    def _load_cell_data_from_db(self, db_connection):
        pass

    @abstractmethod
    def _save_cell_data_in_db(self, db_connection):
        pass

    @abstractmethod
    def _copy_cell_data(self, db_cell_data):
        pass

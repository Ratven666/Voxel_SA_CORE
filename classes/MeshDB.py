from sqlalchemy import delete, select, insert

from classes.ScanDB import ScanDB
from classes.abc_classes.MeshABC import MeshABC
from utils.mesh_utils.mesh_iterators.SqlLiteMeshIterator import SqlLiteMeshIterator
from utils.mesh_utils.mesh_triangulators.ScipyTriangulator import ScipyTriangulator
from utils.start_db import Tables, engine


class MeshDB(MeshABC):
    # """
    # Скан связанный с базой данных
    # Точки при переборе скана берутся напрямую из БД
    # """
    db_table = Tables.meshes_db_table

    def __init__(self, scan, scan_triangulator=ScipyTriangulator, db_connection=None):
        super().__init__(scan, scan_triangulator)
        # self.scan = scan
        # self.scan_triangulator = scan_triangulator
        # self.mesh_name = self.__name_generator()
        # self.len = 0
        self.base_scan_id = None
        self.__init_mesh(db_connection)

    def __iter__(self):
        return iter(SqlLiteMeshIterator(self))

    def delete_mesh(self, db_connection=None):
        self.delete_mesh_by_id(self.id, db_connection=db_connection)

    @classmethod
    def delete_mesh_by_id(cls, mesh_id, db_connection=None):
        """
        Удаляет запись поверхности из БД
        :param mesh_id: id поверхности которую требуется удалить из БД
        :param db_connection: Открытое соединение с БД
        :return: None
        """
        stmt_1 = delete(cls.db_table).where(cls.db_table.c.id == mesh_id)
        stmt_2 = delete(Tables.triangles_db_table).where(Tables.triangles_db_table.c.mesh_id == mesh_id)
        if db_connection is None:
            with engine.connect() as db_connection:
                db_connection.execute(stmt_1)
                db_connection.execute(stmt_2)
                db_connection.commit()
        else:
            db_connection.execute(stmt_1)
            db_connection.execute(stmt_2)
            db_connection.commit()

    @classmethod
    def get_mesh_from_id(cls, mesh_id: int):
        """
        Возвращает объект повепхности по id
        :param mesh_id: id поверхности которую требуется загрузить и вернуть из БД
        :return: объект MeshDB с заданным id
        """
        select_ = select(cls.db_table).where(cls.db_table.c.id == mesh_id)
        with engine.connect() as db_connection:
            db_mesh_data = db_connection.execute(select_).mappings().first()
            if db_mesh_data is not None:
                base_scan = ScanDB.get_scan_from_id(db_mesh_data["base_scan_id"])
                return cls(base_scan)
            else:
                raise ValueError("Нет поверхности с таким id!!!")

    def __load_triangle_data_to_db(self, db_conn, triangulation):
        triangle_data = []
        for triangle in triangulation.faces:
            triangle_data.append({"point_0_id": triangulation.points_id[triangle[0]],
                                  "point_1_id": triangulation.points_id[triangle[1]],
                                  "point_2_id": triangulation.points_id[triangle[2]],
                                  "mesh_id": self.id})
        db_conn.execute(Tables.triangles_db_table.insert(), triangle_data)
        db_conn.commit()

    # def __name_generator(self):
    #     return f"MESH_{self.scan.scan_name}"

    def __init_mesh(self, db_connection=None, triangulation=None):
        """
        Инициализирует поверхности при запуске
        Если поверхность с таким именем уже есть в БД - запускает копирование данных из БД в атрибуты поверхности
        Если такой поверхности нет - создает новую запись в БД
        :param db_connection: Открытое соединение с БД
        :return: None
        """
        def init_logic(db_conn, triangulation):
            select_ = select(self.db_table).where(self.db_table.c.mesh_name == self.mesh_name)
            db_mesh_data = db_conn.execute(select_).mappings().first()
            if db_mesh_data is not None:
                self.__copy_mesh_data(db_mesh_data)
                if triangulation is not None:
                    self.__load_triangle_data_to_db(db_conn, triangulation)
            else:
                triangulation = self.scan_triangulator(self.scan).triangulate()
                self.len = len(triangulation.faces)
                stmt = insert(self.db_table).values(mesh_name=self.mesh_name,
                                                    len=self.len,
                                                    base_scan_id=self.scan.id)
                db_conn.execute(stmt)
                db_conn.commit()
                self.__init_mesh(db_conn, triangulation)

        if db_connection is None:
            with engine.connect() as db_connection:
                init_logic(db_connection, triangulation)
        else:
            init_logic(db_connection, triangulation)

    def __copy_mesh_data(self, db_mesh_data: dict):
        """
        Копирует данные записи из БД в атрибуты поверхности
        :param db_mesh_data: Результат запроса к БД
        :return: None
        """
        self.id = db_mesh_data["id"]
        self.scan_name = db_mesh_data["mesh_name"]
        self.len = db_mesh_data["len"]
        self.base_scan_id = db_mesh_data["base_scan_id"]

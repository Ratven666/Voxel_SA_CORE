import enum


class DemTypeEnum(enum.Enum):
    DEM = 1
    PLANE = 2
    POLYNOMIAL_2 = 3
    BI_DEM_WITH_MSE = 4
    BI_DEM_WITHOUT_MSE = 5
    BI_PLANE_WITH_MSE = 6
    BI_PLANE_WITHOUT_MSE = 7
    BI_POLYNOMIAL_2_WITH_MSE = 8
    BI_POLYNOMIAL_2_WITHOUT_MSE = 9
    MESH = 10

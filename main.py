import time

from classes.BiModelDB import BiModelDB
from classes.DemModelDB import DemModelDB
from classes.MeshDB import MeshDB
from classes.MeshLite import MeshLite
from classes.MeshSegmentModelDB import MeshSegmentModelDB
from classes.PlaneModelDB import PlaneModelDB
from classes.Point import Point
from classes.VoxelModelDB import VoxelModelDB
from classes.VoxelModelLite import VoxelModelLite
from classes.branch_classes.MeshMSEConst import MeshMSEConstDB
from classes.branch_classes.statistic_clasess.SmMseTriComparator import SmMseTriComparator
from classes.branch_classes.terrain_indexes.MaxAbsCurvatureIndex import MaxAbsCurvatureIndex
from classes.branch_classes.terrain_indexes.MeanAbsCurvatureIndex import MeanAbsCurvatureIndex
from classes.branch_classes.terrain_indexes.MyTerrainRuggednessIndex import MyTerrainRuggednessIndex
from classes.branch_classes.terrain_indexes.ProfileCurvatureAbsIndex import ProfileCurvatureAbsIndex, \
    PlaneCurvatureAbsIndex
from classes.branch_classes.terrain_indexes.TerrainRuggednessIndexABSValue import TerrainRuggednessIndexABSValue
from classes.branch_classes.terrain_indexes.TerrainRuggednessIndexClassic import TerrainRuggednessIndexClassic
from classes.branch_classes.terrain_indexes.TerrainRuggednessIndexClassicModify import \
    TerrainRuggednessIndexClassicModify
from db_models.dem_models_table import DemTypeEnum
from utils.logs.console_log_config import console_logger
from utils.mesh_utils.mesh_exporters.DxfMeshExporter import DxfMeshExporter
from utils.mesh_utils.mesh_exporters.MeshExporterABC import MeshExporterABC
from utils.mesh_utils.mesh_exporters.PlyMeshExporter import PlyMeshExporter
from utils.mesh_utils.mesh_exporters.PlyMseMeshExporter import PlyMseMeshExporter
from utils.mesh_utils.mesh_filters.MaxEdgeLengthMeshFilter import MaxEdgeLengthMeshFilter
from utils.mesh_utils.mesh_filters.MaxMseTriangleMeshFilter import MaxMseTriangleMeshFilter
from utils.mesh_utils.mesh_plotters.MeshPlotterPlotly import MeshPlotterPlotly
from utils.scan_utils.scan_filters.ScanFilterByCellMSE import ScanFilterByCellMSE
from utils.scan_utils.scan_filters.ScanFilterByModelMSE import ScanFilterByModelMSE
from utils.scan_utils.scan_filters.ScanFilterForTrees import ScanFilterForTrees
from utils.scan_utils.scan_plotters.ScanPlotterPlotly import ScanPlotterPointsPlotly, ScanPlotterMeshPlotly
from utils.scan_utils.scan_samplers.TotalPointCountScanSampler import TotalPointCountScanSampler
from utils.scan_utils.scan_samplers.VoxelDownsamplingScanSampler import VoxelDownsamplingScanSampler
from utils.scan_utils.scan_serializers.ScanJsonSerializer import ScanJsonSerializer
from utils.segmented_mdl_utils.segmented_models_expoters.sm_to_scan.CellCenterSegmentedModelToScan import \
    CellCenterSegmentedModelToScan
from utils.segmented_mdl_utils.segmented_models_expoters.sm_to_scan.SegmentModelToScan import SegmentedModelToScan
from utils.segmented_mdl_utils.segmented_models_filters.SMFilterByMaxMSE import SMFilterByMaxMSE
from utils.segmented_mdl_utils.segmented_models_filters.SMFilterByMaxPercentile import SMFilterByMaxPercentile
from utils.segmented_mdl_utils.segmented_models_filters.SMFilterPercentile import SMFilterPercentile
from utils.segmented_mdl_utils.segmented_models_plotters.HistMSEPlotterPlotly import HistMSEPlotterPlotly
from utils.segmented_mdl_utils.segmented_models_plotters.SegmentModelPlotly import SegmentModelPlotly
from utils.segmented_mdl_utils.segmented_models_serializers.SegmentedModelJsonSerializer import \
    SegmentedModelJsonSerializer

from utils.start_db import create_db

from classes.ScanDB import ScanDB
from utils.voxel_utils.voxel_model_plotters.Voxel_model_plotter import VoxelModelPlotter
from utils.voxel_utils.voxel_model_separators.FastVMSeparator import FastVMSeparator
from utils.voxel_utils.voxel_model_separators.VMBruteForceSeparatorWithoutVoxelScansPoints import \
    VMBruteForceSeparatorWithoutVoxelScansPoints
from utils.voxel_utils.voxel_model_serializers.VoxelModelJsonSerializer import VoxelModelJsonSerializer


def main():
    create_db()

    scan = ScanDB("SKLD_4")
    scan.load_scan_from_file(file_name="src/Pit - Cloud 0,20.txt")
    # scan.plot(plotter=ScanPlotterPointsPlotly())
    # scan.plot()
    #

    STEP = 3

    vm_1 = VoxelModelDB(scan, step=STEP/3, is_2d_vxl_mdl=True)
    vm_2 = VoxelModelDB(scan, step=STEP, is_2d_vxl_mdl=True)

    dem = DemModelDB(vm_1)
    sm_2 =PlaneModelDB(vm_2)
    # sm_2 =DemModelDB(vm_2)

    # sm = BiModelDB(vm, DemTypeEnum.DEM)

    tri = PlaneCurvatureAbsIndex(dem, full_neighbours=True)
    # tri = MaxAbsCurvatureIndex(dem, full_neighbours=True)
    # tri = MyTerrainRuggednessIndex(dem, full_neighbours=True)


    # sm.plot()
    tri.plot()

    comparator = SmMseTriComparator(tri, sm_2)
    # # print(comparator)
    print(comparator.correlation)
    comparator.plot()

    # vm.plot()

    # scan_for_mesh = VoxelDownsamplingScanSampler(grid_step=1).do_sampling(scan=scan)
    #
    # mesh = MeshDB(scan_for_mesh)
    # mesh.calk_mesh_mse(scan)
    # mesh.plot()
    # scan_for_mesh.save_to_db()
    # scan_for_mesh.plot(plotter=ScanPlotterPointsPlotly())
    # mesh = MeshDB(scan_for_mesh)
    # mesh.plot()


    # scan = mesh.mesh.scan
    # scan.plot(plotter=ScanPlotterPointsPlotly())
    # PlyMeshExporter(mesh).export()
    # PlyMseMeshExporter(mesh).export()

    # mesh_2 = MeshLite(scan)
    # mesh_2.calk_mesh_mse(scan_for_mesh)
    # mesh_2.plot()
    #
    # sampled_scan = VoxelDownsamplingScanSampler(grid_step=20,
    #                                                  is_2d_sampling=True,
    #                                                  average_the_data=False).do_sampling(scan_for_mesh)
    # sampled_scan.plot(plotter=ScanPlotterPointsPlotly())


    # print(mesh)
    # mesh_sm = MeshSegmentModelDB(vm, mesh)
    # mesh.calk_mesh_mse(mesh_sm)
    # print(mesh)

    # MaxEdgeLengthMeshFilter(mesh, max_edge_length=1.5).filter_mesh()
    # print(mesh)
    # MaxMseTriangleMeshFilter(mesh, max_mse=0.3).filter_mesh()
    # print(mesh)

    # PlyMseMeshExporter(mesh, min_mse=0.01, max_mse=0.05).export()
    # PlyMeshExporter(mesh).export()
    # plane_sm = DemModelDB(vm)
    # plane_sm = BiModelDB(vm, DemTypeEnum.PLANE)
    # plane_sm = MeshSegmentModelDB(vm, mesh)
    # sm_scan = SegmentedModelToScan(plane_sm, custom_exporter=CellCenterS egmentedModelToScan).export_to_scan()
    # sm_scan.save_to_db()
    # bi_pl = BiModelDB(vm, DemTypeEnum.PLANE)
    # mesh = MeshLite(sm_scan)
    #
    # mesh_exp = PlyMeshExporter(mesh).export()
    # mesh_exp = DxfMeshExporter(mesh).export()

    # mesh.delete_mesh()
    # MeshDB.delete_mesh_by_id(1)
    # MeshDB.delete_mesh_by_id(2)

    # dem = DemModelDB(vm)
    # plane = PlaneModelDB(vm)
    #
    # bi_plane = BiModelDB(vm, DemTypeEnum.PLANE, enable_mse=True)
    #
    # dxf = DxfExporter(bi_plane, grid_densification=1, filtrate=True).export()
    # ply = PlyExporter(bi_plane, grid_densification=1, filtrate=True).export()


if __name__ == "__main__":
    main()

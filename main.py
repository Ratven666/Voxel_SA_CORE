import time

from MeshMSEConst import MeshMSEConst
from classes.BiModelDB import BiModelDB
from classes.DemModelDB import DemModelDB
from classes.MeshDB import MeshDB
from classes.MeshLite import MeshLite
from classes.MeshSegmentModelDB import MeshSegmentModelDB
from classes.PlaneModelDB import PlaneModelDB
from classes.VoxelModelDB import VoxelModelDB
from classes.VoxelModelLite import VoxelModelLite
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

    scan_for_mesh = ScanDB("4skld")
    scan_for_mesh.load_scan_from_file(file_name="src/4skld_0629_05.txt")
    mesh = MeshMSEConst(scan_for_mesh, max_border_length_m=20, max_triangle_mse_m=0.15, n=10,
                        delete_temp_models=False)
    mesh.plot()
    scan = mesh.mesh.scan
    scan.plot(plotter=ScanPlotterPointsPlotly())
    PlyMeshExporter(mesh).export()
    PlyMseMeshExporter(mesh).export()

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

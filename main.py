import time

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

    scan_for_mesh = ScanDB("4skld.txt")
    scan_for_mesh.load_scan_from_file(file_name="src/4skld_0629.txt")

    # scan_for_mesh.plot(plotter=ScanPlotterPointsPlotly())
    # vm = VoxelModelDB(scan_for_mesh, 4, is_2d_vxl_mdl=True)
    # vm = VoxelModelLite(scan_for_mesh, 1, is_2d_vxl_mdl=True)
    # vm.plot()
    scan = VoxelDownsamplingScanSampler(grid_step=10,
                                        is_2d_sampling=True,
                                        average_the_data=True).do_sampling(scan_for_mesh)
    scan.save_to_db()
    scan.plot(plotter=ScanPlotterPointsPlotly(sampler=None))


    # scan = ScanDB("4skld_0629")
    # scan.load_scan_from_file(file_name="src/4skld_0629.txt")
    # vm = VoxelModelDB(scan, 0.25, dx=0, dy=0, dz=0, is_2d_vxl_mdl=True)
    #
    # mesh = MeshLite(scan_for_mesh)
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

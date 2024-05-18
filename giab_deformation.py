from classes.BiModelDB import BiModelDB
from classes.DemModelDB import DemModelDB
from classes.MeshDB import MeshDB
from classes.MeshSegmentModelDB import MeshSegmentModelDB
from classes.PlaneModelDB import PlaneModelDB
from classes.ScanDB import ScanDB
from classes.VoxelModelDB import VoxelModelDB
from classes.branch_classes.deformation_classes.SubsidenceGMMClassificator import SubsidenceGMMClassificator
from classes.branch_classes.deformation_classes.SubsidenceModelDB import SubsidenceModelDB
from classes.branch_classes.deformation_classes.SubsidenceModelWindowFilter import SubsidenceModelWindowFilter
from classes.branch_classes.terrain_indexes.TerrainCurvaturesIndexesABC import SlopeFullIndex, MaxAbsCurvatureIndex, \
    MeanCurvatureIndex, ProfileCurvatureIndex
from utils.mesh_utils.mesh_filters.MaxEdgeLengthMeshFilter import MaxEdgeLengthMeshFilter
from utils.scan_utils.scan_plotters.ScanPlotterPlotly import ScanPlotterMeshPlotly
from utils.start_db import create_db
from utils.voxel_utils.voxel_model_separators.FastVMSeparator import FastVMSeparator


def main():
    create_db()

    scan_subs_1 = ScanDB("scan_subs_1")
    scan_subs_1.load_scan_from_file(file_name="src/осыпь_01_BF.txt")
    # scan_subs_1.load_scan_from_file(file_name="src/ZigZag_2018_ground_points_BF.txt")

    # # scan_subs_1.plot()
    #
    scan_subs_2 = ScanDB("scan_subs_2")
    scan_subs_2.load_scan_from_file(file_name="src/осыпь_02_BF.txt")
    # scan_subs_2.load_scan_from_file(file_name="src/ZigZag_2020_ground_points_BF.txt")

    # scan_subs_2.plot(plotter=ScanPlotterMeshPlotly())

    # mesh_2 = MeshDB(scan_subs_2)
    # MaxEdgeLengthMeshFilter(mesh_2, max_edge_length=10).filter_mesh()

    # mesh_2.plot()

    STEP = 2
    #
    base_vm = VoxelModelDB(scan_subs_1, step=0.25, is_2d_vxl_mdl=True,
                           voxel_model_separator=FastVMSeparator(drop_empty_voxel=False))
    vm_1 = VoxelModelDB(scan_subs_1, step=STEP, is_2d_vxl_mdl=True)
    vm_2 = VoxelModelDB(scan_subs_2, step=STEP, is_2d_vxl_mdl=True)
    #
    subs_1_dem = MeshSegmentModelDB(vm_1, MeshDB(scan_subs_1))
    subs_2_dem = MeshSegmentModelDB(vm_2, MeshDB(scan_subs_2))
    #
    # subs_1_dem = BiModelDB(PlaneModelDB(vm_1))
    # subs_2_dem = BiModelDB(PlaneModelDB(vm_2))

    # subs_1_dem = BiModelDB(DemModelDB(vm_1))
    # subs_2_dem = BiModelDB(DemModelDB(vm_2))
    #
    subs = SubsidenceModelDB(voxel_model=base_vm, border_subsidence=100, reference_model=subs_1_dem,
                             comparable_model=subs_2_dem,
                             # slope_calculator=SlopeFullIndex,
                             # curvature_calculator=CurvFromSlope,
                             )


    # print(s_gmm_cl.predict_class_prob(0))

    # for cell in subs:
    #     print(cell.classes_probability)

    # s_gmm_cl.plot_classification_result()

    for n in range(1, 20, 2):
        subs_wf = SubsidenceModelWindowFilter(subsidence_model=subs, window_size=n,
                                           border_subs=10,
                                           border_slope=100,
                                           border_curvature=15)

        s_gmm_cl = SubsidenceGMMClassificator(subs_wf, n_of_class=3)
        # s_gmm_cl.plot_classification_result()

        print(s_gmm_cl)
        subs_wf.plot_heat_map(data_type="subsidence_type")

    # subs.plot_surface()


    # subs = SubsidenceModelWindowFilter(subsidence_model=subs, window_size=3, border_subs=0.6,
    #              border_slope=15, border_curvature=0.3)
    # subs = SubsidenceModelWindowFilter(subsidence_model=subs, window_size=1, border_subs=0.6,
    #              border_slope=30, border_curvature=0.6)
    #
    # subs.plot_heat_map(data_type="subsidence")
    # subs.plot_heat_map(data_type="slope")
    # subs.plot_heat_map(data_type="curvature")
    subs.plot_heat_map(data_type="subsidence_type")

    # subs.plot_subsidence_hist(data_type="subsidence")
    # subs.plot_subsidence_hist(data_type="slope")
    # subs.plot_subsidence_hist(data_type="curvature")
    # subs.plot_subsidence_hist(data_type="subsidence_type")

    # subs.plot_surface()


if __name__ == "__main__":
    main()


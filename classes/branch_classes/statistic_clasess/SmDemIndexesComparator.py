import pandas as pd

from classes.Point import Point


class SmDemIndexesComparator:

    def __init__(self, s_model, *dem_indexes_models):
        self.dem_indexes_models = dem_indexes_models
        self.s_model = s_model
        self.df = None
        self._prepare_data()

    def __str__(self):
        return str(self.df)

    def _prepare_data(self):
        data = self._init_data_dict()
        for cell in self.s_model:
            step = cell.voxel.step
            x = cell.voxel.X + step / 2
            y = cell.voxel.Y + step / 2
            z = cell.voxel.Z + step / 2
            point = Point(X=x,
                          Y=y,
                          Z=z,
                          R=cell.voxel.R,
                          G=cell.voxel.G,
                          B=cell.voxel.B,
                          )
            for dem_index_model in self.dem_indexes_models:
                dem_index = dem_index_model.get_index_for_point(point)
                data[dem_index_model.index_name].append(dem_index)
            data["x"].append(x)
            data["y"].append(y)
            data["mse"].append(cell.mse)
        self.df = pd.DataFrame(data)

    def _init_data_dict(self):
        data = {dem_index_model.index_name: [] for dem_index_model in self.dem_indexes_models}
        data["mse"] = []
        data["x"] = []
        data["y"] = []
        return data

    @property
    def correlations_matrix(self):
        return self.df.corr()

    @property
    def correlations_mse_for_dem_indexes(self):
        from scipy.stats import pearsonr
        correlations = {}
        df = self.df.dropna(inplace=False)
        for dem_index_model in self.dem_indexes_models:
            index_name = dem_index_model.index_name
            r, p_value = pearsonr(df["mse"], df[index_name])
            correlations[index_name] = {"r": r,
                                        "p_value": p_value,
                                        }
        return correlations

    def plot(self):
        import seaborn as sns
        sns.set_theme(style="ticks")
        sns_plot = sns.jointplot(x="tri", y="mse", data=self.df,
                          kind="reg",
                          truncate=True,
                          # color="m",
                                 scatter_kws=dict(s=2,
                                                  # linewidths=.7,
                                                  marker="+",
                                                  ),
                                 line_kws=dict(lw=4,
                                               color='r',
                                               ),
                          ratio=3,
                                 )
        sns_plot.set_axis_labels("TRI", "MSE")
        sns_plot.savefig(f"{self.s_model.model_name}.")

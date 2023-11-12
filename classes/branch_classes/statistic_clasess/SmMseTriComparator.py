import pandas as pd

from classes.Point import Point


class SmMseTriComparator:

    def __init__(self, tri, s_model):
        self.tri = tri
        self.s_model = s_model
        self.df = None
        self.__prepare_data()

    def __str__(self):
        return str(self.df)

    def __prepare_data(self):
        data = {"tri": [],
                "mse": [],
                }
        for cell in self.s_model:
            step = cell.voxel.step
            point = Point(X=cell.voxel.X + step / 2,
                          Y=cell.voxel.Y + step / 2,
                          Z=cell.voxel.Z + step / 2,
                          R=cell.voxel.R,
                          G=cell.voxel.G,
                          B=cell.voxel.B,
                          )
            tri = self.tri.get_index_for_point(point)
            mse = cell.mse
            data["tri"].append(tri)
            data["mse"].append(mse)
        self.df = pd.DataFrame(data)

    @property
    def correlation(self):
        return self.df["tri"].corr(self.df["mse"])

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

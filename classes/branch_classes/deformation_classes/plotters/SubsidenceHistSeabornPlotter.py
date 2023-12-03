import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


class SubsidenceHistSeabornPlotter:

    def __init__(self):
        self.model = None
        self.df = None

    def _create_data_frame(self):
        data_dict = {"subsidence": [],
                     "subsidence_mse": []}
        for cell in self.model:
            data_dict["subsidence"].append(cell.subsidence)
            data_dict["subsidence_mse"].append(cell.subsidence_mse)
        self.df = pd.DataFrame(data_dict)

    def plot(self, model):
        self.model = model
        self._create_data_frame()
        sns.displot(self.df, x="subsidence", kde=True)
        plt.show()

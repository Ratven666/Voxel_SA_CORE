import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


class SubsidenceHistSeabornPlotter:

    def __init__(self):
        self.model = None
        self.df = None

    def data_loader(self, cell, data_type):
        if data_type == "subsidence":
            return cell.subsidence + self.model.subsidence_offset if cell.subsidence is not None else None
        elif data_type == "slope":
            return cell.slope
        elif data_type == "curvature":
            return cell.curvature
        elif data_type == "subsidence_type":
            return cell.subsidence_class
        else:
            return None

    def _create_data_frame(self):
        data_dict = {"subsidence": [],
                     "subsidence_mse": [],
                     "slope": [],
                     "curvature": [],
                     "subsidence_type": [],
                     }
        for cell in self.model:
            data_dict["subsidence"].append(cell.subsidence)
            data_dict["slope"].append(cell.slope)
            data_dict["curvature"].append(cell.curvature)
            data_dict["subsidence_mse"].append(cell.subsidence_mse)
            data_dict["subsidence_type"].append(cell.subsidence_class)
        self.df = pd.DataFrame(data_dict)

    def plot(self, model, data_type):
        self.model = model
        self._create_data_frame()
        sns.displot(self.df, x=data_type, kde=True)
        plt.show()

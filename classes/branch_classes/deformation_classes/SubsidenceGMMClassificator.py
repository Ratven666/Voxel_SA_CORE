import numpy as np
from matplotlib import pyplot as plt
from sklearn.mixture import GaussianMixture


class SubsidenceGMMClassificator:

    def __init__(self, subs_model, n_of_class=3):
        self._subs_model = subs_model
        self._n_of_class = n_of_class
        self._subs_arr = None
        self._gmm_classificator = None
        self._class_params_dict = None
        self._stable_zone_idx = None
        self._init_classificator()

    def __iter__(self):
        return iter(self._subs_model)

    def __str__(self):
        return (f"{self.__class__.__name__} "
                f"[subs_model: {repr(self._subs_model)}\tn_of_class: {self._n_of_class}\t"
                f"M_sz: {round(self._class_params_dict[self._stable_zone_idx]["M"], 3)}\t"
                f"Std_sz: {round(self._class_params_dict[self._stable_zone_idx]["Std"], 3)}")

    def _init_subs_arr(self):
        subs_lst = []
        for cell in self:
            if cell.subsidence is not None:
                subs_lst.append(cell.subsidence)
        subs_arr = np.array(subs_lst)
        self._subs_arr = subs_arr

    def _init_classificator(self):
        if self._subs_arr is None:
            self._init_subs_arr()
        self._gmm_classificator = GaussianMixture(self._n_of_class).fit(self._subs_arr.reshape(-1, 1))
        self._init_class_params_dict()
        self._predict_subs_classes()

    def _init_class_params_dict(self):
        self._class_params_dict = {n: {"M": None,
                                       "Kov": None,
                                       "Std": None,
                                       "type": None,
                                       } for n in range(self._n_of_class)}
        for idx, class_params in self._class_params_dict.items():
            class_params["M"] = self._gmm_classificator.means_[idx][0]
            class_params["Kov"] = self._gmm_classificator.covariances_[idx][0]
            class_params["Std"] = self._gmm_classificator.covariances_[idx][0][0] ** 0.5
        self._chose_class_indexes()

    def _chose_class_indexes(self):
        temp_lst = []
        for idx, class_params in self._class_params_dict.items():
            type_ = -1 if class_params["M"] <= 0 else 1
            class_params["type"] = type_
            temp_lst.append(abs(class_params["M"]))
        self._stable_zone_idx = temp_lst.index(min(temp_lst))
        self._class_params_dict[self._stable_zone_idx]["type"] = 0

    def _get_subsidence_type_from_prob_lst(self, prob_lst):
        idx = prob_lst.index(max(prob_lst))
        return self._class_params_dict[idx]["type"]

    def _predict_subs_classes(self):
        for cell in self:
            if cell.subsidence is not None:
                cell.classes_probability = self.predict_classes_probability_for_subsidence(cell.subsidence)[0]
                prob_lst = list(cell.classes_probability)
                cell.subsidence_class = self._get_subsidence_type_from_prob_lst(prob_lst)
            else:
                cell.classes_probability = None
                cell.subsidence_class = None

    def predict_classes_probability_for_subsidence(self, subsidence):
        return self._gmm_classificator.predict_proba([[subsidence]])

    def predict_subsidence_type_for_subsidence(self, subsidence):
        prob_lst = self.predict_classes_probability_for_subsidence(subsidence)
        return self._get_subsidence_type_from_prob_lst(prob_lst)

    def get_stable_zone_params_dict(self):
        return self._class_params_dict[self._stable_zone_idx]

    def plot_classification_result(self, n_for_aic_bic=10):
        X = self._subs_arr.reshape(-1, 1)
        N = np.arange(1, n_for_aic_bic + 1)
        models = [None for i in range(len(N))]
        for i in range(len(N)):
            models[i] = GaussianMixture(N[i]).fit(X)

        # compute the AIC and the BIC
        AIC = [m.aic(X) for m in models]
        BIC = [m.bic(X) for m in models]

        fig = plt.figure(figsize=(5, 1.7))
        fig.subplots_adjust(left=0.12, right=0.97,
                            bottom=0.21, top=0.9, wspace=0.5)

        # plot 1: data + best-fit mixture
        ax = fig.add_subplot(131)
        x = np.linspace(min(self._subs_arr), max(self._subs_arr), 1000)
        logprob = self._gmm_classificator.score_samples(x.reshape(-1, 1))
        responsibilities = self._gmm_classificator.predict_proba(x.reshape(-1, 1))
        pdf = np.exp(logprob)
        pdf_individual = responsibilities * pdf[:, np.newaxis]

        ax.hist(X, 30, density=True, histtype='stepfilled', alpha=0.4)
        ax.plot(x, pdf, '-k')
        ax.plot(x, pdf_individual, '--k')
        ax.text(0.04, 0.96, "GMM\nклассификация",
                ha='left', va='top', transform=ax.transAxes)
        ax.set_xlabel('оседание')
        ax.set_ylabel('$p(оседание)$')

        # plot 2: AIC and BIC
        ax = fig.add_subplot(132)
        ax.plot(N, AIC, '-k', label='AIC')
        ax.plot(N, BIC, '--k', label='BIC')
        ax.set_xlabel('Количество классов')
        ax.set_ylabel('Значение критерия')
        ax.legend(loc="upper right")

        # plot 3: posterior probabilities for each component
        ax = fig.add_subplot(133)

        p = responsibilities
        p = p[:, (1, 0, 2)]  # rearrange order so the plot looks better
        p = p.cumsum(1).T

        ax.fill_between(x, 0, p[0], color='gray', alpha=0.3)
        ax.fill_between(x, p[0], p[1], color='gray', alpha=0.5)
        ax.fill_between(x, p[1], 1, color='gray', alpha=0.7)
        ax.set_xlim(min(x), max(x))
        ax.set_ylim(0, 1)
        ax.set_xlabel('оседание')
        ax.set_ylabel(r'$p({\rm class}|$оседание$)$')

        dx = max(x) - min(x)
        ax.text(min(x) + dx*0.1, 0.3, 'class 1', rotation='vertical')
        # ax.text(-0.6, 0.5, 'class 1', rotation='vertical')
        ax.text(0, 0.5, 'class 2', rotation='vertical')
        # ax.text(-0.05, 0.5, 'class 2', rotation='vertical')
        ax.text(max(x) - dx*0.1, 0.5, 'class 3', rotation='vertical')
        # ax.text(0.6, 0.5, 'class 3', rotation='vertical')
        plt.show()








if __name__ == "__main__":
    pass
from sklearn.base import BaseEstimator
import matplotlib.pyplot as plt
import seaborn as sns
from tree import TreeRegressor
from boosting._gradient_boosting import GradientBoostingRegressor
from boosting._gradient_boosting import RTG
from boosting._gradient_boosting import XGBOOST

from .utils import check_model, check_gain_param
from .utils import check_param
from .utils import check_bool_param
from .utils import check_random_state
from .utils import check_loss
from .utils import get_numpy_array_train_valid

from tree._utils import get_numpy_array_train, convert_type_train, convert_type_test
from tree._utils import get_numpy_array_test

sns.set(style='whitegrid')




class GBRegressor(BaseEstimator, GradientBoostingRegressor):
    def __init__(self,
                 base_model_class = TreeRegressor,
                 base_model_params: dict = None,
                 n_estimators: int = 10,
                 learning_rate: float = 1e-3,
                 randomization = False,
                 subsample: float = 0.3,
                 random_seed: int = 42,
                 custom_loss: str = 'mse',
                 use_best_model: bool = False,
                 n_iter_early_stopping: int = None,
                 valid_control: float = 1e-10,
                 plot: bool = True,
                 show_tqdm = False
                 ):
        """
        Gradient Boosting Regressor - GBRegressor.

        Base Boosting. Work on base Tree.


        :param base_model_class: base estimator
        :param base_model_params: dict - base estimator params
        :param n_estimators: int count estimators
        :param learning_rate: float step length. Greater then zero
        :param randomization: bool - should using bootstrap for all treeS
        :param subsample: float - share of object in bootstrap selection
        :param random_seed: int - random state for reproducibility
        :param custom_loss: str - by which class consider the gradient
        :param use_best_model: bool - should use best n_estimator for best score on valid selection
        :param n_iter_early_stopping: int - count iterations for stop process if diff between score[n_iter] - score[-1] <= valid_control
        :param valid_control: float see n_iter_early_stopping
        :param plot: bool - drawing graphs after fitting
        """

        # checking model and params for her
        check_model(base_model_class, base_model_params)

        # checking params for boosting
        check_param(n_estimators, learning_rate, subsample, n_iter_early_stopping, valid_control)

        # check bool param
        check_bool_param(randomization, use_best_model, plot)

        # check random seed for send to numpy
        check_random_state(random_seed)

        # checking available loss function
        check_loss(custom_loss)

        super().__init__(base_model_class,
                         base_model_params,
                         n_estimators,
                         learning_rate,
                         randomization,
                         subsample,
                         random_seed,
                         custom_loss,
                         use_best_model,
                         n_iter_early_stopping,
                         valid_control,
                         show_tqdm)

        self.plot = plot



    def fit(self, X_train, y_train, X_valid = None, y_valid = None):
        """
        Fitting Boosting

        :param X_train: np.ndarray [dimension = 2], pd.DataFrame - train data
        :param y_train: np.ndarray [dimension = 1], pd.Series - train target
        :param X_valid: np.ndarray [dimension = 2], pd.DataFrame - valid data - optional
        :param y_valid: np.ndarray [dimension = 1], pd.Series - valid target - optional
        :return: self
        """

        # check valid data
        if X_valid is not None and y_valid is not None:
            X_train, y_train, X_valid, y_valid = get_numpy_array_train_valid(X_train, y_train, X_valid, y_valid)

        elif X_valid is None and y_valid is None:
            X_train, y_train = get_numpy_array_train(X_train, y_train)

        else:
            raise TypeError(f"You must send X_train, y_train. "
                            f"X_valid and y_valid = optional.")

        if X_valid is None and y_valid is None and self.use_best_model:
            raise ValueError(f"You can't use argument 'use_best_model' while "
                             f"don't pass validation selection.")

        # start build boosting
        super()._build(X_train, y_train, X_valid, y_valid)

        # draw if plot True

        if self.plot:
            fig, ax = plt.subplots()
            sns.lineplot(data=self.history['train'], label='train', ax=ax)
            sns.lineplot(data=self.history['valid'], label='valid', ax=ax)
            ax.set_title('Зависимость ошибки от номера итерации')
            ax.set_ylabel('Ошибка')
            ax.set_xlabel('Номер итерации')
        return self

    def predict(self, X_test):
        """
        Predict for X_test. Before use this method must be used to .fit(X_train, y_train)

        :param X_test: np.ndarray [dimension = 2], pd.DataFrame - test data
        :return: y_test - prediction
        """

        X_test = get_numpy_array_test(X_test)

        return super()._predict(X_test)




class TreeRegressorGain(RTG):
    def __init__(self,
                 max_depth = 3,
                 min_samples_leaf = 2,
                 min_samples_split = 1,
                 lmd = 1.0,
                 gmm = 0.1,
                 score = 'mse'):

        check_gain_param(max_depth,min_samples_leaf, min_samples_split, lmd, gmm, score)

        super().__init__(max_depth,
                         min_samples_leaf,
                         min_samples_split,
                         lmd,
                         gmm,
                         score)

        self.tree = {}

    def fit(self, X_train, y_train):
        X_train, y_train = get_numpy_array_train(X_train, y_train)
        X_train, y_train = convert_type_train(X_train, y_train)

        if len(y_train.shape) != 1:
            raise IndexError(f"Argument length 'X_train' != 'y_train': {X_train.shape[0]} != {len(y_train)}. "
                             f"Please, check input data.")

        if X_train.shape[0] != len(y_train):
            raise IndexError(f"Argument length 'X_train' != 'y_train': {X_train.shape[0]} != {len(y_train)}. "
                             f"Please, check input data.")

        X_train, y_train = self._check_input(X_train, y_train)
        self.tree = self._build(X_train, y_train, self.tree, self.max_depth)

    def predict(self, X_test):
        X_test = get_numpy_array_test(X_test)
        X_test = convert_type_test(X_test)
        X_test = self._check_input_test(X_test)

        return self._predict(X_test, self.tree)



class xgBoost(XGBOOST):
    def __init__(self,
                 max_depth = 3,
                 min_samples_leaf = 2,
                 min_samples_split = 1,
                 lmd = 1.0,
                 gmm = 0.1,
                 n_estimators = 100,
                 score = 'mse',
                 learning_rate = 0.1,
                 adaptive = True,
                 randomization = False,
                 subsample = 0.3,
                 random_seed = None,
                 use_best_valid_model=False,
                 custom_loss = 'mse',
                 n_iter_early_stopping = None,
                 valid_control = 1e-7,
                 show_tqdm = True):

        base_model_class = TreeRegressorGain

        super().__init__(
            n_estimators,
            max_depth,
            min_samples_leaf,
            min_samples_split,
            lmd,
            gmm,
            score,
            learning_rate,
            adaptive,
            randomization,
            subsample,
            random_seed,
            use_best_valid_model,
            custom_loss,
            n_iter_early_stopping,
            valid_control,
            show_tqdm,
            base_model_class)

    def fit(self, X_train, y_train, X_valid = None, y_valid = None):
        """
        Fitting Boosting

        :param X_train: np.ndarray [dimension = 2], pd.DataFrame - train data
        :param y_train: np.ndarray [dimension = 1], pd.Series - train target
        :param X_valid: np.ndarray [dimension = 2], pd.DataFrame - valid data - optional
        :param y_valid: np.ndarray [dimension = 1], pd.Series - valid target - optional
        :return: self
        """

        # check valid data
        if X_valid is not None and y_valid is not None:
            X_train, y_train, X_valid, y_valid = get_numpy_array_train_valid(X_train, y_train, X_valid, y_valid)

        elif X_valid is None and y_valid is None:
            X_train, y_train = get_numpy_array_train(X_train, y_train)

        else:
            raise TypeError(f"You must send X_train, y_train. "
                            f"X_valid and y_valid = optional.")

        if X_valid is None and y_valid is None and self.use_best_model:
            raise ValueError(f"You can't use argument 'use_best_model' while "
                             f"don't pass validation selection.")

        # start build boosting
        super()._build(X_train, y_train, X_valid, y_valid)

        print("Well Done!")

    def predict(self, X_test):
        """
        Predict for X_test. Before use this method must be used to .fit(X_train, y_train)

        :param X_test: np.ndarray [dimension = 2], pd.DataFrame - test data
        :return: y_test - prediction
        """

        X_test = get_numpy_array_test(X_test)

        return super()._predict(X_test)




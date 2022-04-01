from tree._utils import _check_param
from tree._utils import _check_param_adaptive
from tree._utils import get_numpy_array_train
from tree._utils import get_numpy_array_test
from tree._utils import convert_type_train
from tree._utils import convert_type_test

from sklearn.base import BaseEstimator
from tree._tree import DecisionTreeRegressorSlow, DecisionTreeRegressorFast, DecisionTreeAdaptive


class TreeRegressorSlow(BaseEstimator, DecisionTreeRegressorSlow):
    def __init__(self, max_depth=10, min_samples_leaf=1, min_samples_split=1):
        """
        TreeRegressorSlow calculate MSE for all object in always iteration in X_train and y_train

        :param max_depth: int - depth Tree
        :param min_samples_leaf: int - count minimal samples in leaf
        :param min_samples_split: int - count minimal samples to do split
        """
        # checking input parameters
        _check_param(max_depth, min_samples_leaf, min_samples_split)

        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.min_samples_split = min_samples_split
        self.tree = {}

    def fit(self, X_train, y_train):
        """
        Fitting Tree.

        :param X_train: np.ndarray [dimension = 2], pd.DataFrame - train data
        :param y_train: np.ndarray [dimension = 1], pd.Series - train target
        :return: self
        """

        # checking input data

        # get numpy array from different type
        X_train, y_train = get_numpy_array_train(X_train, y_train)

        # get float64 type
        X_train, y_train = convert_type_train(X_train, y_train)

        # y_train must have 1 dimension
        if len(y_train.shape) != 1:
            raise IndexError(f"Argument 'y_train' not 1 dimension. 'y_train' dim {len(y_train.shape)} != dim 1. "
                             f"Please, check input data")

        # check lenght data
        if X_train.shape[0] != len(y_train):
            raise IndexError(f"Argument length 'X_train' != 'y_train': {X_train.shape[0]} != {len(y_train)}. "
                             f"Please, check input data.")

        X_train, y_train = super(DecisionTreeRegressorSlow, self)._check_input(X_train, y_train)

        # fit tree
        self.tree = super(TreeRegressorSlow, self)._build(X_train, y_train, self.tree, self.max_depth)
        return self

    def predict(self, X_test):
        """
        Predict for X_test. Before use this method must used to .fit(X_train, y_train)

        :param X_test: np.ndarray [dimension = 2], pd.DataFrame - train data
        :return: predicted target for test/val data
        """
        X_test = get_numpy_array_test(X_test)

        X_test = convert_type_test(X_test)

        X_test = super(DecisionTreeRegressorSlow, self)._check_input_test(X_test)
        return super(TreeRegressorSlow, self)._predict(X_test, self.tree)


class TreeRegressor(BaseEstimator, DecisionTreeRegressorFast):
    def __init__(self, max_depth = 10, min_samples_leaf = 1, min_samples_split = 1):
        """
        TreeRegressor calculate MSE for neighbours object in always iteration in X_train and y_train

        :param max_depth: int - depth Tree
        :param min_samples_leaf: int - count minimal samples in leaf
        :param min_samples_split: int - count minimal samples to do split
        """
        # checking input parameters
        _check_param(max_depth, min_samples_leaf, min_samples_split)

        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.min_samples_split = min_samples_split
        self.tree = {}

    def fit(self, X_train, y_train):
        """
        Fitting Tree.

        :param X_train: np.ndarray [dimension = 2], pd.DataFrame - train data
        :param y_train: np.ndarray [dimension = 1], pd.Series - train target
        :return: self
        """
        # checking input data

        # get numpy array from different type
        X_train, y_train = get_numpy_array_train(X_train, y_train)

        # get float64 type
        X_train, y_train = convert_type_train(X_train, y_train)

        # y_train must have 1 dimension
        if len(y_train.shape) != 1:
            raise IndexError(f"Argument length 'X_train' != 'y_train': {X_train.shape[0]} != {len(y_train)}. "
                             f"Please, check input data.")

        # check lenght data
        if X_train.shape[0] != len(y_train):
            raise IndexError(f"Argument length 'X_train' != 'y_train': {X_train.shape[0]} != {len(y_train)}. "
                             f"Please, check input data.")

        X_train, y_train = super(DecisionTreeRegressorFast, self)._check_input(X_train, y_train)

        # fit tree
        self.tree = super(TreeRegressor, self)._build(X_train, y_train, self.tree, self.max_depth)
        return self

    def predict(self, X_test):
        """
        Predict for X_test. Before use this method must used to .fit(X_train, y_train)

        :param X_test: np.ndarray [dimension = 2], pd.DataFrame - train data
        :return: predicted target for test/val data
        """
        X_test = get_numpy_array_test(X_test)

        X_test = convert_type_test(X_test)

        X_test = super(DecisionTreeRegressorFast, self)._check_input_test(X_test)

        return super(TreeRegressor, self)._predict(X_test, self.tree)

class TreeRegressorAdaptive(BaseEstimator, DecisionTreeAdaptive):
    """
    TreeRegressorAdaptive add to X_train different linear feature combination

    :param max_depth: int - depth Tree
    :param min_samples_leaf: int - count minimal samples in leaf
    :param min_samples_split: int - count minimal samples to do split
    :param adaptive: bool - if 'True' linear combination activate, else deactivate
    :param n_combinations: int count combination feature index
    :param randomization: str - aggregating feature
    """
    def __init__(self, max_depth = 10,
                 min_samples_leaf = 1,
                 min_samples_split = 1,
                 adaptive = True,
                 n_combinations = 2,
                 randomization = 'sum'):

        # checking input parameters
        _check_param(max_depth, min_samples_leaf, min_samples_split)
        _check_param_adaptive(adaptive, n_combinations, randomization)

        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.min_samples_split = min_samples_split
        self.adaptive = adaptive
        if self.adaptive:
            self.adaptive_test = True
        else:
            self.adaptive_test = False
        self.n_combinations = n_combinations,
        self.randomization = randomization,
        self.tree = {}

    def fit(self, X_train, y_train):
        """
        Fitting Tree.

        :param X_train: np.ndarray [dimension = 2], pd.DataFrame - train data
        :param y_train: np.ndarray [dimension = 1], pd.Series - train target
        :return: self
        """
        # checking input data

        # get numpy array from different type
        X_train, y_train = get_numpy_array_train(X_train, y_train)

        # get float64 type
        X_train, y_train = convert_type_train(X_train, y_train)

        # y_train must have 1 dimension
        if len(y_train.shape) != 1:
            raise IndexError(f"Argument length 'X_train' != 'y_train': {X_train.shape[0]} != {len(y_train)}. "
                             f"Please, check input data.")

        # check lenght data
        if X_train.shape[0] != len(y_train):
            raise IndexError(f"Argument length 'X_train' != 'y_train': {X_train.shape[0]} != {len(y_train)}. "
                             f"Please, check input data.")

        # check n_combinations
        if self.n_combinations[0] > X_train.shape[1]:
            raise IndexError(f"Argument 'n_combinations' must be less than count features. "
                             f"n_combinations: {self.n_combinations[0]} > {X_train.shape[1]} count features")

        X_train, y_train = super(DecisionTreeAdaptive, self)._check_input(X_train, y_train)

        # fit tree
        self.tree = super(TreeRegressorAdaptive, self)._build(X_train, y_train, self.tree, self.max_depth)
        return self

    def predict(self, X_test):
        """
        Predict for X_test. Before use this method must used to .fit(X_train, y_train)

        :param X_test: np.ndarray [dimension = 2], pd.DataFrame - train data
        :return: predicted target for test/val data
        """
        X_test = get_numpy_array_test(X_test)

        X_test = convert_type_test(X_test)

        X_test = super(DecisionTreeAdaptive, self)._check_input_test(X_test)

        return super(TreeRegressorAdaptive, self)._predict(X_test, self.tree)
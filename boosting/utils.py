########################################################
#           CHECKING - GDBOOST - PARAMS
########################################################


import numpy as np
import pandas as pd
from typing import List
from tree import TreeRegressor
from tree import TreeRegressorSlow
from tree import TreeRegressorAdaptive
from ensemble import BaggingTree
from ensemble import BaggingTreeAdaptive

def check_model(base_model_class, base_model_params):
    if not isinstance(base_model_class(), (TreeRegressor,
                                     TreeRegressorSlow,
                                     TreeRegressorAdaptive,
                                     BaggingTree,
                                     BaggingTreeAdaptive)):

        raise TypeError(f"Argument 'base_model_class' not identified. "
                        f"You must send one of model class. "
                        f"Check input data.")



    if not isinstance(base_model_params, dict) and base_model_params is not None:

        raise TypeError(f"Type argument 'base_model_params' not identified. "
                        f"You must send dictionary. "
                        f"Check input data.")

    # if isinstance(base_model_params, dict):
    #
    #     for param in list(base_model_params.keys()):
    #
    #         if param not in list(base_model_class().get_params().keys()):
    #
    #             raise ValueError(f"Parameter '{param}' not defined in base model parameters. "
    #                              f"You must send this param: "
    #                              f"{list(base_model_class().get_params().keys())}. "
    #                              f"Check input data.")



def check_param(n_estimators, learning_rate, subsample, n_iter_early_stopping, valid_control):

    if (not isinstance(n_estimators, int)) and (not np.issubdtype(n_estimators, np.integer)):
        raise TypeError(f"Type 'n_estimators' must be int. You send type {type(n_estimators).__name__}")

    if n_estimators <= 1:
        raise ValueError(f"Parameter 'n_estimators' must be greater than one. Check 'n_estimators'.")


    if (not isinstance(learning_rate, float)) and (not np.issubdtype(learning_rate, np.float)):
        raise TypeError(f"Type 'learning_rate' must be float. You send type {type(learning_rate).__name__}")

    if learning_rate <= 0:
        raise ValueError(f"Parameter 'learning_rate' must be greater than zero. Check 'learning_rate'.")


    if (not isinstance(subsample, float)) and (not np.issubdtype(subsample, np.float)):
        raise TypeError(f"Type 'subsample' must be float. You send type {type(subsample).__name__}")

    if subsample <= 0 or subsample > 1:
        raise ValueError(f"Parameter 'subsample' must be in range from 0 to 1. Check 'subsample'.")

    if (not isinstance(valid_control, float)) and (not np.issubdtype(valid_control, np.float)):
        raise TypeError(f"Type 'valid_control' must be float. You send type {type(valid_control).__name__}")


    if (not isinstance(n_iter_early_stopping,int)) \
            and (not np.issubdtype(n_iter_early_stopping, np.int))\
            and n_iter_early_stopping is not None:
        raise TypeError(f"Type 'n_iter_early_stopping' must be int. You send type {type(valid_control).__name__}")


    if n_iter_early_stopping is not None:
        if n_iter_early_stopping <= 0:
            raise ValueError(f"Parameter 'n_iter_early_stopping' must be greater than zero. Check 'n_iter_early_stopping'.")



def check_bool_param(randomization, use_best_model, plot):

    if randomization not in [True, False]:
        raise TypeError(f"Argument 'randomization' must be True or False. Check input")

    if use_best_model not in [True, False]:
        raise TypeError(f"Argument 'use_best_model' must be True or False. Check input")

    if plot not in [True, False]:
        raise TypeError(f"Argument 'plot' must be True or False. Check input")


def check_random_state(random_state):

    if (not isinstance(random_state, int)) and (not np.issubdtype(random_state, np.integer)):
        raise TypeError(f"Type 'random_state' must be int. You send type {type(random_state).__name__}")

    if random_state < 0:
        raise ValueError(f"Parameter 'random_state' must be greater than zero. Check 'random_state'.")


def check_loss(custom_loss):

    if custom_loss not in ['mse', 'log_mse', 'log_cosh', 'huber']:

        raise ValueError(f"Argument 'custom_loss' must be str: 'mse', 'log_mse', 'log_cosh', 'huber'. Check input data.")

def get_numpy_array_train_valid(X, y, Xv, yv):
    """Get np.ndarray from X, y"""

    # check X
    if isinstance(X, np.ndarray):
        pass
    if isinstance(X, pd.DataFrame):
        X = X.to_numpy()
    if isinstance(X, List):
        X = np.array(X)

    # check y
    if isinstance(y, np.ndarray):
        pass
    if isinstance(y, (pd.Series, pd.DataFrame)):
        y = y.to_numpy().ravel()
    if isinstance(y, List):
        y = np.array(y)

    # check Xv
    if isinstance(Xv, np.ndarray):
        pass
    if isinstance(Xv, pd.DataFrame):
        Xv = Xv.to_numpy()
    if isinstance(Xv, List):
        Xv = np.array(Xv)

    # check yv
    if isinstance(yv, np.ndarray):
        pass
    if isinstance(yv, (pd.Series, pd.DataFrame)):
        yv = yv.to_numpy().ravel()
    if isinstance(yv, List):
        yv = np.array(yv)

    if not isinstance(X, np.ndarray) and not isinstance(X, pd.DataFrame) and not isinstance(X, List):
        raise TypeError(
            f"Can't convert X_train, because X type is {type(X).__name__}. You must send Numpy, Pandas or List class object")

    if not isinstance(y, np.ndarray) and not isinstance(y, pd.DataFrame) and not isinstance(y, List):
        raise TypeError(
            f"Can't convert Y_train, because Y type is {type(y).__name__}. You must send Numpy, Pandas Series or List class object")

    if not isinstance(Xv, np.ndarray) and not isinstance(Xv, pd.DataFrame) and not isinstance(Xv, List):
        raise TypeError(
            f"Can't convert X_valid, because X type is {type(Xv).__name__}. You must send Numpy, Pandas or List class object")

    if not isinstance(yv, np.ndarray) and not isinstance(yv, pd.DataFrame) and not isinstance(yv, List):
        raise TypeError(
            f"Can't convert Y_valid, because Y type is {type(yv).__name__}. You must send Numpy, Pandas Series or List class object")

    return X, y, Xv, yv


def check_gain_param(max_depth, min_samples_leaf, min_samples_split, lmd, gmm, score):
    if (not isinstance(max_depth, int)) and (not np.issubdtype(max_depth, np.integer)):
        raise TypeError(f"Type 'max_depth' must be int. You send type {type(max_depth).__name__}")

    if not isinstance(min_samples_leaf, int) and not np.issubdtype(min_samples_leaf, np.integer):
        raise TypeError(f"Type 'min_samples_leaf' must be int. You send type {type(min_samples_leaf).__name__}")

    if not isinstance(min_samples_split, int) and not np.issubdtype(min_samples_split, np.integer):
        raise TypeError(f"Type 'min_samples_split' must be int. You send type {type(min_samples_split).__name__}")

    if not isinstance(lmd, (float, int)) and not np.issubdtype(lmd, (np.integer, np.float32, np.float64)):
        raise TypeError(f"Type 'lmd' must be int. You send type {type(lmd).__name__}")

    if not isinstance(gmm, (float, int)) and not np.issubdtype(gmm, (np.integer, np.float32, np.float64)):
        raise TypeError(f"Type 'gmm' must be int. You send type {type(gmm).__name__}")


    if max_depth <= 0:
        raise ValueError(f"Parameter 'max_depth' must be greater than zero. Check 'max_depth'.")

    if min_samples_leaf <= 0:
        raise ValueError(f"Parameter 'min_samples_leaf' must be greater than zero. Check 'min_samples_leaf'.")

    if min_samples_split <= 0:
        raise ValueError(f"Parameter 'min_samples_split' must be greater than zero. Check 'min_samples_split'.")

    if score != 'mse' and score != 'log_mse' and score != 'log_cosh':
        raise ValueError(f"Parameter 'score' must be one of this: 'mse', 'log_mse', 'log_cosh'. Check 'score'.")

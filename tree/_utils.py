import pandas as pd
import numpy as np
from typing import List


def _check_param(max_depth, min_samples_leaf, min_samples_split):
    """Checking type parameters"""

    if (not isinstance(max_depth, int)) and (not np.issubdtype(max_depth, np.integer)):
        raise TypeError(f"Type 'max_depth' must be int. You send type {type(max_depth).__name__}")

    if not isinstance(min_samples_leaf, int) and not np.issubdtype(min_samples_leaf, np.integer):
        raise TypeError(f"Type 'min_samples_leaf' must be int. You send type {type(min_samples_leaf).__name__}")

    if not isinstance(min_samples_split, int) and not np.issubdtype(min_samples_split, np.integer):
        raise TypeError(f"Type 'min_samples_split' must be int. You send type {type(min_samples_split).__name__}")

    if max_depth <= 0:
        raise ValueError(f"Parameter 'max_depth' must be greater than zero. Check 'max_depth'.")

    if min_samples_leaf <= 0:
        raise ValueError(f"Parameter 'min_samples_leaf' must be greater than zero. Check 'min_samples_leaf'.")

    if min_samples_split <= 0:
        raise ValueError(f"Parameter 'min_samples_split' must be greater than zero. Check 'min_samples_split'.")

def _check_param_adaptive(adaptive, n_combinations, randomization):
    if adaptive is not True and adaptive is not False:
        raise TypeError(f"Argument 'adaptive' must be bool type: 'True' or 'False'. Please, check input parameters")

    if not isinstance(n_combinations, int) and not np.issubdtype(n_combinations, np.integer):
        raise TypeError(f"Type 'n_combinations' must be int. You send type {type(n_combinations).__name__}")

    if not isinstance(randomization, str):
        raise TypeError(f"Type 'randomization' must be str. You send type {type(randomization).__name__}")

    if randomization != 'sum' and randomization != 'prod' and randomization != 'mean':
        raise ValueError(f"Argument 'randomization' must be 'str', 'prod' or 'mean'. You send '{randomization}'")

    if n_combinations <= 0:
        raise ValueError(f"Parameter 'n_combinations' must be greater than zero. Check 'n_combinations'.")



def get_numpy_array_train(X, y):
    """Get np.ndarray from X, y"""

    # check X
    if isinstance(X, np.ndarray):
        pass
    elif isinstance(X, pd.DataFrame):
        X = X.to_numpy()
    elif isinstance(X, List):
        X = np.array(X)

    # check y
    if isinstance(y, np.ndarray):
        pass
    elif isinstance(y, (pd.Series, pd.DataFrame)):
        y = y.to_numpy().ravel()
    elif isinstance(y, List):
        y = np.array(y)

    if not isinstance(X, np.ndarray) and not isinstance(X, pd.DataFrame) and not isinstance(X, List):
        raise TypeError(f"Can't convert X, because X type is {type(X).__name__}. You must send Numpy, Pandas or List class object")

    if not isinstance(y, np.ndarray) and not isinstance(y, (pd.Series, pd.DataFrame)) and not isinstance(y, List):
        raise TypeError(f"Can't convert Y, because Y type is {type(y).__name__}. You must send Numpy, Pandas Series or List class object")

    return X, y

def get_numpy_array_test(X):
    """Get np.ndarray from X, y"""

    # check X
    if isinstance(X, np.ndarray):
        pass
    if isinstance(X, pd.DataFrame):
        X = X.to_numpy()
    if isinstance(X, List):
        X = np.array(X)

    if not isinstance(X, np.ndarray) and not isinstance(X, pd.DataFrame) and not isinstance(X, List):
        raise TypeError(f"Can't convert X, because X type is {type(X).__name__}. You must send Numpy, Pandas or List class object")
    return X

def convert_type_train(X, y):
    """Converting to float64"""
    X = X.astype(np.float64)
    y = y.astype(np.float64)

    return X, y


def convert_type_test(X):
    """Converting to float64"""
    X = X.astype(np.float64)

    return X
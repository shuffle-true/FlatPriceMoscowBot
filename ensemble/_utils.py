from tree import TreeRegressorSlow
from tree import TreeRegressor
from tree import TreeRegressorAdaptive

import numpy as np


def _check_base_model_class(base_model):
    if not isinstance(base_model(), (TreeRegressorSlow, TreeRegressor)):
        raise TypeError(f"Argument 'base_model' must be an instance of classes 'TreeRegressorSlow' or 'TreeRegressor'."
                        f"You send instance class {base_model().__class__.__name__}")



def _check_base_model_class_adaptive(base_model):
    if not isinstance(base_model(), (TreeRegressorAdaptive)):
        raise TypeError(f"Argument 'base_model' must be an instance of class 'TreeRegressorAdaptive'."
                        f"You send instance class {base_model().__class__.__name__}")

def _check_param(n_estimators):
    """Checking type parameters"""

    if (not isinstance(n_estimators, int)) and (not np.issubdtype(n_estimators, np.integer)):
        raise TypeError(f"Type 'n_estimators' must be int. You send type {type(n_estimators).__name__}")


    if n_estimators <= 1:
        raise ValueError(f"Parameter 'n_estimators' must be greater than one. Check 'n_estimators'.")




import pickle
from tree import TreeRegressor
from tree import TreeRegressorAdaptive
from tree import TreeRegressorSlow
from ensemble import BaggingTree
from ensemble import BaggingTreeAdaptive
from boosting import GBRegressor


def save_model(model, filename: str):
    # check param

    if not isinstance(model, (TreeRegressor,
                              TreeRegressorSlow,
                              TreeRegressorAdaptive,
                              BaggingTree,
                              BaggingTreeAdaptive,
                              GBRegressor)):

        raise TypeError(f'You must send one of model class. You send {model.__class__.__name__}. Check input data')

    with open(fr"{filename}.pkl", "wb") as output_file:
        pickle.dump(model, output_file)


def open_model(filename: str):
    with open(fr"{filename}.pkl", "rb") as input_file:
        return pickle.load(input_file)
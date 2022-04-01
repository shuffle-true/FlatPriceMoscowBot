import numpy as np
import warnings
warnings.filterwarnings("ignore")


def compute_biase_variance(regressor, X: np.array, y, num_runs=100):
    """
    :param regressor: sklearn estimator with fit(...) and predict(...) method
    :param X: numpy-array representing training set ob objects, shape [n_obj, n_feat]
    :param y: numpy-array representing target for training objects, shape [n_obj]
    :param num_runs: int, number of samples (s in the description of the algorithm)

    :returns: bias (float), variance (float), error (float)
    each value is computed using bootstrap
    """

    prediction = []
    oob = []
    error, counts = np.zeros(X.shape[0]), np.zeros(X.shape[0])
    for i in range(num_runs):
        # генерим индексы объектов, которые попадут в обучающую выборку
        idx = np.random.choice(X.shape[0],
                               size=X.shape[0],
                               replace=True)

        X_train = X[idx]
        y_train = y[idx]

        regressor.fit(X_train, y_train)

        # вычисляем индексы out-of-bag элементов
        idx_X = np.arange(0, X.shape[0])
        oob_ = np.setdiff1d(idx_X, idx)

        # делаем предсказания на этих объектах
        X_test = X[oob_]
        prediction, pred = np.append(prediction, regressor.predict(X_test)), regressor.predict(X_test)

        # считаем ошибку
        counts[oob_] += 1
        error[oob_] += (pred - y[oob_]) ** 2

        oob = np.append(oob, oob_)

    # считаем среднее по объектам
    prediction = prediction[oob.argsort()]
    oob = oob[oob.argsort()]

    pred_oob = np.dstack((oob, prediction))[0]

    res = np.split(pred_oob[:,1], np.unique(pred_oob[:, 0], return_index=True)[1][1:])

    # добавляем среднее смещение и выборочную дисперсию (разброс) для одного объекта
    mean_bias_obj = []
    var_varience_obj = []
    for i in range(len(res)):
        mean_bias_obj = np.append(mean_bias_obj, res[i].mean())
        var_varience_obj = np.append(var_varience_obj, np.nanvar(res[i], ddof = 1))


    # избавляемся от нанов в разбросе
    var_varience_obj =  np.where(np.isnan(var_varience_obj), 0, var_varience_obj)


    # смещение по всем объект
    mean_bias = (y[np.unique(oob).astype(int)] - mean_bias_obj) ** 2

    # усредненное смещение и разброс и ошибку по всем объектам - искомая величина
    bias = mean_bias.mean(axis = 0)
    varience = var_varience_obj.mean(axis = 0)
    error = (error[np.where(counts > 0)] / counts[np.where(counts > 0)]).mean()

    return bias, varience, error

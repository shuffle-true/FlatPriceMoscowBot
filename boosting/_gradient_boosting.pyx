import numpy as np
cimport numpy as np
from tree import TreeRegressor
from tqdm import tqdm

from numpy import float32 as DTYPE
from numpy import float64 as DOUBLE
from numpy import int32 as DTYPE_INT
from numpy import int64 as DOUBLE_INT


#------------------------------------------------------------------
#                      LOSS - FUNCTION - CLASS
#------------------------------------------------------------------

cdef class LossFunction:
    def MSE(self, y, x):
        return 0.5 * np.square(y - x).mean()
    def MSE_der(self, y, x):
        return x - y

    def LogMSE(self, y, x):
        return 0.5 * np.square(np.log2(y) - np.log2(x)).mean()

    def LogMSE_der(self, y, x):
        return ( np.log2(x) - np.log2(y) ) / (np.log(2) * x)

    def Log_cosh(self, y, x):
        return np.log(np.cosh( x - y)).mean()

    def Log_cosh_der(self, y, x):
        return np.tanh( x - y )

    def Huber(self, y, x):
        mod = np.abs( y - x )
        sigm = 1.35
        return (0.5 * ((y - x) ** 2) * (mod < sigm) + sigm * (mod - 0.5 * sigm)  * (mod >= sigm) ).mean()

    def Huber_der(self, y, x):
        mod = np.abs( y - x )
        sigm = 1.35
        return ((x - y) * (mod < sigm) + ((sigm * (x - y)) / np.abs(y - x)) * (mod >= sigm))


#------------------------------------------------------------------
#                      BASE - BOOSTING - CLASS
#------------------------------------------------------------------


cdef class BaseBoosting:
    def __init__(self,
                 base_model_class,
                 dict base_model_params,
                 int n_estimators,
                 float learning_rate,
                 bint randomization,
                 float subsample,
                 random_seed,
                 str custom_loss,
                 bint use_best_model,
                 n_iter_early_stopping,
                 float train_valid_control,
                 show_tqdm
                 ):

        self.base_model_class = base_model_class
        self.base_model_params = {} if base_model_params is None else base_model_params
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        # if true then bootstrap
        self.randomization = randomization
        self.subsample = subsample
        self.random_seed = random_seed
        self.custom_loss = custom_loss
        self.use_best_model = use_best_model
        self.n_iter_early_stopping = n_iter_early_stopping
        self.valid_control = train_valid_control

        self.loss = LossFunction()

        self.history = {}
        self.history['train'] = []
        self.history['valid'] = []

        self.models = []


        if self.custom_loss == 'mse':
            self.loss_fn = self.loss.MSE
            self.loss_derivative = self.loss.MSE_der

        if self.custom_loss == 'log_mse':
            self.loss_fn = self.loss.LogMSE
            self.loss_derivative = self.loss.LogMSE_der

        if self.custom_loss == 'log_cosh':
            self.loss_fn = self.loss.Log_cosh
            self.loss_derivative = self.loss.Log_cosh_der

        if self.custom_loss == 'huber':
            self.loss_fn = self.loss.Huber
            self.loss_derivative = self.loss.Huber_der


        self.show_tqdm = show_tqdm


    cdef _base_build(self, _, sub_X, sub_y, predictions):
        """Building a tree base ensemble"""
        model = self.base_model_class(**self.base_model_params)

        if _ == 0:
            s_train = sub_y
        else:
            s_train = -self.loss_derivative(sub_y, predictions)


        model.fit(sub_X, s_train)

        predictions += self.learning_rate * model.predict(sub_X)

        self.models.append(model)

        return predictions

    cdef _append_history_without_valid(self, y_train, predictions):
        train_loss = self.loss_fn(y_train, predictions)
        self.history['train'].append(train_loss)

    cdef _append_history_with_valid(self, y_train, pred, y_valid, valid_pred):
        train_loss = self.loss_fn(y_train, pred)
        valid_loss = self.loss_fn(y_valid, valid_pred)
        self.history['train'].append(train_loss)
        self.history['valid'].append(valid_loss)



    cdef _predict_valid(self, _, X_valid, mean):
        valid_pred = np.ones([X_valid.shape[0]]) * mean

        for i in range(_):
            valid_pred += self.learning_rate * self.models[i].predict(X_valid)

        return valid_pred



    cdef get_bootstrap(self, sub_X, sub_y):
        np.random.seed(self.random_seed)

        ind = np.random.choice(np.arange(sub_X.shape[0]),
                           size=int(sub_X.shape[0] * self.subsample),
                           replace=False)
        sub_X_bootstrap, sub_y_bootstrap = sub_X[ind], sub_y[ind]

        return sub_X_bootstrap, sub_y_bootstrap



#------------------------------------------------------------------
#                      GRADIENT - BOOSTING - CLASS
#------------------------------------------------------------------


cdef class GradientBoostingRegressor(BaseBoosting):
    def __init__(self,
                 base_model_class = TreeRegressor,
                 dict base_model_params = None,
                 int n_estimators = 10,
                 float learning_rate = 1e-1,
                 bint randomization = False,
                 float subsample = 0.3,
                 random_seed = None,
                 str custom_loss = 'mse',
                 bint use_best_model = False,
                 n_iter_early_stopping = None,
                 train_valid_control = None,
                 show_tqdm = False):

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
                         train_valid_control,
                         show_tqdm)

    cdef fit_without_valid(self, X_train, y_train):
        self.mean_y_train = y_train.mean()

        if self.randomization:
            train_predictions = np.mean(y_train) * np.ones([int(self.subsample * y_train.shape[0])])
        else:
            train_predictions = np.mean(y_train) * np.ones([y_train.shape[0]])

        predictions = train_predictions.copy()

        X_train_, y_train_ = X_train, y_train


        if self.show_tqdm:
            for _ in tqdm(range(self.n_estimators)):

                if self.randomization:
                    X_train_, y_train_ = self.get_bootstrap(X_train, y_train)

                predictions = self._base_build(_, X_train_, y_train_, predictions)

                if _ >= 1:
                    self._append_history_without_valid(y_train_, predictions)

        else:

            for _ in range(self.n_estimators):

                if self.randomization:
                    X_train_, y_train_ = self.get_bootstrap(X_train, y_train)

                predictions = self._base_build(_, X_train_, y_train_, predictions)

                if _ >= 1:
                    self._append_history_without_valid(y_train_, predictions)




    cdef _fit_with_valid(self,
                         X_train,
                         y_train,
                         X_valid,
                         y_valid):

        self.mean_y_train = y_train.mean()

        mean = y_valid.mean()

        if self.randomization:
            train_predictions = np.mean(y_train) * np.ones([int(self.subsample * y_train.shape[0])])
        else:
            train_predictions = np.mean(y_train) * np.ones([y_train.shape[0]])

        predictions = train_predictions.copy()

        X_train_, y_train_ = X_train, y_train


        if self.show_tqdm:
            for _ in tqdm(range(self.n_estimators)):

                if self.randomization:
                    X_train_, y_train_ = self.get_bootstrap(X_train, y_train)

                predictions = self._base_build(_, X_train_, y_train_, predictions)


                if _ >= 1:
                    valid_predictions = self._predict_valid(_, X_valid, mean)

                    self._append_history_with_valid(y_train_, predictions, y_valid, valid_predictions)

                if self.n_iter_early_stopping is not None and _ > self.n_iter_early_stopping:

                    if abs(self.history['valid'][-1] - self.history['valid'][-self.n_iter_early_stopping]) <= self.valid_control:
                        self.n_estimators = _
                        break

        else:

            for _ in range(self.n_estimators):

                if self.randomization:
                    X_train_, y_train_ = self.get_bootstrap(X_train, y_train)

                predictions = self._base_build(_, X_train_, y_train_, predictions)


                if _ >= 1:
                    valid_predictions = self._predict_valid(_, X_valid, mean)

                    self._append_history_with_valid(y_train_, predictions, y_valid, valid_predictions)

                if self.n_iter_early_stopping is not None and _ > self.n_iter_early_stopping:

                    if abs(self.history['valid'][-1] - self.history['valid'][-self.n_iter_early_stopping]) <= self.valid_control:
                        self.n_estimators = _
                        break


    cpdef _build(self, X_train, y_train, X_valid = None, y_valid = None):
        if X_valid is None and y_valid is None:
            self.fit_without_valid(X_train, y_train)

        elif X_valid is not None and y_valid is not None:
            self._fit_with_valid(X_train, y_train, X_valid, y_valid)


    cdef _predict_best_model(self, X_test):
        arg_min = np.argmin(self.history['valid']) + 1

        predictions = np.ones([X_test.shape[0]]) * self.mean_y_train
        # predictions = np.zeros(X_test.shape[0])

        for _ in range(arg_min):
            predictions += self.learning_rate * self.models[_].predict(X_test)

        return predictions



    cpdef _predict(self, X_test):
        if self.use_best_model:
            return self._predict_best_model(X_test)
        else:
            predictions = np.ones([X_test.shape[0]]) * self.mean_y_train

            # predictions = np.zeros(X_test.shape[0])

            for _ in range(self.n_estimators):
                predictions += self.learning_rate * self.models[_].predict(X_test)

            return predictions




#------------------------------------------------------------------
#                      BASE - GAIN - TREE - CLASS
#------------------------------------------------------------------

cdef class RTG:
    def __init__(self,
                 size_t max_depth,
                 size_t min_samples_leaf,
                 size_t min_samples_split,
                 double lmd,
                 double gmm,
                 str score):

        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.min_samples_split = min_samples_split
        self.lmd = lmd
        self.gmm = gmm
        self.score = score


    cpdef tuple _check_input(self, np.ndarray X, np.ndarray y):
        """Checking dtype X, y"""
        if X.dtype != DOUBLE and X.dtype != DTYPE and X.dtype != DOUBLE_INT and X.dtype != DTYPE_INT:
            raise TypeError(f"X_train type must be int or float. Type X_train now: {X.dtype}")

        elif y.dtype != DOUBLE and y.dtype != DTYPE and y.dtype != DOUBLE_INT and y.dtype != DTYPE_INT:
            raise TypeError(f"y_train type must be int or float. Type y_train now: {y.dtype}")

        return X, y

    cpdef np.ndarray _check_input_test(self, np.ndarray X):
        """Checking dtype X_test"""
        if X.dtype != DOUBLE and X.dtype != DTYPE and X.dtype != DOUBLE_INT and X.dtype != DTYPE_INT:
            raise TypeError(f"X_test type must be int or float. Type X_test now: {X.dtype}")
        return X



    cdef list _fit_tree_mse(self,
                 np.ndarray sub_X,
                 np.ndarray sub_y):

        cdef float value = np.mean(sub_y)
        cdef float best_error = ((sub_y - value) ** 2).sum()
        cdef float error = best_error
        cdef size_t cnt_features = sub_X.shape[1]

        cdef np.ndarray[np.int64_t, ndim = 1] arg
        cdef float N = sub_X.shape[0]
        cdef float Nl = sub_X.shape[0]
        cdef float Nr = 0
        cdef size_t ind
        cdef size_t thres = 1
        cdef double gain
        cdef double gl
        cdef double gr

        cdef double best_gain = -self.gmm

        threshold_best, feature_split, left_value, right_value = None, None, None, None


        for feature in range(cnt_features):
            feature_vector = sub_X[:, feature]

            gl = sub_y.sum()
            gr = 0.0

            arg = np.argsort(feature_vector)

            while thres < N - 1:
                Nl -= 1
                Nr += 1

                ind = arg[thres]
                threshold = feature_vector[ind]

                gl -= sub_y[ind]
                gr += sub_y[ind]

                gain = (gl**2) / (Nl + self.lmd)  + (gr**2) / (Nr + self.lmd)
                gain -= ((gl + gr)**2) / (Nl + Nr + self.lmd) + self.gmm

                if (gain > best_gain) and (min(Nl, Nr) > self.min_samples_leaf):
                    best_gain = gain
                    left_value = -gl / (Nl + self.lmd)
                    right_value = -gr / (Nr + self.lmd)
                    threshold_best = threshold
                    feature_split = feature

                thres += 1

        return [value, threshold_best, feature_split, left_value, right_value]


    cpdef _build(self,
                 np.ndarray sub_X,
                 np.ndarray sub_y,
                 dict NODE,
                 size_t depth):

        cdef size_t y_size = sub_y.size

        NODE['samples'] = y_size

        if y_size < self.min_samples_split:
            return

        if depth == 0:
            return

        if self.score == 'mse':
            NODE['value'], NODE['threshold_best'], NODE['feature_split'], left_value, right_value = self._fit_tree_mse(sub_X,
                                                                                                                sub_y)
        elif self.score == 'logmse':
            pass

        if NODE['feature_split'] is None:
            return

        NODE['left_child'], NODE['right_child'] = {}, {}

        NODE['left_child']['value'] = left_value
        NODE['left_child']['feature_split'] = None

        NODE['right_child']['value'] = right_value
        NODE['right_child']['feature_split'] = None


        idx_l = sub_X[:, NODE['feature_split']] > NODE['threshold_best']
        idx_r = sub_X[:, NODE['feature_split']] <= NODE['threshold_best']

        self._build(sub_X[idx_l, :], sub_y[idx_l], NODE['left_child'], depth - 1)
        self._build(sub_X[idx_r, :], sub_y[idx_r], NODE['right_child'], depth - 1)

        return NODE

    cdef _get_predict_node(self, np.ndarray X_test, dict NODE):
        # return target if split not found - const value
        if NODE['feature_split'] is None:
            return NODE['value']

        # get down, if split found
        if X_test[NODE['feature_split']] > NODE['threshold_best']:
            return self._get_predict_node(X_test, NODE['left_child'])
        else:
            return self._get_predict_node(X_test, NODE['right_child'])

    cpdef _predict(self, np.ndarray X_test, dict NODE):
        """Get predict for X_test"""
        predict = []
        for obj in range(X_test.shape[0]):
            predict.append(self._get_predict_node(X_test[obj], NODE))
        return np.array(predict)


#------------------------------------------------------------------
#                      XGBOOST - CLASS
#------------------------------------------------------------------

cdef class XGBOOST(BaseBoosting):
    def __init__(self,
                 size_t n_estimators = 100,
                 size_t max_depth = 3,
                 size_t min_samples_leaf = 2,
                 size_t min_samples_split = 1,
                 double lmd = 1.0,
                 double gmm = 0.1,
                 str score = 'mse',
                 float learning_rate = 0.1,
                 bint adaptive = True,
                 bint randomization = False,
                 float subsample = 0.3,
                 random_seed = None,
                 bint use_best_valid_model = False,
                 str custom_loss = 'mse',
                 n_iter_early_stopping = None,
                 float valid_control = 1e-7,
                 show_tqdm = True,
                 base_model_class = None):

        self.adaptive = adaptive

        base_model_params = {
            'max_depth': max_depth,
            'min_samples_leaf': min_samples_leaf,
            'min_samples_split': min_samples_split,
            'lmd': lmd,
            'gmm': gmm,
            'score': score
            }

        super().__init__(
            base_model_class,
            base_model_params,
            n_estimators,
            learning_rate,
            randomization,
            subsample,
            random_seed,
            custom_loss,
            use_best_valid_model,
            n_iter_early_stopping,
            valid_control,
            show_tqdm)


    cdef _base_build_gain(self, _, sub_X, sub_y, predictions):
        """Building a tree base ensemble"""
        model = self.base_model_class(**self.base_model_params)

        if _ == 0:
            s_train = sub_y
        else:
            s_train = -self.loss_derivative(sub_y, predictions)

        if self.adaptive and _ > 3:
            if np.abs(self.history['train'][-1] - self.history['train'][-2]) < self.valid_control:
                self.valid_control /= 2
                self.base_model_params['max_depth'] += 1
                self.learning_rate /= 1.1

        model.fit(sub_X, -s_train)

        predictions += self.learning_rate * model.predict(sub_X)

        self.models.append(model)

        return predictions


    cdef fit_without_valid(self, X_train, y_train):
        self.mean_y_train = y_train.mean()

        if self.randomization:
            train_predictions = np.mean(y_train) * np.ones([int(self.subsample * y_train.shape[0])])
        else:
            train_predictions = np.mean(y_train) * np.ones([y_train.shape[0]])

        predictions = train_predictions.copy()

        X_train_, y_train_ = X_train, y_train


        if self.show_tqdm:
            for _ in tqdm(range(self.n_estimators)):

                if self.randomization:
                    X_train_, y_train_ = self.get_bootstrap(X_train, y_train)

                predictions = self._base_build_gain(_, X_train_, y_train_, predictions)

                if _ >= 1:
                    self._append_history_without_valid(y_train_, predictions)

        else:

            for _ in range(self.n_estimators):

                if self.randomization:
                    X_train_, y_train_ = self.get_bootstrap(X_train, y_train)

                predictions = self._base_build(_, X_train_, y_train_, predictions)

                if _ >= 1:
                    self._append_history_without_valid(y_train_, predictions)


    cdef _fit_with_valid(self,
                         X_train,
                         y_train,
                         X_valid,
                         y_valid):

        self.mean_y_train = y_train.mean()

        mean = y_valid.mean()

        if self.randomization:
            train_predictions = np.mean(y_train) * np.ones([int(self.subsample * y_train.shape[0])])
        else:
            train_predictions = np.mean(y_train) * np.ones([y_train.shape[0]])

        predictions = train_predictions.copy()

        X_train_, y_train_ = X_train, y_train


        if self.show_tqdm:
            for _ in tqdm(range(self.n_estimators)):

                if self.randomization:
                    X_train_, y_train_ = self.get_bootstrap(X_train, y_train)

                predictions = self._base_build_gain(_, X_train_, y_train_, predictions)


                if _ >= 1:
                    valid_predictions = self._predict_valid(_, X_valid, mean)

                    self._append_history_with_valid(y_train_, predictions, y_valid, valid_predictions)

                if self.n_iter_early_stopping is not None and _ > self.n_iter_early_stopping:

                    if abs(self.history['valid'][-1] - self.history['valid'][-self.n_iter_early_stopping]) <= self.valid_control:
                        self.n_estimators = _
                        break

        else:

            for _ in range(self.n_estimators):

                if self.randomization:
                    X_train_, y_train_ = self.get_bootstrap(X_train, y_train)

                predictions = self._base_build_gain(_, X_train_, y_train_, predictions)


                if _ >= 1:
                    valid_predictions = self._predict_valid(_, X_valid, mean)

                    self._append_history_with_valid(y_train_, predictions, y_valid, valid_predictions)

                if self.n_iter_early_stopping is not None and _ > self.n_iter_early_stopping:

                    if abs(self.history['valid'][-1] - self.history['valid'][-self.n_iter_early_stopping]) <= self.valid_control:
                        self.n_estimators = _
                        break



    cpdef _build(self, X_train, y_train, X_valid = None, y_valid = None):
        if X_valid is None and y_valid is None:
            self.fit_without_valid(X_train, y_train)

        elif X_valid is not None and y_valid is not None:
            self._fit_with_valid(X_train, y_train, X_valid, y_valid)


    cdef _predict_best_model(self, X_test):
        arg_min = np.argmin(self.history['valid']) + 1

        predictions = np.ones([X_test.shape[0]]) * self.mean_y_train
        # predictions = np.zeros(X_test.shape[0])

        for _ in range(arg_min):
            predictions += self.learning_rate * self.models[_].predict(X_test)

        return predictions



    cpdef _predict(self, X_test):
        if self.use_best_model:
            return self._predict_best_model(X_test)
        else:
            predictions = np.ones([X_test.shape[0]]) * self.mean_y_train

            # predictions = np.zeros(X_test.shape[0])

            for _ in range(self.n_estimators):
                predictions += self.learning_rate * self.models[_].predict(X_test)

            return predictions










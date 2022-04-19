from utils_ import open_model
import pandas as pd



def predict(user_name: str):
    flag_dt_40 = True

    model = open_model('ML_MODEL/DECISION_TREE_120')
    X_test = pd.read_excel('USER_REQUEST/{}.xlsx'.format(user_name))
    X_test = X_test.drop('price', axis = 1)
    dt_120 = round(model.predict(X_test)[0])

    model = open_model('ML_MODEL/DECISION_TREE_40')
    dt_40 = round(model.predict(X_test)[0])

    model = open_model('ML_MODEL/DECISION_TREE_SLOW_120')
    dt_slow_120 = round(model.predict(X_test)[0])

    model = open_model('ML_MODEL/BAGGING_TREE_SLOW_120_10')
    bagging_slow_120_10 = round(model.predict(X_test)[0])

    model = open_model('ML_MODEL/BAGGING_TREE_SLOW_120_50')
    bagging_slow_120_50 = round(model.predict(X_test)[0])

    model = open_model('ML_MODEL/BAGGING_TREE_SLOW_120_100')
    bagging_slow_120_100 = round(model.predict(X_test)[0])

    ans = []

    if dt_120 == 40030.0:
        ans.append(( dt_120 + dt_40 ) / 2)
        flag_dt_40 = False

    if flag_dt_40:
        ans.append(dt_120)

    ans.append(dt_slow_120)
    ans.append(bagging_slow_120_10)
    ans.append(bagging_slow_120_50)
    ans.append(bagging_slow_120_100)



    return ans
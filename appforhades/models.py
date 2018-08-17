
# coding: utf-8

from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor
from sklearn.base import TransformerMixin
import pandas as pd
import numpy as np


class Data_Transform(TransformerMixin):
    def __init__(self, columns):
        self._columns = columns
        self._categories = None
    
    def transform(self, X):
        if isinstance(X, list):
            filtered = pd.DataFrame.from_records(X, columns=self._columns)
        else:
            filtered = X.loc[:,self._columns]
        
        filtered.loc[:,'timestamp'] = pd.to_datetime(filtered['timestamp']).astype(np.int64) // 10 ** 9
        filtered['sub_area'] = filtered['sub_area'].astype('category', categories=self._categories)
        one_hots = pd.get_dummies(filtered['sub_area'], prefix='sub_area', dummy_na=True)  
        filtered = pd.concat((one_hots, filtered), axis=1)
        filtered.drop('sub_area', axis=1, inplace=True)
        return filtered
    
    def fit(self, X, y=None, *_):
        self._categories = pd.Series(X['sub_area']).unique()
        return self

    def get_sub_areas(self):
    	return self._categories


class XGRegr(XGBRegressor):
    def __init__(self, max_depth=3, learning_rate=0.1, n_estimators=100, silent=True,
                 objective='reg:linear', booster='gbtree', n_jobs=1, nthread=None,
                 gamma=0, min_child_weight=1, max_delta_step=0, subsample=1,
                 colsample_bytree=1, colsample_bylevel=1, reg_alpha=0,
                 reg_lambda=1, scale_pos_weight=1, base_score=0.5, random_state=0,
                 seed=None, missing=None, **kwargs):
        
        super().__init__(max_depth=max_depth, learning_rate=learning_rate, n_estimators=n_estimators, silent=silent,
                         objective=objective, booster=booster, n_jobs=n_jobs, nthread=nthread,
                         gamma=gamma, min_child_weight=min_child_weight, max_delta_step=max_delta_step, subsample=subsample,
                         colsample_bytree=colsample_bytree, colsample_bylevel=colsample_bylevel, reg_alpha=reg_alpha,
                         reg_lambda=reg_lambda, scale_pos_weight=scale_pos_weight, base_score=base_score, random_state=random_state,
                         seed=seed, missing=missing, **kwargs)
        
    def transform(self, *args):
        return self.predict(*args).reshape(-1,1)


class Pipe:
    def __init__(self):
        self._xgb = XGRegr(n_estimators=100, learning_rate=0.08, gamma=0, subsample=0.75,
                           colsample_bytree=1, max_depth=7)

        self._trans = Data_Transform(['full_sq', 'life_sq', 'floor', 'max_floor',
                                      'num_room', 'build_year', 'timestamp', 'sub_area'])
    
        self._pipe = Pipeline([('trans', self._trans), ('xgb', self._xgb)])

    def get_sub_areas(self):
        return self._trans.get_sub_areas()

    def fit(self, X, y):
        self._pipe.fit(X, y)

    def predict(self, X):
        return self._pipe.predict(X)

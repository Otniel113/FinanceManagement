import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class TopEmitenTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, emiten_list):
        self.emiten_list = emiten_list

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_copy = X.copy()
        if 'Emiten' in X_copy.columns:
            X_copy['Is_Top_Emiten'] = X_copy['Emiten'].apply(lambda x: 1 if x in self.emiten_list else 0)
            # Note: in Tab4, this returned X_copy[fitur_der]. 
            # We'll just return X_copy if it fails in Tab4, we can fix it.
            return X_copy
        return X_copy

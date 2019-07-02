from sklearn.preprocessing import Normalizer
import pandas as pd


# 正则化  'l1', 'l2', or 'max'
def normalizer(df, norm='l1'):
    col_name_list = df.columns.values
    nor = Normalizer(norm=norm)
    df = nor.fit_transform(df)
    df = pd.DataFrame(df, columns=col_name_list)
    return df
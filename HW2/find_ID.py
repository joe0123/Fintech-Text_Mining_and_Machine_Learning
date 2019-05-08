import numpy as np
import pandas as pd

df = pd.read_csv('client_vec_4.csv', encoding='utf-8')
a = (df['曾經持有投資產品-現金、存款、定存、貨幣型基金與保本型基金'].values == 1) & (df['家庭年收入-50 萬元~100 萬元'].values == 1)
print(df['客戶ID'][a].values)
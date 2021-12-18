import pandas as pd

medical=pd.read_csv('medical.csv')
medical.to_pickle('medical.pkl', protocol = 4) 
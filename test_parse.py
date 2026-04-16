import pandas as pd
df = pd.read_csv('dataRaw/HACKATHON ZICER 202604 TRANSAKCIJE.csv', sep=';', encoding='latin-1', low_memory=False, nrows=5)
print(df.columns.tolist())
print(df.iloc[0].to_dict())

import pandas as pd

cols = [
    'IDENTIFIKATOR_PROIZVODA', 'DATUM_I_VRIJEME_TRANSAKCIJE', 'IZNOS_TRANSAKCIJE_U_DOMICILNOJ_VALUTI',
    'VALUTA_TRANSAKCIJE', 'KANAL', 'SMJER', 'DRZAVA_DRUGE_STRANE', 'DJELATNOST_DRUGE_STRANE',
    'KATEGORIJA_DJELATNOSTI_DRUGE_STRANE', 'VRSTA_TRANSAKCIJE'
]
df = pd.read_csv('dataRaw/HACKATHON ZICER 202604 TRANSAKCIJE.csv', sep=';', encoding='latin-1', 
                 names=cols + ['EXTRA'], header=0, low_memory=False, nrows=10)

mask = df['EXTRA'].notna()
df.loc[mask, 'KATEGORIJA_DJELATNOSTI_DRUGE_STRANE'] = df.loc[mask, 'KATEGORIJA_DJELATNOSTI_DRUGE_STRANE'] + ';' + df.loc[mask, 'VRSTA_TRANSAKCIJE']
df.loc[mask, 'VRSTA_TRANSAKCIJE'] = df.loc[mask, 'EXTRA']
df = df.drop(columns=['EXTRA'])

print(df.iloc[0].to_dict())

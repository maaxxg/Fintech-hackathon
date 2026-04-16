import pandas as pd
from pathlib import Path

DATA = Path('dataRaw')
name = 'HACKATHON ZICER 202604 TRANSAKCIJE.csv'
cols = [
    'IDENTIFIKATOR_PROIZVODA', 'DATUM_I_VRIJEME_TRANSAKCIJE', 'IZNOS_TRANSAKCIJE_U_DOMICILNOJ_VALUTI',
    'VALUTA_TRANSAKCIJE', 'KANAL', 'SMJER', 'DRZAVA_DRUGE_STRANE', 'DJELATNOST_DRUGE_STRANE',
    'KATEGORIJA_DJELATNOSTI_DRUGE_STRANE', 'VRSTA_TRANSAKCIJE'
]
df = pd.read_csv(DATA / name, sep=';', encoding='latin-1', 
                 names=cols + ['EXTRA'], header=0, low_memory=False)
mask = df['EXTRA'].notna()
df.loc[mask, 'KATEGORIJA_DJELATNOSTI_DRUGE_STRANE'] = df.loc[mask, 'KATEGORIJA_DJELATNOSTI_DRUGE_STRANE'] + ';' + df.loc[mask, 'VRSTA_TRANSAKCIJE']
df.loc[mask, 'VRSTA_TRANSAKCIJE'] = df.loc[mask, 'EXTRA']
df = df.drop(columns=['EXTRA'])

def parse_date(s):
    s = s.str.strip().str.replace(r'(\d{4})/', r'\1', regex=True)
    return pd.to_datetime(s, format='%d/%m/%Y %H:%M:%S', errors='coerce')

df['DATUM'] = parse_date(df['DATUM_I_VRIJEME_TRANSAKCIJE'])
ts = df['DATUM'].dropna().sort_values()
print("Non-NaT values:", len(ts))

import json

new_func = """def read_csv(name):
    if name == 'HACKATHON ZICER 202604 TRANSAKCIJE.csv':
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
        return df
    else:
        return pd.read_csv(DATA / name, sep=';', encoding='latin-1', low_memory=False)
"""

with open('eda.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        if "def read_csv(name):" in source:
            # Replace the block
            # In the original, it was:
            # def read_csv(name):
            #     return pd.read_csv(DATA / name, sep=';', encoding='latin-1', low_memory=False, index_col=False)
            
            # The cell might have other stuff before or after, so we'll replace just that function
            
            lines = source.split('\n')
            new_lines = []
            skip = False
            for line in lines:
                if line.startswith("def read_csv(name):"):
                    skip = True
                    new_lines.append(new_func)
                elif skip and line.startswith("    return pd.read_csv"):
                    pass # skip this line
                elif skip and not line.startswith("    "):
                    # We are past the function
                    skip = False
                    new_lines.append(line)
                elif not skip:
                    new_lines.append(line)
            
            # Join and convert to array of lines ending with \n except last
            final_source = "\n".join(new_lines).splitlines(True)
            cell['source'] = final_source

with open('eda.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

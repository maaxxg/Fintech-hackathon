import pandas as pd
import json
import random
import sys
import re
import math

def safe_value(v):
    if pd.isna(v):
        return None
    if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
        return None
    return v

# Load data
holdout_ids = json.load(open('processed/split_holdout.json'))
df = pd.read_parquet('processed/clients_eligible.parquet')

# Filter
filtered_df = df[df['IDENTIFIKATOR_KLIJENTA'].isin(holdout_ids)].copy()

# Prepare array
clients_list = []
for idx, row in filtered_df.iterrows():
    client = {}
    client['name'] = f"Client {row['IDENTIFIKATOR_KLIJENTA']}"
    client['riskScore'] = random.randint(10, 95)
    client['riskExplanation'] = 'Fake risk explanation for now.'
    client['valueScore'] = random.randint(10, 95)
    client['valueExplanation'] = 'Fake value explanation for now.'
    client['email'] = f"{str(row['IDENTIFIKATOR_KLIJENTA']).lower()}@example.com"
    client['phone'] = '+385 00 000 0000'
    client['accountType'] = 'Standard'
    
    date_val = safe_value(row['DATUM_PRVOG_POCETKA_POSLOVNOG_ODNOSA'])
    client['joinDate'] = str(date_val)[:10] if date_val else '2020-01-01'

    # Add all other properties
    for col in df.columns:
        val = safe_value(row[col])
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            client[col] = str(val)[:10] if val else None
        else:
            client[col] = val
            
    clients_list.append(client)

# Read seed.js
with open('seed.js', 'r', encoding='utf-8') as f:
    seed_content = f.read()

# Replace the clients array
start_marker = "const clients = ["
end_marker = "];\n\n\tconst clientsCol"

if start_marker in seed_content and end_marker in seed_content:
    parts_1 = seed_content.split(start_marker)
    parts_2 = parts_1[1].split(end_marker)
    
    js_array_str = "[\n"
    for c in clients_list:
        c_str = json.dumps(c, ensure_ascii=False)
        js_array_str += f"\t\t{{ managerId: uid, ...{c_str} }},\n"
    js_array_str += "\t]"
    
    new_content = parts_1[0] + "const clients = " + js_array_str + ";\n\n\tconst clientsCol" + parts_2[1]
    
    with open('seed.js', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully updated seed.js with {} clients.".format(len(clients_list)))
else:
    print("Could not find markers in seed.js")
    sys.exit(1)

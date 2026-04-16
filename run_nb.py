import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import os

with open('eda.ipynb') as f:
    nb = nbformat.read(f, as_version=4)

ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
try:
    ep.preprocess(nb, {'metadata': {'path': os.getcwd()}})
    print("Notebook executed successfully.")
except Exception as e:
    print(f"Error executing notebook: {e}")

with open('eda_executed.ipynb', 'w') as f:
    nbformat.write(nb, f)

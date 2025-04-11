
# Due to Git Large File Storage (LFS) limitations, please visit https://huggingface.co/datasets/sweetssweets/NMRBank to view and download the latest NMRBank dataset.

```python
https://huggingface.co/datasets/sweetssweets/NMRBank
```

## 1. NMRBank data (225809)

We batch processed 380,220 NMR segments using NMRExtractor. After removing entries with empty 13C NMR chemical shifts, we obtained about 260,000 entries. Further filtering out entries with empty IUPAC names and NMR chemical shifts resulted in 225,809 entries. 

- ```NMRBank_data_225809.zip```

## 2. NMRBank data with SMILES (156621)

To normalize these data, we converted IUPAC names to SMILES using ChemDraw and OPSIN, successfully converting 156,621 entries. We then normalized SMILES using RDKit.

- ```NMRBank_data_with_SMILES_156621_in_225809.zip```

## 3. NMRBank dataset in json format

We also provide the NMRBank dataset in JSON format for convenient access and easy viewing.

- ```NMRBank_json_format\NMRBank_data_225809_json.zip```
- ```NMRBank_json_format\NMRBank_data_with_SMILES_156621_in_225809_json.zip```

## 4. NMRBank dataset reading and viewing

### Read csv file
```python
import pandas as pd
# Reading csv Files
df = pd.read_csv(r"NMRBank_data_225809.csv", encoding="utf-8")
df
```

### Read json file
```python
import pandas as pd
# Reading json Files
df = pd.read_json(r"NMRBank_data_225809.json", orient="records", lines=True)
df
```

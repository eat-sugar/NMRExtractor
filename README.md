# 🔔 NMRExtractor

## Download
```bash
git clone https://github.com/eat-sugar/NMRExtractor.git
cd NMRExtractor
```
## PubMed Articles
Publicly available articles from the PubMed database can be downloaded from https://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/

The data description of PubMed database can be found at https://pmc.ncbi.nlm.nih.gov/tools/ftp/

## 🖊 Datasets and Codes

Preprocessed data, NMRExtractor paragraph extraction and fine-tuning code, Rule-based method code, NMRBank datasets, README workflows have been placed in the corresponding folders:

- ```data/```

- ```NMRExtractor/```

- ```Rule-based/```

- ```NMRBank/```


## 💡 Demo of NMRExtractor

### NMR Data Extraction Demo: Extracting data from an NMR data paragraph using NMRExtractor
Here we provide an example notebook using Gradio visualization and NMRExtractor to extract NMR data in ```demo/demo_1_use_NMRExtractor_extract_NMR_data_from_NMR_paragraph.ipynb```, which you can use locally to extract NMR data from paragraphs using your computer's CPU or GPU.

We also provide an online demo of NMRExtractor at https://huggingface.co/spaces/sweetssweets/NMRExtractor

### Complete workflow for NMR data extraction: Obtaining data from literature using NMRExtractor
A full workflow for extracting NMR data from an article using NMRExtractor is also provided in ```demo/demo_2_use_NMRExtractor_extract_NMR_data_from_Article.ipynb```, using 1×40GB A100 (using vllm).


## 🏆 Download and use NMRExtractor model weights

Replace the "model_path" in the code with the folder path where the NMRExtractor weights are located.

The model weights of NMRExtractor can be downloaded from 
https://huggingface.co/sweetssweets/NMRExtractor. 

# 🔔 NMRBank

## 🔔Due to Git Large File Storage (LFS) limitations, please visit https://huggingface.co/datasets/sweetssweets/NMRBank to view and download the latest NMRBank dataset.

The NMRBank dataset can be downloaded from the ```NMRBank``` folder in both csv and json formats.

NMRBank contains 225,809 experimental 1H and 13C NMR data extracted from the literature, and we have successfully converted the IUPAC names of 156,621 of these data into SMILES.
We have normalized the dataset based on standardized SMILES strings. The total number of unique SMILES strings is 149,135.
For the highest confidence interval (0.6–1), the number of unique SMILES records is 123,174.
For the highest confidence interval (0.8–1), the number of unique SMILES records is 91,707.
### NMRBank dataset reading and viewing

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

## 📀 Fine-tuning Open-source Language Models (Mistral, Llama2，Llama3) 

### Environment (Linux)
```bash
mamba create -n llm python=3.10
mamba activate llm 
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pandas numpy ipywidgets tqdm
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple torch==2.1.2  transformers==4.38.2 datasets tiktoken wandb==0.11 openpyxl
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple peft==0.8.0 accelerate bitsandbytes safetensors jsonlines
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple vllm==0.3.1
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple trl==0.7
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple tensorboardX tensorboard
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple textdistance nltk matplotlib seaborn seqeval
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple modelscope
```

## Pretrained Models Downloads

Open-sourced pretrained models (Llama3, Llama2, Mistral) can be downloaded from [huggingface](https://huggingface.co/models) or [modelscope](https://www.modelscope.cn/models).

Here is an example for downloading pretrained models by scripts on linux servers from modelscope:
```python
from modelscope import snapshot_download
model_dir = snapshot_download('AI-ModelScope/Mistral-7B-Instruct-v0.2', revision='master', cache_dir='/home/pretrained_models')
model_dir = snapshot_download("LLM-Research/Meta-Llama-3-8B-Instruct", revision='master', cache_dir='/home/pretrained_models')
```

## Fine-tuning, inference, evaluation, and using of NMRExtractor

Code and tutorials for fine-tuning, inference, evaluation, and using language models (Llama3, Llama2, Mistral) for NMRExtractor are in the - ```NMRExtractor/``` folder.

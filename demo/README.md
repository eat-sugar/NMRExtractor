## 1. NMR Data Extraction Demo: Extracting data from an NMR data paragraph using NMRExtractor

We provide an example notebook for extracting NMR data using Gradio visualization and NMRExtractor in ```demo_1_use_NMRExtractor_extract_NMR_data_from_NMR_paragraph.ipynb```, which you can use locally to extract NMR data from paragraphs using your computer's CPU or GPU.

We also provide an online demo of NMRExtractor at
https://huggingface.co/spaces/sweetssweets/NMRExtractor

### Using GPU
```python
# Using GPU
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
device = "cuda:0" if torch.cuda.is_available() else "cpu"
```

## 2. Complete workflow for NMR data extraction: Obtaining data from literature using NMRExtractor

A complete workflow for extracting NMR data from an article using NMRExtractor is provided in ```demo_2_use_NMRExtractor_extract_NMR_data_from_Article.ipynb```.

Using 1×40GB A100 (using vllm).

## 3. Download and use NMRExtractor model weights

Replace the "model_path" in the code with the folder path where the NMRExtractor weights are located.

The model weights of NMRExtractor can be downloaded from 
https://huggingface.co/sweetssweets/NMRExtractor. 


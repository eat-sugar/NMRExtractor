## 1. Data for NMRExtractor

- Data for fine-tuning LLMs are in ```../data```.


## 2. Methods for NMRExtractor

### Full Parameter Fine-tuning Open-source Large Language Models (Llama3, Llama2, Mistral)

Training Code in ```1_finetune_llms_peft_for_llms.py```

Inferencing Code in ```2_vllm_inference_full_finetuned_llms.ipynb```

### Parameter Efficient Fine-tuning (PEFT) Open-source Large Language Models (Llama3, Llama2, Mistral)

Training Code in ```1_finetune_llms_full_for_llms.py```

Inferencing Code in ```2_vllm_inference_peft_finetuned_llms.ipynb```

## 3. Evaluating the results of NMRExtractor

All predictions will be saved in ```results/predictions```

Evalutating codes for LLMs (ChatGPT, Llama, Mistral) are in ```3_evaluate_llms.ipynb```

## 4. Extract NMR data from Pubmed articles using NMRExtractor

Publicly available articles from the PubMed database can be downloaded from https://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/

The data description of PubMed database can be found at https://pmc.ncbi.nlm.nih.gov/tools/ftp/

The code for extracting NMR data from the PubMed article using NMRExtractor is in ```4_Extract_NMR_data_from_Pubmed_articles_using_NMRExtractor.ipynb```

Using 1×40GB A100 (using vllm).

## 5. Download and use NMRExtractor model weights

Replace the "model_path" in the code with the folder path where the NMRExtractor weights are located.

The model weights of NMRExtractor can be downloaded from 
https://huggingface.co/sweetssweets/NMRExtractor. 
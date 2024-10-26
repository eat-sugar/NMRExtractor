## 1. Data for NMRExtractor

- Data for fine-tuning LLMs are in ```../data```.


## 2. Methods for NMRExtractor

### Full Parameter Fine-tuning Open-source Large Language Models (Llama3, Llama2, Mistral)

Training Code in ```finetune_llms_peft_for_llms.py```

Inferencing Code in ```vllm_inference_full_finetuned_llms.ipynb```

### Parameter Efficient Fine-tuning (PEFT) Open-source Large Language Models (Llama3, Llama2, Mistral)

Training Code in ```finetune_llms_full_for_llms.py```

Inferencing Code in ```vllm_inference_peft_finetuned_llms.ipynb```

## 3. Evaluating the results of Paragraph2NMR

All predictions will be saved in ```results/predictions```

Evalutating codes for LLMs (ChatGPT, Llama, Mistral) are in ```evaluate_llms.ipynb```


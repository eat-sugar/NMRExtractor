## 1. Data for training LLMs

- Data for fine-tuning LLMs are in ```train```:

- ```train_50_in_100.csv```
- ```train_100_in_200.csv```
- ```train_200_in_400.csv```
- ```train_400_in_600.csv```
- ```train_600_in_800.csv```
- ```train_800_in_1000.csv```
- ```train_1000.csv```

The train_1000.csv file contains 1000 samples, and other files such as train_800_in_1000.csv contain 800 samples extracted from the 1000 samples, which are intended to analyze the performance of the model under different sample sizes.

## 2. Data for testing LLMs

- Data for fine-tuning LLMs are in ```test```:
- ```test_set_1_(300).csv```
- ```test_set_2_(1022).csv```
- ```test_set_2_1_(778).csv```
- ```test_set_2_2_(244).csv```

Among them, test_set_1_(300).csv contains 300 samples, and test_set_2_(1022).csv contains 1022 samples.

test_set_2_1_(778).csv contains 778 standardized description samples in test_set_2_(1022) that were manually distinguished, and test_set_2_2_(244).csv contains 244 non-standardized description samples in test_set_2_(1022) that were manually distinguished.

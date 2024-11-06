## Rule-based

### Environment

```bash
pip install python-docx
```
### Using Rule-based methods to extract NMR data
- Running the ```main.py``` file can extract the NMR data from the articles in the ```word``` folder and save them into the corresponding json file.


The code logic is: 
1. Use regular expressions to find text paragraphs that may contain NMR data.
2. Use regular expressions and the collected IUPAC group words of common compounds ```618_common_word_groups_of_IUPAC_name.json``` to obtain the IUPAC name of the compound from the text paragraph that may contain NMR data.
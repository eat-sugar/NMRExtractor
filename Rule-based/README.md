## Rule-based

### Environment

```bash
pip install python-docx
```
### Using Rule-based methods to extract NMR data
- Running the ```main.py``` file can extract the NMR data from the articles in the ```word``` folder and save them into the corresponding json file.


### The code logic is: 
1. Extract text from the word document and save it in the txt_original folder.

2. Used to filter out reference paragraphs and some short, abnormal paragraphs, and store the results in txt_reprocess.

3. Count the number of H spectra and C spectra carried by each document.

4. According to the previous statistical results, extract the literature with HC spectra respectively, and check the H spectrum and C spectrum respectively to see if the determination conditions and corresponding compounds can be found.

5. Returns a folder containing the required JSON files.
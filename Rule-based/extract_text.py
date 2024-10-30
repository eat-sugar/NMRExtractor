import docx.opc.exceptions
from docx import Document
import tqdm
import os
import glob
import re
import lxml


def extract_text(filenamesList, output_path, word_path):
    for filename in filenamesList:
        # filename_ = comp.findall(filename)
        filename_ = filename[:-5]
        try:
            doc = Document(os.path.join(word_path, filename))
        except docx.opc.exceptions.PackageNotFoundError:
            print(filename + '  ' + 'file is not readable')
            continue
        except lxml.etree.XMLSyntaxError:
            print(filename + '  ' + 'file is not readable')
            continue

        count = {'Body Text': 0, 'Normal': 0, 'Title': 0, 'Heading 1': 0,
                 'Heading 2': 0, 'List Paragraph': 0, 'other': []}

        json_path = filename_ + '.txt'
        with open(os.path.join(output_path, json_path), 'w', encoding='utf-8') as t:
            t.truncate(0)
            for paras in doc.paragraphs:
                t.write('\n')
                t.write(paras.text)


if __name__ == '__main__':
    comp = re.compile(r'(.*).docx')
    word = r'D:\Transformed_files\word'
    tmp1 = sorted(os.listdir(word), key=lambda x:int(x.split('-')[1]))
    word_paths = [os.path.join(word, x) for x in tmp1]

    output = r'D:\Transformed_files\txt_original'
    tmp2 = sorted(os.listdir(output), key=lambda x: int(x.split('-')[1]))
    output_paths = [os.path.join(output, x) for x in tmp2]
    zipper = list(zip(word_paths, output_paths))
    # zipper = zipper
    for word_path, output_path in tqdm.tqdm(zipper):
        filenamesList = [os.path.basename(x) for x in glob.iglob(word_path + '/*.docx')]
        comp = re.compile(r'(.*).docx')
        extract_text(filenamesList, output_path, word_path)


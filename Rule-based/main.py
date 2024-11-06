import multiprocessing
import time
from multiprocessing import Process, Lock, Pool, Manager
import re
import os
import tqdm
import glob
import json
from extract_text import extract_text
from Preprocessing_helper import ReadTextFiles, TreeNode
from Statistic_for_paras_and_H import stastic_for_H, stastic_for_C
from Extract_HC_with_Compound import extract_H_with_compound, extract_C_with_compound, find_compound_function
from Extract_HC_with_Compound import stripe_numbers, filter_not_spectrum, get_files_with_H, get_files_with_C
from Divide_into_100 import makedir


def main(args):
    word_path = args[0]
    txt_original_path = args[1]
    txt_reprocess_path = args[2]
    H_path = args[3]
    C_path = args[4]
    json_path = args[5]
    output_H_C_with_compound_H = args[6]
    output_H_C_with_compound_C = args[7]

    dict_path = r'618_common_word_groups_of_IUPAC_name.json'


    # Extract text from the word document and save it in the txt_original folder
    filenamesList = [os.path.basename(x) for x in glob.iglob(word_path + '/*.docx')]
    extract_text(filenamesList, txt_original_path, word_path)

    # ******************************************************************
    # Used to filter out reference paragraphs and some short, abnormal paragraphs, and store the results in txt_reprocess
    text_files = glob.glob(txt_original_path + '/*.txt')
    for i in tqdm.tqdm(range(len(text_files))):
        text_files_name = os.path.basename(text_files[i])
        file_name = text_files[i]
        ReadTextFiles(file_name, text_files_name, dict_path, txt_reprocess_path)

    # ******************************************************************
    # Count the number of H spectra and C spectra carried by each document
    txt_files_list = [x for x in glob.glob(txt_reprocess_path + '/*.txt')]
    for file in txt_files_list:
        lines_dict_for_file_H = {'file_name': os.path.basename(file), 'lines_total': int,
                                 'line_contain_H_total': 0, 'complete_para': 0,
                                 'line_contain_H': [], 'H': []}
        lines_dict_for_file_C = {'file_name': os.path.basename(file), 'lines_total': int,
                                 'line_contain_C_total': 0,
                                 'complete_para': 0,
                                 'line_contain_C': [], 'C': []}
        stastic_for_H(file, lines_dict_for_file_H, H_path)
        stastic_for_C(file, lines_dict_for_file_C, C_path)
    # ******************************************************************
    # According to the previous statistics, the literature with HC spectrum is taken out separately, 
    # and the H spectrum and C spectrum are checked to see if the corresponding compound can be found
    txt_contain_H = get_files_with_H(H_path, txt_reprocess_path, json_path)
    txt_contain_C = get_files_with_C(C_path, txt_reprocess_path, json_path)
    extract_H_with_compound(txt_contain_H, output_H_C_with_compound_H)
    # Returns a folder containing the required JSON files
    extract_C_with_compound(txt_contain_C, output_H_C_with_compound_C)


if __name__ == '__main__':
    word_path = 'word'
    path1 = r'txt_original'
    path2 = r'txt_reprocess'
    path3 = r'spectragram'
    path4 = r'json'
    path5 = r'H_C_with_Compound'
    paths = []

    paths.append(word_path)
    paths.append(path1)
    paths.append(path2)
    paths.append(path3)
    paths.append(path4)
    paths.append(path5)

    files_number = 5000
    for path in paths:
        makedir(path, files_number)
    # Create folders based on the number of files, divided into 5000 files

    word = r'word'
    tmp1 = sorted(os.listdir(word), key=lambda x: int(x.split('-')[1]))
    word_paths = [os.path.join(word, x) for x in tmp1]

    txt_original = r'txt_original'
    tmp2 = sorted(os.listdir(txt_original), key=lambda x: int(x.split('-')[1]))
    txt_original_paths = [os.path.join(txt_original, x) for x in tmp2]

    txt_reprocess = r'txt_reprocess'
    tmp3 = sorted(os.listdir(txt_reprocess), key=lambda x: int(x.split('-')[1]))
    txt_reprocess_paths = [os.path.join(txt_reprocess, x) for x in tmp3]

    spectragram_H = r'spectragram'
    tmp4 = sorted(os.listdir(spectragram_H), key=lambda x: int(x.split('-')[1]))
    H_paths = [os.path.join(spectragram_H, x, 'json_for_H') for x in tmp4]

    spectragram_C = r'spectragram'
    tmp5 = sorted(os.listdir(spectragram_C), key=lambda x: int(x.split('-')[1]))
    C_paths = [os.path.join(spectragram_C, x, 'json_for_C') for x in tmp5]

    json_path = r'json'
    tmp6 = sorted(os.listdir(json_path), key=lambda x: int(x.split('-')[1]))
    json_paths = [os.path.join(json_path, x) for x in tmp6]

    H_C_with_Compound_H = r'H_C_with_Compound'
    tmp7 = sorted(os.listdir(H_C_with_Compound_H), key=lambda x: int(x.split('-')[1]))
    output_H_C_with_compound_H = [os.path.join(H_C_with_Compound_H, x, 'H') for x in tmp7]

    H_C_with_Compound_C = r'H_C_with_Compound'
    tmp8 = sorted(os.listdir(H_C_with_Compound_C), key=lambda x: int(x.split('-')[1]))
    output_H_C_with_compound_C = [os.path.join(H_C_with_Compound_C, x, 'C') for x in tmp8]


    zipper = list(zip(word_paths, txt_original_paths, txt_reprocess_paths, H_paths, C_paths,
                      json_paths, output_H_C_with_compound_H, output_H_C_with_compound_C))

    # dict_path = r'618_common_word_groups_of_IUPAC_name.json'
    #
    # root = TreeNode()
    # Dictionary_compound = open(dict_path, 'r', encoding='utf-8')
    #
    # dict_compound = json.loads(Dictionary_compound.read())['compounds']
    # compounds = dict_compound.keys()
    # compounds = sorted(compounds, key=lambda x: len(x))
    # for k in compounds:
    #     root.insert(k)
    #
    # pattern_H = re.compile(
    #     '(1\s*H.{0,3}?NMR((?!\s*NMR).)*?[;.]\s+)(.{0,8}?(NMR|IR|ESI|MS|Anal|Mass|Found|UV|HMBC|NOESY|31P|/n))', re.I)
    # pattern_C = re.compile(
    #     '(13\s*C.{0,7}?NMR((?!\sNMR).)*?[;.]\s+)(.{0,8}?(NMR|IR|ESI|MS|Anal|Mass|Found|UV|HMBC|NOESY|31P|/n))', re.I)
    # pattern_filter = re.compile('([^0-9]{30,})', re.I)
    # pattern_compound_1 = re.compile('^.*?[;.:]', re.I)
    # # pattern_compound_2 = re.compile('^.*?\s*was\s*obtain', re.I)
    # pattern_filter_again = re.compile('^.*\s+\(.{0,4}\)[\s:.]', re.I)
    #
    # pattern1 = re.compile(
    #     '(1\s*H.{0,3}?NMR((?!\s*NMR).)*?[;.]\s+)(.{0,8}?(NMR|IR|ESI|MS|Anal|Mass|Found|UV|HMBC|NOESY|31P|/n))', re.I)
    #
    # pattern5 = re.compile(
    #     '(13\s*C.{0,7}?NMR((?!\sNMR).)*?[;.]\s+)(.{0,8}?(NMR|IR|ESI|MS|Anal|Mass|Found|UV|HMBC|NOESY|31P|/n))', re.I)
    #
    # comp = re.compile(r'(.*).docx')
    start = time.time()
    cpu_work_num = 4
    lock = multiprocessing.Manager().Lock()
    with Pool(cpu_work_num) as pool:
        pool.map(main, zipper)

    # for i, groups in enumerate(tqdm.tqdm(zipper)):
    #     print(groups)
    #     main(groups)
    end = time.time()
    print('Total time{}'.format(end - start))

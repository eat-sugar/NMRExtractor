import os
import glob
import json
import re
import shutil
import random

def get_files_with_H(H_path, txt_files_path, paths):
    txt_files_contain_H = []
    H_files = glob.glob(H_path + '/*.json')
    H_with_compound_paths = os.path.join(paths, 'H')
    if not os.path.exists(H_with_compound_paths):
        os.makedirs(H_with_compound_paths)
    for file in H_files:
        with open(file, 'r', encoding='utf-8') as H:
            data = json.loads(H.read())
            if data['H']:
                shutil.copy2(file, H_with_compound_paths)
                name = data['file_name'][:-4] + '.txt'
                txt_files_contain_H.append(name)
    txt_files_contain_H = list(os.path.join(txt_files_path, x) for x in txt_files_contain_H)
    # # Returns a list of txt files that have not been processed
    return txt_files_contain_H


def get_files_with_C(C_path, txt_files_path, paths):
    txt_files_contain_C = []
    C_files = glob.glob(C_path + '/*.json')
    C_with_compound_paths = os.path.join(paths, 'C')
    if not os.path.exists(C_with_compound_paths):
        os.makedirs(C_with_compound_paths)
    for file in C_files:
        with open(file, 'r', encoding='utf-8') as H:
            data = json.loads(H.read())
            if data['C']:
                shutil.copy2(file, C_with_compound_paths)
                name = data['file_name'][:-4] + '.txt'
                txt_files_contain_C.append(name)
    txt_files_contain_C = list(os.path.join(txt_files_path, x) for x in txt_files_contain_C)
    # # Returns a list of txt files that have not been processed
    return txt_files_contain_C


def filter_not_spectrum(line: str):
    # Determine whether it is the spectrogram data we need by judging the length of the sentence itself 
    # and the length of the characters after filtering out the numbers
    pattern_filter = re.compile('([^0-9]{30,})', re.I)
    if len(line) <= 50:
        return False
    line = ''.join(line.strip().split(' ')).lower()
    res = re.findall(pattern_filter, line)
    if res:
        return False
    else:
        return True


def stripe_numbers(tmp: str):
    pattern_filter_again = re.compile('^.*\s+\(.{0,4}\)[\s:.]', re.I)
    res = pattern_filter_again.findall(tmp)
    if res and len(res[-1]) > 10:
        r = res[-1].strip()
        lens = len(res[-1])
        l_index = r.index('(', lens - 7, lens - 1)
        r = r[:l_index]
        if len(r) <= 120:
            return r
    return None


def find_compound_function(line):
    kword = re.split('[ ()\[\]{}/;,-]', line)
    for word in kword:
        # If the word is too short, ignore it
        if len(word) < 3:
            continue
        for compound in compounds:
            if len(compound) > len(word):
                break
            if compound in word:
                return True
    return False

def extract_H_with_compound(files_contain_H, output_path_H):
    # files_contain_H = glob.glob(files_contain_H_path + '/*.txt')
    # print(len(files_contain_H))
    pattern_compound_1 = re.compile('^.*?[;.:]', re.I)
    for file in files_contain_H:
        line_dict = {
            'file_name': '', 'count': 0, 'count_for_solution': 0, 'H-compound': [],
            'Solution_H': [], 'H-spectrogram': [], 'Paragraph': []
        }

        with open(file, 'r',  encoding='utf-8') as H:
            lines = H.readlines()
            for i, line in enumerate(lines):
                line = line.strip()
                res5 = pattern_H.findall(line + ' /n')
                # Find possible hydrogen spectra
                if res5:
                    for res in res5:
                        if filter_not_spectrum(res[0]):
                            # Filter the hydrogen spectrum once
                            line_first_sentence = pattern_compound_1.findall(line + '.')
                            # Find a sentence first
                            comp_res = find_compound_function(line_first_sentence[0])
                            if comp_res:
                                t = stripe_numbers(line_first_sentence[0])
                                # Find compound sentences with brackets like xxx (x) and truncate them with (
                                if t:

                                    line_dict['file_name'] = os.path.basename(file)
                                    line_dict['count'] += 1
                                    line_dict['H-spectrogram'].append(res[0])
                                    s_h = find_solution_H.findall(res[0])
                                    if s_h:
                                        line_dict['Solution_H'].append(s_h[0])
                                        line_dict['count_for_solution'] += 1
                                    else:
                                        line_dict['Solution_H'].append('0')
                                    line_dict['H-compound'].append(t)
                                    line_dict['Paragraph'].append(line)
                                    continue
                            else:
                                line_last = lines[i - 1].strip() + '.'
                                if len(line_last) <= 200:
                                    comp_res = find_compound_function(line_last)
                                    if comp_res:
                                        # t = stripe_numbers(line_last)
                                        line_dict['file_name'] = os.path.basename(file)
                                        line_dict['count'] += 1
                                        line_dict['H-spectrogram'].append(res[0])

                                        s_h = find_solution_H.findall(res[0])
                                        if s_h:
                                            line_dict['Solution_H'].append(s_h[0])
                                            line_dict['count_for_solution'] += 1
                                        else:
                                            line_dict['Solution_H'].append('0')
                                        line_dict['H-compound'].append(line_last)
                                        line_line = line_last + ' \t ' + line
                                        line_dict['Paragraph'].append(line_line)
                                        continue
        output_file_name = os.path.basename(file)[:-4] + '.json'
        if not os.path.exists(output_path_H):
            os.makedirs(output_path_H)
        if line_dict['file_name'] != '':
            with open(os.path.join(output_path_H, output_file_name), 'w',) as w:
                w.write(json.dumps(line_dict, indent=4))

def extract_C_with_compound(files_contain_C, output_path_C):
    # files_contain_C = glob.glob(files_contain_C_path + '/*.txt')
    pattern_compound_1 = re.compile('^.*?[;.:]', re.I)
    for file in files_contain_C:
        line_dict = {
            'file_name': '', 'count': 0, 'count_for_solution': 0, 'C-compound': [],
            'Solution_C': [], 'C-spectrogram': [], 'Paragraph': []
        }
        with open(file, 'r', encoding='utf-8') as C:
            lines = C.readlines()
            for i, line in enumerate(lines):
                line = line.strip()
                res5 = pattern_C.findall(line + ' /n')
                # Find possible carbon spectra
                if res5:
                    for res in res5:
                        if filter_not_spectrum(res[0]):
                            # Filter the carbon spectrum once
                            line_first_sentence = pattern_compound_1.findall(line + '.')
                            # Find a sentence first
                            comp_res = find_compound_function(line_first_sentence[0])
                            if comp_res:
                                t = stripe_numbers(line_first_sentence[0])
                                # Find compound sentences with brackets like xxx (x) and truncate them with (
                                if t:
                                    line_dict['file_name'] = os.path.basename(file)
                                    line_dict['count'] += 1
                                    line_dict['C-spectrogram'].append(res[0])
                                    s_c = find_solution_C.findall(res[0])
                                    if s_c:
                                        line_dict['Solution_C'].append(s_c[0])
                                        line_dict['count_for_solution'] += 1
                                    else:
                                        line_dict['Solution_C'].append('0')
                                    line_dict['C-compound'].append(t)
                                    line_dict['Paragraph'].append(line)
                                    continue
                            else:
                                line_last = lines[i - 1].strip()
                                if len(line_last) <= 200:
                                    comp_res = find_compound_function(line_last)
                                    if comp_res:
                                        line_dict['file_name'] = os.path.basename(file)
                                        line_dict['count'] += 1
                                        line_dict['C-spectrogram'].append(res[0])
                                        s_c = find_solution_C.findall(res[0])
                                        if s_c:
                                            line_dict['Solution_C'].append(s_c[0])
                                            line_dict['count_for_solution'] += 1
                                        else:
                                            line_dict['Solution_C'].append('0')
                                        line_dict['C-compound'].append(line_last)
                                        line_line = line_last + ' \t ' + line
                                        line_dict['Paragraph'].append(line_line)
                                        continue
        output_file_name = os.path.basename(file)[:-4] + '.json'
        if not os.path.exists(output_path_C):
            os.makedirs(output_path_C)
        if line_dict['file_name'] != '':
            with open(os.path.join(output_path_C, output_file_name), 'w', ) as w:
                w.write(json.dumps(line_dict, indent=4))

dict_path = r'618_common_word_groups_of_IUPAC_name.json'
Dictionary_compound = open(dict_path, 'r', encoding='utf-8')
dict_compound = json.loads(Dictionary_compound.read())['compounds']
compounds = dict_compound.keys()
compounds = sorted(compounds, key=lambda x: len(x))

pattern_H = re.compile(
    '(1\s*H.{0,3}?NMR((?!\s*NMR).)*?[;.]\s+)(.{0,8}?(NMR|IR|ESI|MS|Anal|Mass|Found|UV|HMBC|NOESY|31P|/n))', re.I)
pattern_C = re.compile(
    '(13\s*C.{0,7}?NMR((?!\sNMR).)*?[;.]\s+)(.{0,8}?(NMR|IR|ESI|MS|Anal|Mass|Found|UV|HMBC|NOESY|31P|/n))', re.I)
pattern_filter = re.compile('([^0-9]{30,})', re.I)
pattern_compound_1 = re.compile('^.*?[;.:]', re.I)
# pattern_compound_2 = re.compile('^.*?\s*was\s*obtain', re.I)
pattern_filter_again = re.compile('^.*\s+\(.{0,4}\)[\s:.]', re.I)
find_solution_H = re.compile('1\s*H.{0,3}?NMR\s*(\(.*?\))', re.I)
find_solution_C = re.compile('13\s*C.{0,7}?NMR\s*(\(.*?\))', re.I)
pattern1 = re.compile(
    '(1\s*H.{0,3}?NMR((?!\s*NMR).)*?[;.]\s+)(.{0,8}?(NMR|IR|ESI|MS|Anal|Mass|Found|UV|HMBC|NOESY|31P|/n))', re.I)

pattern5 = re.compile(
    '(13\s*C.{0,7}?NMR((?!\sNMR).)*?[;.]\s+)(.{0,8}?(NMR|IR|ESI|MS|Anal|Mass|Found|UV|HMBC|NOESY|31P|/n))', re.I)
if __name__ == '__main__':
    random.seed = 50

    pattern_H = re.compile('(1\s*H.{0,3}?NMR((?!\s*NMR).)*?[;.]\s+)(.{0,8}?(NMR|IR|ESI|MS|Anal|Mass|Found|UV|HMBC|NOESY|31P|/n))', re.I)
    # Regular expression for extracting H spectrum
    pattern_C = re.compile('(13\s*C.{0,7}?NMR((?!\sNMR).)*?[;.]\s+)(.{0,8}?(NMR|IR|ESI|MS|Anal|Mass|Found|UV|HMBC|NOESY|31P|/n))', re.I)
    # Regular expression for extracting C spectrum
    pattern_filter = re.compile('([^0-9]{30,})', re.I)
    # To ensure the quality of the extracted spectrogram, it is necessary to filter shorter sentences
    pattern_compound_1 = re.compile('^.*?[;.:]', re.I)
    # pattern_compound_2 = re.compile('^.*?\s*was\s*obtain', re.I)
    pattern_filter_again = re.compile('^.*\s+\(.{0,4}\)[\s:.]', re.I)

    find_solution_H = re.compile('1\s*H.{0,3}?NMR\s*(\(.*?\))', re.I)
    # Determine whether the extracted H NMR is followed by brackets, which are usually solvents
    find_solution_C = re.compile('13\s*C.{0,7}?NMR\s*(\(.*?\))', re.I)
    # Determine whether the extracted C NMR is followed by brackets, which usually contain solvents
    pattern1 = re.compile(
        '(1\s*H.{0,3}?NMR((?!\s*NMR).)*?[;.]\s+)(.{0,8}?(NMR|IR|ESI|MS|Anal|Mass|Found|UV|HMBC|NOESY|31P|/n))', re.I)

    pattern5 = re.compile(
        '(13\s*C.{0,7}?NMR((?!\sNMR).)*?[;.]\s+)(.{0,8}?(NMR|IR|ESI|MS|Anal|Mass|Found|UV|HMBC|NOESY|31P|/n))', re.I)


    txt_reprocess = r'txt_reprocess'
    tmp1 = sorted(os.listdir(txt_reprocess), key=lambda x: int(x.split('-')[1]))
    txt_paths = [os.path.join(txt_reprocess, x) for x in tmp1]

    output_path_H = r'spectragram'
    tmp2 = sorted(os.listdir(output_path_H), key=lambda x: int(x.split('-')[1]))
    H_paths = [os.path.join(output_path_H, x, 'json_for_H') for x in tmp2]

    output_path_C = r'spectragram'
    tmp3 = sorted(os.listdir(output_path_C), key=lambda x: int(x.split('-')[1]))
    C_paths = [os.path.join(output_path_C, x, 'json_for_C') for x in tmp3]


    output_path = r'json'
    tmp4 = sorted(os.listdir(output_path), key=lambda x: int(x.split('-')[1]))
    paths = [os.path.join(output_path, x) for x in tmp4]

    json_path_H = r'H_C_with_Compound'
    tmp5 = sorted(os.listdir(json_path_H), key=lambda x: int(x.split('-')[1]))
    output_H_C_with_compound_H = [os.path.join(json_path_H, x, 'H') for x in tmp5]
    # print(output_H_C_with_compound_H)

    json_path_C = r'H_C_with_Compound'
    tmp6 = sorted(os.listdir(json_path_C), key=lambda x: int(x.split('-')[1]))
    output_H_C_with_compound_C = [os.path.join(json_path_C, x, 'C') for x in tmp6]

    dict_path = r'618_common_word_groups_of_IUPAC_name.json'
    zipper = list(zip(txt_paths, H_paths, C_paths, paths, output_H_C_with_compound_H, output_H_C_with_compound_C))
    print(zipper)
    # root = TreeNode()
    Dictionary_compound = open(dict_path, 'r', encoding='utf-8')
    dict_compound = json.loads(Dictionary_compound.read())['compounds']
    compounds = dict_compound.keys()
    compounds = sorted(compounds, key=lambda x: len(x))
    # for k in compounds:
    #     root.insert(k)

    for txt_path, H_path, C_path, json_paths, output_H_C_with_compound_H, output_H_C_with_compound_C in zipper:
        txt_contain_H = get_files_with_H(H_path, txt_path, json_paths)
        # Find text with H spectrum
        txt_contain_C = get_files_with_C(C_path, txt_path, json_paths)
        # Find text with C notation

        extract_H_with_compound(txt_contain_H, output_H_C_with_compound_H)
        # Save the H spectrum in the current file separately in json format

        extract_C_with_compound(txt_contain_C, output_H_C_with_compound_C)
        # Save the C spectrum in the current file separately in json format





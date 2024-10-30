import json
import os
import glob
import re
import tqdm

def filter_not_spectrum(line:str):
    # pattern_filter = re.compile('([^0-9]{30,})', re.I)
    if len(line) <= 50:
        return False
    line = ''.join(line.strip().split(' ')).lower()
    res = re.findall(pattern_filter, line)
    if res:
        return False
    else:
        return True


def stastic_for_H(file, lines_dict_for_file, output_path):
    f = open(file, 'r', encoding='utf-8')
    lines = f.readlines()
    lines_dict_for_file['lines_total'] = int(len(lines))
    for line in lines:
        if '.' in line[-6:]:
            lines_dict_for_file['complete_para'] += 1
        line = line.strip()
        res1 = pattern1.findall(line + ' /n')
        if res1:
            for res in res1:
                if filter_not_spectrum(res[0]):
                    lines_dict_for_file['line_contain_H_total'] += 1
                    lines_dict_for_file['H'].append(res[0])
                    lines_dict_for_file['line_contain_H'].append(line)
    f.close()
    output_file_name = os.path.basename(file)[:-4] + '.json'
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    with open(os.path.join(output_path, output_file_name), 'w',) as w:
        w.write(json.dumps(lines_dict_for_file, indent=4) + '\n')


def stastic_for_C(file, lines_dict_for_file, output_path):
    f = open(file, 'r', encoding='utf-8')
    lines = f.readlines()
    lines_dict_for_file['lines_total'] = int(len(lines))
    for line in lines:
        if '.' in line[-6:]:
            lines_dict_for_file['complete_para'] += 1
        line = line.strip()
        res5 = pattern5.findall(line + ' /n')
        if res5:
            for res in res5:
                if filter_not_spectrum(res[0]):
                    lines_dict_for_file['line_contain_C_total'] += 1
                    lines_dict_for_file['C'].append(res[0])
                    lines_dict_for_file['line_contain_C'].append(line)
    f.close()
    output_file_name = os.path.basename(file)[:-4] + '.json'
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    with open(os.path.join(output_path, output_file_name), 'w',) as w:
        w.write(json.dumps(lines_dict_for_file, indent=4) + '\n')

pattern1 = re.compile('(1\s*H.{0,3}?NMR((?!\s*NMR).)*?[;.]\s+)(.{0,8}?(NMR|IR|ESI|MS|Anal|Mass|Found|UV|HMBC|NOESY|31P|/n))', re.I)

pattern5 = re.compile('(13\s*C.{0,7}?NMR((?!\sNMR).)*?[;.]\s+)(.{0,8}?(NMR|IR|ESI|MS|Anal|Mass|Found|UV|HMBC|NOESY|31P|/n))', re.I)
pattern_filter = re.compile('([^0-9]{30,})', re.I)

if __name__ == '__main__':
    pattern1 = re.compile('(1\s*H.{0,3}?NMR((?!\s*NMR).)*?[;.]\s+)(.{0,8}?(NMR|IR|ESI|MS|Anal|Mass|Found|UV|HMBC|NOESY|31P|/n))', re.I)

    pattern5 = re.compile('(13\s*C.{0,7}?NMR((?!\sNMR).)*?[;.]\s+)(.{0,8}?(NMR|IR|ESI|MS|Anal|Mass|Found|UV|HMBC|NOESY|31P|/n))', re.I)
    pattern_filter = re.compile('([^0-9]{30,})', re.I)

    txt_reprocess = r'D:\Transformed_files\txt_reprocess'
    tmp1 = sorted(os.listdir(txt_reprocess), key=lambda x: int(x.split('-')[1]))
    txt_paths = [os.path.join(txt_reprocess, x) for x in tmp1]

    output_path_H = r'D:\Transformed_files\spectragram'
    tmp2 = sorted(os.listdir(output_path_H), key=lambda x: int(x.split('-')[1]))
    H_paths = [os.path.join(output_path_H, x, 'json_for_H') for x in tmp2]

    output_path_C = r'D:\Transformed_files\spectragram'
    tmp3 = sorted(os.listdir(output_path_C), key=lambda x: int(x.split('-')[1]))
    C_paths = [os.path.join(output_path_C, x, 'json_for_C') for x in tmp3]
    zipper = list(zip(txt_paths, H_paths, C_paths))

    for txt_path, H_path, C_path in tqdm.tqdm(zipper):
        files_list = [x for x in glob.glob(txt_path + '/*.txt')]
        for file in files_list:
            lines_dict_for_file_H = {'file_name': os.path.basename(file), 'lines_total': int, 'line_contain_H_total': 0, 'complete_para': 0,
                                   'line_contain_H': [], 'H': []}
            lines_dict_for_file_C = {'file_name': os.path.basename(file), 'lines_total': int, 'line_contain_C_total': 0,
                                   'complete_para': 0,
                                   'line_contain_C': [], 'C': []}
            stastic_for_H(file, lines_dict_for_file_H, H_path)
            # store the stastic of H-spectrum
            stastic_for_C(file, lines_dict_for_file_C, C_path)
            # store the stastic of C-spectrum

# {'paragraph_total': 7569859, 'paragraph_contain_C_total': 5798, 'complete_paras': 5880140}
# {'paragraph_total': 7569859, 'paragraph_contain_H_total': 8712, 'complete_paras': 5880140}
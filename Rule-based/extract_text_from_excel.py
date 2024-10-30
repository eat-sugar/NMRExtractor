import tqdm
import os
import glob
import re
import pandas as pd
import xlrd


def merge_lines(lines: list):
    sheet_contain_table = False
    is_table = False
    res = []
    tmp = []
    for line in lines:
        if all(i == '' for i in line) and tmp:
            if is_table:
                res.append('=='.join(tmp))
            else:
                res.append(' '.join(tmp))
            tmp = []
            is_table = False
        elif is_table or (len(line) >= 1 and any(i != '' for i in line[1:])):
            is_table = True
            sheet_contain_table = True
            for i, l in enumerate(line):
                if l == '':
                    line[i] = '<None>'
            t = '<TAB_S>' + '||'.join(line) + '<TAB_E>'
            tmp.append(t)
        elif tmp and tmp[-1].endswith('-'):
            p = tmp.pop()
            t = line[0].strip()
            tmp.append(p + t)
        else:
            t = line[0].strip()
            tmp.append(t)
    if tmp:
        if is_table:
            res.append('=='.join(tmp))
        else:
            res.append(' '.join(tmp))
    return res, sheet_contain_table


def extract_text_from_excel(input, output):
    input_files = glob.glob(input + '/*.xlsx')
    for file in input_files:
        file_name = os.path.basename(file)
        q = pd.DataFrame()
        output_file_name = os.path.join(output, file_name[:-4] + '.csv')
        data = xlrd.open_workbook(file)
        sheets = data.sheet_names()
        print(sheets)
        file_names = []
        sheet_names = []
        contain_table = []
        all_res = []
        for i, sheet_obj in enumerate(data.sheets()):
            lines = [sheet_obj.row_values(row) for row in range(sheet_obj.nrows)]
            res, sheet_contain_table = merge_lines(lines)
            sheet_name = 'sheet' + str(i + 1)
            all_res.append('\n'.join(res))
            file_names.append(file_name)
            sheet_names.append(sheet_name)
            contain_table.append(sheet_contain_table)
        q[0] = file_names
        q[1] = sheet_names
        q[2] = all_res
        q[3] = contain_table
        print(all_res)
        q.to_csv(output_file_name, encoding='utf-8-sig', index=False)



        # for k, v in all_data.items():
        #     print(k, v)
        # break


if __name__ == '__main__':
    excel = r'C:\Users\fxt\Desktop\tmp'
    tmp1 = sorted(os.listdir(excel), key=lambda x: int(x.split('-')[1]))
    excel_paths = [os.path.join(excel, x) for x in tmp1]

    output = r'C:\Users\fxt\Desktop\tmp_text'
    tmp2 = sorted(os.listdir(output), key=lambda x: int(x.split('-')[1]))
    output_paths = [os.path.join(output, x) for x in tmp2]

    zipper = list(zip(excel_paths, output_paths))
    for excel_path, output_path in tqdm.tqdm(zipper):
        extract_text_from_excel(excel_path, output_path)
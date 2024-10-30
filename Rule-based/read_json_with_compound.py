import json
import glob
import os

def read_json(json_files_list_H, json_files_list_C):
    for file in json_files_list_H:
        f = open(file, 'r', encoding='utf-8')
        data = json.loads(f.read())
        json_dict_total_H['paragraph_with_H_and_compound'] += data['count']
        json_dict_total_H['Solution_H'] += data['count_for_solution']
        f.close()
    print(json_dict_total_H)

    for file in json_files_list_C:
        f = open(file, 'r', encoding='utf-8')
        data = json.loads(f.read())
        json_dict_total_C['paragraph_with_C_and_compound'] += data['count']
        json_dict_total_C['Solution_C'] += data['count_for_solution']
        f.close()
    print(json_dict_total_C)


if __name__ == '__main__':
    json_path_H = r'D:\tmp_statistic\H_C_with_Compound'
    tmp1 = sorted(os.listdir(json_path_H), key=lambda x: int(x.split('-')[1]))
    H_paths = [os.path.join(json_path_H, x, 'H') for x in tmp1]

    json_path_C = r'D:\tmp_statistic\H_C_with_Compound'
    tmp2 = sorted(os.listdir(json_path_C), key=lambda x: int(x.split('-')[1]))
    C_paths = [os.path.join(json_path_C, x, 'C') for x in tmp2]
    zipper = list(zip(H_paths, C_paths))

    json_dict_total_H = {'paragraph_with_H_and_compound': 0, 'Solution_H': 0}
    json_dict_total_C = {'paragraph_with_C_and_compound': 0, 'Solution_C': 0}

    for output_H, output_C in zipper:
        json_files_list_H = glob.glob(output_H + '/*.json')

        json_files_list_C = glob.glob(output_C + '/*.json')
        read_json(json_files_list_H, json_files_list_C)


# {'paragraph_with_H_and_compound': 5123}
# {'paragraph_with_C_and_compound': 3775}


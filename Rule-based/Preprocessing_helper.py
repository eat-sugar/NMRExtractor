import json
import os
import re


class TreeNode(object):
    def __init__(self):
        self.nodes = {}         # Record the child nodes of the current node
        self.is_leaf = False   # Does the current node represent a word?
        self.count = 0          # The total number of words in the word tree

    def insert(self, word):
        if len(word) <= 4:
            return
        curr = self
        for c in word:
            if not curr.nodes.get(c, None):
                new_node = TreeNode()
                curr.nodes[c] = new_node
            curr = curr.nodes[c]
            if curr.is_leaf:
                curr.count += 1
                break
        curr.is_leaf = True
        curr.count += 1
        return

    def search(self, word):
        if len(word) <= 4:
            return
        curr = self
        try:
            for c in word:
                curr = curr.nodes[c]
                if curr.is_leaf:
                    return True
            if curr.is_leaf:
                return True
        except:
            return False
        return False

    def travel(self):  # Return all the words spelled out by the node and its child nodes
        root = self
        res = []
        count_all = []
        def recusive(root, word):
            if root.is_leaf:
                if len(word) > 4:
                    res.append(word)
                    count_all.append(root.count)
            if not root.nodes:
                return
            for i, v in root.nodes.items():
                word += i
                recusive(v, word)
                word = word[:-1]
        recusive(root, '')
        return res, count_all


def ReadTextFiles(file_name, text_files_name, dict_path, output_path):
    root = TreeNode()
    Dictionary_compound = open(dict_path, 'r', encoding='utf-8')
    dict_compound = json.loads(Dictionary_compound.read())['compounds']
    compounds = dict_compound.keys()
    compounds = sorted(compounds, key=lambda x: len(x))
    # print(compounds)
    # for k in compounds:
    #     root.insert(k)
    line_dict = {
        'text': [], 'is_para': [0], 'long_enough': [0]
    }
    tmp_name = os.path.join(output_path, text_files_name)
    with open(file_name, 'r', encoding='utf-8') as r, open(tmp_name, 'w+', encoding='utf-8') as w:
        lines = r.readlines()
        for l, line in enumerate(lines):
            line = line.strip()
            if len(line) < 24 and l > 25 and ('bibliograph' in line.lower() or 'references' in line.lower() or 'literature cited' in line.lower()):
                break
            if line != '':
                if len(line) >= 120:
                    line_dict['text'].append(line)
                else:
                    pattern = re.compile('^(1H|13C|IR|ESI|MS|Anal|Mass|HRMS|Isomer|Found|UV|HMBC|NOESY|31P)', re.I)
                    tmp1 = pattern.findall(line)
                    if 'abstract' in line:
                        line_dict['text'].append(line)
                        continue
                    elif 'conclusion' in line:
                        line_dict['text'].append(line)
                        continue
                    elif 'synthesis of' in line or 'procedure for' in line:
                        line_dict['text'].append(line)
                        continue
                    elif len(line) <= 3:
                        pattern = re.compile('[1-9]{1,2}?[a-z]{1}', re.I)
                        tmp2 = pattern.findall(line)
                        if tmp2:
                            line_dict['text'].append(line)
                            continue
                    elif tmp1:
                        line_dict['text'].append(line)
                        continue
                    else:
                        kword = re.split('[ ()\[\]{};,-]', line)
                        count_compound = 0
                        for word in kword:
                            word = word.strip()
                            # If the word is too short, ignore it
                            if len(word) < 4:
                                continue

                            for compound in compounds:
                                if len(compound) > len(word):
                                    break
                                if compound in word:
                                    count_compound += 1
                                    break
                        #     if root.search(word.lower()):
                        #         count_compound += 1
                            if count_compound:
                                line_dict['text'].append(line)
                                break
        for t in line_dict['text']:
            w.write(t + '\n')


def re_deal(line):
    line = re.sub('\s\[,*[0-9]*(,\s[0-9]*)*]', '', line)
    return line





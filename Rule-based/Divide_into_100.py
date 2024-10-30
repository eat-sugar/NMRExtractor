import glob
import os
import shutil
# import PyPDF2 as p
import tqdm


def divided_into_more(files_list, folders_name, output):
    start = 0
    end = 5000
    len_f = len(files_list)
    print(len_f)
    print(type(folders_name))
    for f in folders_name:
        path = os.path.join(output, f)
        if not os.path.exists(path):
            os.makedirs(path)
        if start >= len_f:
            break
        for i in tqdm.tqdm(range(start, end)):
            if i > len_f - 1:
                break
            try:
                pdf_file = files_list[i]
            except:
                print('No more files, exit the program')
                break
            with open(pdf_file, 'rb'):
                try:
                    rd = p.PdfFileReader(pdf_file, strict=False)
                except:
                    print('encrypted PDF', pdf_file)
            if not rd.getIsEncrypted():
                # print(files_list[i])
                shutil.copy2(files_list[i], path)
        start += 5000
        end += 5000




def makedir(path, total):
    start = 1
    end = 5000
    l = total + 1
    nums = l // end
    chile_name = os.path.basename(path)
    for i in range(nums):
        folder_name = str(chile_name) + str(start) + '-' + str(end)
        # makedir(output1, folder_name)
        start += 5000
        end += 5000
        pathname = path + '\\' + folder_name
        if not os.path.exists(pathname):
            os.makedirs(pathname)
        else:
            print(pathname)
            pass


if __name__ ==  '__main__':
    files_path = r'D:\pdfs_all\pdfs'
    word_path = r'word'
    pdf_path = r'pdf'
    path1 = r'txt_original'
    path2 = r'txt_reprocess'
    path3 = r'spectragram'
    path4 = r'json'
    path5 = r'H_C_with_Compound'
    pathway6= r'tmp_for_pathways'
    paths = []

    paths.append(word_path)
    paths.append(pdf_path)
    paths.append(path1)
    paths.append(path2)
    paths.append(path3)
    paths.append(path4)
    paths.append(path5)

    for path in paths:
        makedir(path, 5000)
    # makedir(pathway6, 5000)
    # makedir(r'D:\Transformed_files\tmp_for_pathways', 15000)

    # files_list = glob.glob(files_path + '/*.pdf')
    # folder_name = sorted(os.listdir(pdf_path), key=lambda x:int(x.split('-')[1]))
    #
    # divided_into_more(files_list, folder_name, pdf_path)
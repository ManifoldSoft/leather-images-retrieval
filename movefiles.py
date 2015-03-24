# -*- coding: utf-8 -*-
# 用于将当前目录下不同类别的文件夹下的图片搬到某个文件夹，并在文件前面加上目录名字

import os
import fnmatch
import shutil
import random
import math

query_number_percent = 0.5 # 设置每类拿百分之多少出来作为查询

directory = "Brodatz"  # 设置新路径

if not os.path.exists(directory):
    os.makedirs(directory)

newImgDBPath = os.path.abspath(directory)

# walk through the folder
f = open("./Brodatz111classes.txt", "w")
g = open("./queryImgs.txt", "w")
for root, dirs, files in os.walk('Brodatz111classes'):
    for str_each_folder in dirs:
        # we get the directory path
        str_the_path = '/'.join([root, str_each_folder])

        files_number = len(fnmatch.filter(os.listdir(str_the_path), '*.png'))
        # 生成查询图片实例
        index = random.sample(range(0, files_number), int(math.floor(query_number_percent*files_number)))
        # list all the files using directory path
        for ind, str_each_file in enumerate(os.listdir(str_the_path)):
            # look for the files we want
            if str_each_file.endswith('.png'):
                # now add the new one
                str_new_name = str_each_folder + '_' + str_each_file
                if ind in index:
                    g.writelines('%s\n' % str_new_name)
                # full path for both files
                str_old_name = '/'.join([str_the_path, str_each_file])
                str_new_name = '/'.join([newImgDBPath, str_new_name])

                # now rename using the two above strings
                # and the full path to the files
                # os.rename(str_old_name, str_new_name) # move files
                shutil.copy2(str_old_name, str_new_name)  # 拷贝原文件到设置的新目录下

        #  we can print the folder name so we know
        # that all files in the folder are done
        print '%s, %d images' % (str_each_folder, files_number)
        # f.writelines('%s\n' % (str_each_folder))
        f.writelines('%s %d\n' % (str_each_folder, files_number))

f.close

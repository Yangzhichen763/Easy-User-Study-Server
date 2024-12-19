# 将文件夹下所有文件名为 ['a.png'].* 的文件重命名为 a.png
import os
import re

if __name__ == '__main__':
    dir_path = "images"
    def rename_file(dir_path):
        for file in os.listdir(dir_path):
            # 文件夹递归
            file_dir_path = os.path.join(dir_path, file)
            if os.path.isdir(file_dir_path):
                rename_file(file_dir_path)
                continue

            # 文件改名
            match = re.match(r"\['(.*?)'].*", file)
            if match:
                file_path = os.path.join(file_dir_path)
                new_file_path = os.path.join(dir_path, match.group(1))
                os.rename(file_path, new_file_path)

    rename_file(dir_path)



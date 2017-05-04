# -*- coding: UTF-8 -*-
# 中英文都能handle。

import os
import re
import commands


# unrar x /home/hadoop/Desktop/rar/*.rar /tmp
def uncompression_rar_file(file_name, output_path):
    s = "unrar x "
    s = s + file_name + " " + output_path
    os.system(s)

    # delete *.rar
    s = "rm -rf "
    s = s + file_name
    os.system(s)


# unzip /home/hadoop/Desktop/rar/*.zip -d /tmp
def uncompression_zip_file(file_name, output_path):
    s = "unzip -n "
    s = s + file_name + " -d " + output_path
    os.system(s)

    # delete *.zip
    s = "rm -rf "
    s = s + file_name
    os.system(s)


# 7za x phpMyAdmin-3.3.8.1-all-languages.7z -r -o./
# 递归一次就好了
def uncompression_7z_file(file_name, output_path):
    s = "7za x "
    s = s + file_name + " -r -o" + output_path
    os.system(s)

    # delete *.7z
    s = "rm -rf "
    s = s + file_name
    os.system(s)


def visit(input_path):
    s = "ls " + input_path + "/*.7z"
    z_files = commands.getoutput(s)
    if len(z_files) > 0 and z_files != "ls: cannot access " + input_path + "/*.7z: No such file or directory":
        z_files = z_files.split("\n")
        for file in z_files:
            uncompression_7z_file(file, input_path + "/")
    uncompression_zip_file(input_path + "/*.zip", input_path)
    uncompression_rar_file(input_path + "/*.rar", input_path)

    files = commands.getoutput("ls " + input_path)
    if len(files) > 0 and files != "ls: cannot access " + input_path + ": No such file or directory":
        files = files.split("\n")

        for f in files:
            if f.endswith(".zip") or f.endswith(".rar") or f.endswith(".7z"):
                files.remove(f)

        for f in files:
            t = input_path + "/" + f
            if os.path.isdir(t):
                visit(t)


def main():
    print 'begin'
    begin_path = "/home/sun/Desktop/uncompress/1"
    visit(begin_path)


if __name__ == '__main__':
    main()
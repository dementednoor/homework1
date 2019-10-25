import hashlib
import os
import sys


class File:  # creating class for more comfortable data storage of concrete file
    def __init__(self, name, method, cs_value):
        self.name = name
        self.method = method
        self.cs_value = cs_value


if __name__ == '__main__':
    try:
        file_path = sys.argv[1]
        bins_path = sys.argv[2]
        os.chdir(file_path)  # or whatever the address is
        path = os.getcwd()
        with open(file_path + 'cs.txt', 'r') as f:
            content = f.read()  # getting info from the textfile
        strings = content.split('\n')  # every file info begins with the new string so we divide them
        files = []  # list of file objects

        for s in strings:
            params = s.split(' ')  # structuring the parameters of file
            try:
                files.append(File(params[0], params[1], params[2]))  # and identify those parameters
            except IndexError as e:
                continue

        #  comparing data from files list with data that we're about to calculate
        os.chdir(bins_path)
        for f in files:  # data from files list
            md5 = hashlib.md5()
            sha1 = hashlib.sha1()
            sha256 = hashlib.sha256()
            try:
                check = f.name
                with open(check, 'rb') as curr_f:  # curr_f for current file
                    m = f.method
                    if m == 'md5':
                        md5.update(curr_f.read())
                        cs = md5.hexdigest()
                    elif m == 'sha1':
                        sha1.update(curr_f.read())
                        cs = sha1.hexdigest()
                    else:
                        sha256.update(curr_f.read())
                        cs = sha256.hexdigest()
                if f.cs_value == cs:
                    print('{} OK\n'.format(f.name))
                elif f.cs_value != cs:
                    print('{} FAIL\n'.format(f.name))
            except FileNotFoundError:
                print('{} NOT FOUND\n'.format(f.name))
            continue

    except (IndexError, FileNotFoundError):
        print("You didn't specify path to the file or bin files correctly. Please, try again.")
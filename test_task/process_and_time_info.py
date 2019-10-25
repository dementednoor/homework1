import os
import re
import subprocess
import sys


def timer_info_print(timer_name):
    try:
        timer_name = timer_name + '.timer'  # giving timer an appropriate name
        contents = subprocess.check_output('systemctl status {}'.format(timer_name),  # capturing bash-command output
                                           stderr=subprocess.STDOUT, shell=True).decode()
        contents_list = contents.split('\n')  # dividing that output by paragraphs
        print(contents_list[2])  # printing activity section
    except subprocess.CalledProcessError:
        print("Timer doesn't exist. Please, enter it's name properly.")


def service_info_print(service_name):
    contents = subprocess.run('service {} status'.format(service_name), stderr=subprocess.STDOUT, shell=True,
                              check=False, stdout=subprocess.PIPE).stdout.decode()
    if contents.rfind('could not be found') != -1:
        print("Process doesn't exist")
    else:
        contents_list = contents.split('\n')
        print('{} {}'.format(service_name, contents_list[2]))
        if contents_list[2].rfind('Active: active') != -1:
            try:
                user_info = subprocess.check_output('ps -eo pid,comm,euser,supgrp | grep {}'.format(service_name),
                                                    stderr=subprocess.STDOUT, shell=True).decode()
                space = re.compile('[ ]+')  # in case there are several spaces between ps arguments
                info_list = space.split(user_info)
                print('user - {}, group(s) - {}'.format(info_list[-2], info_list[-1]))
            except (subprocess.CalledProcessError, IndexError):
                print('user = None, group = None')


if __name__ == '__main__':
    try:
        if sys.argv[1] == '--timer':
            os.chdir('/etc/systemd/system/timers.target.wants')
            timer_info_print(sys.argv[2])
        elif sys.argv[1] == '--service':
            service_info_print(sys.argv[2])
        else:
            print("You didnt' specify '--service' or '--timer' as a second parameter. Please, try again.")

    except IndexError:
        print("You didn't enter name of timer or service properly. Please, try again.")
#!/usr/bin/env python

from datetime import datetime
import os
import sys
import shutil

months = {'Jan': 'Q1',
          'Feb': 'Q1',
          'Mar': 'Q1',
          'Apr': 'Q2',
          'May': 'Q2',
          'Jun': 'Q2',
          'Jul': 'Q3',
          'Aug': 'Q3',
          'Sep': 'Q3',
          'Oct': 'Q4',
          'Nov': 'Q4',
          'Dec': 'Q4'}

basedrive = 'z:'
fmm_basedir = os.path.join(basedrive, "\\powershell", "fmm")
current_month = datetime.now().strftime('%h')
current_qtr = months.get(current_month)
today = datetime.now().strftime('%Y%m%d')
dest_basedir = r"c:\Users\monet\OneDrive\Documents\exportxfb"


def check_dir(dir):
    status = os.path.exists(dir)
    if status:
        print("{} exists".format(dir))
    else:
        print("{} does not exists".format(dir))
    return status


def copy_dir(src, dest):
    print("Copying the data from {} to {}".format(src, dest))
    shutil.copytree(src, dest, dirs_exist_ok=True)


def main():
    if check_dir(fmm_basedir):
        os.chdir(fmm_basedir)
        if current_qtr in os.listdir(os.getcwd()):
            current_qtr_dir = os.path.join(fmm_basedir, current_qtr)
            os.chdir(current_qtr_dir)
            datadirs = os.listdir(os.getcwd())
            today_dirs = [d for d in datadirs if today in d]
            sorted_today_dirs = sorted(today_dirs)
            print(sorted_today_dirs)
            latest_today_dir = sorted_today_dirs[-1]
            source_dir = os.path.join(current_qtr_dir, latest_today_dir)
            dest_dir = os.path.join(dest_basedir, latest_today_dir)
            print('The latest output directory {} marked for copy'.format(source_dir))
            copy_dir(source_dir, dest_dir)
        else:
            print('{} directory does not exists, exiting...'.format(current_qtr))
            sys.exit(1)
    else:
        print("{} does not exists, exiting...".format(fmm_basedir))
        sys.exit(1)


if __name__ == '__main__':
    main()

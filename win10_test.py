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

src_basedir = r"z:\powershell\FMM_CYCLE\B - LIST CREATION OUTPUT"
dest_basedir = r"c:\Users\monet\OneDrive\Documents\exportxfb"
current_month = datetime.now().strftime('%h')
current_year = datetime.now().strftime('%Y')
current_qtr = months.get(current_month)
current_year_qtr = '_'.join([current_year, current_qtr])
today = datetime.now().strftime('%Y%m%d')


def check_dir(dir):
    status = os.path.exists(dir)
    if status:
        print("[ INFO ] {} exists.".format(dir))
    else:
        print("[ FAIL ] {} does not exists.".format(dir))
    return status


def copy_dir(src, dest):
    print("[ INFO ] Copying the data from {} to {}.".format(src, dest))
    try:
        shutil.copytree(src, dest, dirs_exist_ok=True)
    except Exception as e:
        print("[ FAIL ] Data copy encountered issues {}, please check manually.".format(e))


def main():
    if check_dir(src_basedir):
        os.chdir(src_basedir)
        if current_year_qtr in os.listdir(os.getcwd()):
            current_year_qtr_dir = os.path.join(src_basedir, current_year_qtr)
            os.chdir(current_year_qtr_dir)
            datadirs = os.listdir(os.getcwd())
            today_dirs = [d for d in datadirs if today in d]
            sorted_today_dirs = sorted(today_dirs)
            latest_today_dir = sorted_today_dirs[-1]
            source_dir = os.path.join(current_year_qtr_dir, latest_today_dir)
            dest_dir = os.path.join(dest_basedir, latest_today_dir)
            print("[ INFO ] {} identified as the latest source data directory.".format(source_dir))
            copy_dir(source_dir, dest_dir)
        else:
            print('[ INFO ] {} directory does not exists, exiting...'.format(current_year_qtr))
            sys.exit(1)
    else:
        print("[ FATAL ] {} does not exists, exiting...".format(src_basedir))
        sys.exit(1)


if __name__ == '__main__':
    main()

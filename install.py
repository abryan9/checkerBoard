#!/usr/bin/env Python3
import os
import platform

ABS_PATH = __file__.removesuffix('install.py')
OS = platform.platform()

os.system('mkdir C:\\UWApps\\checkerBoard')
os.system(f'xcopy {ABS_PATH} C:\\UWApps\\checkerBoard /s /e > nul')

if 'Windows' in OS:
    os.system(f'cscript C:/UWApps/checkerBoard/local_dist/install/install.vbs')
else:
    print('[-] ERROR: Operating System Not Supported.')
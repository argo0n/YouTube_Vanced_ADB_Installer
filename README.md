# YouTube_Vanced_ADB_Installer
A script to install YouTube Vanced without using the Vanced Manager app.
This Installer should not be confused with the official Vanced Manager. It is an alternative solution for people who would not like to use the Vanced Manager to install YouTube Vanced, such as Xiaomi users who need to disable optimization every time they install.

## Dependencies
- `tqdm` - For progress bar
- `requests` - To get latest version from Vanced API and download required APKs. 

## How to use it
1) This script uses ADB to install the APKs to your phone. You need to enable USB Debugging on your Android phone and connect it to your PC, where the script will be run.
2) `git clone https://github.com/argo0n/YouTube_Vanced_ADB_Installer`
3) `cd YouTube_Vanced_ADB_Installer`
4) `pip install -r requirements.txt`
5) `python3 main.py`

## Features
- Only requires ADB, no other separate APK is needed
- Does not run unnecessasry code if your Vanced app is up to date

## Warning
- This script probably only supports 64-bit Android devices.


## Future plans
- Currently, the language and theme is hardcoded to `en` and `black` respectively. In the future there will be a way to configure them.
- The script does not install MicroG at the same time.
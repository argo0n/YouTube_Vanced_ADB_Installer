import os
import subprocess
import requests
from tqdm import tqdm
def main():
    def get_current_directory():
        result = subprocess.run(['cd'], stdout=subprocess.PIPE, shell=True)
        decoded = result.stdout.decode('utf-8')
        return decoded.strip()
    current_directory = get_current_directory()

    print("===============================================================")
    print("Vanced Updater v1.0.0 by Argon")
    print("===============================================================")
    print(" ")
    print("===============================================================")
    print("Getting device and installed YouTube Vanced information...")
    print("===============================================================")
    print(" ")
            
    def get_top_connected_device_id_in_adb_via_subprocess():
        result = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE, shell=True)
        decoded = result.stdout.decode('utf-8')
        if "is not recognized as an internal or external command" in decoded:
            raise ValueError("I did not detect an installation of ADB. If you have it downloaded, add the path to your adb.exe file to your PATH environment variable. Restart your computer after doing so.")
        lines = decoded.splitlines()
        if len(lines) < 2:
            raise ValueError("No devices are connected to your PC.")
        if "List of devices attached" not in lines[0]:
            raise ValueError("Something went wrong. Please try again.")
        line2 = lines[1]
        if line2 == "":
            raise ValueError("No detected Android devices are connected to your PC.")
        if "device" not in line2:
            if "unauthorized" in line2:
                raise ValueError("Please allow USB Debugging to your Android phone before running this script.")
            else:
                raise ValueError("Something went wrong. Please try again.")
        else:
            device_id = line2.split()[0].strip()

        if device_id is None:
            raise ValueError("Something went wrong. Please try again.")
        return device_id

        
    device_id = get_top_connected_device_id_in_adb_via_subprocess()

    def get_device_vendor_manufacturer_and_model_in_adb(device_id):
            result = subprocess.run(['adb', '-s', device_id, 'shell', 'getprop', 'ro.product.manufacturer'], stdout=subprocess.PIPE, shell=True)
            decoded = result.stdout.decode('utf-8')
            manufacturer = decoded.strip()
            result = subprocess.run(['adb', '-s', device_id, 'shell', 'getprop', 'ro.product.model'], stdout=subprocess.PIPE, shell=True)
            decoded = result.stdout.decode('utf-8')
            model = decoded.strip()
            return manufacturer, model
    manufactuerer, model = get_device_vendor_manufacturer_and_model_in_adb(device_id)
    def get_architecture(device_id):
        result = subprocess.run(['adb', '-s', device_id, 'shell', 'getprop', 'ro.product.cpu.abi'], stdout=subprocess.PIPE, shell=True)
        decoded = result.stdout.decode('utf-8')
        architecture = decoded.strip()
        return architecture
    architecture = get_architecture(device_id)
    if architecture not in ['x86', 'arm64-v8a', 'armeabi-v7a']:
        raise ValueError("Your device is not supported as its architecture is not one of 'x86', 'arm64-v8a', 'armeabi-v7a'. Please try again.")
    architecture = architecture.replace('-', '_')
    print(f"Detected Android device: {manufactuerer} {model} with architecture {architecture}.")
    def get_vanced_version(device_id):
        if os.name == 'nt':
            command = ['adb', '-s', device_id, 'shell', 'dumpsys', 'package', 'com.vanced.android.youtube', '|', 'findstr', 'versionName']
        else:
            command = ['adb', '-s', device_id, 'shell', 'dumpsys', 'package', 'com.vanced.android.youtube', '|', 'grep', 'versionName']
        result = subprocess.run(command, stdout=subprocess.PIPE, shell=True)
        decoded = result.stdout.decode('utf-8')
        if len(decoded) < 1:
            ver = "0.0.0"
        else:
            ver = decoded.strip().replace('\r\n', '').split('=')[1]
        return ver
    current_installed_version = get_vanced_version(device_id)
    if current_installed_version == "0.0.0":
        print(f"{model} does not have YouTube Vanced installed.")
    else:
        print(f"Installed YouTube Vanced version: {current_installed_version}")
    
    print(" ")
    print("===============================================================")
    print("Starting Vanced app installation...")
    print("===============================================================")
    print(" ")

    def get_latest_vanced_apk_version_via_requests():
        url = "https://api.vancedapp.com/api/v1/latest.json"
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError("I could not connect to the Vanced API to get the latest infromation, sorry.")
        data = response.json()
        return data['vanced']['version']

    print("Getting latest YouTube Vanced version:")
    version = get_latest_vanced_apk_version_via_requests()
    if version is None:
        raise ValueError("Something went wrong. Please try again.")
    print(f"Latest YouTube Vanced version: {version}")
    if version == current_installed_version:
        print("You have the latest YouTube Vanced version installed, there's no need for an update.")
        return
    print(f"Downloading YouTube Vanced with configuration THEME: BLACK, ROOT: NONROOT, LANGUAGE: EN, ARCHITECTURE: {architecture}...")
    theme = 'black'
    root = 'nonroot'
    language = 'en'

    def download_file(size, path, response):
        with open(path, 'wb') as file:
            for chunk in tqdm(response.iter_content(), total=size, unit='B', unit_scale=True, desc=path):
                file.write(chunk)
        return
    def get_vanced_theme_apk_via_requests(version):
        print(f"Downloading theme {theme}.apk...")
        filename = f"{theme}.apk"
        url = f"https://vancedapp.com/api/v1/apks/v{version}/nonroot/Theme/{theme}.apk"
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(f"I was not able to download the file, sorry. \nError: Faced a {response.status_code} code while downloading from {url}.")
        download_file(int(response.headers['Content-Length']), f"{theme}.apk", response)
        print(f"Downloaded {current_directory}\\{theme}.apk")
        return filename

    def get_vanced_language_apk_via_requests(version):
        print(f"Downloading language split_config.{language}.apk...")
        filename = f"split_config.{language}.apk"
        url = f"https://vancedapp.com/api/v1/apks/v{version}/nonroot/Language/split_config.{language}.apk"
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(f"I was not able to download the file, sorry. \nError: Faced a {response.status_code} code while downloading from {url}.")
        download_file(int(response.headers['Content-Length']), f"split_config.{language}.apk", response)
        print(f"Downloaded {current_directory}\\{language}.apk")
        return filename

    def get_vanced_architecture_apk_via_requests(version):
        print(f"Downloading architecture split_config.{architecture}.apk...")
        filename = f"split_config.{architecture}.apk"
        url = f"https://vancedapp.com/api/v1/apks/v{version}/nonroot/Arch/split_config.{architecture}.apk"
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(f"I was not able to download the file, sorry. \nError: Faced a {response.status_code} code while downloading from {url}.")
        download_file(int(response.headers['Content-Length']), f"split_config.{architecture}.apk", response)
        print(f"Downloaded {current_directory}\\{architecture}.apk")
        return filename

    
    theme_filename = get_vanced_theme_apk_via_requests(version)
    language_filename = get_vanced_language_apk_via_requests(version)
    architecture_filename = get_vanced_architecture_apk_via_requests(version)
    print(f"All 3 required files ({theme_filename}, {language_filename}, {architecture_filename}) downloaded.")
    print("Installing YouTube Vanced...\nAllow the installation to proceed if it prompts.")
    def install_apk():
        result = subprocess.run(['adb', 'install-multiple', theme_filename, language_filename, architecture_filename], stdout=subprocess.PIPE, shell=True)
        return result.stdout.decode('utf-8')
    print(install_apk())


if __name__ == '__main__':
    try:
        main()
    except ValueError as e: 
        print(str(e))
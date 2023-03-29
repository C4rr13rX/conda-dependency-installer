import subprocess
import json
import time
import sys

def run_command(cmd):
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result.check_returncode()
        return result
    except subprocess.CalledProcessError as e:
        return e

def find_dependencies(package):
    result = subprocess.run(['conda', 'search', package, '--info', '--json'], stdout=subprocess.PIPE)
    packages = json.loads(result.stdout)

    for package_info in packages.values():
        if package_info[0]['name'] == package:
            return package_info[0]['depends']
    
    return []



def install_dependencies(package):
    dependencies = find_dependencies(package)
    print(f"Installing dependencies for {package}...")
    for dep in dependencies:
        print(f"Installing package: {dep}...")
        attempts = 0
        while attempts < 100:
            cmd = ["conda", "install", "-y", dep]
            result = run_command(cmd)
            if isinstance(result, subprocess.CalledProcessError):
                print(f"Error installing {dep}. Retrying in 2 seconds...")
                time.sleep(2)
                attempts += 1
            else:
                break
        if attempts == 100:
            print(f"Failed to install {dep}")
            return False
    return True

def install_package(package):
    print(f"Installing package: {package}...")
    attempts = 0
    while attempts < 100:
        cmd = ["conda", "install", "-y", package]
        result = run_command(cmd)
        if isinstance(result, subprocess.CalledProcessError):
            print(f"Error installing {package}. Retrying in 2 seconds...")
            time.sleep(2)
            attempts += 1
        else:
            break
    if attempts == 100:
        print(f"Failed to install {package}")
        return False
    return True

if __name__ == '__main__':
    package = sys.argv[1]
    print(f"Installing package: {package}")
    if install_dependencies(package) and install_package(package):
        print(f"Successfully installed {package}")
    else:
        print(f"Failed to install all dependencies and/or {package}")

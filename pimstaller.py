#!/usr/bin/python

import yaml
import argparse
import glob
import sys
import subprocess
import os
import colorama

def print_color(color, message):
    print(color + message + colorama.Fore.RESET)

def print_error(message):
    print_color(colorama.Fore.RED, message)

def print_warning(message):
    print_color(colorama.Fore.YELLOW, message)

def print_error(message):
    print_color(colorama.Fore.RED, message)

def print_ok(message):
    print_color(colorama.Fore.GREEN, message)

def _sudo(process):
    process = "sudo " + process
    
    #print(process)

    proc = subprocess.Popen(process,
        shell=True,
	stdin=subprocess.PIPE,
	stdout=subprocess.PIPE)

    return_code = proc.wait()

    #print("Process returned: {}".format(return_code))
    response = proc.communicate()

    return {'output': response[0], 'error': response[1], 'code': return_code}

def _apt_get_update():
    response = _sudo("apt-get update")
    if 'Done' in response:
        print_ok("-- Package lists updated!")
    else:
        print_error("-- Something went wrong!")
    

def _check_hw(hw):
    if hw == 'i2c':
        print("- Checking if i2c is enabled...")
    pass

def _install_pip(python_version, package_name):
    print_warning("- Installing {} for {}".format(package_name, python_version))

    # '/usr/local/bin/pip-3.2'
    pip = "/usr/bin/pip"

    if python_version == "python3":
        pip = "/usr/local/bin/pip-3.2"

    response = _sudo("/usr/bin/pip install {}".format(package_name))
    #print(response)
    if 'already satisfied' in response['output']:
        print_ok("-- {} already installed!".format(package_name))
    elif 'Successfully installed' in response['output']:
        print_ok("-- {} installed successfully!".format(package_name))

def _install_apt(python_version, package_name):
    print_warning("- Installing {} for {}".format(package_name, python_version))
    response = _sudo("/usr/bin/apt-get install {} -y".format(package_name))
    print(response)
  
    if 'already the newest version' in response['output']:
        print_ok("-- {} already installed!".format(package_name))

def _action_install(args):
    data = None
    package = args.package
    
    local_file = "./{}.yaml".format(package)
    if os.path.isfile(local_file):
        data = yaml.load(open(local_file).read())
        print_warning("Using local file: {}".format(local_file))
    else:
        data = None

    if data == None:
        print_error("""
Unrecognised Package: {}
""".format(package))
        return 1


    if 'name' in data:
        print_ok("Package Name: {}".format(data['name']))
    else:
        print_error("Malformed package. Missing key 'name'")
        return 0

    if 'supported' in data:
        print("Supports: {}".format(','.join(data['supported'])))
    else:
        print_error("Malformed package. Missing key 'supported'")
        return 0

    deps = data['dependencies']

    if 'hw' in deps:
        print("\nChecking hardware dependencies...")
        for hw in deps['hw']:
            _check_hw(hw)

    if 'pip' in deps:
        print("\nChecking pip dependencies...")
        for package_name in deps['pip']:
            for python_version in data['supported']:
                _install_pip(python_version, package_name)

    if 'apt' in deps:
        print("\nChecking apt dependencies...")
        for python_version in deps['apt'].keys():
            for package_name in deps['apt'][python_version]:
                #print(python_version, package_name)
                _install_apt(python_version, package_name)

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

s_install = subparsers.add_parser("install")
s_install.set_defaults(action=_action_install)
s_install.add_argument("package", help="Package name")

args = parser.parse_args()

if hasattr(args, "action"):
    exit(args.action(args))

parser.print_usage()

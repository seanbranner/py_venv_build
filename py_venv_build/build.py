import subprocess
from pathlib import Path
from os import mkdir, path
import json

json_path = Path('config.json')

with open(json_path, 'r') as f:
    config = json.load(f)

root_path = Path(config['APP']['ROOT'])

app_name = config['APP']['NAME']
package_list = config['APP']['PACKAGES']
app_dir = root_path.joinpath(app_name)
project_name = app_name.replace('-', '_')
project_dir = app_dir.joinpath(project_name)

venv_name = f".venv_{project_name}"

log_file_name = "build.log"

if not path.exists(app_dir):
    mkdir(app_dir)
    mkdir(project_dir)

if config['APP']['EXECUTABLE']:
    project_app_dir = project_dir.joinpath("App")  # add ability to create if not there
    mkdir(project_app_dir)
    project_dist_dir = project_app_dir.joinpath("dist")
    project_build_dir = project_app_dir.joinpath("build")
    executable_dir = project_dist_dir.joinpath(app_name)

venv_dir = app_dir.joinpath(venv_name)
venv_script_dir = venv_dir.joinpath("Scripts")
venv_python = venv_script_dir.joinpath("python.exe")
venv_activate = venv_script_dir.joinpath("activate.bat")

package_install_file = app_dir.joinpath("install_packages.bat")

build_cmd = f"python -m venv --clear {venv_dir}"
print(build_cmd)
subprocess.call(build_cmd, cwd=root_path)

# install_packages_command = f"pip install"
# for package in package_list:
#     install_packages_command = f"{install_packages_command} {package}"
#
# install_packages_script = open(package_install_file, "w")
# install_packages_script.write(f'{str(venv_activate)} && {install_packages_command}')
# install_packages_script.close()

# subprocess.call(package_install_file)

# print(venv_script_dir)
# subprocess.call(venv_activate, cwd=venv_script_dir)

# install_packages_command = f"""
#     {venv_activate}
#     pip install"""
# for package in package_list:
#     install_packages_command = f"{install_packages_command} {package}"
# print(install_packages_command)
# subprocess.call(install_packages_command)
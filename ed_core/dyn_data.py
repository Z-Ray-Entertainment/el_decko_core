import os
import json
import shutil

from xdg import (
    xdg_cache_home,
    xdg_config_dirs,
    xdg_config_home,
    xdg_data_dirs,
    xdg_data_home,
    xdg_runtime_dir,
    xdg_state_home,
)

__app_name = "eldecko"
CONFIG_ROOT: str = ""
DATA_ROOT: str = ""
if os.name == "nt":
    CONFIG_ROOT = os.getenv('LOCALAPPDATA') + "/" + __app_name + "/"
    DATA_ROOT = os.getenv('LOCALAPPDATA') + "/" + __app_name + "/"
elif os.name == "posix":
    CONFIG_ROOT = str(xdg_config_home()) + "/" + __app_name + "/"
    DATA_ROOT = str(xdg_data_home()) + "/" + __app_name + "/"
else:
    CONFIG_ROOT = ""
    DATA_ROOT = ""

CONFIG_ROOT_BACKEND = CONFIG_ROOT + "backends/"
ASSETS_ROOT = DATA_ROOT + "assets/"

if not os.path.exists(ASSETS_ROOT):
    os.makedirs(ASSETS_ROOT)
if not os.path.exists(CONFIG_ROOT):
    os.makedirs(CONFIG_ROOT)


def load_config(root_path: str, file_name: str):
    if not os.path.exists(root_path):
        os.makedirs(root_path)
    try:
        with open(root_path + file_name) as input_file:
            data = json.load(input_file)
            return data
    except json.decoder.JSONDecodeError as e:
        print(e)


def store_config(root_path: str, file_name: str, data: dict):
    if not os.path.exists(root_path):
        os.makedirs(root_path)
    with open(root_path + file_name, "w+", encoding="utf-8") as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=2)


def store_image(source: str):
    file_name = os.path.basename(source).split('/')[-1]
    shutil.copyfile(source, ASSETS_ROOT + file_name)


def config_exists(root_path: str, file_name: str):
    return os.path.isfile(root_path + file_name)

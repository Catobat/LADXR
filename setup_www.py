import json
import os
from settings import Settings
import shutil
import tarfile


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def tar_filter(member: tarfile.TarInfo):
    if member.name == "":
        return member
    split_path = os.path.split(member.name)
    file_name = split_path[-1]
    if member.isdir():
        if not file_name.startswith(".") and file_name != "__pycache__" and member.name != "docs" and member.name != "www":
            return member
    else:
        if not file_name.startswith("LADXR_") and not file_name.endswith(".gbc"):
            return member


def create_setting_json():
    with open(os.path.join(BASE_DIR, "www", "js", "options.js"), "w") as output:
        output.write("var options =\n")
        output.write(json.dumps(Settings().toJson(), indent=1))
        output.write("\n")


def copy_gfx_previews():
    src_path = os.path.join(BASE_DIR, "gfx")
    dst_path = os.path.join(BASE_DIR, "www", "LADXR", "gfx")
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)
        for file in os.listdir(src_path):
            if file.endswith(".bin.png"):
                shutil.copy(os.path.join(src_path, file), dst_path)


def create_tar_gz():
    src = os.path.dirname(__file__)
    dest = os.path.join(BASE_DIR, "www", "js", "ladxr.tar.gz")
    with tarfile.open(dest, "w:gz") as tar:
        tar.add(src, arcname="", filter=tar_filter)


if __name__ == "__main__":
    create_setting_json()
    copy_gfx_previews()
    create_tar_gz()

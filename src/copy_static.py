import shutil
from pathlib import Path

"""
delete all contents in destination dirnamed public)
copy and paste all files and subdirectories, 
nested files within subdirectories to destination dir


pseudocode:
    ok so if there is no destination directory, can just make it.

    then for every file in the source directory, copy it to the destination directory
    for every subdirectory in the source directory, make a copy of it to destination directory
        then recurse until no more subdirs/files left


    if there is a dest dir
        for every file in dest dir
            delete the file
        for every subdir in dest dir
            delete all files in sub dir by recursing
            remove the subdir
"""


def delete_dir_contents(path):
    for item in path.iterdir():
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            delete_dir_contents(item)
            item.rmdir()


def copy_dir_contents(source, dest):
    for item in source.iterdir():
        dest_item = dest / item.name
        if item.is_file():
            shutil.copy2(item, dest_item)
        elif item.is_dir():
            dest_item.mkdir()
            copy_dir_contents(item, dest_item)


def copy_static():
    root = Path(__file__).parent.parent
    static = root / "static"
    public = root / "public"

    if public.exists():
        delete_dir_contents(public)
    else:
        public.mkdir(parents=True, exist_ok=True)
    copy_dir_contents(static, public)

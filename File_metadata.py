import argparse
import os
import sys
import datetime

def get_file_metadata(file_path, ext, mtime, size):
    stat_info = os.stat(file_path)
    
    # Filter by file extension
    if ext and not file_path.endswith(ext):
        return
    
    # Filter by date modified
    if mtime and stat_info.st_mtime < mtime:
        return
    
    # Filter by file size
    if size and stat_info.st_size > size:
        return
    
    print("File path:", file_path)
    print("File size:", stat_info.st_size, "bytes")
    print("Number of hard links:", stat_info.st_nlink)
    print("File mode:", stat_info.st_mode)
    print("File inode number:", stat_info.st_ino)
    print("Device ID:", stat_info.st_dev)
    print("Group ID:", stat_info.st_gid)
    print("User ID:", stat_info.st_uid)
    print("Modified time:", datetime.datetime.fromtimestamp(stat_info.st_mtime))
    print("Access time:", datetime.datetime.fromtimestamp(stat_info.st_atime))
    print("Creation time:", datetime.datetime.fromtimestamp(stat_info.st_ctime))
    print("Absolute path:", os.path.abspath(file_path))
    if os.path.islink(file_path):
        print("This is a symbolic link.")
        print("Link target:", os.readlink(file_path))
    else:
        print("This is not a symbolic link.")
    print("Directory it resides in:", os.path.dirname(os.path.abspath(file_path)))
    print("=" * 50)

def process_dir(dir_path, ext, mtime, size):
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)
            get_file_metadata(file_path, ext, mtime, size)

def main():
    parser = argparse.ArgumentParser(description="Get file metadata.")
    parser.add_argument("dir_path", help="Path to the directory to process")
    parser.add_argument("-e", "--ext", help="File extension to filter by")
    parser.add_argument("-t", "--mtime", type=float, help="Modified time filter (unix timestamp)")
    parser.add_argument("-s", "--size", type=int, help="File size filter (bytes)")
    args = parser.parse_args()
    dir_path = args.dir_path
    ext = args.ext
    mtime = args.mtime
    size = args.size
    
    if not os.path.exists(dir_path):
        print("Error:", dir_path, "does not exist.")
        sys

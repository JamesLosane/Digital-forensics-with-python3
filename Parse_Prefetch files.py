import os
import struct
import datetime

def parse_prefetch_file(filename):
    # Open the Prefetch file and read the header
    with open(filename, "rb") as f:
        header = f.read(0x40)

    # Parse the header fields
    magic, _, _ = struct.unpack("<4sHH", header[:8])
    if magic != b'MAM\x00':
        raise ValueError("Invalid Prefetch file format")
    exec_count, _, _ = struct.unpack("<HHH", header[0x10:0x16])
    path_offset, _ = struct.unpack("<II", header[0x3C:0x44])

    # Read the file path from the Prefetch file
    with open(filename, "rb") as f:
        f.seek(path_offset)
        path = ""
        while True:
            c = f.read(1)
            if c == b"\x00":
                break
            path += c.decode("utf-16le")

    # Get the creation time of the Prefetch file
    ctime = os.path.getctime(filename)

    # Return the parsed data as a dictionary
    return {
        "filename": os.path.basename(filename),
        "executable_path": path,
        "execution_count": exec_count,
        "created_time": datetime.datetime.fromtimestamp(ctime),
        "last_run_time": None,
        "run_count": 0,
    }

def analyze_prefetch_files(directory):
    # Find all Prefetch files in the specified directory
    prefetch_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".pf")]

    # Parse each Prefetch file and build a dictionary of program information
    program_info = {}
    for filename in prefetch_files:
        try:
            data = parse_prefetch_file(filename)
        except ValueError:
            continue
        program_name = os.path.splitext(data["filename"])[0]
        if program_name not in program_info:
            program_info[program_name] = {
                "executable_path": data["executable_path"],
                "last_run_time": data["created_time"],
                "run_count": data["execution_count"],
                "prefetch_files": [],
            }
        else:
            program_info[program_name]["run_count"] += data["execution_count"]
            if data["created_time"] > program_info[program_name]["last_run_time"]:
                program_info[program_name]["last_run_time"] = data["created_time"]
        program_info[program_name]["prefetch_files"].append(data)

    # Sort the program information by last run time
    program_info = {k: v for k, v in sorted(program_info.items(), key=lambda item: item[1]["last_run_time"], reverse=True)}

    # Print the program information
    for program_name, info in program_info.items():
        print(f"Program: {program_name}")
        print(f"  Executable path: {info['executable_path']}")
        print(f"  Last run time: {info['last_run_time']}")
        print(f"  Total run count: {info['run_count']}")
        print("  Prefetch files:")
        for data in info["prefetch_files"]:
            print(f"    {data['filename']} (created: {data['created_time']})")

if __name__ == "__main__":
    # Example usage: analyze Prefetch files in the "C:\Windows\Prefetch" directory
    prefetch_directory = r"C:\Windows\Prefetch"
    analyze_prefetch_files(prefetch_directory)

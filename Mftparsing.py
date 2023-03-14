import argparse
from mft_analyzer import analyze_mft

# Define command line arguments
parser = argparse.ArgumentParser(description="Analyze an NTFS MFT file")
parser.add_argument("filename", help="Path to the MFT file")

# Parse command line arguments
args = parser.parse_args()

# Analyze the MFT file
mft = analyze_mft(args.filename)

# Print summary information about the MFT file
print(f"Total Records: {mft['total_records']}")
print(f"Bytes Per Record: {mft['bytes_per_record']}")
print(f"Clusters Per Record: {mft['clusters_per_record']}")
print(f"Bytes Per Cluster: {mft['bytes_per_cluster']}")

# Print detailed information about each MFT record
for record in mft["records"]:
    print(f"\nRecord Number: {record['record_number']}")
    print(f"Signature: {record['signature'].hex()}")
    print(f"Fixup Offset: {record['fixup_offset']}")
    print(f"Fixup Count: {record['fixup_count']}")
    print(f"Logfile Sequence Number: {record['logfile_seq_num']}")
    print(f"Sequence Number: {record['sequence_num']}")
    print(f"Link Count: {record['link_count']}")
    print(f"Attribute Offset: {record['attr_offset']}")
    print(f"Flags: {record['flags']}")
    print(f"Record Size: {record['record_size']}")
    print(f"Filename Length: {record['filename_length']}")
    print(f"Allocated Size: {record['alloc_size']}")
    print(f"Filename: {record['filename']}")
    for attribute in record["attributes"]:
        print(f"\nAttribute Type: {attribute['type']}")
        print(f"Attribute Length: {attribute['length']}")
        print(f"Attribute Offset: {attribute['offset']}")
        print(f"Attribute Data: {attribute['data'].hex()}")
        if attribute['type'] == 0x30: # file name attribute
            for file_record in attribute['data']:
                print(f"\nFile Name: {file_record['filename']}")
                print(f"File Size: {file_record['filesize']}")
                print(f"Created Time: {file_record['created_time']}")
                print(f"Modified Time: {file_record['modified_time']}")
                print(f"MFT Record Number: {file_record['mft_record_num']}")
                print(f"Parent MFT Record Number: {file_record['parent_mft_record_num']}")
                print(f"Is Directory: {file_record['is_directory']}")

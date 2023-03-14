import argparse
import struct

# Define the MFT header structure
MFT_HEADER_FORMAT = "<4sHHHHIHHH16s16sI"
MFT_HEADER_SIZE = struct.calcsize(MFT_HEADER_FORMAT)

# Define the MFT record header structure
MFT_RECORD_HEADER_FORMAT = "<IHHHHIHH"
MFT_RECORD_HEADER_SIZE = struct.calcsize(MFT_RECORD_HEADER_FORMAT)

# Define the MFT attribute header structure
MFT_ATTRIBUTE_HEADER_FORMAT = "<QQIBBH"
MFT_ATTRIBUTE_HEADER_SIZE = struct.calcsize(MFT_ATTRIBUTE_HEADER_FORMAT)

# Define the attribute type constants
ATTR_STANDARD_INFORMATION = 0x10
ATTR_ATTRIBUTE_LIST = 0x20
ATTR_FILENAME = 0x30
ATTR_OBJECT_ID = 0x40
ATTR_SECURITY_DESCRIPTOR = 0x50
ATTR_VOLUME_NAME = 0x60
ATTR_VOLUME_INFORMATION = 0x70
ATTR_DATA = 0x80
ATTR_INDEX_ROOT = 0x90
ATTR_INDEX_ALLOCATION = 0xA0
ATTR_BITMAP = 0xB0
ATTR_REPARSE_POINT = 0xC0
ATTR_EA_INFORMATION = 0xD0
ATTR_EA = 0xE0
ATTR_LOGGED_UTILITY_STREAM = 0x100

# Parse the command-line arguments
parser = argparse.ArgumentParser(description="Analyze an MFT file")
parser.add_argument("input_file", help="the input MFT file")
args = parser.parse_args()

# Open the input file
with open(args.input_file, "rb") as f:

    # Read the MFT header
    mft_header = struct.unpack(MFT_HEADER_FORMAT, f.read(MFT_HEADER_SIZE))

    # Print the MFT header information
    print("Signature: {}".format(mft_header[0].decode("ascii")))
    print("Fixup offset: {}".format(mft_header[1]))
    print("Fixup entries: {}".format(mft_header[2]))
    print("Log sequence number: {}".format(mft_header[3]))
    print("Sequence value: {}".format(mft_header[4]))
    print("Hard link count: {}".format(mft_header[5]))
    print("First attribute offset: {}".format(mft_header[6]))
    print("Flags: {}".format(mft_header[7]))
    print("Used size: {}".format(mft_header[8]))
    print("Allocated size: {}".format(mft_header[9]))
    print("Base file record segment: {}".format(mft_header[10]))
    print("Next attribute ID: {}".format(mft_header[11]))

    # Read the MFT records
    offset = mft_header[6]
    while True:

        # Move to the record offset
        f.seek(offset)

        # Read the record header
        record_header = struct.unpack(MFT_RECORD_HEADER_FORMAT, f.read(MFT_RECORD_HEADER_SIZE))

        # Print the record header information
        print("Record header:")
        print("  Signature: {}".format(hex(record_header[0])))
        print("  Update sequence offset: {}".format(record_header[1]))
        print("  Update sequence count: {}".format(record_header[2]))
        print("  Log sequence number: {}".format(record_header[3]))
        print("  Sequence number: {}".format(record_header[4]))
        print("  Hard link count: {}".format(record_header[5]))
        print("  First attribute offset: {}".format(record_header[6]))
        print("  Flags: {}".format(record_header[7]))

                # Read the record attributes
        attribute_offset = offset + record_header[6]
        while True:

            # Move to the attribute offset
            f.seek(attribute_offset)

            # Read the attribute header
            attribute_header = struct.unpack(MFT_ATTRIBUTE_HEADER_FORMAT, f.read(MFT_ATTRIBUTE_HEADER_SIZE))

            # Print the attribute header information
            print("Attribute header:")
            print("  Type code: {}".format(hex(attribute_header[0])))
            print("  Record length: {}".format(attribute_header[1]))
            print("  Non-resident flag: {}".format(attribute_header[2]))
            print("  Name length: {}".format(attribute_header[3]))
            print("  Name offset: {}".format(attribute_header[4]))
            print("  Flags: {}".format(attribute_header[5]))
            print("  Attribute ID: {}".format(attribute_header[6]))

            # Determine the attribute type
            if attribute_header[0] == ATTR_STANDARD_INFORMATION:
                print("Attribute type: Standard Information")
            elif attribute_header[0] == ATTR_ATTRIBUTE_LIST:
                print("Attribute type: Attribute List")
            elif attribute_header[0] == ATTR_FILENAME:
                print("Attribute type: Filename")
            elif attribute_header[0] == ATTR_OBJECT_ID:
                print("Attribute type: Object ID")
            elif attribute_header[0] == ATTR_SECURITY_DESCRIPTOR:
                print("Attribute type: Security Descriptor")
            elif attribute_header[0] == ATTR_VOLUME_NAME:
                print("Attribute type: Volume Name")
            elif attribute_header[0] == ATTR_VOLUME_INFORMATION:
                print("Attribute type: Volume Information")
            elif attribute_header[0] == ATTR_DATA:
                print("Attribute type: Data")
            elif attribute_header[0] == ATTR_INDEX_ROOT:
                print("Attribute type: Index Root")
            elif attribute_header[0] == ATTR_INDEX_ALLOCATION:
                print("Attribute type: Index Allocation")
            elif attribute_header[0] == ATTR_BITMAP:
                print("Attribute type: Bitmap")
            elif attribute_header[0] == ATTR_REPARSE_POINT:
                print("Attribute type: Reparse Point")
            elif attribute_header[0] == ATTR_EA_INFORMATION:
                print("Attribute type: Extended Attributes Information")
            elif attribute_header[0] == ATTR_EA:
                print("Attribute type: Extended Attributes")
            elif attribute_header[0] == ATTR_LOGGED_UTILITY_STREAM:
                print("Attribute type: Logged Utility Stream")
            else:
                print("Attribute type: Unknown ({})".format(hex(attribute_header[0])))

            # If the attribute is non-resident, read the data runs
            if attribute_header[2] != 0:

                # TODO: Read the data runs

            # Otherwise, read the attribute value
            else:

                # Determine the attribute value length
                value_length = attribute_header[1] - attribute_header[4] - attribute_header[3]

                # Read the attribute value
                attribute_value = f.read(value_length)

                # Print the attribute value information
                print("Attribute value:")
                print("  Length: {}".format(value_length))
                print("  Value: {}".format(attribute_value))

            # If this is the last attribute, break out of the loop
            if attribute_header[1] == 0:
                break

            # Otherwise, move to the next attribute
            attribute_offset += attribute_header[1]

        # If this is the last record, break out of the loop
        if record_header[6] == 0:
            break

                # Otherwise, move to the next record
        offset = record_header[6]

    # Close the file
    f.close()


if __name__ == "__main__":

    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="MFT filename")
    args = parser.parse_args()

    # Analyze the MFT
    analyze_mft(args.filename)


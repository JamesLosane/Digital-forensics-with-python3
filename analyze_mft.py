def analyze_mft(filename):

    # Open the MFT file in binary mode
    with open(filename, "rb") as f:

        # Read the first record header
        offset = 0
        record_header = f.read(48)

        # Loop through the MFT records
        while record_header:

            # Extract record header fields
            signature = record_header[0:4]
            fixup_offset = int.from_bytes(record_header[4:6], byteorder="little")
            fixup_count = int.from_bytes(record_header[6:8], byteorder="little")
            logfile_seq_num = int.from_bytes(record_header[8:16], byteorder="little")
            sequence_num = int.from_bytes(record_header[16:18], byteorder="little")
            link_count = int.from_bytes(record_header[18:20], byteorder="little")
            attr_offset = int.from_bytes(record_header[20:22], byteorder="little")
            flags = int.from_bytes(record_header[22:24], byteorder="little")
            record_size = int.from_bytes(record_header[24:26], byteorder="little")
            filename_length = int.from_bytes(record_header[26:28], byteorder="little")
            alloc_size = int.from_bytes(record_header[40:48], byteorder="little")

            # Extract filename
            filename = f.read(filename_length*2).decode("utf-16le")

            # Read the record attributes
            offset = attr_offset
            while offset < record_size:

                # Read attribute header
                attr_header = f.read(16)
                attr_type = int.from_bytes(attr_header[0:4], byteorder="little")
                attr_length = int.from_bytes(attr_header[4:8], byteorder="little")
                attr_offset = int.from_bytes(attr_header[8:16], byteorder="little")

                # Extract attribute data
                attr_data = f.read(attr_length-24)

                # Print attribute information
                print(f"Attribute Type: {attr_type}")
                print(f"Attribute Length: {attr_length}")
                print(f"Attribute Offset: {attr_offset}")
                print(f"Attribute Data: {attr_data.hex()}")

                # Move to the next attribute
                offset = attr_offset + attr_length

            # Move to the next record
            offset = record_header[6]
            record_header = f.read(48)

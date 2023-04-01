#!/usr/bin/env python3


# Takes a filename, starting and ending offsets in hex or decimal.
# Extract that chunk into a new file

import os, sys

def print_help():
    print('Usage: %s inputfile outputfile firstbye [lastbyte]\n' % sys.argv[0])
    print('Extract/carve out segments of a binary (or any) file into a new file.')
    print('Firstbye and lastbye offsets can be in decimal or hex (prefix with 0x for hex).')
    print('Omit "lastbyte" to copy until it reaches the end of the file.')


def main():
    if len(sys.argv) < 4:
        print_help()
        exit(1)

    # etract data from command-line
    s_infile = sys.argv[1]
    s_outfile = sys.argv[2]
    s_first_byte = sys.argv[3]
    if len(sys.argv) == 5:
        s_last_byte = sys.argv[4]
    else:
        s_last_byte = str(os.stat(s_infile).st_size - 1)
    i_first_byte = int(s_first_byte, 0)
    i_last_byte = int(s_last_byte, 0)
    i_file_size = i_last_byte - i_first_byte + 1
    fiveSpaces = ' ' * 5

    print('Extracting bytes %i to %i (%i bytes total) from %s...' % (i_first_byte, i_last_byte, i_file_size, s_infile))
    print('%s%s' % (fiveSpaces, s_outfile), end='')

    with open(s_infile, 'rb') as f:
        f.seek(i_first_byte)
        remaining_bytes = i_file_size
        with open(s_outfile, 'wb') as ofile:
            while remaining_bytes > 0:
                chunk_size = min(4096, remaining_bytes)
                ofile.write(f.read(chunk_size))
                remaining_bytes -= chunk_size
                print('\r%i%%' % int(100 - ((100 * remaining_bytes) / i_file_size)), end='')

    print('\rWrote to file: %s' % s_outfile)


if __name__ == '__main__':
    main()

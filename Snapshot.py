import os
import hashlib
import argparse

def directory_list(path):
    directory=[]
    for dirpath, _, files in os.walk(path):
        for f in files:
            directory.append(os.path.join(dirpath, f))
    return directory

def generate_hash(path,dir,snapshit="snapshit.txt"):
    with open(snapshit,'w',encoding='utf-8') as output:
        for file in dir:
            hash = hashlib.sha256()
            BLOCK_SIZE = 65536
            with open(file,'rb') as f:
                for byte_block in iter(lambda: f.read(BLOCK_SIZE),b""):
                    hash.update(byte_block)
            output.write(file + "," + hash.hexdigest() + "\n")

def compare_string(string1,string2):
    if string1 == string2:
        #print(f"string {string1} matches {string2}")
        toggle=1
        return toggle

def compare_files(file,file2):
    with open(file, 'r') as string1_file:
        for string1 in string1_file:
            fnamehash1=string1.split(',')
            with open(file2, 'r') as string2_file:
                match=0
                fmatch=0
                for string2 in string2_file:
                    fnamehash2=string2.split(',')
                    toggle=compare_string(fnamehash1[0].strip(),fnamehash2[0].strip())
                    if toggle==1:
                        fmatch=1
                        hash_toggle=compare_string(fnamehash1[1].strip(),fnamehash2[1].strip())
                        if hash_toggle==1:
                            match=1
                        else:
                            nomatch_hash=fnamehash2[1].strip()
                if fmatch==0:
                    print(f"\nNo match for {fnamehash1[0].strip()}\n")
                elif fmatch==1 and match==0:
                    print(f"\n{fnamehash1[0].strip()} has changed..\n Source hash: {fnamehash1[1].strip()}\n Dest hash: {nomatch_hash}\n")
 

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--snapshit", help="specify new snapshit file name", action="store")
    parser.add_argument("-c", "--compare", help="specify file (or files) to compare", action="store_true")
    parser.add_argument("spath", help="Enter path to snapshit")
    parser.add_argument("dpath", help="Enter path to compare snapshit to",nargs="?")
    return parser.parse_args()


def main():
    args=parse_args()
    if args.snapshit:
        snapshit=args.snapshit
    else:
        snapshit="./snapshit.txt"
    if args.compare and not args.snapshit:
        snapshit="./cshit.txt"
    if args.dpath and args.compare:
        compare_files(args.spath,args.dpath)
    elif args.dpath and not args.compare:
        print("You can't specify a 2nd positional argument without -c")
        quit()
    else:
        dir=directory_list(args.spath)
        generate_hash(args.spath,dir,snapshit)
        if args.compare:
            compare_files("./snapshit.txt","./cshit.txt") 
    

if __name__ == "__main__":
    main()

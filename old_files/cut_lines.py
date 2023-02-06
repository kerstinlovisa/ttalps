import argparse
import re

def main(file):
    ifile = open(file,'r')
    ofile = open(file+"cut.txt",'w')
    for line in ifile:
        if re.search('[^\s]',line):
            ofile.write(line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Count occurrences of values")
    parser.add_argument('--file', metavar='path', required=True, dest='file',
                        help="the file whose values to count")
    args = parser.parse_args()
    main(args.file)

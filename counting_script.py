import argparse

def main(file):
    file = open(file,'r')
    d = dict()
    for line in file:
        line = line.split()[0]
        if line in d:
            d[line] = d[line]+1
        else:
            d[line] = 1
    for key in sorted(d.keys()):
        print(str(key)+" : "+str(d[key]))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Count occurrences of values")
    parser.add_argument('--file', metavar='path', required=True, dest='file',
                        help="the file whose values to count")
    args = parser.parse_args()
    main(args.file)

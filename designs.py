#Logo
def printbanner():
    fh = open(r"banner.txt")
    print(fh.read())
    fh.close()

if __name__== 'c':
    printbanner()
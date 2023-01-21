import pdb

import sys
import os

import re
'''
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k

d = dict()
d["/"] = dict()

# iterates through input to create dictionary
while i < len(lines):

    d["/"] = ls_d(d["/"], i, lines)
    

# adds all files and directories to dictionary
def ls_d(d,i,lines):
    while lines[i][0] != $:
        if lines[3:] == dir:
            d[name] = dict
    return d

{
    / : {
        __/__size: 2...
        a: {
            e: {
                i: 584
            }
            f: 29,,,
            g: 2557
            h.lst: 62...
        }
        b.txt: 14848514
        c.dat: 8504156
        d: {
            j: ..
            ...
        }
    }

}




### diectory of size ###


'''
i = 0
def main():
    
    # get input file 
    filepath = sys.argv[1]
    if not os.path.isfile(filepath):
       print("File path {} does not exist. Exiting...".format(filepath))
       sys.exit()

    
    with open(filepath, 'r') as file:
        
        data = file.read() # string
        lines = data.split('\n') # list of strings
        ####### create dictionary ########
        
        fp = []
        d = dict()       
        
        #while i < len(lines): 
        print(f"TOP dict:{d}\ni:{i} line:\"{lines[i]}\"")
        pdb.set_trace() 
        d = ls_dict(d,lines,fp)
        #i += 1
        print(f"~~~~~~~~~~~~~~\nd: {d}")
        print("##############")
        
        
        
        ####### calculate  ########
        dirsize = calc_size(d["/"],[])
        print(dirsize)
        total = 0
        for x in dirsize:
            if x <= 100000:
                total += x
        print(total)
        #pdb.set_trace()
    

def calc_size(d,ds):
    s = 0
    for y, x in d.items():
        if type(x) is dict:
            ds = calc_size(x,ds)
            #if ds[y] <= 100000:
            #print(ds[y])
            s += ds[-1]
        else:
            #if int(x) <= 100000:
            s += int(x)
            #print(ds)
    #print(f"s:{ds}")
    ds.append(s)
    return ds


def ls_dict(d,lines,fp):
    global i
    while i < len(lines):
        if lines[i][:1] != "$":
            print(f"dict:{d}\ni:{i} line:\"{lines[i]}\"")
            if lines[i][:3] == "dir":
                d[lines[i][4:]] = dict()
            else:
                line = lines[i].split(" ")
                d[line[1]] = line[0]
        else:
            print(f"$ dict:{d}\ni:{i} line:\"{lines[i]}\"")    
            if i < len(lines) and lines[i].strip() != "$ cd ..":
                filename = lines[i].strip()[5:]
                fp.append(filename)
                i += 1
                print(f"REC fp:{fp} dir({filename}) dict:{d}\ni:{i} line:\"{lines[i]}\"")
                i += 1
                d[filename] = ls_dict(d[filename],lines,fp)
            else:
                p = fp.pop()
                print(f"RETURN fp:{fp} pop({p}) dict:{d}\ni:{i} line:\"{lines[i]}\"")
                return d
        i += 1
    return d


if __name__ == '__main__':
    main()
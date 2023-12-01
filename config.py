import pdb
import sys
import os

def main():    
    DAY = int(sys.argv[1])
    if len(sys.argv) < 3:
        YEAR = "2023"
    else:
      YEAR = sys.argv[2]   
    filepath = f"{YEAR}/Day{DAY :02d}"
    
    print(f"~~~~~~~~~\n{filepath}\n~~~~~~~~")
    if not os.path.exists(YEAR):
       os.system(f'mkdir {YEAR}')
    if not os.path.exists(filepath):
       os.system(f'mkdir {filepath}')

    with open('cookie.txt','r') as file:
        SESSION = file.read() # string
        cmd_str = f'curl https://adventofcode.com/{YEAR}/day/{DAY}/input --cookie "session={SESSION}" > {filepath}/input.txt'
        print(cmd_str)
        os.system(cmd_str)

if __name__ == '__main__':
    main()


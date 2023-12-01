import pdb
import sys
import os

def main():    
    DAY = sys.argv[1]
    YEAR = sys.argv[2] if len(sys.argv) < 3 else "2023"
    filepath = f"{YEAR}/Day{DAY : 03d}"
    
    print(f"~~~~~~~~~\n{filepath}\n~~~~~~~~")
    if not os.path.exists(YEAR):
       os.system(f'mkdir {YEAR}')
    if not os.path.exists(filepath):
       os.system(f'mkdir {filepath}')

    with open('cookie.txt','r') as file:
        SESSION = file.read() # string
        os.system(f'curl https://adventofcode.com/2018/day/DAY/input --cookie "session={SESSION}" > {filepath}/input.txt')

if __name__ == '__main__':
    main()


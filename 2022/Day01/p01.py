import sys
import os

def main():
   filepath = sys.argv[1]
   if not os.path.isfile(filepath):
       print("File path {} does not exist. Exiting...".format(filepath))
       sys.exit()
  
   max_cals = 0
   sum_cals = 0
   with open(filepath) as fp:
        for line in fp:
            if len(line.strip()) == 0:
                if max_cals < sum_cals:
                    max_cals = sum_cals
                print(f"max: {max_cals} cals: {sum_cals}")
                sum_cals = 0
            else:
                sum_cals += int(line.strip())

            

if __name__ == '__main__':
    main()
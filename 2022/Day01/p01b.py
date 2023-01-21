import sys
import os

def main():
   filepath = sys.argv[1]
   if not os.path.isfile(filepath):
       print("File path {} does not exist. Exiting...".format(filepath))
       sys.exit()
  
   sum_cals = 0
   max_cals = []
   
   with open(filepath) as fp:
        for line in fp:
            if len(line.strip()) == 0:
                if len(max_cals) < 3:
                    max_cals.append(sum_cals)
                elif max_cals[0] < sum_cals:
                    max_cals[0] = sum_cals
                    max_cals.sort()
                print(f"max: {max_cals} cals: {sum_cals}")
                sum_cals = 0
            else:
                sum_cals += int(line.strip())

        print(f"Sum of top 3: {sum(max_cals)}")

 
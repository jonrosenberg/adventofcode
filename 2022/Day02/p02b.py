import sys
import os

def main():
    print("hello world")
    filepath = sys.argv[1]
    if not os.path.isfile(filepath):
       print("File path {} does not exist. Exiting...".format(filepath))
       sys.exit()
    print("hello world")

    game_guide = {
    "A Y" : 4,
    "A Z" : 8,
    "A X" : 3,
    "B X" : 1,
    "B Y" : 5,
    "B Z" : 9,
    "C Z" : 7,
    "C X" : 2,
    "C Y" : 6
    }

    total_score = 0
    '''
    Dictionary

    [A]Rock = 1 [B]Paper = 2 [C]Scissors = 3
    [X]Lose = 0 [Y]Tie = 3 [Z]Win = 6
    New  Old
    AY = AX = 1+3 = 4
    AZ = AY = 2+6 = 8
    AX = AZ = 3+0 = 3
    BX = BX = 1+0 = 1
    BY = BY = 2+3 = 5
    BZ = BZ = 3+6 = 9
    CZ = CX = 1+6 = 7
    CX = CY = 2+0 = 2
    CY = CZ = 3+3 = 6
    '''

    with open(filepath) as fp:
        for line in fp:
            key = line.strip()
            total_score += game_guide[key]
            print(f"key: {key} value: {game_guide[key]} total_score: {total_score}")        
            


        print(f"total score: {total_score}")

if __name__ == '__main__':
    main()
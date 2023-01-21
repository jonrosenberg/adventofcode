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
    "A X" : 4,
    "A Y" : 8,
    "A Z" : 3,
    "B X" : 1,
    "B Y" : 5,
    "B Z" : 9,
    "C X" : 7,
    "C Y" : 2,
    "C Z" : 6
    }

    total_score = 0
    '''
    Dictionary

    [AX]Rock = 1 [BY]Paper = 2 [CZ]Scissors = 3
    Lose = 0 Tie = 3 Win = 6
    AX = 1+3 = 4
    AY = 2+6 = 8
    AZ = 3+0 = 3
    BX = 1+0 = 1
    BY = 2+3 = 5
    BZ = 3+6 = 9
    CX = 1+6 = 7
    CY = 2+0 = 2
    CZ = 3+3 = 6
    '''

    with open(filepath) as fp:
        for line in fp:
            key = line.strip()
            total_score += game_guide[key]
            print(f"key: {key} value: {game_guide[key]} total_score: {total_score}")        
            


        print(f"total score: {total_score}")

if __name__ == '__main__':
    main()
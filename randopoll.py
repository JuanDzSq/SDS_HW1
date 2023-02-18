from argparse import ArgumentParser
from poller import Poller
from subprocess import run

"""Main function that starts the random poll program with a given file name.

This program manipulates a csv file with participant polling information. It will choose a random student from those that
have the lowest polled number, and prompt the user to input if they answered, were correct, were excused or were missing.
If the user inputs the quit command, the program stops and re-writes the new data to the csv file
"""
parser = ArgumentParser(prog = "RandoPoll",
                    description = "What the program does")
parser.add_argument("filename")

args = parser.parse_args()

def main():
    locked = False
    with Poller(args.filename) as poller:
        for participant in poller:
            while True:
                print("%s: (A)nswered (C)orrect (E)xcused (M)issing (Q)uit" % participant)
                command = input().lower()
                if command == "a":
                    poller.attempted()
                    break
                elif command == "c":
                    poller.correct()
                    break
                elif command == "e":
                    poller.excused()
                    break
                elif command == "q":
                    locked = poller.stop()
                    break
                elif command == "m":
                    poller.missing()
                    break
                print("Unknown response")
            if locked:    # This ends the program if the 'q' command is called.
                break
    

if __name__ == "__main__":
    main()
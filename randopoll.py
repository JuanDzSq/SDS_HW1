from argparse import ArgumentParser
from poller import Poller
from subprocess import run

#parser = ArgumentParser(prog = "RandoPoll",
#                    description = "What the program does")
#parser.add_argument("filename")

#args = parser.parse_args()

def main():
    locked = False
    with Poller('participants.csv') as poller:    #args.filename
        for participant in poller:
            while True:
                print("%s: (A)nswered (C)orrect (E)xcused (M)issing (Q)uit" % participant)
                command = input().lower()
                if command == "a":
                    poller.attempted() # participant.attempted() ?
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
            if locked:
                break
    

if __name__ == "__main__":
    main()
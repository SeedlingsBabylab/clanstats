import os
import sys
import subprocess as sp

if __name__ == "__main__":

    clan_files = os.listdir(sys.argv[1])

    for file in clan_files:
        command = ["python", "clanstats.py", os.path.join(sys.argv[1], file), sys.argv[2], str(0)]

        pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10**8)
        pipe.communicate()


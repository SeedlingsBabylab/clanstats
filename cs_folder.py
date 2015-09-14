import os
import sys
import subprocess as sp

if __name__ == "__main__":

    input = sys.argv[1]
    output = sys.argv[2]
    window_size = sys.argv[3]

    clan_files = os.listdir(input)

    for file in clan_files:
        command = ["python", "clanstats.py", os.path.join(sys.argv[1], file), output, str(window_size)]

        pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10**8)
        pipe.communicate()


    aggregate = []

    with open("aggregate_long.csv", "wb") as aggregate_out:
        aggregate_out.write("subject,month,speaker_category,classifier,annotation\n")
        for file in os.listdir(output):
            with open(os.path.join(output, file), "rU") as single_file:
                single_file.readline()
                for line in single_file:
                    aggregate_out.write(line)


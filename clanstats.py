import os
import sys
import csv
import re

male_clan_codes = ["MAN", "MAF"]
female_clan_codes = ["FAN", "FAF"]
child_clan_codes = ["CHN", "CHF", "CXN", "CXF"]
noise_clan_codes = ["NON", "NOF"]
overlap_clan_codes = ["OLN", "OLF"]

clan_codes = {"male": male_clan_codes,
              "female": female_clan_codes,
              "child": child_clan_codes,
              "noise": noise_clan_codes,
              "overlap": overlap_clan_codes
}

male_codes = [
                "FAT",  # father
                "BRO",  # brother
                "GRP",  # grandpa
                "UNC",  # uncle
                "EXM",  # male experimenter
                "MFT",  # mother and father
                "MFV",  # mother, father, and TV/radio/CD/etc...
                "FTY",  # father and toy in unison
                "FTV",  # father and TV/radio/CD/etc...
                "BTY",  # brother and toy in unison
                "BR1",  # brother
                "BR2",  # brother
                "ADM",  # adult male
                "MFR",  # male friend
                "AM1",  # adult male
                "AM2",  # adult male
                "AM3",  # adult male
                "AM4",  # adult male
                "GUN",  # great uncle
                "FTB",  # father and brother in unison
            ]

female_codes = [
                "MOT",  # mother
                "SIS",  # sister
                "GRM",  # grandma
                "GGR",  # great grandma
                "AUN",  # aunt
                "EXF",  # female experimenter
                "MFT",  # mother and father
                "MFV",  # mother, father, and TV/radio/CD/etc...
                "MTV",  # mother and TV/radio/CD
                "MTY",  # mother and toy in unison
                "LFV",  # live female voice
                "MIS",  # mother and sister in unison
                "AF1",  # adult female
                "STY",  # sister and toy in unison
                "GTY",  # grandma and toy in unison
                "AFF",  # adult female friend
                "FFR",  # female friend
                "ADF",  # adult female
                "AD2",  # adult female 2
                "AD3",  # adult female 3
                "LFV",  # live female voice
                "AW1",  # adult female
                "AW2",  # adult female
                "AW3",  # adult female
                "AW4",  # adult female
                "AW5",  # adult female
                "SI1",  # sister 1
                "SI2",  # sister 2
                "MT2",  # other mother
                "MTT",  # moms together in unison

            ]

child_codes = [
                "CHI",  # baby
                "CH1",  # random child
                "BRO",  # brother
                "SIS",  # sister
                "SIB",  # sibling ambiguous
                "CO1",  # cousin
                "CO2",  # cousin 2
                "CO3",  # cousin 3
                "KID",  # friend's child
            ]

male_female_codes = [
                "FTS",  # father and sister together

                    ]

artificial_codes = [
                "TOY",  # toy
                "TVN",  # TV/radio/CD/etc...
                "TVF",  # TV female
                "RAD",  # radio
                "CAR",  # car voice
                "TVS",  # youtube characters

                ]

overlap_codes = [
                "MFT",  # mother father
                "MFV",  # mother father TV/etc...
                "FTB",  # father brother
                "MIS"   # mother sister
]

class ClanFile:

    def __init__(self, path, output_path):
        self.clanfile_path = path
        if os.path.isdir(output_path):
            out_name = os.path.splitext(path)[0]
            out_name = os.path.split(out_name)[1] + "_clanstats.csv"
            self.out_path = os.path.join(self.out_path, out_name)
        else:
            self.out_path = output_path
        self.out_path = output_path
        self.filename = os.path.split(path)[1]
        print "filename: " + self.filename
        self.annotated = False
        self.clan_intervals = []
        self.entries = []

        self.parse_clan()

        self.speaker_match = None   # percent correct speaker codes


    def parse_clan(self):
        print "hello there"
        interval_regx = re.compile("(\d+_\d+)")

        re1 ='(&)'	             # ampersand
        re2 ='(.)'	             # utterance type
        re3 ='(\\|)'	         # first pipe
        re4 ='(.)'	             # object present
        re5 ='(\\|)'	         # second pipe
        re6 ='((?:[a-z][a-z]+))' # speaker code

        entry_regx = re.compile(re1+re2+re3+re4+re5+re6, re.IGNORECASE | re.DOTALL)


        with open(self.clanfile_path, "rU") as file:

            for line in file:
                clan_code = None
                if line.startswith("*"):
                    clan_code = line[1:4]
                    m = entry_regx.search(line)
                    if m:
                        amp          = m.group(1)
                        utt_type     = m.group(2)
                        first_pipe   = m.group(3)
                        present      = m.group(4)
                        second_pipe  = m.group(5)
                        speaker_code = m.group(6)
                        # print "clan code: " + clan_code
                        # print "("+amp+")"+\
                        #       "("+utt_type+")"+\
                        #       "("+first_pipe+")"+\
                        #       "("+present+")"+\
                        #       "("+second_pipe+")"+\
                        #       "("+speaker_code+")"
                        comparison = self.check_code(clan_code, speaker_code)
                        #print "comparison: " + str(comparison)
                        # print
                        interval = interval_regx.search(line).group(1).split("_")
                        self.entries.append((clan_code,
                                             speaker_code,
                                             comparison,
                                             interval[0],
                                             interval[1]))

        print " % correct: " + str(self.calc_stats())


    def check_code(self, clan_code, entry_code):
        if clan_code in clan_codes['male']:
            if entry_code not in male_codes:
                return False
            else:
                return True
        if clan_code in clan_codes['female']:
            if entry_code not in female_codes:
                return False
            else:
                return True
        if clan_code in clan_codes['child']:
            if entry_code not in child_codes:
                return False
            else:
                return True
        if clan_code in clan_codes['overlap']:
            if entry_code not in overlap_codes:
                return False
            else:
                return True
        if clan_code in clan_codes['noise']:    # always return false if clan classified as noise
            return False
        else:
            return False    # base case to check out anomalies

    def calc_stats(self):
        num_true = 0
        num_false = 0

        for entry in self.entries:
            if entry[2] is True:
                num_true += 1
            else:
                num_false += 1

        percent_correct = float(num_true)/len(self.entries)

        return percent_correct

    def export(self):

        with open(self.out_path, "w") as file:
            writer = csv.writer(file)
            writer.writerow(["clan_code", "speaker_code", "matched", "onset", "offset"])
            for entry in self.entries:
                writer.writerow([entry[0],
                                entry[1],
                                entry[2],
                                entry[3],
                                entry[4]])
class ClanDir:

    def __init__(self, path, output_path):
        self.clandir_path = path        # the directory where all the clan files live
        self.out_path = output_path     # this is the directory to put exported csv's in
        self.clan_filepaths = []

        for root, dirs, files in os.walk(os.path.abspath(self.clandir_path)):
            for file in files:
                if file.endswith(".cex"):
                    self.clan_filepaths.append(os.path.join(root, file))

        self.clan_files = []

        for path in self.clan_filepaths:
            out_name = os.path.splitext(path)[0]
            out_name = os.path.split(out_name)[1] + "_clanstats.csv"
            out_filepath = os.path.join(self.out_path, out_name)
            self.clan_files.append(ClanFile(path, out_filepath))

        self.build_clanfiles()
        self.export_csvs()

    def build_clanfiles(self):
        print "hello there person"
        for path in self.clan_filepaths:
            out_name = os.path.splitext(path)[0]
            out_name = os.path.split(out_name)[1] + "_clanstats.csv"
            print out_name
            print "joined put path: " + os.path.join(self.out_path, out_name)
            self.clan_files.append(ClanFile(path, os.path.join(self.out_path, out_name)))

    def export_csvs(self):
        for clan_file in self.clan_files:
            clan_file.export()



def print_usage():
    print "\nUSAGE: \n"
    print "You can run clanstats on a single clan file, or a"
    print "directory containing many clan files. \n"
    print "$ python clanstats.py /path/to/clanfile.cex /path/to/output.csv\n\nor..."
    print "\n$ python clanstats.py /path/to/clanfile-directory/ /path/to/output-directory"


if __name__ == "__main__":

    if len(sys.argv) < 3:
        print_usage()

    clan_file = None
    clan_dir = None

    # handle single files and directories differently

    if sys.argv[1].endswith(".cex"):                # single file
        clan_file = ClanFile(sys.argv[1], sys.argv[2])
    else:                                           # directory
        clan_dir = ClanDir(sys.argv[1], sys.argv[2])



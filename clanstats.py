import os
import sys
import csv
import re

from collections import Counter

from tkMessageBox import showwarning


male_clan_codes = ["MAN", "MAF"]
female_clan_codes = ["FAN", "FAF"]
child_clan_codes = ["CHN", "CHF", "CXN", "CXF"]
noise_clan_codes = ["NON", "NOF"]
overlap_clan_codes = ["OLN", "OLF"]
artificial_clan_codes = ["TVN", "TVF"]

clan_codes = {"male": male_clan_codes,
              "female": female_clan_codes,
              "adult": male_clan_codes +female_clan_codes,
              "child": child_clan_codes,
              "noise": noise_clan_codes,
              "overlap": overlap_clan_codes,
              "artificial": artificial_clan_codes
}

male_codes = [
                "FAT",  # father
                #"BRO",  # brother
                "GRP",  # grandpa
                "UNC",  # uncle
                "EXM",  # male experimenter
                "MFT",  # mother and father
                "MFV",  # mother, father, and TV/radio/CD/etc...
                "FTY",  # father and toy in unison
                "FTV",  # father and TV/radio/CD/etc...
                #"BTY",  # brother and toy in unison
                #"BR1",  # brother
                #"BR2",  # brother
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
                #"SIS",  # sister
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
                #"STY",  # sister and toy in unison
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
                #"SI1",  # sister 1
                #"SI2",  # sister 2
                "MT2",  # other mother
                "MTT",  # moms together in unison

            ]

child_codes = [
                "CHI",  # baby
                "CH1",  # random child
                "BRO",  # brother
                "BR1",
                "BR2",
                "BTY",
                "SIS",  # sister
                "SI1",
                "SI2",
                "SIB",  # sibling ambiguous
                "CO1",  # cousin
                "CO2",  # cousin 2
                "CO3",  # cousin 3
                "KID",  # friend's child
            ]

male_female_codes = [
                "FTS",  # father and sister together

                    ]

adult_codes = male_codes + female_codes

artificial_codes = [
                "TOY",  # toy
                "TVN",  # TV/radio/CD/etc...
                "TVF",  # TV female
                "RAD",  # radio
                "CAR",  # car voice
                "TVS",  # youtube characters
                "ATV"

                ]

overlap_codes = [
                "MFT",  # mother father
                "MFV",  # mother father TV/etc...
                "FTB",  # father brother
                "MIS"   # mother sister
]


all_codes = male_codes + female_codes + male_female_codes +\
            child_codes + artificial_codes + overlap_codes

class ClanFile:

    def __init__(self, path, output_path, window_size):
        self.clanfile_path = path
        self.window_size = window_size
        if os.path.isdir(output_path):
            out_name = os.path.splitext(path)[0]
            out_name = os.path.split(out_name)[1] + "_clanstats.csv"
            self.out_path = os.path.join(output_path, out_name)
        else:
            self.out_path = output_path
        # self.out_path = output_path
        self.filename = os.path.split(path)[1]
        self.annotated = False
        self.clan_intervals = []
        self.entries = []
        self.false_entries = []
        self.windows = []
        self.entry_count = 0
        self.lines = [] # the entire file split line by line

        # counts from annotation
        self.adult_count = 0
        self.child_count = 0
        self.male_count = 0
        self.female_count = 0
        self.artificial_count = 0

        self.incorrect_windows = []
        self.correct_windows = []

        self.correct_adult = []
        self.correct_child = []
        self.correct_male  = []
        self.correct_female = []
        self.correct_artificial = []

        self.incorrect_adult = []
        self.incorrect_child = []
        self.incorrect_male  = []
        self.incorrect_female = []
        self.incorrect_artificial = []


        self.incorrect_adult_dist  = []
        self.incorrect_child_dist  = []
        self.incorrect_male_dist   = []
        self.incorrect_female_dist = []
        self.incorrect_artificial_dist = []

        self.correct_adult_dist  = []
        self.correct_child_dist  = []
        self.correct_male_dist   = []
        self.correct_female_dist = []
        self.correct_artificial_dist = []



        self.interval_regx = re.compile("(\d+_\d+)")

        re1 ='(&)'	             # ampersand
        re2 ='(.)'	             # utterance type
        re3 ='(\\|)'	         # first pipe
        re4 ='(.)'	             # object present
        re5 ='(\\|)'	         # second pipe
        re6 ='((?:[a-z][a-z]+))' # speaker code

        self.entry_regx = re.compile(re1+re2+re3+re4+re5+re6, re.IGNORECASE | re.DOTALL)

        self.parse_clan()
        self.build_windows()

        self.incorrect_adult_dist = self.count_incorrect(self.incorrect_adult)
        self.incorrect_child_dist = self.count_incorrect(self.incorrect_child)
        self.incorrect_female_dist = self.count_incorrect(self.incorrect_female)
        self.incorrect_male_dist = self.count_incorrect(self.incorrect_male)
        self.incorrect_artificial_dist = self.count_incorrect(self.incorrect_artificial)

        self.correct_adult_dist = self.count_correct(self.correct_adult)
        self.correct_child_dist = self.count_correct(self.correct_child)
        self.correct_female_dist = self.count_correct(self.correct_female)
        self.correct_male_dist = self.count_correct(self.correct_male)
        self.correct_artificial_dist = self.count_correct(self.correct_artificial)

        self.speakers = Counter([entry[0][0][1] for entry in self.windows]).most_common()


        print "speakers: {}".format(self.speakers)


        print self.incorrect_adult_dist
        print self.incorrect_child_dist
        print self.incorrect_female_dist
        print self.incorrect_male_dist
        print self.incorrect_artificial_dist

        self.export2()


    def parse_clan(self):
        last_line = ""
        multi_line = ""

        with open(self.clanfile_path, "rU") as file:
            clan_code = None
            entries = None
            interval = [None, None]
            interval_regx_result = None
            for line in file:
                if line.startswith("*"):
                    multi_line = ""
                    clan_code = line[1:4]
                    entries = self.entry_regx.findall(line)
                    #print line
                    interval_regx_result = self.interval_regx.search(line)

                    if interval_regx_result is None:
                        last_line = line
                        continue
                    else:
                        last_line = ""
                        interval = interval_regx_result.group().split("_")

                if line.startswith("\t"):
                    if last_line:
                        line += last_line
                        interval_regx_result = self.interval_regx.search(line)
                        entries = self.entry_regx.findall(line)

                        interval = interval_regx_result.group().split("_")

                if line.startswith("%com"):
                    continue

                if entries:
                    temp = [None] * len(entries)
                    for index, entry in enumerate(entries):
                        amp          = entry[0]
                        utt_type     = entry[1]
                        first_pipe   = entry[2]
                        present      = entry[3]
                        second_pipe  = entry[4]
                        speaker_code = entry[5]
                        #comparison = self.check_code(clan_code, speaker_code)
                        temp[index] = (clan_code,
                                       speaker_code,
                                       interval[0],
                                       interval[1])
                        self.entry_count += 1
                    self.lines.append(temp)
                else:
                    # no words on this line, just use "NA" in place of speaker code
                    self.lines.append([(clan_code,
                                      "NA",
                                      interval[0],
                                      interval[1])])

    def build_windows(self):

        window = [None] * self.window_size

        current = 0
        start = 0
        end = self.window_size + 1

        while current < len(self.lines):
            if current < self.window_size:
                window = self.lines[start:end]

                if self.lines[current][0][1] == "NA":
                    current += 1
                    end += 1
                    continue
                else:
                    self.process_window(self.lines[current], window)
                    current += 1
                    end += 1
                    continue

            elif current + self.window_size == len(self.lines):
                window = self.lines[start:end]

                if self.lines[current][0][1] == "NA":
                    current += 1
                    start += 1
                    continue
                else:
                    self.process_window(self.lines[current], window)
                    current += 1
                    start += 1
                    continue
            else:
                window = self.lines[start:end]

                if self.lines[current][0][1] == "NA":
                    current += 1
                    start += 1
                    end += 1
                    continue
                else:
                    self.process_window(self.lines[current], window)
                    current += 1
                    start += 1
                    end += 1
                    continue

    def process_window(self, current, window):


        self.windows.append((current, window))

        # if the speaker code isn't in the dictionary,
        # then we need to stop the program and add it
        if current[0][1] not in all_codes:
            showwarning("Speaker Code Not in Dictionary", "code:  {}".format(current[0]))
            raise Exception("Speaker code \"{}\" is not in the dictionary. Please add it.")

        if current[0][1] in child_codes:
            child_result = self.analyze_child(current, window)
            self.child_count += 1

            if child_result:
                self.correct_child.append((current, child_result[1], window))
            else:
                self.incorrect_child.append((current, window))

        if current[0][1] in adult_codes:
            adult_result = self.analyze_adult(current, window)
            self.adult_count += 1

            if adult_result:
                self.correct_adult.append((current, adult_result[1], window))
            else:
                self.incorrect_adult.append((current, window))

        if current[0][1] in male_codes:
            male_result = self.analyze_male(current, window)
            self.male_count += 1

            if male_result:
                self.correct_male.append((current, male_result[1], window))
            else:
                self.incorrect_male.append((current, window))

        if current[0][1] in female_codes:
            female_result = self.analyze_female(current, window)
            self.female_count += 1

            if female_result:
                self.correct_female.append((current, female_result[1], window))
            else:
                self.incorrect_female.append((current, window))

        if current[0][1] in artificial_codes:
            artificial_result = self.analyze_artificial(current, window)
            self.artificial_count += 1

            if artificial_result:
                self.correct_artificial.append((current, artificial_result[1], window))
            else:
                self.incorrect_artificial.append((current, window))

        elif current[0][1] in clan_codes["noise"]:
            print "noise comparison"

    def analyze_child(self, curr_entry, window):
        results = [None] * len(window)

        for index, entry in enumerate(window):
            if entry[0][0] in clan_codes["child"]:
                results[index] = True
            else:
                results[index] = False


        if True in results:
            if curr_entry[0][0] in clan_codes["child"]:
                return (True, curr_entry)
            else:
                return (True, window[results.index(True)])
        else:
            return False

    def analyze_adult(self, curr_entry, window):
        results = [None] * len(window)

        for index, entry in enumerate(window):
            if entry[0][0] in clan_codes["adult"]:
                results[index] = True
            else:
                results[index] = False

        if True in results:
            if curr_entry[0][0] in clan_codes["adult"]:
                return (True, curr_entry)
            else:
                return (True, window[results.index(True)])
        else:
            return False

    def analyze_male(self, curr_entry, window):
        results = [None] * len(window)

        for index, entry in enumerate(window):
            if entry[0][0] in clan_codes["male"]:
                results[index] = True
            else:
                results[index] = False

        if True in results:
            if curr_entry[0][0] in clan_codes["male"]:
                return (True, curr_entry)
            else:
                return (True, window[results.index(True)])
        else:
            return False

    def analyze_female(self, curr_entry, window):
        results = [None] * len(window)

        for index, entry in enumerate(window):
            if entry[0][0] in clan_codes["female"]:
                results[index] = True
            else:
                results[index] = False
        if True in results:
            if curr_entry[0][0] in clan_codes["female"]:
                return (True, curr_entry)
            else:
                return (True, window[results.index(True)])
        else:
            return False

    def analyze_artificial(self, curr_entry, window):
        results = [None] * len(window)

        for index, entry in enumerate(window):
            if entry[0][0] in clan_codes["artificial"]:
                results[index] = True
            else:
                results[index] = False

        if True in results:
            if curr_entry[0][0] in clan_codes["artificial"]:
                return (True, curr_entry)
            else:
                return (True, window[results.index(True)])
        else:
            return False

    def count_incorrect(self, incorrect):
        uncounted = []
        for entry in incorrect:
            uncounted.append(entry[0][0][0])
        result = Counter(uncounted)
        return result

    def count_correct(self, correct):
        uncounted = []
        for entry in correct:
            uncounted.append(entry[1][0][0])
        result = Counter(uncounted)
        return result

    def calc_stats(self):
        num_true = 0
        num_false = 0

        # get basic true/false counts
        for entry in self.entries:
            if entry[2] is True:
                num_true += 1
            else:
                num_false += 1

        percent_correct = float(num_true)/self.entry_count

        # load all the incorrect matches into this list
        for entry in self.entries:
            if entry[2] is False:
                self.false_entries.append(entry)

        # count all the *adult* male-female mismatches
        adult_gender_mismatch_count = 0
        adult_gender_mismatch_list = []
        for entry in self.false_entries:
            if entry[0] in clan_codes['male']\
                and entry[1] not in child_codes\
                and entry[1] in female_codes:
                    adult_gender_mismatch_count += 1
                    adult_gender_mismatch_list.append(entry)
            elif entry[0] in clan_codes['female']\
                and entry[1] not in child_codes\
                and entry[1] in male_codes:
                adult_gender_mismatch_count += 1
                adult_gender_mismatch_list.append(entry)

        # print adult_gender_mismatch_count
        # print adult_gender_mismatch_list
        return percent_correct

    def export(self):

        with open(self.out_path, "w") as file:
            writer = csv.writer(file)

            file.write("total_annotations: {}\n\n".format(len(self.windows)))
            file.write("child_count: {}\n".format(self.child_count))
            file.write("adult_count: {}\n".format(self.adult_count))
            file.write("female_count: {}\n".format(self.female_count))
            file.write("male_count: {}\n".format(self.male_count))
            file.write("artificial_count: {}\n\n\n".format(self.artificial_count))

            file.write("Correct child distribution:        {}\n".format(self.correct_child_dist.most_common()))
            file.write("Correct adult distribution:        {}\n".format(self.correct_adult_dist.most_common()))
            file.write("Correct female distribution:       {}\n".format(self.correct_female_dist.most_common()))
            file.write("Correct male distribution:         {}\n".format(self.correct_male_dist.most_common()))
            file.write("Correct artificial distribution:   {}\n\n".format(self.correct_artificial_dist.most_common()))

            file.write("Incorrect child distribution:        {}\n".format(self.incorrect_child_dist.most_common()))
            file.write("Incorrect adult distribution:        {}\n".format(self.incorrect_adult_dist.most_common()))
            file.write("Incorrect female distribution:       {}\n".format(self.incorrect_female_dist.most_common()))
            file.write("Incorrect male distribution:         {}\n".format(self.incorrect_male_dist.most_common()))
            file.write("Incorrect artificial distribution:   {}\n".format(self.incorrect_artificial_dist.most_common()))


    def export2(self):

        with open(self.out_path, "w") as file:
            writer = csv.writer(file)

            file.write("total: {}\n\n".format(len(self.windows)))
            file.write("child: {}\n".format(self.child_count))
            file.write("adult: {}\n".format(self.adult_count))
            file.write("female: {}\n".format(self.female_count))
            file.write("male: {}\n".format(self.male_count))
            file.write("artificial: {}\n\n\n".format(self.artificial_count))


            file.write("speakers: {}\n\n".format(self.speakers))


            file.write("correct_child_distribution:        {}\n".format(self.correct_child_dist.most_common()))
            file.write("correct_adult_distribution:        {}\n".format(self.correct_adult_dist.most_common()))
            file.write("correct_female_distribution:       {}\n".format(self.correct_female_dist.most_common()))
            file.write("correct_male_distribution:         {}\n".format(self.correct_male_dist.most_common()))
            file.write("correct_artificial_distribution:   {}\n\n".format(self.correct_artificial_dist.most_common()))

            file.write("incorrect_child_distribution:        {}\n".format(self.incorrect_child_dist.most_common()))
            file.write("incorrect_adult_distribution:        {}\n".format(self.incorrect_adult_dist.most_common()))
            file.write("incorrect_female_distribution:       {}\n".format(self.incorrect_female_dist.most_common()))
            file.write("incorrect_male_distribution:         {}\n".format(self.incorrect_male_dist.most_common()))
            file.write("incorrect_artificial_distribution:   {}\n".format(self.incorrect_artificial_dist.most_common()))





class ClanDir:
    def __init__(self, path, output_path, window_size):
        self.clandir_path = path        # the directory where all the clan files live
        self.out_path = output_path     # this is the directory to put exported csv's in
        self.window_size = window_size
        self.clan_filepaths = []

        for root, dirs, files in os.walk(os.path.abspath(self.clandir_path)):
            for file in files:
                if file.endswith(".cex"):
                    self.clan_filepaths.append(os.path.join(root, file))

        self.clan_files = []
        self.build_clanfiles()
        self.export_csvs()

    def build_clanfiles(self):
        for path in self.clan_filepaths:
            out_name = os.path.splitext(path)[0]
            out_name = os.path.split(out_name)[1] + "_clanstats.csv"
            self.clan_files.append(ClanFile(path, os.path.join(self.out_path, out_name), self.window_size))

    def export_csvs(self):
        for clan_file in self.clan_files:
            clan_file.export()

def print_usage():
    print "\nUSAGE: \n"
    print "You can run clanstats on a single clan file, or a"
    print "directory containing many clan files. \n"
    print "$ python clanstats.py /path/to/clanfile.cex /path/to/output.csv window_size\n\nor..."
    print "\n$ python clanstats.py /path/to/clanfile-directory/ /path/to/output-directory window_size"

if __name__ == "__main__":

    if len(sys.argv) < 4:
        print_usage()

    clan_file = None
    clan_dir = None

    # handle single files and directories differently

    if sys.argv[1].endswith(".cex"):                # single file
        clan_file = ClanFile(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    else:                                           # directory
        clan_dir = ClanDir(sys.argv[1], sys.argv[2], int(sys.argv[3]))



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
                #"MFV",  # mother, father, and TV/radio/CD/etc...
                #"FTY",  # father and toy in unison
                #"FTV",  # father and TV/radio/CD/etc...
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
                #"FTB",  # father and brother in unison
                "MAN",
                "AUD",
                "LMV",   # live male voice
                "MF2",  # male family friends 2-4
                "MF3",
                "MF4",
                "MF5",
                "UM1",  # unknown male 1
                "UM2"   # unknown male 2
            ]

female_codes = [
                "MOT",  # mother
                #"SIS",  # sister
                "GRM",  # grandma
                "GGR",  # great grandma
                "AUN",  # aunt
                "EXF",  # female experimenter
                #"MFT",  # mother and father
                #"MFV",  # mother, father, and TV/radio/CD/etc...
               # "MTV",  # mother and TV/radio/CD
                #"MTY",  # mother and toy in unison
                "LFV",  # live female voice
                #"MIS",  # mother and sister in unison
                "AF1",  # adult female
                #"STY",  # sister and toy in unison
                #"GTY",  # grandma and toy in unison
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
                #"MTT",  # moms together in unison
                "LVF", # live voice female
                "FF2",  # female family friends 2-5
                "FF3",
                "FF4",
                "FF5",
                "UF1",   # unknown female
                "UF2"

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
                "MCH",   # male child (07_07)
                "COU",   # cousin
                #"STY"   # sister/toy in unison
            ]

male_female_codes = [
                "FTS",  # father and sister together

                    ]


just_adult_codes = [
                "AD1",
                "ADU",
                "ADU2",
                "ADU3",
                "NB1"

]

adult_codes = male_codes + female_codes + just_adult_codes



artificial_codes = [
                "TOY",  # toy
                "TOYS",
                "TVN",  # TV/radio/CD/etc...
                "TVF",  # TV female
                "RAD",  # radio
                "CAR",  # car voice
                "TVS",  # youtube characters
                "ATV",
                "TVM"
                ]

overlap_codes = [
                "MFT",  # mother father
                "MFV",  # mother father TV/etc...
                "FTB",  # father brother
                "MIS",   # mother sister
                "FTY",
                "FTV",
                "GTY",
                "MTT",
                "STY",
                "STV",
                "BTY",
                "MTV",
                "MTY"
]


all_codes = male_codes + female_codes + male_female_codes +\
            child_codes + artificial_codes + overlap_codes + just_adult_codes

class ClanFile:

    def __init__(self, path, output_path, window_size):
        self.clanfile_path = path
        self.window_size = window_size
        if os.path.isdir(output_path):
            out_name = os.path.splitext(path)[0]
            out_name = os.path.split(out_name)[1] + "_clanstats.csv"
            long_out_name = out_name.replace(".csv", "_long.csv")
            self.out_path = os.path.join(output_path, out_name)
            self.long_out_path = os.path.join(output_path, long_out_name)
        else:
            self.out_path = output_path
            self.long_out_path = output_path
        # self.out_path = output_path
        self.filename = os.path.split(path)[1]
        self.subject = self.filename[0:2]
        self.month = self.filename[3:5]
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
        self.overlap_count = 0

        self.incorrect_windows = []
        self.correct_windows = []

        self.correct_adult = []
        self.correct_child = []
        self.correct_male  = []
        self.correct_female = []
        self.correct_artificial = []
        self.correct_overlap = []

        self.incorrect_adult = []
        self.incorrect_child = []
        self.incorrect_male  = []
        self.incorrect_female = []
        self.incorrect_artificial = []
        self.incorrect_overlap = []

        self.incorrect_adult_dist  = []
        self.incorrect_child_dist  = []
        self.incorrect_male_dist   = []
        self.incorrect_female_dist = []
        self.incorrect_artificial_dist = []
        self.incorrect_overlap_dist = []

        self.correct_adult_dist  = []
        self.correct_child_dist  = []
        self.correct_male_dist   = []
        self.correct_female_dist = []
        self.correct_artificial_dist = []
        self.correct_overlap_dist = []

        self.interval_regx = re.compile("(\d+_\d+)")
        self.interval_regx_cha = re.compile("(\025\d+_\d+)")

        re0 = '((?:[a-z][a-z0-9_+]*))'  #the word
        re00 = '(\\s+)'          # space
        re1 ='(&)'	             # ampersand
        re2 ='(.)'	             # utterance type
        re3 ='(\\|)'	         # first pipe
        re4 ='(.)'	             # object present
        re5 ='(\\|)'	         # second pipe
        re6 ='((?:[a-z][a-z0-9_]*))' # speaker code

        self.entry_regx = re.compile(re0+re00+re1+re2+re3+re4+re5+re6, re.IGNORECASE | re.DOTALL)

        re1cha='((?:[a-z][a-z0-9_+]*))' # the word
        re2cha='(\\s+)'	                # whitespace
        re3cha='(&=)'	                # &=
        re4cha='(.)'	                # utterance_type
        re5cha='(_+)'	                # _
        re6cha='(.)'	                # object_present
        re7cha='(_+)'	                # _
        re8cha='((?:[a-z][a-z0-9]*))'   # speaker

        self.entry_regx_cha = re.compile(re1cha+re2cha+re3cha+re4cha+re5cha+re6cha+re7cha+re8cha, re.IGNORECASE | re.DOTALL)

        if self.clanfile_path.endswith(".cex"):
            self.parse_cex()
            self.build_windows()
        if self.clanfile_path.endswith(".cha"):
            self.parse_cha()
            self.build_windows()
        if self.clanfile_path.endswith(".csv"):
            self.parse_csv()


        self.incorrect_adult_dist = self.count_incorrect(self.incorrect_adult)
        self.incorrect_child_dist = self.count_incorrect(self.incorrect_child)
        self.incorrect_female_dist = self.count_incorrect(self.incorrect_female)
        self.incorrect_male_dist = self.count_incorrect(self.incorrect_male)
        self.incorrect_artificial_dist = self.count_incorrect(self.incorrect_artificial)
        self.incorrect_overlap_dist = self.count_incorrect(self.incorrect_overlap)

        self.incorrect_adult_dist2 = self.count_incorrect2(self.incorrect_adult)
        self.incorrect_child_dist2 = self.count_incorrect2(self.incorrect_child)
        self.incorrect_female_dist2 = self.count_incorrect2(self.incorrect_female)
        self.incorrect_male_dist2 = self.count_incorrect2(self.incorrect_male)
        self.incorrect_artificial_dist2 = self.count_incorrect2(self.incorrect_artificial)
        self.incorrect_overlap_dist2 = self.count_incorrect2(self.incorrect_overlap)

        self.correct_adult_dist = self.count_correct(self.correct_adult)
        self.correct_child_dist = self.count_correct(self.correct_child)
        self.correct_female_dist = self.count_correct(self.correct_female)
        self.correct_male_dist = self.count_correct(self.correct_male)
        self.correct_artificial_dist = self.count_correct(self.correct_artificial)
        self.correct_overlap_dist = self.count_correct(self.correct_overlap)

        self.correct_adult_dist2 = self.count_correct2(self.correct_adult)
        self.correct_child_dist2 = self.count_correct2(self.correct_child)
        self.correct_female_dist2 = self.count_correct2(self.correct_female)
        self.correct_male_dist2 = self.count_correct2(self.correct_male)
        self.correct_artificial_dist2 = self.count_correct2(self.correct_artificial)
        self.correct_overlap_dist2 = self.count_correct2(self.correct_overlap)

        self.speakers = Counter([entry[0][0][1] for entry in self.windows]).most_common()


        print "speakers: {}".format(self.speakers)


        print self.incorrect_adult_dist
        print self.incorrect_child_dist
        print self.incorrect_female_dist
        print self.incorrect_male_dist
        print self.incorrect_artificial_dist


        #self.export()
        self.long_export()

    def parse_cex(self):
        last_line = ""
        multi_line = ""

        with open(self.clanfile_path, "rU") as file:
            clan_code = None
            entries = None
            interval = [None, None]
            interval_regx_result = None
            for index, line in enumerate(file):
                #print index
                #print line
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
                        if interval_regx_result is None:
                            last_line = line
                            continue
                        else:
                            last_line = ""
                            entries = self.entry_regx.findall(line)

                        interval = interval_regx_result.group().split("_")

                if line.startswith("%com"):
                    continue

                if entries:
                    temp = [None] * len(entries)
                    for index, entry in enumerate(entries):
                        word         = entry[0]
                        amp          = entry[2]
                        utt_type     = entry[3]
                        first_pipe   = entry[4]
                        present      = entry[5]
                        second_pipe  = entry[6]
                        speaker_code = entry[7]
                        #comparison = self.check_code(clan_code, speaker_code)
                        temp[index] = (clan_code,
                                       speaker_code,
                                       interval[0],
                                       interval[1],
                                       word,
                                       utt_type,
                                       present)
                        self.entry_count += 1
                    self.lines.append(temp)
                else:
                    # no words on this line, just use "NA" in place of speaker code
                    self.lines.append([(clan_code,
                                      "NA",
                                      interval[0],
                                      interval[1])])


    def parse_cha(self):

        clan_code = None

        last_line = ""
        multi_line = ""

        prev_interval = [None, None]
        curr_interval = [None, None]

        with open(self.clanfile_path, "rU") as input:
            for index, line in enumerate(input):

                if line.startswith("%"):
                    continue
                if line.startswith("*"):

                    clan_code = line[1:4]
                    # reset multi_line
                    multi_line = ""
                    interval_reg_result = self.interval_regx_cha.search(line)

                    if interval_reg_result is None:
                        #print "interval regx returned none. clan line: " + str(index)
                        last_line = line
                        multi_line += line
                        continue
                     # rearrange previous and current intervals
                    prev_interval[0] = curr_interval[0]
                    prev_interval[1] = curr_interval[1]

                    # set the new curr_interval
                    interval_str = interval_reg_result.group().replace("\025", "")
                    interval = interval_str.split("_")
                    curr_interval[0] = int(interval[0])
                    curr_interval[1] = int(interval[1])

                    # find correctly formatted entries
                    entries = self.entry_regx_cha.findall(line)


                    if entries:
                        temp = [None] * len(entries)
                        for index, entry in enumerate(entries):
                            word         = entry[0]
                            amp          = entry[2]
                            utt_type     = entry[3]
                            first_pipe   = entry[4]
                            present      = entry[5]
                            second_pipe  = entry[6]
                            speaker_code = entry[7]
                            #comparison = self.check_code(clan_code, speaker_code)
                            temp[index] = (clan_code,
                                           speaker_code,
                                           interval[0],
                                           interval[1],
                                           word,
                                           utt_type,
                                           present)
                            self.entry_count += 1

                        self.lines.append(temp)


                    else:
                        # no words on this line, just use "NA" in place of speaker code
                        self.lines.append([(clan_code,
                                            "NA",
                                            interval[0],
                                            interval[1])])
                    last_line = line

                # intervals spanning more than 1 line start with a tab (\t)
                if line.startswith("\t"):
                    interval_reg_result = self.interval_regx_cha.search(line)

                    if interval_reg_result is None:
                        multi_line += line
                        continue

                    prev_interval[0] = curr_interval[0]
                    prev_interval[1] = curr_interval[1]

                    # set the new curr_interval
                    interval_str = interval_reg_result.group().replace("\025", "")
                    interval = interval_str.split("_")
                    curr_interval[0] = int(interval[0])
                    curr_interval[1] = int(interval[1])

                    entries = self.entry_regx.findall(multi_line + line)


                    if entries:
                        temp = [None] * len(entries)
                        for index, entry in enumerate(entries):
                            word         = entry[0]
                            amp          = entry[2]
                            utt_type     = entry[3]
                            first_pipe   = entry[4]
                            present      = entry[5]
                            second_pipe  = entry[6]
                            speaker_code = entry[7]
                            #comparison = self.check_code(clan_code, speaker_code)
                            temp[index] = (clan_code,
                                           speaker_code,
                                           interval[0],
                                           interval[1],
                                           word,
                                           utt_type,
                                           present)
                            self.entry_count += 1

                        self.lines.append(temp)

                    multi_line = "" # empty the mutiple line buffer

        print "done parsing cha"


    def parse_csv(self):

        with open(self.clanfile_path, "rU") as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                classifier = row[0][1:]
                annotation = row[4]
                onset = row[5].split("_")[0]
                offset = row[5].split("_")[1]
                current = [(classifier,annotation,onset,offset)]
                window = [[(classifier,annotation,onset,offset)]]
                self.process_window(current, window)


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
                self.correct_child.append((current, child_result[1], window, child_result[2]))
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
                self.correct_male.append((current, male_result[1], window, male_result[2]))
            else:
                self.incorrect_male.append((current, window))

        if current[0][1] in female_codes:
            female_result = self.analyze_female(current, window)
            self.female_count += 1

            if female_result:
                self.correct_female.append((current, female_result[1], window, female_result[2]))
            else:
                self.incorrect_female.append((current, window))

        if current[0][1] in artificial_codes:
            artificial_result = self.analyze_artificial(current, window)
            self.artificial_count += 1

            if artificial_result:
                self.correct_artificial.append((current, artificial_result[1], window, artificial_result[2]))
            else:
                self.incorrect_artificial.append((current, window))

        if current[0][1] in overlap_codes:
            overlap_result = self.analyze_overlap(current, window)
            self.overlap_count += 1

            if overlap_result:
                self.correct_overlap.append((current, overlap_result[1], window, overlap_result[2]))
            else:
                self.incorrect_overlap.append((current, window))

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
                return (True, curr_entry, 999)
            else:
                return (True, window[results.index(True)], results.index(True))
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
                return (True, curr_entry, 999)  # 999 means it's the current line (this is a hack)
            else:
                return (True, window[results.index(True)], results.index(True))
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
                return (True, curr_entry, 999)
            else:
                return (True, window[results.index(True)], results.index(True))
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
                return (True, curr_entry, 999)
            else:
                return (True, window[results.index(True)], results.index(True))
        else:
            return False

    def analyze_overlap(self, curr_entry, window):
        results = [None] * len(window)

        for index, entry in enumerate(window):
            if entry[0][0] in clan_codes["overlap"]:
                results[index] = True
            else:
                results[index] = False

        if True in results:
            if curr_entry[0][0] in clan_codes["overlap"]:
                return (True, curr_entry, 999)
            else:
                return (True, window[results.index(True)], results.index(True))
        else:
            return False

    def count_incorrect(self, incorrect):
        uncounted = []
        for entry in incorrect:
            uncounted.append(entry[0][0][0])
        result = Counter(uncounted)
        return result

    def count_incorrect2(self, incorrect):
        uncounted = []
        for entry in incorrect:
            uncounted.append((entry[0][0][0], entry[0][0][1]))
        #result = Counter(uncounted)
        return uncounted

    def count_correct(self, correct):
        uncounted = []
        for entry in correct:
            uncounted.append(entry[1][0][0])
        result = Counter(uncounted)
        return result

    def count_correct2(self, correct):
        uncounted = []
        for entry in correct:
            uncounted.append((entry[1][0][0], entry[1][0][1]))
        #result = Counter(uncounted)
        return uncounted

    def export(self):

        with open(self.out_path, "w") as file:
            writer = csv.writer(file)

            file.write("total:\t{}\n\n".format(len(self.windows)))
            file.write("child:\t{}\n".format(self.child_count))
            file.write("adult:\t{}\n".format(self.adult_count))
            file.write("female:\t{}\n".format(self.female_count))
            file.write("male:\t{}\n".format(self.male_count))
            file.write("artificial:\t{}\n".format(self.artificial_count))
            file.write("overlap:\t{}\n\n\n".format(self.overlap_count))


            file.write("speakers:\t{}\n\n".format(self.speakers))


            file.write("correct_child_distribution:\t{}\n".format(self.correct_child_dist.most_common()))
            file.write("correct_adult_distribution:\t{}\n".format(self.correct_adult_dist.most_common()))
            file.write("correct_female_distribution:\t{}\n".format(self.correct_female_dist.most_common()))
            file.write("correct_male_distribution:\t{}\n".format(self.correct_male_dist.most_common()))
            file.write("correct_artificial_distribution:\t{}\n".format(self.correct_artificial_dist.most_common()))
            file.write("correct_overlap_distribution:\t{}\n\n".format(self.correct_overlap_dist.most_common()))

            file.write("incorrect_child_distribution:\t{}\n".format(self.incorrect_child_dist.most_common()))
            file.write("incorrect_adult_distribution:\t{}\n".format(self.incorrect_adult_dist.most_common()))
            file.write("incorrect_female_distribution:\t{}\n".format(self.incorrect_female_dist.most_common()))
            file.write("incorrect_male_distribution:\t{}\n".format(self.incorrect_male_dist.most_common()))
            file.write("incorrect_artificial_distribution:\t{}\n".format(self.incorrect_artificial_dist.most_common()))
            file.write("incorrect_overlap_distribution:\t{}\n".format(self.incorrect_overlap_dist.most_common()))

    def long_export(self):
        with open(self.long_out_path, "w") as file:
            writer = csv.writer(file)
            writer.writerow(["subject",
                             "month",
                             "speaker_category",
                             "timestamp",
                             "word",
                             "utterance_type",
                             "object_present",
                             "speaker_win",
                             "lena_win-2",
                             "lena_win-1",
                             "lena_win-0",
                             "lena_win+1",
                             "lena_win+2",
                             "win_match",
                             "timestamp_match"])

            #07_06 correct_male index 13 shows what's up
            # timestamp, word, utt_type, obj_present, speaker_win, lena_win1, lena_win1, win_match, timestamp_match

            for element in self.correct_male:
                window = None
                temp_window = element[2]
                correct_index = '0'
                if element[3] == 999:
                    correct_index = '0'
                else:
                    if element[3] == 0:
                        correct_index = '-2'
                    if element[3] == 1:
                        correct_index = '-1'
                    if element[3] == 2:
                        correct_index = '0'
                    if element[3] == 3:
                        correct_index = '+1'
                    if element[3] == 4:
                        correct_index = '+2'

                if len(temp_window) == 5:
                    window = temp_window

                if len(temp_window) == 3:
                    window = [[('NA', 'NA', 'NA', 'NA')],
                              temp_window[0],
                              temp_window[1],
                              temp_window[2],
                              [('NA', 'NA', 'NA', 'NA')]]

                if len(temp_window) == 1:
                    window = [[('NA', 'NA', 'NA', 'NA')],
                              [('NA', 'NA', 'NA', 'NA')],
                              temp_window[0],
                              [('NA', 'NA', 'NA', 'NA')],
                              [('NA', 'NA', 'NA', 'NA')]]


                writer.writerow([self.subject,
                                 self.month,
                                 "male_correct",
                                 element[0][0][2]+"_"+element[0][0][3],   # timestamp
                                 element[0][0][4],                        # word
                                 element[0][0][5],                        # utt_type
                                 element[0][0][6],                        # obj_present
                                 element[0][0][1],                        # speaker_win
                                 window[0][0][0],                         # -2 lena code
                                 window[1][0][0],                         # -1 lena code
                                 element[0][0][0],                        #  0 lena code
                                 window[3][0][0],                         # +1 lena code
                                 window[4][0][0],                         # +2 lena code
                                 correct_index,                           # index of correct match (in window)
                                 element[1][0][2]+"_"+element[1][0][3]])  # timestamp for match

            for element in self.incorrect_male:
                window = None
                temp_window = element[1]
                correct_index = '0'

                if len(temp_window) == 5:
                    window = temp_window

                if len(temp_window) == 3:
                    window = [[('NA', 'NA', 'NA', 'NA')],
                              temp_window[0],
                              temp_window[1],
                              temp_window[2],
                              [('NA', 'NA', 'NA', 'NA')]]

                if len(temp_window) == 1:
                    window = [[('NA', 'NA', 'NA', 'NA')],
                              [('NA', 'NA', 'NA', 'NA')],
                              temp_window[0],
                              [('NA', 'NA', 'NA', 'NA')],
                              [('NA', 'NA', 'NA', 'NA')]]


                writer.writerow([self.subject,
                                 self.month,
                                 "male_incorrect",
                                 element[0][0][2]+"_"+element[0][0][3],   # timestamp
                                 element[0][0][4],                        # word
                                 element[0][0][5],                        # utt_type
                                 element[0][0][6],                        # obj_present
                                 element[0][0][1],                        # speaker_win
                                 window[0][0][0],                         # -2 lena code
                                 window[1][0][0],                         # -1 lena code
                                 element[0][0][0],                        #  0 lena code
                                 window[3][0][0],                         # +1 lena code
                                 window[4][0][0],                         # +2 lena code
                                 '0',                                     # index of correct match (in window)
                                 element[0][0][2]+"_"+element[0][0][3]])  # timestamp for match

            for element in self.correct_female:
                window = None
                temp_window = element[2]
                correct_index = '0'
                if element[3] == 999:
                    correct_index = '0'
                else:
                    if element[3] == 0:
                        correct_index = '-2'
                    if element[3] == 1:
                        correct_index = '-1'
                    if element[3] == 2:
                        correct_index = '0'
                    if element[3] == 3:
                        correct_index = '+1'
                    if element[3] == 4:
                        correct_index = '+2'

                if len(temp_window) == 5:
                    window = temp_window

                if len(temp_window) == 3:
                    window = [[('NA', 'NA', 'NA', 'NA')],
                              temp_window[0],
                              temp_window[1],
                              temp_window[2],
                              [('NA', 'NA', 'NA', 'NA')]]

                if len(temp_window) == 1:
                    window = [[('NA', 'NA', 'NA', 'NA')],
                              [('NA', 'NA', 'NA', 'NA')],
                              temp_window[0],
                              [('NA', 'NA', 'NA', 'NA')],
                              [('NA', 'NA', 'NA', 'NA')]]


                writer.writerow([self.subject,
                                 self.month,
                                 "female_correct",
                                 element[0][0][2]+"_"+element[0][0][3],   # timestamp
                                 element[0][0][4],                        # word
                                 element[0][0][5],                        # utt_type
                                 element[0][0][6],                        # obj_present
                                 element[0][0][1],                        # speaker_win
                                 window[0][0][0],                         # -2 lena code
                                 window[1][0][0],                         # -1 lena code
                                 element[0][0][0],                        #  0 lena code
                                 window[3][0][0],                         # +1 lena code
                                 window[4][0][0],                         # +2 lena code
                                 correct_index,                           # index of correct match (in window)
                                 element[1][0][2]+"_"+element[1][0][3]])  # timestamp for match

            for element in self.incorrect_female:
                window = None
                temp_window = element[1]
                correct_index = '0'

                if len(temp_window) == 5:
                    window = temp_window

                if len(temp_window) == 3:
                    window = [[('NA', 'NA', 'NA', 'NA')],
                              temp_window[0],
                              temp_window[1],
                              temp_window[2],
                              [('NA', 'NA', 'NA', 'NA')]]

                if len(temp_window) == 1:
                    window = [[('NA', 'NA', 'NA', 'NA')],
                              [('NA', 'NA', 'NA', 'NA')],
                              temp_window[0],
                              [('NA', 'NA', 'NA', 'NA')],
                              [('NA', 'NA', 'NA', 'NA')]]


                writer.writerow([self.subject,
                                 self.month,
                                 "female_incorrect",
                                 element[0][0][2]+"_"+element[0][0][3],   # timestamp
                                 element[0][0][4],                        # word
                                 element[0][0][5],                        # utt_type
                                 element[0][0][6],                        # obj_present
                                 element[0][0][1],                        # speaker_win
                                 window[0][0][0],                         # -2 lena code
                                 window[1][0][0],                         # -1 lena code
                                 element[0][0][0],                        #  0 lena code
                                 window[3][0][0],                         # +1 lena code
                                 window[4][0][0],                         # +2 lena code
                                 '0',                                     # index of correct match (in window)
                                 element[0][0][2]+"_"+element[0][0][3]])  # timestamp for match

            for element in self.correct_child:
                window = None
                temp_window = element[2]
                correct_index = '0'
                if element[3] == 999:
                    correct_index = '0'
                else:
                    if element[3] == 0:
                        correct_index = '-2'
                    if element[3] == 1:
                        correct_index = '-1'
                    if element[3] == 2:
                        correct_index = '0'
                    if element[3] == 3:
                        correct_index = '+1'
                    if element[3] == 4:
                        correct_index = '+2'

                if len(temp_window) == 5:
                    window = temp_window

                if len(temp_window) == 3:
                    window = [[('NA', 'NA', 'NA', 'NA')],
                              temp_window[0],
                              temp_window[1],
                              temp_window[2],
                              [('NA', 'NA', 'NA', 'NA')]]

                if len(temp_window) == 1:
                    window = [[('NA', 'NA', 'NA', 'NA')],
                              [('NA', 'NA', 'NA', 'NA')],
                              temp_window[0],
                              [('NA', 'NA', 'NA', 'NA')],
                              [('NA', 'NA', 'NA', 'NA')]]


                writer.writerow([self.subject,
                                 self.month,
                                 "child_correct",
                                 element[0][0][2]+"_"+element[0][0][3],   # timestamp
                                 element[0][0][4],                        # word
                                 element[0][0][5],                        # utt_type
                                 element[0][0][6],                        # obj_present
                                 element[0][0][1],                        # speaker_win
                                 window[0][0][0],                         # -2 lena code
                                 window[1][0][0],                         # -1 lena code
                                 element[0][0][0],                        #  0 lena code
                                 window[3][0][0],                         # +1 lena code
                                 window[4][0][0],                         # +2 lena code
                                 correct_index,                           # index of correct match (in window)
                                 element[1][0][2]+"_"+element[1][0][3]])  # timestamp for match

            for element in self.incorrect_child:
                window = None
                temp_window = element[1]
                correct_index = '0'

                if len(temp_window) == 5:
                    window = temp_window

                if len(temp_window) == 3:
                    window = [[('NA', 'NA', 'NA', 'NA')],
                              temp_window[0],
                              temp_window[1],
                              temp_window[2],
                              [('NA', 'NA', 'NA', 'NA')]]

                if len(temp_window) == 1:
                    window = [[('NA', 'NA', 'NA', 'NA')],
                              [('NA', 'NA', 'NA', 'NA')],
                              temp_window[0],
                              [('NA', 'NA', 'NA', 'NA')],
                              [('NA', 'NA', 'NA', 'NA')]]


                writer.writerow([self.subject,
                                 self.month,
                                 "child_incorrect",
                                 element[0][0][2]+"_"+element[0][0][3],   # timestamp
                                 element[0][0][4],                        # word
                                 element[0][0][5],                        # utt_type
                                 element[0][0][6],                        # obj_present
                                 element[0][0][1],                        # speaker_win
                                 window[0][0][0],                         # -2 lena code
                                 window[1][0][0],                         # -1 lena code
                                 element[0][0][0],                        #  0 lena code
                                 window[3][0][0],                         # +1 lena code
                                 window[4][0][0],                         # +2 lena code
                                 '0',                                     # index of correct match (in window)
                                 element[0][0][2]+"_"+element[0][0][3]])  # timestamp for match

            for element in self.correct_artificial:
                window = None
                temp_window = element[2]
                correct_index = '0'
                if element[3] == 999:
                    correct_index = '0'
                else:
                    if element[3] == 0:
                        correct_index = '-2'
                    if element[3] == 1:
                        correct_index = '-1'
                    if element[3] == 2:
                        correct_index = '0'
                    if element[3] == 3:
                        correct_index = '+1'
                    if element[3] == 4:
                        correct_index = '+2'

                if len(temp_window) == 5:
                    window = temp_window

                if len(temp_window) == 3:
                    window = [[('NA', 'NA', 'NA', 'NA')],
                              temp_window[0],
                              temp_window[1],
                              temp_window[2],
                              [('NA', 'NA', 'NA', 'NA')]]

                if len(temp_window) == 1:
                    window = [[('NA', 'NA', 'NA', 'NA')],
                              [('NA', 'NA', 'NA', 'NA')],
                              temp_window[0],
                              [('NA', 'NA', 'NA', 'NA')],
                              [('NA', 'NA', 'NA', 'NA')]]


                writer.writerow([self.subject,
                                 self.month,
                                 "artificial_correct",
                                 element[0][0][2]+"_"+element[0][0][3],   # timestamp
                                 element[0][0][4],                        # word
                                 element[0][0][5],                        # utt_type
                                 element[0][0][6],                        # obj_present
                                 element[0][0][1],                        # speaker_win
                                 window[0][0][0],                         # -2 lena code
                                 window[1][0][0],                         # -1 lena code
                                 element[0][0][0],                        #  0 lena code
                                 window[3][0][0],                         # +1 lena code
                                 window[4][0][0],                         # +2 lena code
                                 correct_index,                           # index of correct match (in window)
                                 element[1][0][2]+"_"+element[1][0][3]])  # timestamp for match

            for element in self.incorrect_artificial:
                window = None
                temp_window = element[1]
                correct_index = '0'

                if len(temp_window) == 5:
                    window = temp_window

                if len(temp_window) == 3:
                    window = [[('NA', 'NA', 'NA', 'NA')],
                              temp_window[0],
                              temp_window[1],
                              temp_window[2],
                              [('NA', 'NA', 'NA', 'NA')]]

                if len(temp_window) == 1:
                    window = [[('NA', 'NA', 'NA', 'NA')],
                              [('NA', 'NA', 'NA', 'NA')],
                              temp_window[0],
                              [('NA', 'NA', 'NA', 'NA')],
                              [('NA', 'NA', 'NA', 'NA')]]


                writer.writerow([self.subject,
                                 self.month,
                                 "artificial_incorrect",
                                 element[0][0][2]+"_"+element[0][0][3],   # timestamp
                                 element[0][0][4],                        # word
                                 element[0][0][5],                        # utt_type
                                 element[0][0][6],                        # obj_present
                                 element[0][0][1],                        # speaker_win
                                 window[0][0][0],                         # -2 lena code
                                 window[1][0][0],                         # -1 lena code
                                 element[0][0][0],                        #  0 lena code
                                 window[3][0][0],                         # +1 lena code
                                 window[4][0][0],                         # +2 lena code
                                 '0',                                     # index of correct match (in window)
                                 element[0][0][2]+"_"+element[0][0][3]])  # timestamp for match

            for element in self.correct_overlap:
                window = None
                temp_window = element[2]
                correct_index = '0'
                if element[3] == 999:
                    correct_index = '0'
                else:
                    if element[3] == 0:
                        correct_index = '-2'
                    if element[3] == 1:
                        correct_index = '-1'
                    if element[3] == 2:
                        correct_index = '0'
                    if element[3] == 3:
                        correct_index = '+1'
                    if element[3] == 4:
                        correct_index = '+2'

                if len(temp_window) == 5:
                    window = temp_window

                if len(temp_window) == 3:
                    window = [[('NA', 'NA', 'NA', 'NA')],
                              temp_window[0],
                              temp_window[1],
                              temp_window[2],
                              [('NA', 'NA', 'NA', 'NA')]]

                if len(temp_window) == 1:
                    window = [[('NA', 'NA', 'NA', 'NA')],
                              [('NA', 'NA', 'NA', 'NA')],
                              temp_window[0],
                              [('NA', 'NA', 'NA', 'NA')],
                              [('NA', 'NA', 'NA', 'NA')]]


                writer.writerow([self.subject,
                                 self.month,
                                 "overlap_correct",
                                 element[0][0][2]+"_"+element[0][0][3],   # timestamp
                                 element[0][0][4],                        # word
                                 element[0][0][5],                        # utt_type
                                 element[0][0][6],                        # obj_present
                                 element[0][0][1],                        # speaker_win
                                 window[0][0][0],                         # -2 lena code
                                 window[1][0][0],                         # -1 lena code
                                 element[0][0][0],                        #  0 lena code
                                 window[3][0][0],                         # +1 lena code
                                 window[4][0][0],                         # +2 lena code
                                 correct_index,                           # index of correct match (in window)
                                 element[1][0][2]+"_"+element[1][0][3]])  # timestamp for match

            for element in self.incorrect_overlap:
                window = None
                temp_window = element[1]
                correct_index = '0'

                if len(temp_window) == 5:
                    window = temp_window

                if len(temp_window) == 3:
                    window = [[('NA', 'NA', 'NA', 'NA')],
                              temp_window[0],
                              temp_window[1],
                              temp_window[2],
                              [('NA', 'NA', 'NA', 'NA')]]

                if len(temp_window) == 1:
                    window = [[('NA', 'NA', 'NA', 'NA')],
                              [('NA', 'NA', 'NA', 'NA')],
                              temp_window[0],
                              [('NA', 'NA', 'NA', 'NA')],
                              [('NA', 'NA', 'NA', 'NA')]]


                writer.writerow([self.subject,
                                 self.month,
                                 "overlap_incorrect",
                                 element[0][0][2]+"_"+element[0][0][3],   # timestamp
                                 element[0][0][4],                        # word
                                 element[0][0][5],                        # utt_type
                                 element[0][0][6],                        # obj_present
                                 element[0][0][1],                        # speaker_win
                                 window[0][0][0],                         # -2 lena code
                                 window[1][0][0],                         # -1 lena code
                                 element[0][0][0],                        #  0 lena code
                                 window[3][0][0],                         # +1 lena code
                                 window[4][0][0],                         # +2 lena code
                                 '0',                                     # index of correct match (in window)
                                 element[0][0][2]+"_"+element[0][0][3]])  # timestamp for match
            # for element in self.correct_male_dist2:
            #     writer.writerow([self.subject, self.month, "male_correct", element[0], element[1]])
            # for element in self.incorrect_male_dist2:
            #     writer.writerow([self.subject, self.month, "male_incorrect", element[0], element[1]])
            #
            #
            # for element in self.correct_female_dist2:
            #     writer.writerow([self.subject, self.month, "female_correct", element[0], element[1]])
            # for element in self.incorrect_female_dist2:
            #     writer.writerow([self.subject, self.month, "female_incorrect", element[0], element[1]])
            #
            #
            # for element in self.correct_child_dist2:
            #     writer.writerow([self.subject, self.month, "child_correct", element[0], element[1]])
            # for element in self.incorrect_child_dist2:
            #     writer.writerow([self.subject, self.month, "child_incorrect", element[0], element[1]])
            #
            #
            # for element in self.correct_artificial_dist2:
            #     writer.writerow([self.subject, self.month, "artificial_correct", element[0], element[1]])
            # for element in self.incorrect_artificial_dist2:
            #     writer.writerow([self.subject, self.month, "artificial_incorrect", element[0], element[1]])
            #
            #
            # for element in self.correct_overlap_dist2:
            #     writer.writerow([self.subject, self.month, "overlap_correct", element[0], element[1]])
            # for element in self.incorrect_overlap_dist2:
            #     writer.writerow([self.subject, self.month, "overlap_incorrect", element[0], element[1]])

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
    print "You can run clanstats on a single clan file or on csv files produced by parse_clan\n"
    print "When running on csv files, the window size must be 0"
    print "$ python clanstats.py /path/to/clanfile.cex /path/to/output.csv window_size\n\n"


if __name__ == "__main__":

    if len(sys.argv) < 4:
        print_usage()

    clan_file = None
    clan_dir = None

    input = sys.argv[1]
    # handle single files and directories differently

    if input.endswith(".cex") or input.endswith(".cha"):
        clan_file = ClanFile(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    elif sys.argv[1].endswith(".csv"):
        clan_file = ClanFile(sys.argv[1], sys.argv[2], 0)
    # else:                                           # directory
    #     clan_dir = ClanDir(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    #
    #

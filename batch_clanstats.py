import os
import sys
import operator

import clanstats

class BatchClanstats:

    def __init__(self, input_path, output_path, conf_table_output):
        self.path = input_path
        self.output = output_path
        self.conf_table_output = conf_table_output
        self.files = os.listdir(self.path)
        print self.files
        self.stats = {}

        self.aggregate = None

        for file in self.files:
            self.parse(file)

        self.aggregate_files()

        self.export()
        self.export_conf_table()
    def parse(self, clanstat_file):
        """
        Parses a clanstats output file and stores the values in
        the self.stats dictionary keyed by subject_month (e.g. "01_06")

        :param clanstat_file: the clanstats output file
        :return:
        """
        file_id = clanstat_file[0:5]

        total = None
        child = None
        adult = None
        female = None
        male = None
        artificial = None
        overlap = None
        speakers = None
        corr_child = None
        corr_adult = None
        corr_female = None
        corr_male = None
        corr_artificial = None
        corr_overlap = None
        incorr_child = None
        incorr_adult = None
        incorr_female = None
        incorr_male = None
        incorr_artificial = None
        incorr_overlap = None

        with open(os.path.join(self.path, clanstat_file), "rU") as file:

            for line in file:
                split_line = line.strip().split("\t")

                # if nothing on the line, continue
                if not split_line:
                    continue

                if split_line[0] == "total:":
                    total = int(split_line[1])
                    continue
                if split_line[0] == "child:":
                    child = int(split_line[1])
                    continue
                if split_line[0] == "adult:":
                    adult = int(split_line[1])
                    continue
                if split_line[0] == "female:":
                    female = int(split_line[1])
                    continue
                if split_line[0] == "male:":
                    male = int(split_line[1])
                    continue
                if split_line[0] == "artificial:":
                    artificial = int(split_line[1])
                    continue
                if split_line[0] == "overlap:":
                    overlap = int(split_line[1])
                    continue

                if split_line[0] == "speakers:":
                    speakers = eval(split_line[1])
                    continue

                if split_line[0] == "correct_child_distribution:":
                    corr_child = eval(split_line[1])
                    continue
                if split_line[0] == "correct_adult_distribution:":
                    corr_adult = eval(split_line[1])
                    continue
                if split_line[0] == "correct_female_distribution:":
                    corr_female = eval(split_line[1])
                    continue
                if split_line[0] == "correct_male_distribution:":
                    corr_male = eval(split_line[1])
                    continue
                if split_line[0] == "correct_artificial_distribution:":
                    corr_artificial = eval(split_line[1])
                    continue
                if split_line[0] == "correct_overlap_distribution:":
                    corr_overlap = eval(split_line[1])
                    continue


                if split_line[0] == "incorrect_child_distribution:":
                    incorr_child = eval(split_line[1])
                    continue
                if split_line[0] == "incorrect_adult_distribution:":
                    incorr_adult = eval(split_line[1])
                    continue
                if split_line[0] == "incorrect_female_distribution:":
                    incorr_female = eval(split_line[1])
                    continue
                if split_line[0] == "incorrect_male_distribution:":
                    incorr_male = eval(split_line[1])
                    continue
                if split_line[0] == "incorrect_artificial_distribution:":
                    incorr_artificial = eval(split_line[1])
                    continue
                if split_line[0] == "incorrect_overlap_distribution:":
                    incorr_overlap = eval(split_line[1])
                    continue

        self.stats[file_id] = Clanstats(total, child, adult, female,
                                        male, artificial,overlap, speakers, corr_child,
                                        corr_adult, corr_female, corr_male, corr_artificial,corr_overlap,
                                        incorr_child, incorr_adult, incorr_female, incorr_male,
                                        incorr_artificial, incorr_overlap)

    def aggregate_files(self):

        self.aggregate = Clanstats()


        for key, entry in self.stats.iteritems():
            self.aggregate.total += entry.total
            self.aggregate.child += entry.child
            self.aggregate.adult += entry.adult
            self.aggregate.male += entry.male
            self.aggregate.female += entry.female
            self.aggregate.artificial += entry.artificial
            self.aggregate.overlap += entry.overlap

            for speaker in entry.speakers:
                if speaker[0] in [aggr_speaker[0] for aggr_speaker in self.aggregate.speakers]:
                    index = [aggr_speaker[0] for aggr_speaker in self.aggregate.speakers].index(speaker[0])
                    self.aggregate.speakers[index][1] += speaker[1]
                else:
                    self.aggregate.speakers.append(list(speaker))


            # self.aggregate all the correct distributions
            for corr_child in entry.corr_child:
                if corr_child[0] in [aggr_corr_child[0] for aggr_corr_child in self.aggregate.corr_child]:
                    index = [aggr_corr_child[0] for aggr_corr_child in self.aggregate.corr_child].index(corr_child[0])
                    self.aggregate.corr_child[index][1] += corr_child[1]
                else:

                    self.aggregate.corr_child.append(list(corr_child))

            for corr_adult in entry.corr_adult:
                if corr_adult[0] in [aggr_corr_adult[0] for aggr_corr_adult in self.aggregate.corr_adult]:
                    index = [aggr_corr_adult[0] for aggr_corr_adult in self.aggregate.corr_adult].index(corr_adult[0])
                    self.aggregate.corr_adult[index][1] += corr_adult[1]
                else:
                    self.aggregate.corr_adult.append(list(corr_adult))

            for corr_female in entry.corr_female:
                if corr_female[0] in [aggr_corr_female[0] for aggr_corr_female in self.aggregate.corr_female]:
                    index = [aggr_corr_female[0] for aggr_corr_female in self.aggregate.corr_female].index(corr_female[0])
                    self.aggregate.corr_female[index][1] += corr_female[1]
                else:
                    self.aggregate.corr_female.append(list(corr_female))

            for corr_male in entry.corr_male:
                if corr_male[0] in [aggr_corr_male[0] for aggr_corr_male in self.aggregate.corr_male]:
                    index = [aggr_corr_male[0] for aggr_corr_male in self.aggregate.corr_male].index(corr_male[0])
                    self.aggregate.corr_male[index][1] += corr_male[1]
                else:
                    self.aggregate.corr_male.append(list(corr_male))

            for corr_artificial in entry.corr_artificial:
                if corr_artificial[0] in [aggr_corr_artificial[0] for aggr_corr_artificial in self.aggregate.corr_artificial]:
                    index = [aggr_corr_artificial[0] for aggr_corr_artificial in self.aggregate.corr_artificial].index(corr_artificial[0])
                    self.aggregate.corr_artificial[index][1] += corr_artificial[1]
                else:
                    self.aggregate.corr_artificial.append(list(corr_artificial))

            for corr_overlap in entry.corr_overlap:
                if corr_overlap[0] in [aggr_corr_overlap[0] for aggr_corr_overlap in self.aggregate.corr_overlap]:
                    index = [aggr_corr_overlap[0] for aggr_corr_overlap in self.aggregate.corr_overlap].index(corr_overlap[0])
                    self.aggregate.corr_overlap[index][1] += corr_overlap[1]
                else:
                    self.aggregate.corr_overlap.append(list(corr_overlap))

            # self.aggregate all the incorrect distributions
            for incorr_child in entry.incorr_child:
                if incorr_child[0] in [aggr_incorr_child[0] for aggr_incorr_child in self.aggregate.incorr_child]:
                    index = [aggr_incorr_child[0] for aggr_incorr_child in self.aggregate.incorr_child].index(incorr_child[0])
                    self.aggregate.incorr_child[index][1] += incorr_child[1]
                else:

                    self.aggregate.incorr_child.append(list(incorr_child))

            for incorr_adult in entry.incorr_adult:
                if incorr_adult[0] in [aggr_incorr_adult[0] for aggr_incorr_adult in self.aggregate.incorr_adult]:
                    index = [aggr_incorr_adult[0] for aggr_incorr_adult in self.aggregate.incorr_adult].index(incorr_adult[0])
                    self.aggregate.incorr_adult[index][1] += incorr_adult[1]
                else:
                    self.aggregate.incorr_adult.append(list(incorr_adult))

            for incorr_female in entry.incorr_female:
                if incorr_female[0] in [aggr_incorr_female[0] for aggr_incorr_female in self.aggregate.incorr_female]:
                    index = [aggr_incorr_female[0] for aggr_incorr_female in self.aggregate.incorr_female].index(incorr_female[0])
                    self.aggregate.incorr_female[index][1] += incorr_female[1]
                else:
                    self.aggregate.incorr_female.append(list(incorr_female))

            for incorr_male in entry.incorr_male:
                if incorr_male[0] in [aggr_incorr_male[0] for aggr_incorr_male in self.aggregate.incorr_male]:
                    index = [aggr_incorr_male[0] for aggr_incorr_male in self.aggregate.incorr_male].index(incorr_male[0])
                    self.aggregate.incorr_male[index][1] += incorr_male[1]
                else:
                    self.aggregate.incorr_male.append(list(incorr_male))

            for incorr_artificial in entry.incorr_artificial:
                if incorr_artificial[0] in [aggr_incorr_artificial[0] for aggr_incorr_artificial in self.aggregate.incorr_artificial]:
                    index = [aggr_incorr_artificial[0] for aggr_incorr_artificial in self.aggregate.incorr_artificial].index(incorr_artificial[0])
                    self.aggregate.incorr_artificial[index][1] += incorr_artificial[1]
                else:
                    self.aggregate.incorr_artificial.append(list(incorr_artificial))

            for incorr_overlap in entry.incorr_overlap:
                if incorr_overlap[0] in [aggr_incorr_overlap[0] for aggr_incorr_overlap in self.aggregate.incorr_overlap]:
                    index = [aggr_incorr_overlap[0] for aggr_incorr_overlap in self.aggregate.incorr_overlap].index(incorr_overlap[0])
                    self.aggregate.incorr_overlap[index][1] += incorr_overlap[1]
                else:
                    self.aggregate.incorr_overlap.append(list(incorr_overlap))

        self.aggregate.sort()
        self.aggregate.sum()

    def export(self):
        with open(self.output, "w") as output:
            output.write(str(self.aggregate))

    def export_conf_table(self):
        with open(self.conf_table_output, "w") as output:
            table = self.aggregate.confusion_table()
            output.write(" ,adult,child,artificial,overlap\n")
            for counts in table:
                for count in counts:
                    output.write("{},".format(count))
                output.write("\n")


class Clanstats(object):

    def __init__(self,
                 total=0,
                 child=0,
                 adult=0,
                 female=0,
                 male=0,
                 artificial=0,
                 overlap=0,
                 speakers=[],
                 corr_child=[],
                 corr_adult=[],
                 corr_female=[],
                 corr_male=[],
                 corr_artificial=[],
                 corr_overlap=[],
                 incorr_child=[],
                 incorr_adult=[],
                 incorr_female=[],
                 incorr_male=[],
                 incorr_artificial=[],
                 incorr_overlap=[]):

        self.total = total
        self.child = child
        self.adult = adult
        self.female = female
        self.male = male
        self.artificial = artificial
        self.overlap = overlap
        self.speakers = speakers
        self.corr_child = corr_child
        self.corr_adult = corr_adult
        self.corr_female = corr_female
        self.corr_male = corr_male
        self.corr_artificial = corr_artificial
        self.corr_overlap = corr_overlap

        self.incorr_child = incorr_child
        self.incorr_adult = incorr_adult
        self.incorr_female = incorr_female
        self.incorr_male = incorr_male
        self.incorr_artificial = incorr_artificial
        self.incorr_overlap = incorr_overlap

        self.corr_child_sum = 0
        self.child_adult_sum = 0
        self.child_male_sum = 0
        self.child_female_sum = 0
        self.child_artificial_sum = 0
        self.child_overlap_sum = 0

        self.corr_adult_sum = 0
        self.adult_child_sum = 0
        self.adult_artificial_sum = 0
        self.adult_overlap_sum = 0

        self.corr_female_sum = 0
        self.female_male_sum = 0
        self.female_child_sum = 0
        self.female_artificial_sum = 0
        self.female_overlap_sum = 0

        self.corr_male_sum = 0
        self.male_female_sum = 0
        self.male_child_sum = 0
        self.male_artificial_sum = 0
        self.male_overlap_sum = 0

        self.corr_artificial_sum = 0
        self.artificial_child_sum = 0
        self.artificial_adult_sum = 0
        self.artificial_male_sum = 0
        self.artificial_female_sum = 0
        self.artificial_overlap_sum = 0

        self.corr_overlap_sum = 0
        self.overlap_child_sum = 0
        self.overlap_adult_sum = 0
        self.overlap_male_sum = 0
        self.overlap_female_sum = 0
        self.overlap_artificial_sum = 0

        self.sum()



    def __repr__(self):
        return  "\ntotal:\t{}\n\
child:\t{}\n\
adult:\t{}\n\
female:\t{}\n\
male:\t{}\n\
artificial:\t{}\n\
overlap:\t{}\n\n\
speakers:\t{}\n\n\
corr_child:\t{}\n\
corr_adult:\t{}\n\
corr_female:\t{}\n\
corr_male:\t{}\n\
corr_artificial:\t{}\n\
corr_overlap:\t{}\n\n\
incorr_child:\t{}\n\
incorr_adult:\t{}\n\
incorr_female:\t{}\n\
incorr_male:\t{}\n\
incorr_artificial:\t{}\n\
incorr_overlap:\t{}\n".format(self.total,
                              self.child,
                              self.adult,
                              self.female,
                              self.male,
                              self.artificial,
                              self.overlap,
                              self.speakers,
                              self.corr_child,
                              self.corr_adult,
                              self.corr_female,
                              self.corr_male,
                              self.corr_artificial,
                              self.corr_overlap,
                              self.incorr_child,
                              self.incorr_adult,
                              self.incorr_female,
                              self.incorr_male,
                              self.incorr_artificial,
                              self.incorr_overlap)

    def sort(self):

        self.speakers.sort(key=operator.itemgetter(1), reverse=True)
        self.corr_child.sort(key=operator.itemgetter(1), reverse=True)
        self.corr_adult.sort(key=operator.itemgetter(1), reverse=True)
        self.corr_female.sort(key=operator.itemgetter(1), reverse=True)
        self.corr_male.sort(key=operator.itemgetter(1), reverse=True)
        self.corr_artificial.sort(key=operator.itemgetter(1), reverse=True)
        self.corr_overlap.sort(key=operator.itemgetter(1), reverse=True)

        self.incorr_child.sort(key=operator.itemgetter(1), reverse=True)
        self.incorr_adult.sort(key=operator.itemgetter(1), reverse=True)
        self.incorr_female.sort(key=operator.itemgetter(1), reverse=True)
        self.incorr_male.sort(key=operator.itemgetter(1), reverse=True)
        self.incorr_artificial.sort(key=operator.itemgetter(1), reverse=True)
        self.incorr_overlap.sort(key=operator.itemgetter(1), reverse=True)

    def confusion_table(self):

                    # Adult                   Child                    Artificial                  Overlap
        table = [
                    ["adult",self.corr_adult_sum, self.adult_child_sum, self.adult_artificial_sum, self.adult_overlap_sum],
                    ["child",self.child_adult_sum, self.corr_child_sum, self.child_artificial_sum, self.child_overlap_sum],
                    ["artificial",self.artificial_adult_sum, self.artificial_child_sum, self.corr_artificial_sum, self.artificial_overlap_sum],
                    ["overlap", self.overlap_adult_sum, self.overlap_child_sum, self.overlap_artificial_sum, self.corr_overlap_sum]
                ]

        return table

    def sum(self):

        for speaker in self.corr_child:
            self.corr_child_sum += speaker[1]
        for speaker in self.corr_adult:
            self.corr_adult_sum += speaker[1]
        for speaker in self.corr_female:
            self.corr_female_sum += speaker[1]
        for speaker in self.corr_male:
            self.corr_male_sum += speaker[1]
        for speaker in self.corr_artificial:
            self.corr_artificial_sum += speaker[1]
        for speaker in self.corr_overlap:
            self.corr_overlap_sum += speaker[1]

        print "correct_child_sum:   {}".format(self.corr_child_sum)

        for speaker in self.incorr_child:
            if speaker[0] in clanstats.clan_codes["adult"]:
                self.child_adult_sum += speaker[1]
            if speaker[0] in clanstats.clan_codes["artificial"]:
                self.child_artificial_sum += speaker[1]
            if speaker[0] in clanstats.clan_codes["overlap"]:
                self.child_overlap_sum += speaker[1]

        print "child_incorrectly_adult: {}".format(self.child_adult_sum)
        print "child_incorrectly_artificial: {}".format(self.child_artificial_sum)
        print "child_incorrectly_overlap: {}\n\n".format(self.child_overlap_sum)

        for speaker in self.incorr_adult:
            if speaker[0] in clanstats.clan_codes["child"]:
                self.adult_child_sum += speaker[1]
            if speaker[0] in clanstats.clan_codes["artificial"]:
                self.adult_artificial_sum += speaker[1]
            if speaker[0] in clanstats.clan_codes["overlap"]:
                self.adult_overlap_sum += speaker[1]

        for speaker in self.incorr_female:
            if speaker[0] in clanstats.clan_codes["child"]:
                self.female_child_sum += speaker[1]
            if speaker[0] in clanstats.clan_codes["male"]:
                self.female_male_sum += speaker[1]
            if speaker[0] in clanstats.clan_codes["artificial"]:
                self.female_artificial_sum += speaker[1]
            if speaker[0] in clanstats.clan_codes["overlap"]:
                self.female_overlap_sum += speaker[1]

        for speaker in self.incorr_male:
            if speaker[0] in clanstats.clan_codes["child"]:
                self.male_child_sum += speaker[1]
            if speaker[0] in clanstats.clan_codes["female"]:
                self.male_female_sum += speaker[1]
            if speaker[0] in clanstats.clan_codes["artificial"]:
                self.male_artificial_sum += speaker[1]
            if speaker[0] in clanstats.clan_codes["overlap"]:
                self.male_overlap_sum += speaker[1]

        for speaker in self.incorr_artificial:
            if speaker[0] in clanstats.clan_codes["child"]:
                self.artificial_child_sum += speaker[1]
            if speaker[0] in clanstats.clan_codes["adult"]:
                self.artificial_adult_sum += speaker[1]
            if speaker[0] in clanstats.clan_codes["female"]:
                self.artificial_female_sum += speaker[1]
            if speaker[0] in clanstats.clan_codes["male"]:
                self.artificial_male_sum += speaker[1]
            if speaker[0] in clanstats.clan_codes["overlap"]:
                self.artificial_overlap_sum += speaker[1]

        for speaker in self.incorr_overlap:
            if speaker[0] in clanstats.clan_codes["child"]:
                self.overlap_child_sum += speaker[1]
            if speaker[0] in clanstats.clan_codes["adult"]:
                self.overlap_adult_sum += speaker[1]
            if speaker[0] in clanstats.clan_codes["female"]:
                self.overlap_female_sum += speaker[1]
            if speaker[0] in clanstats.clan_codes["male"]:
                self.overlap_male_sum += speaker[1]
            if speaker[0] in clanstats.clan_codes["artificial"]:
                self.overlap_artificial_sum += speaker[1]



if __name__ == "__main__":

    batch_clanstats = BatchClanstats(sys.argv[1], sys.argv[2], sys.argv[3])

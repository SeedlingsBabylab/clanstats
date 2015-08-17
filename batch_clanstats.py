import os
import sys
import operator

class BatchClanstats:

    def __init__(self, input_path, output_path):
        self.path = input_path
        self.output = output_path
        self.files = os.listdir(self.path)

        self.stats = {}

        self.aggregate = None

        for file in self.files:
            self.parse(file)

        self.aggregate_files()

        self.export()
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
        speakers = None
        corr_child = None
        corr_adult = None
        corr_female = None
        corr_male = None
        corr_artificial = None
        incorr_child = None
        incorr_adult = None
        incorr_female = None
        incorr_male = None
        incorr_artificial = None

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

        self.stats[file_id] = Clanstats(total, child, adult, female,
                                        male, artificial, speakers, corr_child,
                                        corr_adult, corr_female, corr_male, corr_artificial,
                                        incorr_child, incorr_adult, incorr_female, incorr_male,
                                        incorr_artificial)

    def aggregate_files(self):

        self.aggregate = Clanstats()


        for key, entry in self.stats.iteritems():
            self.aggregate.total += entry.total
            self.aggregate.child += entry.child
            self.aggregate.adult += entry.adult
            self.aggregate.male += entry.male
            self.aggregate.female += entry.female
            self.aggregate.artificial += entry.artificial

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

        self.aggregate.sort()

    def export(self):
        with open(self.output, "w") as output:
            output.write(str(self.aggregate))

class Clanstats(object):

    def __init__(self,
                 total=0,
                 child=0,
                 adult=0,
                 female=0,
                 male=0,
                 artificial=0,
                 speakers=[],
                 corr_child=[],
                 corr_adult=[],
                 corr_female=[],
                 corr_male=[],
                 corr_artificial=[],
                 incorr_child=[],
                 incorr_adult=[],
                 incorr_female=[],
                 incorr_male=[],
                 incorr_artificial=[]):

        self.total = total
        self.child = child
        self.adult = adult
        self.female = female
        self.male = male
        self.artificial = artificial
        self.speakers = speakers
        self.corr_child = corr_child
        self.corr_adult = corr_adult
        self.corr_female = corr_female
        self.corr_male = corr_male
        self.corr_artificial = corr_artificial
        self.incorr_child = incorr_child
        self.incorr_adult = incorr_adult
        self.incorr_female = incorr_female
        self.incorr_male = incorr_male
        self.incorr_artificial = incorr_artificial

    def __repr__(self):
        return  "\ntotal:\t{}\n\
child:\t{}\n\
adult:\t{}\n\
female:\t{}\n\
male:\t{}\n\
artificial:\t{}\n\n\
speakers:\t{}\n\n\
corr_child:\t{}\n\
corr_adult:\t{}\n\
corr_female:\t{}\n\
corr_male:\t{}\n\
corr_artificial:\t{}\n\n\
incorr_child:\t{}\n\
incorr_adult:\t{}\n\
incorr_female:\t{}\n\
incorr_male:\t{}\n\
incorr_artificial:\t{}\n".format(self.total,
                                                 self.child,
                                                 self.adult,
                                                 self.female,
                                                 self.male,
                                                 self.artificial,
                                                 self.speakers,
                                                 self.corr_child,
                                                 self.corr_adult,
                                                 self.corr_female,
                                                 self.corr_male,
                                                 self.corr_artificial,
                                                 self.incorr_child,
                                                 self.incorr_adult,
                                                 self.incorr_female,
                                                 self.incorr_male,
                                                 self.incorr_artificial)

    def sort(self):

        self.speakers.sort(key=operator.itemgetter(1), reverse=True)
        self.corr_child.sort(key=operator.itemgetter(1), reverse=True)
        self.corr_adult.sort(key=operator.itemgetter(1), reverse=True)
        self.corr_female.sort(key=operator.itemgetter(1), reverse=True)
        self.corr_male.sort(key=operator.itemgetter(1), reverse=True)
        self.corr_artificial.sort(key=operator.itemgetter(1), reverse=True)

        self.incorr_child.sort(key=operator.itemgetter(1), reverse=True)
        self.incorr_adult.sort(key=operator.itemgetter(1), reverse=True)
        self.incorr_female.sort(key=operator.itemgetter(1), reverse=True)
        self.incorr_male.sort(key=operator.itemgetter(1), reverse=True)
        self.incorr_artificial.sort(key=operator.itemgetter(1), reverse=True)

if __name__ == "__main__":

    batch_clanstats = BatchClanstats(sys.argv[1], sys.argv[2])

import os
import sys

class BatchClanstats:

    def __init__(self, path):
        self.path = path
        self.files = os.listdir(self.path)
        print self.files
        self.stats = {}

        for file in self.files:
            self.parse(file)

        self.aggregate()
    def parse(self, clanstat_file):
        """
        Parses a clanstats output file and stores the values in
        the self.stats dictionary keyed by subject_month (e.g. "01_06")

        :param clanstat_file: the clanstats output file
        :return:
        """
        file_id = clanstat_file[0:5]
        print file_id

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

    def aggregate(self):

        aggregate = Clanstats()


        for key, entry in self.stats.iteritems():
            aggregate.total += entry.total
            aggregate.child += entry.child
            aggregate.adult += entry.adult
            aggregate.male += entry.male
            aggregate.female += entry.female
            aggregate.artificial += entry.artificial

            for speaker in entry.speakers:
                print [aggr_speaker[0] for aggr_speaker in aggregate.speakers]
                if speaker[0] in [aggr_speaker[0] for aggr_speaker in aggregate.speakers]:
                    aggregate.speakers[aggregate.speakers.index(speaker[0])][1] += speaker[1]
                else:
                    aggregate.speakers.append(speaker)





        print aggregate


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
        return  "\ntotal = {}\n\
                child = {}\n\
                adult = {}\n\
                female = {}\n\
                male = {}\n\
                artificial = {}\n\
speakers = {}\n\n\
corr_child = {}\n\
corr_adult = {}\n\
corr_female = {}\n\
corr_male = {}\n\
corr_artificial = {}\n\n\
incorr_child = {}\n\
incorr_adult = {}\n\
incorr_female = {}\n\
incorr_male = {}\n\
incorr_artificial = {}\n".format(self.total,
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

if __name__ == "__main__":

    batch_clanstats = BatchClanstats(sys.argv[1])

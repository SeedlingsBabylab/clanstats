import os
import sys
import operator
import csv

import clanstats

class BatchClanstats:

    def __init__(self, input_path, output_path, conf_table_output):
        self.path = input_path
        self.output = output_path
        self.adultchild_conftable = conf_table_output.replace(".csv", "_adultchild.csv")
        self.malefemale_conftable = conf_table_output.replace(".csv", "_malefemale.csv")
        self.files = os.listdir(self.path)
        print self.files
        self.stats = {}

        self.aggregate = None

        for file in self.files:
            self.parse(file)

        self.aggregate_files()

        self.export()
        self.export_conf_tables()
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
        self.aggregate.calc_stats()

    def export(self):
        with open(self.output, "w") as output:
            output.write(str(self.aggregate))

    def export_conf_tables(self):
        table = self.aggregate.confusion_table()
        with open(self.adultchild_conftable, "w") as adultchild_output:
            with open(self.malefemale_conftable, "w") as malefemale_output:
                ac_writer = csv.writer(adultchild_output)
                mf_writer = csv.writer(malefemale_output)

                ac_writer.writerow([" ","adult","child","artificial","overlap","noise","total"])
                mf_writer.writerow([" ","male","female", "child","artificial","overlap","noise","total"])
                for counts in table[0]:
                    ac_writer.writerow([str(count) for count in counts])
                for counts in table[1]:
                    ac_writer.writerow([str(count)[0:4] for count in counts])

                ac_writer.writerow(["adult_tpr", str(self.aggregate.adult_tpr)[0:5]])
                ac_writer.writerow(["adult_spc", str(self.aggregate.adult_spc)[0:5]])
                ac_writer.writerow(["adult_ppv", str(self.aggregate.adult_ppv)[0:5]])
                ac_writer.writerow(["adult_npv", str(self.aggregate.adult_npv)[0:5]])
                ac_writer.writerow(["adult_fpr", str(self.aggregate.adult_fpr)[0:5]])
                ac_writer.writerow(["adult_fdr", str(self.aggregate.adult_fdr)[0:5]])
                ac_writer.writerow(["adult_fnr", str(self.aggregate.adult_fnr)[0:5]])
                ac_writer.writerow(["adult_F1", str(self.aggregate.adult_f1)[0:5]])

                ac_writer.writerow(["child_tpr", str(self.aggregate.child_tpr)[0:5]])
                ac_writer.writerow(["child_spc", str(self.aggregate.child_spc)[0:5]])
                ac_writer.writerow(["child_ppv", str(self.aggregate.child_ppv)[0:5]])
                ac_writer.writerow(["child_npv", str(self.aggregate.child_npv)[0:5]])
                ac_writer.writerow(["child_fpr", str(self.aggregate.child_fpr)[0:5]])
                ac_writer.writerow(["child_fdr", str(self.aggregate.child_fdr)[0:5]])
                ac_writer.writerow(["child_fnr", str(self.aggregate.child_fnr)[0:5]])
                ac_writer.writerow(["child_F1", str(self.aggregate.child_f1)[0:5]])

                ac_writer.writerow(["artificial_tpr", str(self.aggregate.artificial_tpr)[0:5]])
                ac_writer.writerow(["artificial_spc", str(self.aggregate.artificial_spc)[0:5]])
                ac_writer.writerow(["artificial_ppv", str(self.aggregate.artificial_ppv)[0:5]])
                ac_writer.writerow(["artificial_npv", str(self.aggregate.artificial_npv)[0:5]])
                ac_writer.writerow(["artificial_fpr", str(self.aggregate.artificial_fpr)[0:5]])
                ac_writer.writerow(["artificial_fdr", str(self.aggregate.artificial_fdr)[0:5]])
                ac_writer.writerow(["artificial_fnr", str(self.aggregate.artificial_fnr)[0:5]])
                ac_writer.writerow(["artificial_F1", str(self.aggregate.artificial_f1)[0:5]])

                for counts in table[2]:
                    mf_writer.writerow([str(count) for count in counts])
                for counts in table[3]:
                    mf_writer.writerow([str(count)[0:4] for count in counts])

                mf_writer.writerow(["male_tpr", str(self.aggregate.male_tpr)[0:5]])
                mf_writer.writerow(["male_spc", str(self.aggregate.male_spc)[0:5]])
                mf_writer.writerow(["male_ppv", str(self.aggregate.male_ppv)[0:5]])
                mf_writer.writerow(["male_npv", str(self.aggregate.male_npv)[0:5]])
                mf_writer.writerow(["male_fpr", str(self.aggregate.male_fpr)[0:5]])
                mf_writer.writerow(["male_fdr", str(self.aggregate.male_fdr)[0:5]])
                mf_writer.writerow(["male_fnr", str(self.aggregate.male_fnr)[0:5]])
                mf_writer.writerow(["male_F1", str(self.aggregate.male_f1)[0:5]])

                mf_writer.writerow(["female_tpr", str(self.aggregate.female_tpr)[0:5]])
                mf_writer.writerow(["female_spc", str(self.aggregate.female_spc)[0:5]])
                mf_writer.writerow(["female_ppv", str(self.aggregate.female_ppv)[0:5]])
                mf_writer.writerow(["female_npv", str(self.aggregate.female_npv)[0:5]])
                mf_writer.writerow(["female_fpr", str(self.aggregate.female_fpr)[0:5]])
                mf_writer.writerow(["female_fdr", str(self.aggregate.female_fdr)[0:5]])
                mf_writer.writerow(["female_fnr", str(self.aggregate.female_fnr)[0:5]])
                mf_writer.writerow(["female_F1", str(self.aggregate.female_f1)[0:5]])

                mf_writer.writerow(["child_tpr", str(self.aggregate.mf_child_tpr)[0:5]])
                mf_writer.writerow(["child_spc", str(self.aggregate.mf_child_spc)[0:5]])
                mf_writer.writerow(["child_ppv", str(self.aggregate.mf_child_ppv)[0:5]])
                mf_writer.writerow(["child_npv", str(self.aggregate.mf_child_npv)[0:5]])
                mf_writer.writerow(["child_fpr", str(self.aggregate.mf_child_fpr)[0:5]])
                mf_writer.writerow(["child_fdr", str(self.aggregate.mf_child_fdr)[0:5]])
                mf_writer.writerow(["child_fnr", str(self.aggregate.mf_child_fnr)[0:5]])
                mf_writer.writerow(["child_F1", str(self.aggregate.mf_child_f1)[0:5]])

                mf_writer.writerow(["artificial_tpr", str(self.aggregate.mf_artificial_tpr)[0:5]])
                mf_writer.writerow(["artificial_spc", str(self.aggregate.mf_artificial_spc)[0:5]])
                mf_writer.writerow(["artificial_ppv", str(self.aggregate.mf_artificial_ppv)[0:5]])
                mf_writer.writerow(["artificial_npv", str(self.aggregate.mf_artificial_npv)[0:5]])
                mf_writer.writerow(["artificial_fpr", str(self.aggregate.mf_artificial_fpr)[0:5]])
                mf_writer.writerow(["artificial_fdr", str(self.aggregate.mf_artificial_fdr)[0:5]])
                mf_writer.writerow(["artificial_fnr", str(self.aggregate.mf_artificial_fnr)[0:5]])
                mf_writer.writerow(["artificial_F1", str(self.aggregate.mf_artificial_f1)[0:5]])

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
        self.child_noise_sum = 0

        self.corr_adult_sum = 0
        self.adult_child_sum = 0
        self.adult_artificial_sum = 0
        self.adult_overlap_sum = 0
        self.adult_noise_sum = 0

        self.corr_female_sum = 0
        self.female_male_sum = 0
        self.female_child_sum = 0
        self.female_artificial_sum = 0
        self.female_overlap_sum = 0
        self.female_noise_sum = 0

        self.corr_male_sum = 0
        self.male_female_sum = 0
        self.male_child_sum = 0
        self.male_artificial_sum = 0
        self.male_overlap_sum = 0
        self.male_noise_sum = 0

        self.corr_artificial_sum = 0
        self.artificial_child_sum = 0
        self.artificial_adult_sum = 0
        self.artificial_male_sum = 0
        self.artificial_female_sum = 0
        self.artificial_overlap_sum = 0
        self.artificial_noise_sum = 0

        self.corr_overlap_sum = 0
        self.overlap_child_sum = 0
        self.overlap_adult_sum = 0
        self.overlap_male_sum = 0
        self.overlap_female_sum = 0
        self.overlap_artificial_sum = 0
        self.overlap_noise_sum = 0

        self.adult_classifier_count = 0
        self.child_classifier_count = 0
        self.artificial_classifier_count = 0
        self.overlap_classifier_count = 0
        self.noise_classifier_count = 0

        self.adult_tp = 0   # true positive
        self.adult_tn = 0   # true negative
        self.adult_fp = 0   # false positive
        self.adult_fn = 0   # false negative

        self.adult_tpr = 0  # true positive rate (sensitivity)
        self.adult_spc = 0  # specificity (true negative rate)
        self.adult_ppv = 0  # positive predictive value (precision)
        self.adult_npv = 0  # negative predictive value
        self.adult_fpr = 0  # false positive rate
        self.adult_fdr = 0  # false discovery rate
        self.adult_fnr = 0  # false negative rate
        self.adult_acc = 0  # accuracy
        self.adult_f1  = 0  # F1 score


        self.child_tp = 0
        self.child_tn = 0
        self.child_fp = 0
        self.child_fn = 0

        self.child_tpr = 0  # true positive rate (sensitivity)
        self.child_spc = 0  # specificity (true negative rate)
        self.child_ppv = 0  # positive predictive value (precision)
        self.child_npv = 0  # negative predictive value
        self.child_fpr = 0  # false positive rate
        self.child_fdr = 0  # false discovery rate
        self.child_fnr = 0  # false negative rate
        self.child_acc = 0  # accuracy
        self.child_f1  = 0  # F1 score

        self.artificial_tp = 0
        self.artificial_tn = 0
        self.artificial_fp = 0
        self.artificial_fn = 0

        self.artificial_tpr = 0  # true positive rate (sensitivity)
        self.artificial_spc = 0  # specificity (true negative rate)
        self.artificial_ppv = 0  # positive predictive value (precision)
        self.artificial_npv = 0  # negative predictive value
        self.artificial_fpr = 0  # false positive rate
        self.artificial_fdr = 0  # false discovery rate
        self.artificial_fnr = 0  # false negative rate
        self.artificial_acc = 0  # accuracy
        self.artificial_f1  = 0  # F1 score

        self.overlap_tp = 0
        self.overlap_tn = 0
        self.overlap_fp = 0
        self.overlap_fn = 0

        self.overlap_tpr = 0  # true positive rate (sensitivity)
        self.overlap_spc = 0  # specificity (true negative rate)
        self.overlap_ppv = 0  # positive predictive value (precision)
        self.overlap_npv = 0  # negative predictive value
        self.overlap_fpr = 0  # false positive rate
        self.overlap_fdr = 0  # false discovery rate
        self.overlap_fnr = 0  # false negative rate
        self.overlap_acc = 0  # accuracy
        self.overlap_f1  = 0  # F1 score

        self.male_tp = 0
        self.male_tn = 0
        self.male_fp = 0
        self.male_fn = 0

        self.male_tpr = 0  # true positive rate (sensitivity)
        self.male_spc = 0  # specificity (true negative rate)
        self.male_ppv = 0  # positive predictive value (precision)
        self.male_npv = 0  # negative predictive value
        self.male_fpr = 0  # false positive rate
        self.male_fdr = 0  # false discovery rate
        self.male_fnr = 0  # false negative rate
        self.male_acc = 0  # accuracy
        self.male_f1  = 0  # F1 score

        self.female_tp = 0
        self.female_tn = 0
        self.female_fp = 0
        self.female_fn = 0

        self.female_tpr = 0  # true positive rate (sensitivity)
        self.female_spc = 0  # specificity (true negative rate)
        self.female_ppv = 0  # positive predictive value (precision)
        self.female_npv = 0  # negative predictive value
        self.female_fpr = 0  # false positive rate
        self.female_fdr = 0  # false discovery rate
        self.female_fnr = 0  # false negative rate
        self.female_acc = 0  # accuracy
        self.female_f1  = 0  # F1 score

        self.mf_child_tp = 0
        self.mf_child_tn = 0
        self.mf_child_fp = 0
        self.mf_child_fn = 0

        self.mf_child_tpr = 0  # true positive rate (sensitivity)
        self.mf_child_spc = 0  # specificity (true negative rate)
        self.mf_child_ppv = 0  # positive predictive value (precision)
        self.mf_child_npv = 0  # negative predictive value
        self.mf_child_fpr = 0  # false positive rate
        self.mf_child_fdr = 0  # false discovery rate
        self.mf_child_fnr = 0  # false negative rate
        self.mf_child_acc = 0  # accuracy
        self.mf_child_f1  = 0  # F1 score

        self.mf_artificial_tp = 0
        self.mf_artificial_tn = 0
        self.mf_artificial_fp = 0
        self.mf_artificial_fn = 0

        self.mf_artificial_tpr = 0  # true positive rate (sensitivity)
        self.mf_artificial_spc = 0  # specificity (true negative rate)
        self.mf_artificial_ppv = 0  # positive predictive value (precision)
        self.mf_artificial_npv = 0  # negative predictive value
        self.mf_artificial_fpr = 0  # false positive rate
        self.mf_artificial_fdr = 0  # false discovery rate
        self.mf_artificial_fnr = 0  # false negative rate
        self.mf_artificial_acc = 0  # accuracy
        self.mf_artificial_f1  = 0  # F1 score

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

        adult_counts_table = [
                                ["adult",
                                 self.corr_adult_sum,
                                 self.adult_child_sum,
                                 self.adult_artificial_sum,
                                 self.adult_overlap_sum,
                                 self.adult_noise_sum,
                                 self.adult ],

                                ["child",
                                 self.child_adult_sum,
                                 self.corr_child_sum,
                                 self.child_artificial_sum,
                                 self.child_overlap_sum,
                                 self.child_noise_sum,
                                 self.child],

                                ["artificial",
                                 self.artificial_adult_sum,
                                 self.artificial_child_sum,
                                 self.corr_artificial_sum,
                                 self.artificial_overlap_sum,
                                 self.artificial_noise_sum,
                                 self.artificial],

                                ["overlap",
                                 self.overlap_adult_sum,
                                 self.overlap_child_sum,
                                 self.overlap_artificial_sum,
                                 self.corr_overlap_sum,
                                 self.overlap_noise_sum,
                                 self.overlap],

                                ["total",
                                 self.adult_classifier_count,
                                 self.child_classifier_count,
                                 self.artificial_classifier_count,
                                 self.noise_classifier_count,
                                 self.overlap_classifier_count]
        ]

        gender_counts_table = [
                                ["male",
                                 self.corr_male_sum,
                                 self.male_female_sum,
                                 self.male_child_sum,
                                 self.male_artificial_sum,
                                 self.male_overlap_sum,
                                 self.male_noise_sum,
                                 self.male],

                                ["female",
                                 self.female_male_sum,
                                 self.corr_female_sum,
                                 self.female_child_sum,
                                 self.female_artificial_sum,
                                 self.female_overlap_sum,
                                 self.female_noise_sum,
                                 self.female],

                                ["child",
                                 self.child_male_sum,
                                 self.child_female_sum,
                                 self.corr_child_sum,
                                 self.child_overlap_sum,
                                 self.child_artificial_sum,
                                 self.child_noise_sum,
                                 self.child],

                                ["artificial",
                                 self.artificial_male_sum,
                                 self.artificial_female_sum,
                                 self.artificial_child_sum,
                                 self.corr_artificial_sum,
                                 self.artificial_overlap_sum,
                                 self.artificial_noise_sum,
                                 self.artificial],

                                ["overlap",
                                 self.overlap_male_sum,
                                 self.overlap_female_sum,
                                 self.overlap_child_sum,
                                 self.overlap_artificial_sum,
                                 self.corr_overlap_sum,
                                 self.overlap_noise_sum,
                                 self.overlap],

                                ["total",
                                 self.male_classifier_count,
                                 self.female_classifier_count,
                                 self.child_classifier_count,
                                 self.artificial_classifier_count,
                                 self.overlap_classifier_count,
                                 self.noise_classifier_count]
        ]

        adult_percents_table = [
                                    ["adult",
                                     float(self.corr_adult_sum)/self.adult,
                                     float(self.adult_child_sum)/self.adult,
                                     float(self.adult_artificial_sum)/self.adult,
                                     float(self.adult_overlap_sum)/self.adult,
                                     float(self.adult_noise_sum)/self.adult],

                                    ["child",
                                     float(self.child_adult_sum)/self.child,
                                     float(self.corr_child_sum)/self.child,
                                     float(self.child_artificial_sum)/self.child,
                                     float(self.child_overlap_sum)/self.child,
                                     float(self.child_noise_sum)/self.child],

                                    ["artificial",
                                     float(self.artificial_adult_sum)/self.artificial,
                                     float(self.artificial_child_sum)/self.artificial,
                                     float(self.corr_artificial_sum)/self.artificial,
                                     float(self.artificial_overlap_sum)/self.artificial,
                                     float(self.artificial_noise_sum)/self.artificial],

                                    ["overlap",
                                     float(self.overlap_adult_sum)/self.overlap,
                                     float(self.overlap_child_sum)/self.overlap,
                                     float(self.overlap_artificial_sum)/self.overlap,
                                     float(self.corr_overlap_sum)/self.overlap,
                                     float(self.overlap_noise_sum)/self.overlap]
        ]

        gender_percents_table = [
                                    ["male",
                                     float(self.corr_male_sum)/self.male,
                                     float(self.male_female_sum)/self.male,
                                     float(self.male_child_sum)/self.male,
                                     float(self.male_artificial_sum)/self.male,
                                     float(self.male_overlap_sum)/self.male,
                                     float(self.male_noise_sum)/self.male],

                                    ["female",
                                     float(self.female_male_sum)/self.female,
                                     float(self.corr_female_sum)/self.female,
                                     float(self.female_child_sum)/self.female,
                                     float(self.female_artificial_sum)/self.female,
                                     float(self.female_overlap_sum)/self.female,
                                     float(self.female_noise_sum)/self.female],

                                    ["child",
                                     float(self.child_male_sum)/self.child,
                                     float(self.child_female_sum)/self.child,
                                     float(self.corr_child_sum)/self.child,
                                     float(self.child_artificial_sum)/self.child,
                                     float(self.child_overlap_sum)/self.child,
                                     float(self.child_noise_sum)/self.child
                                     ],

                                    ["artificial",
                                     float(self.artificial_male_sum)/self.artificial,
                                     float(self.artificial_female_sum)/self.artificial,
                                     float(self.artificial_child_sum)/self.artificial,
                                     float(self.corr_artificial_sum)/self.artificial,
                                     float(self.artificial_overlap_sum)/self.artificial,
                                     float(self.artificial_noise_sum)/self.artificial],

                                    ["overlap",
                                     float(self.overlap_male_sum)/self.overlap,
                                     float(self.overlap_female_sum)/self.overlap,
                                     float(self.overlap_child_sum)/self.overlap,
                                     float(self.overlap_artificial_sum)/self.overlap,
                                     float(self.corr_overlap_sum)/self.overlap,
                                     float(self.overlap_noise_sum)/self.overlap]
        ]
        return (adult_counts_table, adult_percents_table, gender_counts_table, gender_percents_table)

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
            if speaker[0] in clanstats.clan_codes["noise"]:
                self.adult_noise_sum += speaker[1]

        for speaker in self.incorr_female:
            if speaker[0] in clanstats.clan_codes["child"]:
                self.female_child_sum += speaker[1]
            if speaker[0] in clanstats.clan_codes["male"]:
                self.female_male_sum += speaker[1]
            if speaker[0] in clanstats.clan_codes["artificial"]:
                self.female_artificial_sum += speaker[1]
            if speaker[0] in clanstats.clan_codes["overlap"]:
                self.female_overlap_sum += speaker[1]
            if speaker[0] in clanstats.clan_codes["noise"]:
                self.female_noise_sum += speaker[1]

        for speaker in self.incorr_male:
            if speaker[0] in clanstats.clan_codes["child"]:
                self.male_child_sum += speaker[1]
            if speaker[0] in clanstats.clan_codes["female"]:
                self.male_female_sum += speaker[1]
            if speaker[0] in clanstats.clan_codes["artificial"]:
                self.male_artificial_sum += speaker[1]
            if speaker[0] in clanstats.clan_codes["overlap"]:
                self.male_overlap_sum += speaker[1]
            if speaker[0] in clanstats.clan_codes["noise"]:
                self.male_noise_sum += speaker[1]


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
            if speaker[0] in clanstats.clan_codes["noise"]:
                self.artificial_noise_sum += speaker[1]

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
            if speaker[0] in clanstats.clan_codes["male"]:
                self.overlap_noise_sum += speaker[1]


        self.adult_classifier_count = self.corr_adult_sum + self.child_adult_sum + self.artificial_adult_sum + self.overlap_adult_sum
        self.male_classifier_count = self.corr_male_sum + self.female_male_sum + self.child_male_sum + self.artificial_male_sum + self.overlap_male_sum
        self.female_classifier_count = self.corr_female_sum + self.male_female_sum + self.child_female_sum + self.artificial_female_sum + self.overlap_male_sum
        self.child_classifier_count = self.corr_child_sum + self.adult_child_sum + self.artificial_child_sum + self.overlap_child_sum
        self.artificial_classifier_count = self.corr_artificial_sum + self.child_artificial_sum + self.adult_artificial_sum + self.overlap_artificial_sum
        self.overlap_classifier_count = self.corr_overlap_sum + self.child_overlap_sum + self.adult_overlap_sum + self.artificial_overlap_sum
        self.noise_classifier_count = self.child_noise_sum + self.adult_noise_sum + self.artificial_noise_sum + self.overlap_noise_sum


        self.adult_tp = self.corr_adult_sum
        self.adult_tn = self.corr_child_sum + self.child_artificial_sum + self.child_overlap_sum +\
                        self.child_noise_sum + self.artificial_child_sum +self.corr_artificial_sum +\
                        self.artificial_overlap_sum + self.artificial_noise_sum + self.overlap_child_sum +\
                        self.overlap_artificial_sum + self.corr_overlap_sum + self.overlap_noise_sum
        self.adult_fp = self.child_adult_sum + self.artificial_adult_sum + self.overlap_adult_sum
        self.adult_fn = self.adult_child_sum + self.adult_artificial_sum + self.adult_overlap_sum + self.adult_noise_sum


        self.child_tp = self.corr_child_sum
        self.child_tn = self.corr_adult_sum + self.adult_artificial_sum + self.adult_overlap_sum +\
                        self.adult_noise_sum + self.artificial_adult_sum + self.corr_artificial_sum +\
                        self.artificial_overlap_sum + self.artificial_noise_sum + self.overlap_adult_sum +\
                        self.overlap_artificial_sum + self.corr_overlap_sum + self.overlap_noise_sum
        self.child_fp = self.adult_child_sum + self.artificial_child_sum + self.overlap_child_sum
        self.child_fn = self.child_adult_sum + self.child_artificial_sum + self.child_overlap_sum + self.child_noise_sum


        self.artificial_tp = self.corr_artificial_sum
        self.artificial_tn = self.corr_adult_sum + self.adult_child_sum + self.adult_overlap_sum +\
                             self.adult_noise_sum + self.child_adult_sum + self.corr_child_sum +\
                             self.child_overlap_sum + self.child_noise_sum + self.overlap_adult_sum +\
                             self.overlap_child_sum + self.corr_overlap_sum + self.overlap_noise_sum
        self.artificial_fp = self.adult_artificial_sum + self.child_artificial_sum + self.overlap_artificial_sum
        self.artificial_fn = self.artificial_adult_sum + self.artificial_child_sum + self.artificial_overlap_sum + self.artificial_noise_sum


        self.overlap_tp = self.corr_overlap_sum



        self.male_tp = self.corr_male_sum
        self.male_tn = self.corr_female_sum + self.female_child_sum + self.female_artificial_sum +\
                       self.female_overlap_sum + self.female_noise_sum + self.child_female_sum +\
                       self.corr_child_sum + self.child_artificial_sum + self.child_overlap_sum +\
                       self.child_noise_sum + self.artificial_female_sum + self.artificial_child_sum +\
                       self.corr_artificial_sum + self.artificial_overlap_sum + self.artificial_noise_sum +\
                       self.overlap_female_sum + self.overlap_child_sum + self.overlap_artificial_sum +\
                       self.corr_overlap_sum + self.overlap_noise_sum
        self.male_fp = self.female_male_sum + self.child_male_sum + self.artificial_male_sum + self.overlap_male_sum
        self.male_fn = self.male_female_sum + self.male_child_sum + self.male_artificial_sum + self.male_overlap_sum + self.male_noise_sum


        self.female_tp = self.corr_female_sum
        self.female_tn = self.corr_male_sum + self.male_child_sum + self.male_artificial_sum +\
                         self.male_overlap_sum + self.male_noise_sum + self.child_male_sum +\
                         self.corr_child_sum + self.child_artificial_sum + self.child_overlap_sum +\
                         self.child_noise_sum + self.artificial_male_sum + self.artificial_child_sum +\
                         self.corr_artificial_sum + self.artificial_overlap_sum + self.artificial_noise_sum +\
                         self.overlap_male_sum + self.overlap_child_sum + self.overlap_artificial_sum +\
                         self.overlap_noise_sum
        self.female_fp = self.male_female_sum + self.child_female_sum + self.artificial_female_sum + self.overlap_female_sum
        self.female_fn = self.female_male_sum + self.female_child_sum + self.female_artificial_sum + self.female_overlap_sum + self.female_noise_sum


        self.mf_child_tp = self.corr_child_sum
        self.mf_child_tn = self.corr_male_sum + self.male_female_sum + self.male_artificial_sum +\
                           self.male_overlap_sum + self.male_noise_sum + self.female_male_sum +\
                           self.corr_female_sum + self.female_artificial_sum + self.female_overlap_sum +\
                           self.female_noise_sum + self.artificial_male_sum + self.artificial_female_sum +\
                           self.corr_artificial_sum + self.artificial_overlap_sum + self.artificial_noise_sum +\
                           self.overlap_male_sum + self.overlap_female_sum + self.overlap_artificial_sum +\
                           self.corr_overlap_sum + self.overlap_noise_sum
        self.mf_child_fp = self.male_child_sum + self.female_child_sum + self.artificial_child_sum +\
                           self.overlap_child_sum
        self.mf_child_fn = self.child_male_sum + self.child_female_sum + self.child_artificial_sum + self.child_overlap_sum + self.child_noise_sum


        self.mf_artificial_tp = self.corr_artificial_sum
        self.mf_artificial_tn = self.corr_male_sum + self.male_female_sum + self.male_child_sum +\
                                self.male_overlap_sum + self.male_noise_sum + self.female_male_sum +\
                                self.corr_female_sum + self.female_child_sum + self.female_overlap_sum +\
                                self.female_noise_sum + self.child_male_sum + self.child_female_sum +\
                                self.corr_child_sum + self.child_overlap_sum + self.child_noise_sum +\
                                self.overlap_male_sum + self.overlap_female_sum + self.overlap_child_sum +\
                                self.corr_overlap_sum + self.overlap_noise_sum
        self.mf_artificial_fp = self.male_artificial_sum + self.female_artificial_sum + self.child_artificial_sum + self.overlap_artificial_sum
        self.mf_artificial_fn = self.artificial_male_sum + self.artificial_female_sum + self.artificial_child_sum + self.artificial_overlap_sum + self.artificial_noise_sum


    def calc_stats(self):

        self.adult_tpr = float(self.adult_tp) / (self.adult_tp + self.adult_fn)
        self.adult_spc = float(self.adult_tn) / (self.adult_fp + self.adult_tn)
        self.adult_ppv = float(self.adult_tp) / (self.adult_tp + self.adult_fp)
        self.adult_npv = float(self.adult_tn) / (self.adult_tn + self.adult_fn)
        self.adult_fpr = float(self.adult_fp) / (self.adult_fp + self.adult_tn)
        self.adult_fdr = float(self.adult_fp) / (self.adult_fp + self.adult_tp)
        self.adult_fnr = float(self.adult_fn) / (self.adult_fn + self.adult_tp)
        self.adult_f1 = float(2*self.adult_tp) / (2*self.adult_tp + self.adult_fp + self.adult_fn)

        self.child_tpr = float(self.child_tp) / (self.child_tp + self.child_fn)
        self.child_spc = float(self.child_tn) / (self.child_fp + self.child_tn)
        self.child_ppv = float(self.child_tp) / (self.child_tp + self.child_fp)
        self.child_npv = float(self.child_tn) / (self.child_tn + self.child_fn)
        self.child_fpr = float(self.child_fp) / (self.child_fp + self.child_tn)
        self.child_fdr = float(self.child_fp) / (self.child_fp + self.child_tp)
        self.child_fnr = float(self.child_fn) / (self.child_fn + self.child_tp)
        self.child_f1 = float(2*self.child_tp) / (2*self.child_tp + self.child_fp + self.child_fn)

        self.artificial_tpr = float(self.artificial_tp) / (self.artificial_tp + self.artificial_fn)
        self.artificial_spc = float(self.artificial_tn) / (self.artificial_fp + self.artificial_tn)
        self.artificial_ppv = float(self.artificial_tp) / (self.artificial_tp + self.artificial_fp)
        self.artificial_npv = float(self.artificial_tn) / (self.artificial_tn + self.artificial_fn)
        self.artificial_fpr = float(self.artificial_fp) / (self.artificial_fp + self.artificial_tn)
        self.artificial_fdr = float(self.artificial_fp) / (self.artificial_fp + self.artificial_tp)
        self.artificial_fnr = float(self.artificial_fn) / (self.artificial_fn + self.artificial_tp)
        self.artificial_f1 = float(2*self.artificial_tp) / (2*self.artificial_tp + self.artificial_fp + self.artificial_fn)

        self.male_tpr = float(self.male_tp) / (self.male_tp + self.male_fn)
        self.male_spc = float(self.male_tn) / (self.male_fp + self.male_tn)
        self.male_ppv = float(self.male_tp) / (self.male_tp + self.male_fp)
        self.male_npv = float(self.male_tn) / (self.male_tn + self.male_fn)
        self.male_fpr = float(self.male_fp) / (self.male_fp + self.male_tn)
        self.male_fdr = float(self.male_fp) / (self.male_fp + self.male_tp)
        self.male_fnr = float(self.male_fn) / (self.male_fn + self.male_tp)
        self.male_f1 = float(2*self.male_tp) / (2*self.male_tp + self.male_fp + self.male_fn)

        self.female_tpr = float(self.female_tp) / (self.female_tp + self.female_fn)
        self.female_spc = float(self.female_tn) / (self.female_fp + self.female_tn)
        self.female_ppv = float(self.female_tp) / (self.female_tp + self.female_fp)
        self.female_npv = float(self.female_tn) / (self.female_tn + self.female_fn)
        self.female_fpr = float(self.female_fp) / (self.female_fp + self.female_tn)
        self.female_fdr = float(self.female_fp) / (self.female_fp + self.female_tp)
        self.female_fnr = float(self.female_fn) / (self.female_fn + self.female_tp)
        self.female_f1 = float(2*self.female_tp) / (2*self.female_tp + self.female_fp + self.female_fn)

        self.mf_child_tpr = float(self.mf_child_tp) / (self.mf_child_tp + self.mf_child_fn)
        self.mf_child_spc = float(self.mf_child_tn) / (self.mf_child_fp + self.mf_child_tn)
        self.mf_child_ppv = float(self.mf_child_tp) / (self.mf_child_tp + self.mf_child_fp)
        self.mf_child_npv = float(self.mf_child_tn) / (self.mf_child_tn + self.mf_child_fn)
        self.mf_child_fpr = float(self.mf_child_fp) / (self.mf_child_fp + self.mf_child_tn)
        self.mf_child_fdr = float(self.mf_child_fp) / (self.mf_child_fp + self.mf_child_tp)
        self.mf_child_fnr = float(self.mf_child_fn) / (self.mf_child_fn + self.mf_child_tp)
        self.mf_child_f1 = float(2*self.mf_child_tp) / (2*self.mf_child_tp + self.mf_child_fp + self.mf_child_fn)

        self.mf_artificial_tpr = float(self.mf_artificial_tp) / (self.mf_artificial_tp + self.mf_artificial_fn)
        self.mf_artificial_spc = float(self.mf_artificial_tn) / (self.mf_artificial_fp + self.mf_artificial_tn)
        self.mf_artificial_ppv = float(self.mf_artificial_tp) / (self.mf_artificial_tp + self.mf_artificial_fp)
        self.mf_artificial_npv = float(self.mf_artificial_tn) / (self.mf_artificial_tn + self.mf_artificial_fn)
        self.mf_artificial_fpr = float(self.mf_artificial_fp) / (self.mf_artificial_fp + self.mf_artificial_tn)
        self.mf_artificial_fdr = float(self.mf_artificial_fp) / (self.mf_artificial_fp + self.mf_artificial_tp)
        self.mf_artificial_fnr = float(self.mf_artificial_fn) / (self.mf_artificial_fn + self.mf_artificial_tp)
        self.mf_artificial_f1 = float(2*self.mf_artificial_tp) / (2*self.mf_artificial_tp + self.mf_artificial_fp + self.mf_artificial_fn)

if __name__ == "__main__":

    batch_clanstats = BatchClanstats(sys.argv[1], sys.argv[2], sys.argv[3])

#clanstats
library(dplyr)
library(magrittr)
library(tidyr)
library(ggplot2)
library(irr)

setwd("/Users/elikab/Desktop/clanstats_git/clanstats/csv_data_01-43_6_7month/")
filenames <- list.files(path = "/Users/elikab/Desktop/clanstats_git/clanstats/csv_data_01-43_6_7month/")

clanstats <- do.call(rbind, lapply(filenames, 
                      function(X) {
  data.frame(id = basename(X), read.csv(X))}))

summary(clanstats)

clanstats <- do.call("rbind", lapply(filenames, read.csv, header = TRUE))

setwd("/Users/elikab/Desktop/clanstats_git/clanstats/")
write.csv(clanstats, "concat_6_7_basiclevel_9-17-15_uncleaned.csv", row.names= F)

clanstats_tempfixed <- read.csv("concat_6_7_basiclevel_tempfixed_9-17-15.csv", header=T)
summary(clanstats_tempfixed)
levels(clanstats_tempfixed$speaker)

head(clanstats)
dim(clanstats)
clanstats <- clanstats_tempfixed %>%
  rename("annotation" = speaker)%>%
  mutate(classifier = as.factor(substring(tier, 2,4)),
         subject = as.factor(substring(id, 1,2)),
         month = as.factor(substring(id, 4,5)),
    lena_cat = as.factor(ifelse(classifier %in% c("MAN","MAF"),"adu_m",
                ifelse(classifier %in% c("FAN","FAF"),"adu_f",
                       ifelse(classifier %in% c("CHN","CHF","CXN","CXF"),"child",
                              ifelse(classifier %in% c("TVN","TVF"),"artif",
                                     ifelse(classifier %in% c("OLN","OLF"), "multi",
                                            ifelse(classifier %in% c("NON","NOF", "SIL"),"other", NA))))))),
         human_cat = as.factor(ifelse(annotation %in% c("FAT",  # father
                                              "GRP",  # grandpa
                                              "UNC",  # uncle
                                              "UM1",  #unknown male 1
                                              "UM2",  #unknown male 2
                                              "EXM",  # male experimenter
                                              "ADM",  # adult male
                                              "MFR",  # male friend
                                              "AM1",  # adult male
                                              "AM2",  # adult male
                                              "AM3",  # adult male
                                              "AM4",  # adult male
                                              "GUN",  # great uncle
                                              "MAN",
                                              "AUD",
                                              "LMV",   # live male voice
                                              "MF2",  # male family friends 2-5
                                              "MF3",
                                              "MF4",
                                              "MF5"),"adu_m",
                            ifelse(annotation %in% c("MOT",  # mother
                                                     "GRM",  # grandma
                                                     "GGR",  # great grandma
                                                     "AUN",  # aunt
                                                     "EXF",  # female experimenter
                                                     "LFV",  # live female voice
                                                     "AF1",  # adult female
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
                                                     "MT2",  # other mother
                                                     "LVF", # live voice female
                                                     "FF2",  # female family friends 2-5
                                                     "FF3",
                                                     "FF4",
                                                     "FF5",
                                                     "UF1",   # unknown female
                                                     "UF2"), "adu_f",
                                   ifelse(annotation %in% c("CHI",  # baby
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
                                                            "COU"   # cousin
                                                            ),"child",
                                          ifelse(annotation %in% c("TOY",  # toy
                                                                   "TOYS",
                                                                   "TVN",  # TV/radio/CD/etc...
                                                                   "TVF",  # TV female
                                                                   "TVM",  # TV male
                                                                   "RAD",  # radio
                                                                   "CAR",  # car voice
                                                                   "TVS",  # youtube characters
                                                                   "ATV"), "artif",
                                                 ifelse(annotation %in% c("MFT",  # mother father
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
                                                                          "MTY"), "multi","misc_adult")))))))
#AD1 MOM ADU FTS MAS NB1 MMT FAY UKC EAW AFW AF2 ADC DOC WAI LF2 LF3 AD4 LF1
#TEA CH2 LLF LFM LFF CF2 CFF SST YBS MBR AD5 PAP AUY UF3
unique(subset(clanstats, human_cat =="misc_adult")$annotation)
clanstats_matrix <- clanstats%>%
  group_by(lena_cat)%>%
  summarise(num_lenacat = n())%>%
  rename("cat" = lena_cat)%>%
  full_join(clanstats%>%
              group_by(human_cat)%>%
              summarise(num_humancat = n())%>%
              rename("cat" = human_cat))
clanstats_matrix_prop
clanstats_conf <- clanstats %>%
  #mutate(lena_cat  = as.factor(lena_cat),
  #       human_cat = as.factor(human_cat))%>%
  group_by(human_cat,lena_cat)%>%
  tally()%>%
  mutate(n_prop = round(n/sum(n),2))
as.data.frame(clanstats_conf)

lena_comparison_table <-clanstats %>%
  mutate(human_cat_collapsed = ifelse(human_cat %in% c("adu_f", "adu_m", "misc_adult"),"adult", 
                                      ifelse(human_cat %in% c("multi","other"),"other", 
                                             ifelse(human_cat == "artif", "TV","child"))),
         lena_cat_collapsed = ifelse(lena_cat %in% c("adu_f", "adu_m"),"adult", 
                                      ifelse(lena_cat %in% c("multi","other"),"other", 
                                             ifelse(lena_cat == "artif", "TV","child"))),
         lena_cat_collapsed = factor(lena_cat_collapsed, levels = c("adult","child","TV","other")),
         human_cat_collapsed = factor(human_cat_collapsed, levels = c("other","TV","child","adult")))%>%
  group_by(human_cat_collapsed,lena_cat_collapsed)%>%
  tally()%>%
  mutate(n_prop = round(n/sum(n),2))

summary(clanstats)
#clanstats$object_present[clanstats$object_present == "b"]<-"n"
#clanstats$object_present[clanstats$object_present == "d"]<-"y"
#clanstats$utterance_type[clanstats$utterance_type == "|"]<-"d"

#clanstats$utterance_type[clanstats$utterance_type == ""]<-"d"
levels(clanstats$utterance_type)
#clanstats <- drop.levels(clanstats)


ggplot(clanstats_conf, aes(lena_cat, human_cat, fill = n_prop, alpha=log(n)))+geom_tile()+
#  scale_fill_gradient2(low = "blue", high = "red", mid = "white", 
#  midpoint = 0.5, limit = c(0,1), name="Pearson\nCorrelation") +
  theme_minimal(base_size=18)+ geom_text(aes(lena_cat, human_cat, label = n_prop), color = "black", size = 4)+
  theme(axis.text.x = element_text(angle = 45, vjust = 1, 
                                   size = 16, hjust = 1))
ggplot(lena_comparison_table, aes(lena_cat_collapsed, human_cat_collapsed, fill = n_prop, alpha=log(n)))+geom_tile()+
  theme_minimal(base_size=18)+ geom_text(aes(lena_cat_collapsed, human_cat_collapsed, label = n_prop), color = "black", size = 4)+
  theme(axis.text.x = element_text(angle = 45, vjust = 1, 
                                   size = 16, hjust = 1))

lena_props <-c(.14, .04,.06,.76,.08,0,.71,.21,.07, .76, 0, .17, .82, .02, .04, .12)
cor.test(lena_comparison_table$n_prop, lena_props, method = "spearman") # .87 correlation, p <.001
cor.test(as.numeric(as.factor(clanstats$lena_cat)), as.numeric(as.factor(clanstats$human_cat)), method = "spearman")[5]


head(clanstats)
kappa2(clanstats[c(5,8)],"unweighted")$value

clanstats_kappa_tau <- clanstats %>%
  group_by(subject, month)%>%
  summarise(kappa = kappa2(cbind(lena_cat, human_cat))$value,
            kappa_pval = round(kappa2(cbind(lena_cat, human_cat))$p.value,3),
            tau = cor.test(as.numeric(as.factor(lena_cat)), as.numeric(as.factor(human_cat)), method = "kendall")$estimate,
            tau_pval = round(cor.test(as.numeric(as.factor(lena_cat)), as.numeric(as.factor(human_cat)), method = "kendall")$p.value,3))#%>%
  #as.data.frame()%>%
  #summary()
cor.test(clanstats_kappa_tau$kappa, clanstats_kappa_tau$tau)
summary(clanstats_kappa_tau)

# Create a ggheatmap
head(clanstats)
summary(clanstats)
summary(clanstats$classifier)
summary(clanstats$classifier)
levels(clanstats$annotation)

clanstats_sum<-clanstats %>%
  group_by(subject, month)%>%
  summarise(numspeakers = n_distinct(annotation),
         numwords = n())#

ggplot(clanstats_sum, aes(numspeakers, numwords))+geom_point()+geom_smooth()

ggplot(clanstats_sum, aes(as.factor(month), numwords, color = factor(subject)))+geom_point()+
  stat_summary(fun.data=mean_cl_boot, na.rm=T, geom="pointrange",size=1, color="red", size=3)+
  geom_line(aes(group=subject))+
  stat_smooth(aes(group=1), color="red", size = 3)+theme_bw(base_size=16)+
  scale_y_continuous(breaks=seq(200,2000, 100))

ggplot(clanstats_sum, aes(as.factor(month), numspeakers, color = factor(subject)))+geom_point()+
  stat_summary(fun.data=mean_cl_boot, na.rm=T, geom="pointrange",size=1, color="red", size=3)+
  geom_line(aes(group=subject))+
  stat_smooth(aes(group=1), color="red", size = 3)+theme_bw(base_size=16)+
  scale_y_continuous(breaks=seq(1,15, 1))


cor.test(clanstats_sum$numspeakers, clanstats_sum$numwords)
shapiro.test(clanstats_sum$numspeakers)
shapiro.test(clanstats_sum$numwords)

ggplot(clanstats_sum, aes(subject,numspeakers, color=factor(subject)))+
  geom_point(size=3)+theme_bw(base_size=18)

ggplot(clanstats_sum, aes(numspeakers))+geom_histogram()+facet_wrap(~month, nrow=2)



ggplot(clanstats, aes(as.factor(subject),fill=classifier))+
  geom_bar(stat="bin", position = "fill")+theme_bw(base_size=14)


ggplot(clanstats, aes(as.factor(subject), fill=annotation))+
  geom_bar(stat="bin", position = "fill")+theme_bw(base_size=14)


ggplot(clanstats, aes(as.factor(subject), fill=human_cat))+
  geom_histogram(stat="bin", position = "stack")+theme_bw(base_size=10)+
  facet_wrap(~month, nrow=2)+theme_bw(base_size=18)

ggplot(clanstats, aes(as.factor(month), fill=human_cat))+
  geom_histogram(stat="bin", position = "stack",)+theme_bw(base_size=10)+
  theme_bw(base_size=18)

ggplot(clanstats, aes(as.factor(subject), fill=utterance_type))+
  geom_histogram(stat="bin", position = "stack")+theme_bw(base_size=10)+
  theme_bw(base_size=18)+facet_wrap(~month, nrow=2)

ggplot(clanstats, aes(utterance_type, fill=utterance_type))+
  geom_histogram(stat="bin", position = "stack")+theme_bw(base_size=10)+
  theme_bw(base_size=18)
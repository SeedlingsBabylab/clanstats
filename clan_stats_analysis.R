#clanstats
library(dplyr)
library(magrittr)
library(tidyr)
library(ggplot2)

setwd("/Users/elikab/Desktop/clanstats_git/clanstats/csv_data_01-43_6_7month/")
filenames <- list.files(path = "/Users/elikab/Desktop/clanstats_git/clanstats/csv_data_01-43_6_7month/")

clanstats <- do.call(rbind, lapply(filenames, 
                      function(X) {
  data.frame(id = basename(X), read.csv(X))}))

summary(clanstats)

#clanstats <- do.call("rbind", lapply(filenames, read.csv, header = TRUE))
write.csv(clanstats, "concat_6_7_basiclevel.csv", row.names= F)

levels(clanstats$speaker)

head(clanstats)
dim(clanstats)
clanstats <- clanstats %>%
  mutate(lena_cat = as.factor(ifelse(classifier %in% c("MAN","MAF"),"adu_m",
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
                                                                          "MTY"), "multi","misc")))))))
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
  mutate(human_cat_collapsed = ifelse(human_cat %in% c("adu_f", "adu_m"),"adult", 
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
cor.test(lena_comparison_table$n_prop, lena_props, method = "spearman") # .86 correlation, p <.001
cor.test(as.numeric(as.factor(clanstats$lena_cat)), as.numeric(as.factor(clanstats$human_cat)), method = "spearman")[5]
?cor.test
install.packages("irr")
library(irr)

kappa2(clanstats[6:7],"unweighted")$value

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
ggheatmap <- ggplot(clanstats, aes(lena_cat, Var1, fill = value))+
  geom_tile(color = "white")+
  scale_fill_gradient2(low = "blue", high = "red", mid = "white", 
                       midpoint = 0, limit = c(-1,1), name="Pearson\nCorrelation") +
  theme_minimal()+ # minimal theme
  theme(axis.text.x = element_text(angle = 45, vjust = 1, 
                                   size = 12, hjust = 1))+
  coord_fixed()
head(clanstats)
summary(clanstats)
summary(clanstats$classifier)
summary(clanstats$speaker_category)
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

ggplot(clanstats, aes(speaker_category, fill=classifier))+geom_bar()+
  theme_bw(base_size=16)

ggplot(clanstats, aes(classifier, fill=speaker_category))+geom_bar()+
  theme_bw(base_size=16)+
  

ggplot(clanstats, aes(as.factor(subject),fill=speaker_category))+
  geom_bar(stat="bin", position = "fill")+theme_bw(base_size=14)

ggplot(clanstats, aes(as.factor(subject),fill=classifier))+
  geom_bar(stat="bin", position = "fill")+theme_bw(base_size=14)

ggplot(clanstats, aes(as.factor(subject),fill=speaker_category))+
  geom_bar(stat="bin", position = "stack")+theme_bw(base_size=14)+
  facet_wrap(~month, nrow=2)

ggplot(clanstats, aes(as.factor(subject), fill=annotation))+
  geom_bar(stat="bin", position = "fill")+theme_bw(base_size=14)


ggplot(clanstats, aes(as.factor(subject), fill=human_cat))+
  geom_histogram(stat="bin", position = "stack")+theme_bw(base_size=10)+
  facet_wrap(~month, nrow=2)+theme_bw(base_size=18)

ggplot(clanstats, aes(as.factor(month), fill=human_cat))+
  geom_histogram(stat="bin", position = "stack",)+theme_bw(base_size=10)+
  theme_bw(base_size=18)

malefemale_clanstats<-subset(clanstats, speaker_category %in% c("male_correct", "female_correct", "female_incorrect", "male_incorrect"))
summary(malefemale_clanstats)
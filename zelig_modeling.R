# install.pakcages("psych") # for dummy coding
library(Zelig)

# color scheme for plotting
grey <- rgb(169, 169, 170,255*.75, max =255)
grey2 <- rgb(169, 169, 170,255, max =255)
grey3 <- rgb(169, 169, 170,255*.25, max =255)
grey4 <- rgb(169, 169, 170,255*.1, max =255)
blue <- rgb(79, 120, 165, 255*.75, max=255)
blue2 <- rgb(79, 120, 165, 255, max=255)
blue3 <- rgb(79, 120, 165, 255*.25, max=255)
blue4 <- rgb(79, 120, 165, 255*.1, max=255)
red		<- rgb(203, 29 ,  33, 255*.75, max=255)
rep2		<- rgb(203, 29 ,  33, 255, max=255)
red3		<- rgb(203, 29 ,  33, 255*.25, max=255)
red4		<- rgb(203, 29 ,  33, 255*.1, max=255)
green <- rgb(105, 179, 155, 255*.75, max = 255)
green2 <- rgb(105, 179, 155, 255, max = 255)
green3 <- rgb(105, 179, 155, 255*.25, max = 255)
green4 <- rgb(105, 179, 155, 255*.1, max = 255)
orange <-  rgb(222, 130, 68, 255*.75, max = 255)
orange2 <- rgb(222, 130, 68, 255, max = 255)
orange3 <- rgb(222, 130, 68, 255*.25, max = 255)
orange4 <- rgb(222, 130, 68, 255*.1, max = 255)


# **************************************
# set up dataframes
# **************************************

df <- read.csv('/Users/anobles/Documents/rAskDocs/Results/ModelingInR/df_modeling_R_update_race_gender.csv') # 190974 observations

# subset of data without known age
df_unknown_age <- subset(df, age == 'unknown') # 66800 observations
df_unknown_age$age_bins = factor('unknown')

# subset of data with known age
df_known_age <- subset(df, age != 'unknown') # 124174 observations

# bin age
b <- c(-Inf, 10, 20, 30, 40, 50, 60, 70, 80, 90, Inf)
names <- c("0-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80-89", ">90")
age_num <- as.numeric(as.character(df_known_age$age))
df_known_age$age_bins <- cut(age_num, breaks = b, labels = names, right=FALSE)
summary(df_known_age$age_bins)

# combine uknown and known age
df <- rbind(df_unknown_age, df_known_age)

# df_to_save<- df[c("timestamp", "parent_id", "race", "gender", "age", "age_bins", "received_comment", "num_comments", 
#                       "num_comment_authors", "student", "health_prof", "doctor", "first_response_time", "topic_num",
#                       "topic_label")]
# write.csv(df_to_save, file='/Users/anobles/Documents/rAskDocs/Results/ModelingInR/df_modeling_R_update_race_gender_binnedage.csv')


# dummy code variables and make new df for modeling
race_black = ifelse(df$race == 'black', 1, 0)
race_white = ifelse(df$race == 'white', 1, 0)
race_asian = ifelse(df$race == 'asian', 1, 0)
race_hispanic = ifelse(df$race == 'hispanic', 1, 0)
race_indian = ifelse(df$race == 'indian', 1, 0)
race_mixed = ifelse(df$race == 'mixed', 1, 0)
race_unknown = ifelse(df$race == 'unknown', 1, 0)
race_middle_eastern = ifelse(df$race == 'middle_eastern', 1, 0)

sex_female = ifelse(df$gender == 'female', 1, 0)
sex_male = ifelse(df$gender == 'male', 1, 0)
sex_trans = ifelse(df$gender == 'trans', 1, 0)
sex_unknown = ifelse(df$gender == 'unknown', 1, 0)

age_0_9  = ifelse(df$age_bins == '0-9', 1, 0)
age_10_19 = ifelse(df$age_bins == '10-19', 1, 0)
age_20_29 = ifelse(df$age_bins == '20-29', 1, 0)
age_30_39 = ifelse(df$age_bins == '30-39', 1, 0)
age_40_49 = ifelse(df$age_bins == '40-49', 1, 0)
age_50_59 = ifelse(df$age_bins == '50-59', 1, 0)
age_60_69 = ifelse(df$age_bins == '60-69', 1, 0)
age_70_79 = ifelse(df$age_bins == '70-79', 1, 0)
age_80_89 = ifelse(df$age_bins == '80-89', 1, 0)
age_90_100 = ifelse(df$age_bins == '>90', 1, 0)
age_unknown = ifelse(df$age_bins == 'unknown', 1, 0)

doc_comment = ifelse(df$doctor == 'True', 1, 0)
any_comment = ifelse(df$received_comment == 'True', 1, 0)

d_any_comment <- data.frame(any_comment, race_black, race_white, race_asian, race_hispanic, race_indian, race_mixed, race_unknown, race_middle_eastern, sex_female, sex_male, sex_trans, sex_unknown, age_0_9, age_10_19, age_20_29, age_30_39, age_40_49, age_50_59, age_60_69, age_70_79, age_80_89, age_90_100, age_unknown)
d_doc_comment <- data.frame(doc_comment, race_black, race_white, race_asian, race_hispanic, race_indian, race_mixed, race_unknown, race_middle_eastern, sex_female, sex_male, sex_trans, sex_unknown, age_0_9, age_10_19, age_20_29, age_30_39, age_40_49, age_50_59, age_60_69, age_70_79, age_80_89, age_90_100, age_unknown)


# **************************************
# response ~ race + sex + age
# **************************************
# model
s <- zelig(any_comment ~  sex_female + sex_male + sex_trans + race_black + race_white + race_asian + race_hispanic + race_indian + race_mixed + race_middle_eastern, data = d_any_comment, model = "logit", cite = F)

# intialize a list
dd <- vector("list", length = 12)

# race asian
s <-  setx(s, race_black = 0, race_white = 0, race_asian = 1, race_hispanic = 0, race_indian = 0, race_mixed = 0, race_middle_eastern = 0)
sims <- sim(s)
qi.out <- zelig_qi_to_df(sims)
dd[[12]] <- qi.out[qi.out$setx_value == "x",] 

# race black
s <-  setx(s, race_black = 1, race_white = 0, race_asian = 0, race_hispanic = 0, race_indian = 0, race_mixed = 0, race_middle_eastern = 0)
sims <- sim(s)
qi.out <- zelig_qi_to_df(sims)
dd[[11]] <- qi.out[qi.out$setx_value == "x",] 

# race hispanic
s <-  setx(s, race_black = 0, race_white = 0, race_asian = 0, race_hispanic = 1, race_indian = 0, race_mixed = 0, race_middle_eastern = 0)
sims <- sim(s)
qi.out <- zelig_qi_to_df(sims)
dd[[10]] <- qi.out[qi.out$setx_value == "x",] 

# race indian
s <-  setx(s, race_black = 0, race_white = 0, race_asian = 0, race_hispanic = 0, race_indian = 1, race_mixed = 0, race_middle_eastern = 0)
sims <- sim(s)
qi.out <- zelig_qi_to_df(sims)
dd[[9]] <- qi.out[qi.out$setx_value == "x",] 

# middle eastern
s <-  setx(s, race_black = 0, race_white = 0, race_asian = 0, race_hispanic = 0, race_indian = 0, race_mixed = 0, race_middle_eastern = 1)
sims <- sim(s)
qi.out <- zelig_qi_to_df(sims)
dd[[8]] <- qi.out[qi.out$setx_value == "x",] 

# mixed
s <-  setx(s, race_black = 0, race_white = 0, race_asian = 0, race_hispanic = 0, race_indian = 0, race_mixed = 1, race_middle_eastern = 0)
sims <- sim(s)
qi.out <- zelig_qi_to_df(sims)
dd[[7]] <- qi.out[qi.out$setx_value == "x",] 

# white
s <-  setx(s, race_black = 0, race_white = 1, race_asian = 0, race_hispanic = 0, race_indian = 0, race_mixed = 0, race_middle_eastern = 0)
sims <- sim(s)
qi.out <- zelig_qi_to_df(sims)
dd[[6]] <- qi.out[qi.out$setx_value == "x",] 

# unknown race
s <-  setx(s, race_black = 0, race_white = 0, race_asian = 0, race_hispanic = 0, race_indian = 0, race_mixed = 0, race_middle_eastern = 0)
sims <- sim(s)
qi.out <- zelig_qi_to_df(sims)
dd[[5]] <- qi.out[qi.out$setx_value == "x",] 

# sex female
s <-  setx(s, sex_female = 1, sex_male = 0, sex_trans = 0)
sims <- sim(s)
qi.out <- zelig_qi_to_df(sims)
dd[[4]] <- qi.out[qi.out$setx_value == "x",] 

# sex male
s <-  setx(s, sex_female = 0, sex_male = 1, sex_trans = 0)
sims <- sim(s)
qi.out <- zelig_qi_to_df(sims)
dd[[3]] <- qi.out[qi.out$setx_value == "x",] 

# sex trans
s <-  setx(s, sex_female = 0, sex_male = 0, sex_trans = 1)
sims <- sim(s)
qi.out <- zelig_qi_to_df(sims)
dd[[2]] <- qi.out[qi.out$setx_value == "x",] 

# sex unknown
s <-  setx(s, sex_female = 0, sex_male = 0, sex_trans = 0)
sims <- sim(s)
qi.out <- zelig_qi_to_df(sims)
dd[[1]] <- qi.out[qi.out$setx_value == "x",] 

# storing data for plotting
m_any_comment <- matrix(nrow=12, ncol=3)

for (i in 1:12){
  m_any_comment[i, 1:3] <- quantile(dd[[i]]$expected_value, c(0.5, 0.025, 0.975))
}


# **************************************
# doctor ~ race + sex + age
# **************************************
# model
s <- zelig(doc_comment ~  sex_female + sex_male + sex_trans + race_black + race_white + race_asian + race_hispanic + race_indian + race_mixed + race_middle_eastern, data = d_doc_comment, model = "logit", cite = F)

# intialize a list
dd <- vector("list", length = 12)

# race asian
s <-  setx(s, race_black = 0, race_white = 0, race_asian = 1, race_hispanic = 0, race_indian = 0, race_mixed = 0, race_middle_eastern = 0)
sims <- sim(s)
qi.out <- zelig_qi_to_df(sims)
dd[[12]] <- qi.out[qi.out$setx_value == "x",] 

# race black
s <-  setx(s, race_black = 1, race_white = 0, race_asian = 0, race_hispanic = 0, race_indian = 0, race_mixed = 0, race_middle_eastern = 0)
sims <- sim(s)
qi.out <- zelig_qi_to_df(sims)
dd[[11]] <- qi.out[qi.out$setx_value == "x",] 

# race hispanic
s <-  setx(s, race_black = 0, race_white = 0, race_asian = 0, race_hispanic = 1, race_indian = 0, race_mixed = 0, race_middle_eastern = 0)
sims <- sim(s)
qi.out <- zelig_qi_to_df(sims)
dd[[10]] <- qi.out[qi.out$setx_value == "x",] 

# race indian
s <-  setx(s, race_black = 0, race_white = 0, race_asian = 0, race_hispanic = 0, race_indian = 1, race_mixed = 0, race_middle_eastern = 0)
sims <- sim(s)
qi.out <- zelig_qi_to_df(sims)
dd[[9]] <- qi.out[qi.out$setx_value == "x",] 

# middle eastern
s <-  setx(s, race_black = 0, race_white = 0, race_asian = 0, race_hispanic = 0, race_indian = 0, race_mixed = 0, race_middle_eastern = 1)
sims <- sim(s)
qi.out <- zelig_qi_to_df(sims)
dd[[8]] <- qi.out[qi.out$setx_value == "x",] 

# mixed
s <-  setx(s, race_black = 0, race_white = 0, race_asian = 0, race_hispanic = 0, race_indian = 0, race_mixed = 1, race_middle_eastern = 0)
sims <- sim(s)
qi.out <- zelig_qi_to_df(sims)
dd[[7]] <- qi.out[qi.out$setx_value == "x",] 

# white
s <-  setx(s, race_black = 0, race_white = 1, race_asian = 0, race_hispanic = 0, race_indian = 0, race_mixed = 0, race_middle_eastern = 0)
sims <- sim(s)
qi.out <- zelig_qi_to_df(sims)
dd[[6]] <- qi.out[qi.out$setx_value == "x",] 

# unknown race
s <-  setx(s, race_black = 0, race_white = 0, race_asian = 0, race_hispanic = 0, race_indian = 0, race_mixed = 0, race_middle_eastern = 0)
sims <- sim(s)
qi.out <- zelig_qi_to_df(sims)
dd[[5]] <- qi.out[qi.out$setx_value == "x",] 

# sex female
s <-  setx(s, sex_female = 1, sex_male = 0, sex_trans = 0)
sims <- sim(s)
qi.out <- zelig_qi_to_df(sims)
dd[[4]] <- qi.out[qi.out$setx_value == "x",] 

# sex male
s <-  setx(s, sex_female = 0, sex_male = 1, sex_trans = 0)
sims <- sim(s)
qi.out <- zelig_qi_to_df(sims)
dd[[3]] <- qi.out[qi.out$setx_value == "x",] 

# sex trans
s <-  setx(s, sex_female = 0, sex_male = 0, sex_trans = 1)
sims <- sim(s)
qi.out <- zelig_qi_to_df(sims)
dd[[2]] <- qi.out[qi.out$setx_value == "x",] 

# sex unknown
s <-  setx(s, sex_female = 0, sex_male = 0, sex_trans = 0)
sims <- sim(s)
qi.out <- zelig_qi_to_df(sims)
dd[[1]] <- qi.out[qi.out$setx_value == "x",] 

# storing data for plotting
m_doc_comment <- matrix(nrow=12, ncol=3)

for (i in 1:12){
  m_doc_comment[i, 1:3] <- quantile(dd[[i]]$expected_value, c(0.5, 0.025, 0.975))
}


# **************************************
# plotting
# **************************************
quartz("main", 5, 4)

m_layout <- matrix(seq(1,2,by =1), nrow = 1, ncol = 2, byrow = TRUE)
layout(mat = m_layout)
par(
  oma = c(0,3.75,0.5,0.25),
  mar = c(3, 0, 0, 1),
  mgp = c(2,0.1,0))


# plot 1
plot(1, xlim = c(0, 1), ylim = c(0.75, 12.25), type= "n", ylab = "", xlab = "", main = "", cex.main = 0.8, cex.lab = 0.8, axes = F)

axis(1, at = seq(from= 0, to = 1, by = 0.2), label = seq(from= 0, to = 100, by = 20), cex.axis =  0.5, tcl=2, tck = 0.01, col = "black", lty = "solid", las=1, mgp = c(0.05,0.0001,0))
axis(2, at = seq(from=1, to =12, by = 1) , labels = c("Unknown", "Transgender", "Male", "Female", "Unknown", "White", "Multiracial", "Middle Eastern", "Indian", "Hispanic", "Black", "Asian"), 
     cex.axis =  0.5, mgp = c(1,0.2,0), tcl=2, tck = 0.01, col = "black", lty = "solid",las=1)


#abline(v =0 ,xpd =F)
abline(h = seq(1,12, by = 1), col ="grey", lty = 3,xpd =F)
abline(h = 4.5, col = "black", lty = 1, xpd = F)
#abline(h = 12.5, col = "black", lty = 1, xpd = F)

segments( y0 = 1:12, x0 = m_any_comment[,2], x1 =  m_any_comment[,3], col = blue2, lwd =2)	
points(y = 1:12, x = m_any_comment[,1], pch = 19, col = blue2, cex = 0.5)
title(xlab = "Probability of Any Response (%)", mgp = c(0.75,0.1,0), cex.lab = 0.5)
box()


# plot 2
plot(1, xlim = c(0, 1), ylim = c(0.75, 12.25), type= "n", ylab = "", xlab = "", main = "", cex.main = 0.8, cex.lab = 0.8, axes = F)

axis(1, at = seq(from= 0, to = 1, by = 0.2), label = seq(from= 0, to = 100, by = 20), cex.axis =  0.5, tcl=2, tck = 0.01, col = "black", lty = "solid",las=1 )

#abline(v =0 ,xpd =F)
abline(h = seq(1,12, by = 1), col ="grey", lty = 3,xpd =F)
abline(h = 4.5, col = "black", lty = 1, xpd = F)
#abline(h = 12.5, col = "black", lty = 1, xpd = F)

segments( y0 = 1:12, x0 = m_doc_comment[,2], x1 =  m_doc_comment[,3], col = blue2, lwd =2)	
points(y = 1:12, x = m_doc_comment[,1], pch = 19, col = blue2, cex = 0.5)
title(xlab = "Probability of Response by a Physician (%)", mgp = c(0.75,0.1,0), cex.lab = 0.5)
box()

mtext("             Gender/Sex                                                  Race/Ethnicity", side = 4, cex = 0.5, adj = 0, line=0.01)

#quartz.save(file='/Users/anobles/Documents/rAskDocs/Results/Viz/Test/mod_demo_response1_age_sex_only.jpg', type = "jpg", canvas="white", dpi=300)
dev.off()


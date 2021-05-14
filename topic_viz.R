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
df = read.csv('~/Documents/rAskDocs/Results/CleanedData/Model100_NumToken/df_for_viz_model100_numtoken.csv')
# df_1 <- as.data.frame(table(df$topic_label))
# df_1 <- df_1[order(df_1$Freq, decreasing=TRUE),]
# df_1$Var1 <- as.character(df_1$Var1)
#df_1$Freq <- df_1$Freq/190974*100

# re-label the topics by merging the new labels
labels = read.csv('/Users/anobles/Desktop/topics_model100_numtoken_labels_relabel.csv')
labels$old_label  = labels$label
labels = subset(labels, select = -c(words,count, label))
summary(labels)
total <- merge(df,labels,by="topic_num")

df_1 <- as.data.frame(table(total$new_label))
df_1 <- df_1[order(df_1$Freq, decreasing=TRUE),]
df_1$Var1 <- as.character(df_1$Var1)
#df_1$Freq <- df_1$Freq/190974*100


# **************************************
# plotting
# **************************************
quartz("main", 6.5, 4)

m_layout <- matrix(seq(1,2,by =1), nrow = 1, ncol = 2, byrow = TRUE)
layout(mat = m_layout)
# shrink left and right of mar, grow left and right of oma
# grow bottom of oma for title and shrink bottom of mar
# top of mar and oma can be small

par(
  oma = c(3,7.5,0.5,8), # margin outside of figures
  mar = c(0, 0.5, 0, 0.5), # margin around figures
  mgp = c(2,0.1,0))


# plot 1
plot(1, xlim = c(0,15000), ylim = c(0.75, 35.25), type= "n", ylab = "", xlab = "", main = "", cex.main = 0.8, cex.lab = 0.8, axes = F)

axis(1, at = seq(from= 0, to = 15000, by = 3000), label = seq(from= 0, to = 15000, by = 3000), cex.axis =  0.5, tcl=2, tck = 0.01, col = "black", lty = "solid", las=1, mgp = c(0.05,0.0001,0))
axis(2, at = seq(from=1, to =35, by = 1) , labels = rev(df_1[1:35,]$Var1), 
     cex.axis =  0.5, mgp = c(1,0.2,0), tcl=2, tck = 0.01, col = "black", lty = "solid",las=1)


abline(h = seq(1,35, by = 1), col ="grey", lty = 3,xpd =F)

points(y = 1:35, x = rev(df_1[1:35,]$Freq), pch = 19, col = blue2, cex = 0.5)
#title(xlab = "No of Posts", mgp = c(0.75,0.1,0), cex.lab = 0.5)
box()


# plot 2
plot(1, xlim = c(0,15000), ylim = c(0.75, 35.25), type= "n", ylab = "", xlab = "", main = "", cex.main = 0.8, cex.lab = 0.8, axes = F)

axis(1, at = seq(from= 0, to = 15000, by = 3000), label = seq(from= 0, to = 15000, by = 3000), cex.axis =  0.5, tcl=2, tck = 0.01, col = "black", lty = "solid", las=1, mgp = c(0.05,0.0001,0))
axis(4, at = seq(from=1, to =35, by = 1) , labels = rev(df_1[36:70,]$Var1), 
     cex.axis =  0.5, mgp = c(1,0.2,0), tcl=2, tck = 0.01, col = "black", lty = "solid",las=1)


abline(h = seq(1,35, by = 1), col ="grey", lty = 3,xpd =F)

points(y = 1:35, x = rev(df_1[36:70,]$Freq), pch = 19, col = blue2, cex = 0.5)
#title(xlab = "No of Posts", mgp = c(0.75,0.1,0), cex.lab = 0.5)
box()

mtext(text="Number of Posts",side=1,line=1,outer = TRUE, cex=0.6)

quartz.save(file='/Users/anobles/Documents/rAskDocs/Results/Viz/Test/topic_viz_relabeled2.jpg', type = "jpg", canvas="white", dpi=300)
dev.off()


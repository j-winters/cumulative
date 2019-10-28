library(ggplot2)
library(dplyr)
library(data.table)
library(ggthemes)
library(ggpubr)
library(RColorBrewer)

setwd("your/path/here")
cc <- fread("cc.csv")
cc_notr <- fread("cc_notr.csv")
cc_opt <- fread("cc_opt.csv")

#Creating separate dfs for asocial and social events
transmission <- cc %>% select(sim_run,generation,ts,optimization,exploration,trans_freq)
transmission <- transmission %>% rename(freq=trans_freq)
transmission$event <- 'transmission'
innovation <- cc %>% select(sim_run,generation,ts,optimization,exploration,inn_freq)
innovation <- innovation %>% rename(freq=inn_freq)
innovation$event <- 'innovation'
deletion <- cc %>% select(sim_run,generation,ts,optimization,exploration,del_freq)
deletion <- deletion %>% rename(freq=del_freq)
deletion$event <- 'deletion'
recombination <- cc %>% select(sim_run,generation,ts,optimization,exploration,rec_freq)
recombination <- recombination %>% rename(freq=rec_freq)
recombination$event <- 'recombination'
freq_df <- rbind(transmission,innovation,deletion,recombination)
freq_df$event <- as.factor(freq_df$event)

#FIG 4 TOP
cc_heat <- cc %>%
  filter(generation==99) %>%
  select(sim_run,optimization,exploration,LD_norm,solution_length,solution_pool) %>%
  group_by(optimization,exploration) %>%
  dplyr::summarise(optimal=mean(LD_norm,na.rm=TRUE),complexity=mean(solution_length,na.rm=TRUE),diversity=mean(solution_pool,na.rm=TRUE) )

ggplot(cc_heat, aes(x = optimization, y = exploration, fill = optimal)) + theme(axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0.5)) + geom_tile() + theme_hc() + theme(axis.text=element_text(size=14), axis.title=element_text(size=16,face="bold"), legend.title = element_text(size = 14, face="bold"), legend.text = element_text(size = 12), legend.key.width = unit(4,"line") ) + scale_fill_viridis_c(direction = -1,option="inferno",limits=c(0,1))

#FIG 4 BOTTOM
getPalette = colorRampPalette(brewer.pal(9, "Blues"))
ggplot(subset(cc,optimization==c(1.0) & exploration==c(0.8)), aes(x = generation, y = LD_norm, colour = as.factor(sim_run) )) + stat_summary(fun.y = mean, geom="line", size=1, alpha=0.7) + ylab("LD(solution,problem)") + theme_hc() + theme(legend.position="none",axis.text=element_text(size=14), axis.title=element_text(size=16,face="bold"), legend.title = element_text(size = 14, face="bold"), legend.text = element_text(size = 12)) + scale_color_manual(values = getPalette(30))

#FIG 5
gd_opt <- cc_opt %>%
  select(generation,transmission,LD_norm,solution_complexity) %>%
  group_by(generation,transmission) %>%
  summarise(LD_norm = mean(LD_norm),solution_complexity=mean(solution_complexity))
ggplot(cc_opt, aes(x = generation, y = LD_norm, color = transmission)) + geom_point(aes(group=as.factor(sim_run), color=transmission), alpha=.2) + geom_line(data = gd_opt, alpha = .8, size = 3) + theme_hc() + theme(legend.position="none",axis.text=element_text(size=14), axis.title=element_text(size=16,face="bold"), legend.title = element_text(size = 14, face="bold"), legend.text = element_text(size = 12)) + scale_color_manual(values=c("#00AFBB", "#E7B800"))

#FIG 6
getPalette1 = colorRampPalette(brewer.pal(9, "Greens"))
com1 <- ggplot(subset(cc,optimization==c(1.0) & exploration==c(0.2)), aes(x = generation, y = solution_complexity, colour = as.factor(sim_run) )) + stat_summary(fun.y = mean, geom="line", size=3, alpha=.7) + ylab("Solution Complexity") + theme_hc() + theme(legend.position="none",axis.text=element_text(size=14), axis.title=element_text(size=16,face="bold"), legend.title = element_text(size = 14, face="bold"), legend.text = element_text(size = 12)) + scale_color_manual(values = getPalette1(30)) + ylim(0,74)
com2 <- ggplot(subset(cc,optimization==c(0.6) & exploration==c(0.6)), aes(x = generation, y = solution_complexity, colour = as.factor(sim_run) )) + stat_summary(fun.y = mean, geom="line", size=3, alpha=.7) + ylab("Solution Complexity") + theme_hc() + theme(legend.position="none",axis.text=element_text(size=14), axis.title=element_text(size=16,face="bold"), legend.title = element_text(size = 14, face="bold"), legend.text = element_text(size = 12)) + scale_color_manual(values = getPalette1(30)) + ylim(0,74)
com3 <- ggplot(subset(cc,optimization==c(0.6) & exploration==c(0.2)), aes(x = generation, y = solution_complexity, colour = as.factor(sim_run) )) + stat_summary(fun.y = mean, geom="line", size=3, alpha=.7) + ylab("Solution Complexity") + theme_hc() + theme(legend.position="none",axis.text=element_text(size=14), axis.title=element_text(size=16,face="bold"), legend.title = element_text(size = 14, face="bold"), legend.text = element_text(size = 12)) + scale_color_manual(values = getPalette1(30)) + ylim(0,74)
ggarrange(com1,com3,com2,ncol=3,nrow=1)

getPalette2 = colorRampPalette(brewer.pal(9, "Reds"))
div1 <- ggplot(subset(cc,optimization==c(1.0) & exploration==c(0.2)), aes(x = generation, y = solution_pool, colour = as.factor(sim_run) )) + stat_summary(fun.y = mean, geom="line", size=3, alpha=.7) + ylab("Solution Diversity") + theme_hc() + theme(legend.position="none",axis.text=element_text(size=14), axis.title=element_text(size=16,face="bold"), legend.title = element_text(size = 14, face="bold"), legend.text = element_text(size = 12)) + scale_color_manual(values = getPalette2(30)) + ylim(0,100)
div2 <- ggplot(subset(cc,optimization==c(0.6) & exploration==c(0.6)), aes(x = generation, y = solution_pool, colour = as.factor(sim_run) )) + stat_summary(fun.y = mean, geom="line", size=3, alpha=.7) + ylab("Solution Diversity") + theme_hc() + theme(legend.position="none",axis.text=element_text(size=14), axis.title=element_text(size=16,face="bold"), legend.title = element_text(size = 14, face="bold"), legend.text = element_text(size = 12)) + scale_color_manual(values = getPalette2(30)) + ylim(0,100)
div3 <- ggplot(subset(cc,optimization==c(0.6) & exploration==c(0.2)), aes(x = generation, y = solution_pool, colour = as.factor(sim_run) )) + stat_summary(fun.y = mean, geom="line", size=3, alpha=.7) + ylab("Solution Diversity") + theme_hc() + theme(legend.position="none",axis.text=element_text(size=14), axis.title=element_text(size=16,face="bold"), legend.title = element_text(size = 14, face="bold"), legend.text = element_text(size = 12)) + scale_color_manual(values = getPalette2(30)) + ylim(0,100)
ggarrange(com1,com3,com2,div1,div3,div2,ncol=3,nrow=2)

#FIG 7
event3 <- ggplot(subset(freq_df,optimization==c(0.6) & exploration==c(0.2)), aes(x = generation, y = freq, colour = event )) + stat_summary(fun.y = mean, geom="line", size=3) + ylab("Event Frequency") + theme_hc() + theme(axis.text=element_text(size=14), axis.title=element_text(size=16,face="bold"), legend.title = element_text(size = 14, face="bold"), legend.text = element_text(size = 12)) + scale_color_manual(values=c("#00AFBB", "#E7B800", "#FC4E07","#52854C")) + coord_cartesian(ylim=c(0, 30))
event1 <- ggplot(subset(freq_df,optimization==c(1.0) & exploration==c(0.2)), aes(x = generation, y = freq, colour = event )) + stat_summary(fun.y = mean, geom="line", size=3) + ylab("Event Frequency") + theme_hc() + theme(axis.text=element_text(size=14), axis.title=element_text(size=16,face="bold"), legend.title = element_text(size = 14, face="bold"), legend.text = element_text(size = 12)) + scale_color_manual(values=c("#00AFBB", "#E7B800", "#FC4E07","#52854C")) + coord_cartesian(ylim=c(0, 30))
event2 <- ggplot(subset(freq_df,optimization==c(0.6) & exploration==c(0.6)), aes(x = generation, y = freq, colour = event )) + stat_summary(fun.y = mean, geom="line", size=3) + ylab("Event Frequency") + theme_hc() + theme(axis.text=element_text(size=14), axis.title=element_text(size=16,face="bold"), legend.title = element_text(size = 14, face="bold"), legend.text = element_text(size = 12)) + scale_color_manual(values=c("#00AFBB", "#E7B800", "#FC4E07","#52854C")) + coord_cartesian(ylim=c(0, 30))
ggarrange(event1,event3,event2,ncol=3,nrow=1)

#FIG 8
gd_notr <- cc_notr %>%
  select(generation,transmission,solution_complexity) %>%
  group_by(generation,transmission) %>%
  summarise(solution_complexity = mean(solution_complexity))
ggplot(cc_notr, aes(x = generation, y = solution_complexity, color = transmission)) + geom_point(aes(group=as.factor(sim_run), color=transmission), alpha=.2) + geom_line(data = gd_notr, alpha = .8, size = 3) + theme_hc() + theme(legend.position="none",axis.text=element_text(size=14), axis.title=element_text(size=16,face="bold"), legend.title = element_text(size = 14, face="bold"), legend.text = element_text(size = 12)) + scale_color_manual(values=c("#00AFBB", "#E7B800"))


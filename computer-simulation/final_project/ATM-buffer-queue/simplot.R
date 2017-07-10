library(dplyr)
library(ggplot2)

#Set working directory
setwd("/home/olaaun/computer_simulation/final_project/ATM_buffer_queue")

#Read data
sys_wait = read.csv("sys-wait.csv")
q_wait = read.csv("q-wait.csv")
sys_num = read.csv("sys-num.csv")
q_num = read.csv("q-num.csv")

#Combine system and waiting times to one dataframe
wait = data.frame(ARRIVALS=sys_wait$ARRIVALS, SYS=sys_wait$SYSWAITTIME, Q=q_wait$QWAITTIME,
                  AN_SYS=8.21e-6, AN_Q = 5.47e-6)

#Combine system and queue size to one dataframe
num = data.frame(EVENTS=sys_num$EVENTS, SYS=sys_num$SYSNUM, Q=q_num$QNUM,
                 AN_SYS=2.4, AN_Q = 1.6)

#Plot average time results
ggplot(wait, aes(ARRIVALS)) + 
  geom_line(aes(y=Q, color="blue")) + 
  geom_line(aes(y=SYS, color="red")) +
  geom_line(aes(y=AN_Q, color="black"), linetype="dashed") + 
  geom_line(aes(y=AN_SYS, color="green"), linetype="dashed") +
  scale_color_manual(name="Legend",
                     values = c("blue","red","black", "green"),
                     labels = c("Queue wait - Analytical", 
                                  "Queue wait - Simulation", 
                                  "System wait - Analytical", 
                                  "System wait - Simulation")) +
  theme(legend.position=c(.8,.2)) +
  xlab("Departures") +
  ylab("Time in seconds") +
  ggtitle("Average System/Queue Waiting Times")

#Plot average size results
  ggplot(num, aes(EVENTS)) + 
  geom_line(aes(y=Q, color="blue")) + 
  geom_line(aes(y=SYS, color="red")) +
  geom_line(aes(y=AN_Q, color="black"), linetype="dashed") + 
  geom_line(aes(y=AN_SYS, color="green"), linetype="dashed") +
  scale_color_manual(name="Legend",
                     values = c("blue","red","black", "green"),
                     labels = c("Queue size - Analytical",
                                "Queue size - Simulation", 
                                "System size - Analytical", 
                                "System size - Simulation")) +
  theme(legend.position=c(.8,.2)) +
  xlab("Events") +
  ylab("Size") + 
  ggtitle("Average System/Queue Size")



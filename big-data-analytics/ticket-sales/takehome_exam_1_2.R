library(ggplot2)
library(dplyr)
library(tidyr)
library(scales)

Sys.setlocale("LC_TIME", "en_US.UTF-8")

#FOR TAKE-HOME EXAM

#Set your own working directory
setwd("/home/olaaun/big_data_analytics/take_home_exam")

data = read.csv("girlgeneration(utf8).csv", stringsAsFactors = FALSE)

#Create my_date column
data <- separate(data, CREATE_DATE, into = c( "TEMP_DATE", "AM_PM", "TIME" ), sep = " " )
data$my_date <- as.POSIXct(strptime( paste( data$TEMP_DATE,  data$TIME, sep = " " ), 
                                     format = "%Y/%m/%d %H:%M:%S" )) 
data$my_date[ data$AM_PM == "p.m." ] <- data$my_date[ data$AM_PM == "p.m." ] + 12*60*60


#PROBLEM 1
#Retrieve data related to floor 3
f3_member = data %>% filter(T_STANDARD_TICKET_TYPE_NAME == "member") %>% filter(grepl("Floor3", SEAT_REGION_NAME))
f3_nonmember = data %>% filter(T_STANDARD_TICKET_TYPE_NAME == "non-member") %>% filter(grepl("Floor3", SEAT_REGION_NAME))

#Find latest tickets sold
f3_member = f3_member %>% group_by(SEAT_ROW) %>%
  mutate(the_rank  = rank(my_date, ties.method = "random")) %>%
  filter(the_rank ==  max(the_rank)) 

f3_nonmember = f3_nonmember %>% select(SEAT_ROW, my_date) %>% group_by(SEAT_ROW) %>%
  mutate(the_rank  = rank(my_date, ties.method = "random")) %>%
  filter(the_rank == max(the_rank)) %>%
  arrange(SEAT_ROW) #Arrange because of lack of rows, which are added later

ggplot(f3_member, aes(x=SEAT_ROW, y=my_date)) + geom_line() + 
  geom_area( fill="blue", alpha=.2) + 
  coord_cartesian(ylim=c(min(f3_member$my_date),max(f3_member$my_date))) +
  ggtitle("Member: 3F's selling speed by row") + 
  labs(x="Seat row", y="Time")


#This is a workaround for plotting correctly 
#Some seat rows were not sold to non-members
#If row not in dataframe, set last sold ticket to underneath the shown coordinates.
min_date = min(f3_nonmember$my_date)
rows = 1:29
none = as.POSIXct(-1, origin="1970-1-1")
complete_rows = data.frame("SEAT_ROW"=rows, "my_date" = rep(none, length(rows)))
complete_rows$my_date[complete_rows$SEAT_ROW %in% f3_nonmember$SEAT_ROW] = f3_nonmember$my_date
f3_nonmember = complete_rows

ggplot(f3_nonmember, aes(x=SEAT_ROW, y=my_date)) + geom_line() + 
  geom_area( fill="blue", alpha=.2) + 
  coord_cartesian(ylim=c(min_date,max(f3_nonmember$my_date) )) +
  ggtitle("Non-member: 3F's selling speed by row") + 
  labs(x="Seat row", y="Time")

#PROBLEM 2
data = arrange(data, my_date)
sections = distinct(select(data, SEAT_REGION_NAME))
temp <- vector(mode = "list", length = nrow(sections))
#Add a count column to show how many tickets have been sold in section so far
for(i in 1:nrow(sections)){
  data_t = subset(data, SEAT_REGION_NAME == sections[i,])
  data_t$count = 1: nrow(data_t) 
  temp[[i]] <- data_t
}
data <- do.call( rbind, temp )

fb1_member = data %>% filter(T_STANDARD_TICKET_TYPE_NAME == "member") %>% filter(grepl("FloorB1", SEAT_REGION_NAME))
fb1_nonmember = data %>% filter(T_STANDARD_TICKET_TYPE_NAME == "non-member") %>% filter(grepl("FloorB1", SEAT_REGION_NAME)) 

ggplot(fb1_member, aes(x= my_date, y=count, color = SEAT_REGION_NAME)) + geom_line( size = 1 ) + 
  ggtitle("Member: Selling speed of floorB1 by section") +
  scale_x_datetime(labels = date_format("%b. %d \n %H:%M:%S"))
ggplot(fb1_nonmember, aes(x= my_date, y=count, color = SEAT_REGION_NAME)) + geom_line( size = 1 ) + 
  ggtitle("Non-member: Selling speed of floorB1 by section") +
  scale_x_datetime(labels = date_format("%b. %d") )

f2_red_member = data %>% filter(T_STANDARD_TICKET_TYPE_NAME == "member") %>% filter(grepl("red", SEAT_REGION_NAME)) %>% arrange(my_date)
f2_red_nonmember = data %>% filter(T_STANDARD_TICKET_TYPE_NAME == "non-member") %>% filter(grepl("red", SEAT_REGION_NAME)) %>% arrange(my_date)
f2_purple_member = data %>% filter(T_STANDARD_TICKET_TYPE_NAME == "member") %>% filter(grepl("purple", SEAT_REGION_NAME)) %>% arrange(my_date)
f2_purple_nonmember = data %>% filter(T_STANDARD_TICKET_TYPE_NAME == "non-member") %>% filter(grepl("purple", SEAT_REGION_NAME)) %>% arrange(my_date)

ggplot() + 
  geom_line(data=f2_red_member, aes(y=1:nrow(f2_red_member), x=f2_red_member$my_date), color='red') + 
  geom_line(data=f2_purple_member, aes(y=1:nrow(f2_purple_member), x=f2_purple_member$my_date), color='purple') +
  xlab("Time") + ylab("Number of tickets sold") + ggtitle("Member:Red vs Purple zone sale speed ")  +
  scale_x_datetime(labels = date_format("%b. %d \n %H:%M:%S"))

ggplot() + 
  geom_line(data=f2_red_nonmember, aes(y=1:nrow(f2_red_nonmember), x=f2_red_nonmember$my_date), color='red') + 
  geom_line(data=f2_purple_nonmember, aes(y=1:nrow(f2_purple_nonmember), x=f2_purple_nonmember$my_date), color='purple') +
  xlab("Time") + ylab("Number of tickets sold") + ggtitle("Non-member: Red vs Purple zone sale speed ") +
  scale_x_datetime(labels = date_format("%b. %d \n %H:%M:%S"))

#For finding a number for speed
rmem = nrow(f2_red_member)/as.numeric(difftime(max(f2_red_member$my_date),min(f2_red_member$my_date), unit="hour"))
pmem = nrow(f2_purple_member)/as.numeric(difftime(max(f2_purple_member$my_date),min(f2_purple_member$my_date), unit="hour"))
rnon = nrow(f2_red_nonmember)/as.numeric(difftime(max(f2_red_nonmember$my_date),min(f2_red_nonmember$my_date), unit="hour"))
pnon = nrow(f2_purple_nonmember)/as.numeric(difftime(max(f2_purple_nonmember$my_date),min(f2_purple_nonmember$my_date), unit="hour"))

total_speed_red = rmem*(nrow(f2_red_member)/(nrow(f2_red_member) + 
                                               nrow(f2_red_nonmember))) + rnon*(nrow(f2_red_nonmember)/(nrow(f2_red_member) + nrow(f2_red_nonmember)))

total_speed_purple = rmem*(nrow(f2_purple_member)/(nrow(f2_purple_member) + 
                                                     nrow(f2_purple_nonmember))) + rnon*(nrow(f2_purple_nonmember)/(nrow(f2_purple_member) + nrow(f2_purple_nonmember)))

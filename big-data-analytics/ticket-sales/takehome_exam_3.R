library(ggplot2)
library(dplyr)
library(tidyr)

#Set your own working directory
setwd("/home/olaaun/big_data_analytics/take_home_exam")

data = read.csv("ticketdata.csv", stringsAsFactors = FALSE)
colnames(data) <- c("TicketCode","SoldDate","TicketSiteCode","TicketSite","SoldTime","DisplayDate","OriginalPrice","SoldPrice","ExhibitionHall","SeatArea","Row","SeatNo","TicketName","URL","Gender","ZipCode","City","Birthday","Seatmap")

data$SoldDate = as.Date(data$SoldDate, format = "%Y-%m-%d")
data$SoldTime = as.Date(data$SoldTime, format = "%Y-%m-%d")

data = arrange(data, SoldDate)

#Number of tickets sold
data %>% 
  select(ExhibitionHall) %>%
  group_by(ExhibitionHall) %>%
  summarise(count=n()) %>%
  arrange(desc(count))

#Total revenue
data %>%
  group_by(ExhibitionHall) %>%
  summarise(sum=sum(SoldPrice)) %>%
  arrange(desc(sum))


#Average sale speed
#For every avenue, for every concert, calculate tickets_sold/time_taken
#For every avenue take average of concert sale speeds
avenues = unique(data[, c('ExhibitionHall')])
sale_speeds = data.frame(Avenue=character(length(avenues)), Speed=numeric(length(avenues)), stringsAsFactors = FALSE)
iteration = 1
for(avenue in avenues){
  concerts = data %>% filter(ExhibitionHall == avenue) %>% distinct(TicketCode)
  speeds = vector(length = nrow(concerts))
  if(nrow(concerts) < 5) next
  for(i in 1:nrow(concerts)){
    concert = concerts[i,]
    concert_data = data %>% filter(TicketCode == concert) %>% summarise(first=min(SoldDate), last = max(SoldDate), n=n())
    total_tickets_sold = concert_data$n
    if(total_tickets_sold <= 1){
      next
    } 
    first_ticket_sold = concert_data$first
    last_ticket_sold = concert_data$last
    duration = difftime(last_ticket_sold, first_ticket_sold, unit="days") + 1
    speeds[i] = total_tickets_sold/as.numeric(duration)
  }
  sale_speeds[iteration,] = c(avenue, mean(speeds))
  iteration = iteration + 1
}
sale_speeds$Speed = as.numeric(sale_speeds$Speed)
sale_speeds %>% arrange(desc(Speed))
  
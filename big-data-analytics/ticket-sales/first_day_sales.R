library(tidyr)
library(ggplot2)
library(data.table)

Sys.setlocale("LC_ALL", "cht")

#Set your own working directory
setwd("/home/olaaun/big_data_analytics/")

data  <- fread( "ticketdata.csv", stringsAsFactors = FALSE, header = TRUE, sep = ",", colClasses = "character" )
colnames(data) <- c("TicketCode","SoldDate","TicketSiteCode","TicketSite","SoldTime","DisplayDate","OriginalPrice","SoldPrice","ExhibitionHall","SeatArea","Row","SeatNo","TicketName","URL","Gender","ZipCode","City","Birthday","Seatmap")
data$SoldDate = as.Date(data$SoldDate, format = "%Y-%m-%d")

concerts = unique(data[, c('TicketCode')])
concerts = subset(concerts, !(TicketCode %in% data[OriginalPrice==10]$TicketCode))

#First day sales, one column for ticket name, one column for amount sold (1 is all tickets, 0.5 is half etc)
fds = data.frame(matrix("", ncol = 2, nrow = nrow(concerts)), stringsAsFactors = FALSE)
colnames(fds) = c("TicketCode", "RATIO_SOLD")

#Time it takes to sell out each concert
time_taken = data.frame(matrix("", ncol = 2, nrow = nrow(concerts)), stringsAsFactors = FALSE)
colnames(time_taken) = c("TicketCode", "TIME")

for(i in 1:nrow(concerts)){
  concert = concerts[i,]
  concert_data = data[TicketCode == concert]
  concert_data = concert_data[order(SoldDate),]
  
  total_tickets = nrow(concert_data)
  first_date = min(concert_data[,SoldDate])
  first_date_sales = nrow(concert_data[SoldDate==first_date])
  duration = difftime(concert_data$SoldDate[total_tickets*0.75], concert_data$SoldDate[1], units="days")
  fds[i,] = c(concert, first_date_sales/total_tickets, duration)
  time_taken[i,] = c(concert, duration)
}

fds$RATIO_SOLD = as.numeric(fds$RATIO_SOLD)
time_taken$TIME = as.numeric(time_taken$TIME)
time_taken$TIME[which(time_taken$TIME > 365)] = NA #Dataset is for one year
ggplot(data.frame(fds, time_taken),aes(x=TIME,y=RATIO_SOLD)) + geom_point(alpha = 0.25) + labs(y="First day ratio", x="Days to sell 75%")
mean(fds$RATIO_SOLD)
save(fds, file="first_day_sales.RData")


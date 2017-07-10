library(dplyr)
library(tidyr)

data = read.csv("/home/olaaun/Downloads/girlgeneration(utf8).csv", stringsAsFactors = FALSE)
Sys.setlocale("LC_TIME", "C")
seat_regions = unique(data[,c("SEAT_REGION_NAME")])

# Step 1 : separate the date row
data <- separate(data, CREATE_DATE, into = c( "DAY", "AM_PM", "TIME" ), sep = " " ) 
data2 = data %>%
  mutate(date = as.Date(DAY, "%Y/%m/%d"))
data$DAY = as.Date(data$DAY, "%Y/%m/%d")


print(head(data, 2))
days = unique(sort(data[,c("DAY")]))

print(days)
number_of_days = vector(length = length(seat_regions))
last_ticket_sold = vector(length = length(seat_regions))
k = 0
for(region in seat_regions){
  k = k + 1
  last_ticket_sold[k] = data %>%
         filter(SEAT_REGION_NAME==region) %>%
         summarise(max = max(DAY)) %>%
         match(days)
  number_of_seats = length(filter(data, SEAT_REGION_NAME==region))
  total = 0
  for(i in 1:length(days)){
    total = total + (i*data %>%
                              filter(SEAT_REGION_NAME==region, DAY==days[i]) %>%
                              summarise(total.count=n()))
  }
  
  number_of_days[k] = total/(8*length(data[data$SEAT_REGION_NAME == region,]))


}

names(last_ticket_sold) = days
barplot(last_ticket_sold, horiz=TRUE, cex.names=0.01)
text(seat_regions)
ggplot(test, aes(seat_regions, last_ticket_sold)) + geom_bar(stat="identity") +
       theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5)) + xlab("Zone") +
       ylab("Days") 



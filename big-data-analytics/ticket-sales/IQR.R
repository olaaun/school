library(dplyr)
library(tidyr)
library(ggplot2)

data = read.csv("/home/olaaun/Downloads/girlgeneration(utf8).csv", stringsAsFactors = FALSE)
Sys.setlocale("LC_TIME", "C")
seat_regions = unique(arrange(data,PRICE)[,c("SEAT_REGION_NAME")])

# Step 1 : separate the date row
data <- separate(data, CREATE_DATE, into = c( "TEMP_DATE", "AM_PM", "TIME" ), sep = " " ) 

#Change dates, so duration column is correctly calculated
data$TEMP_DATE[which(data$TEMP_DATE == "2010/10/09")] = "2010/09/20"
data$TEMP_DATE[which(data$TEMP_DATE == "2010/10/10")] = "2010/09/21"
data$TEMP_DATE[which(data$TEMP_DATE == "2010/10/11")] = "2010/09/22"
data$TEMP_DATE[which(data$TEMP_DATE == "2010/10/12")] = "2010/09/23"
data$TEMP_DATE[which(data$TEMP_DATE == "2010/10/13")] = "2010/09/24"
data$TEMP_DATE[which(data$TEMP_DATE == "2010/10/14")] = "2010/09/25"

# Step 2 : first ignore the p.m. part and create the date 
data$my_date <- as.POSIXct(strptime( paste( data$TEMP_DATE,  data$TIME, sep = " " ), 
                          format = "%Y/%m/%d %H:%M:%S" )) 
# Step 3 : add 12 hours(add in unit of seconds) to the data that are in the afternoon (i.e. p.m.)
data$my_date[ data$AM_PM == "p.m." ] <- data$my_date[ data$AM_PM == "p.m." ] + 12*60*60

data = arrange(data, my_date)

data$duration = as.numeric(difftime(data$my_date, data$my_date[1], units="mins"))

#Remove newly created columns, except duration
drops <- c("TEMP_DATE", "my_date", "AM_PM", "TIME")
data = data[ , !(names(data) %in% drops)]

iqr = vector(length = length(seat_regions))
k = 0

#For every region, calculuate iqr
for(region in seat_regions){
  region_frame = data[which(data$SEAT_REGION_NAME==region),]
  k = k + 1
  reg_length = nrow(region_frame)
  iqr[k] = (region_frame$duration[reg_length*0.75] + region_frame$duration[reg_length*0.25])/2
}

#Create datafra with results, and then plot it
iqr_frame = arrange(data.frame(iqr, seat_regions), iqr)
ggplot(iqr_frame, aes(seat_regions, iqr)) + geom_bar(stat="identity") +
    xlab("Zone") +
  ylab("Minutes") + coord_flip()


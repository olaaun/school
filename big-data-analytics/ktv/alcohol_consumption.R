library(ggplot2)
library(dplyr)
library(tidyr)
library(scales)

Sys.setlocale("LC_TIME", "en_US.UTF-8")

#Set your own working directory
setwd("/home/olaaun/big_data_analytics/final_project")

data = read.csv("customerBehavior3.csv", stringsAsFactors = FALSE)
data$OrderTime = as.POSIXct(data$OrderTime)
data$hour = format(data$OrderTime, format="%H")
drinks = c("啤酒類", "飲料類(不含調酒用)s", "調酒品", "其他酒類", "烈酒類", "調味酒類", "葡萄酒類", "開瓶費" )
drinks_english = c("Beer", "Other drinks", "Cocktail", "Other wine", "Spirits", "Flavored wine", "Wine", "Open bottle fee")
for(i in 1:length(drinks)) {
  data$MealType[data$MealType == drinks[i]] = drinks_english[i]
}

city_frame_names = c('Kaohsiung', 'Jiayi', 'Taoyuan', 'Taipei', 'Taipei', 'Taipei')
cities_codes = c('0113', '0112', '0108', '0107', '0114', 'K01 ')
cityFrame = data.frame(CityName=city_frame_names, StoreCode=cities_codes, stringsAsFactors = FALSE)
city_names = c('Kaohsiung', 'Jiayi', 'Taoyuan', 'Taipei')

plot_frame = data.frame(matrix("", ncol = 3, nrow = length(drinks_english)*length(city_names)), stringsAsFactors = FALSE)
colnames(plot_frame) = c("City", "Drink", "Percentage")
#Average alcohol spending per person
averages = c()

frame_index = 0
#For loop for calculating average spending and, what is being drunk
for(i in 1:length(city_names)) {
  codes = cityFrame %>% filter(CityName == city_names[i])
  city_data = data %>%
    filter(StoreCode %in% codes$StoreCode)
  drink_spending_sum = 0
  cat(city_names[i], "\n")
  percentages = c()
  for(dr in drinks_english) {
    frame_index = frame_index + 1
    dr_data = city_data %>%
      filter(MealType == dr)
    drink_spending = sum(dr_data$MealSpending)
    perc_drink = drink_spending/sum(city_data$MealSpending)
    percentages = c(percentages, perc_drink)
    drink_spending_sum = drink_spending_sum + drink_spending
    plot_frame[frame_index,] = c(city_names[i], dr, perc_drink)
  }
  people_sum =city_data %>%
    group_by(BillCode) %>%
    summarize(cust = sum(sum(CustomerNumber)/n())) 
  averages = c(averages, drink_spending_sum/sum(people_sum$cust))
}

#Plot percentage of drink spending
plot_frame$Percentage = as.numeric(plot_frame$Percentage)
ggplot(plot_frame, aes(City, Percentage, fill = Drink)) + 
  geom_bar(stat="identity") + 
  scale_fill_brewer(palette = "Set1") + xlab("City") +
  ggtitle("Percentage of MealSpending") +scale_y_continuous(labels = scales::percent) + 
  theme(plot.title = element_text(hjust = 0.5))

#Plot average alcohol spending per person
averages_frame = data.frame(City=city_names, Average=averages)
ggplot(averages_frame, aes(City, Average, fill=City)) + 
  geom_bar(stat="identity") + 
  scale_fill_brewer(palette = "Set1") + xlab("City") +
  guides(fill=FALSE) + ggtitle("Average spending per person (TWD)") + 
  scale_y_continuous(labels = scales::dollar) + 
  theme(plot.title = element_text(hjust = 0.5))

#Find purchase based on time
time_city_frame = data.frame(matrix("", ncol = 3, nrow = length(city_names)*24), stringsAsFactors = FALSE)
colnames(time_city_frame) = c("Hour", "City", "Percentage")
total_spending_sum = sum(data[data$MealType %in% drinks_english,]$MealSpending)
hours = unique(data$hour)
frame_index = 0
for(i in hours){
  hour_data = data %>%
    filter(hour == i) %>% 
    filter(MealType %in% drinks_english)
  for(city in city_names) {
    codes = cityFrame %>% filter(CityName == city)
    frame_index = frame_index + 1
    city_data = hour_data %>%
      filter(StoreCode %in% codes$StoreCode) %>%
      summarise(drink_sum = sum(MealSpending))
    test_sum = test_sum + city_data$drink_sum
    time_city_frame[frame_index,] = c(i, city, city_data$drink_sum / total_spending_sum)
  }
}
time_city_frame = arrange(time_city_frame, Hour)
time_city_frame$Hour = as.numeric(time_city_frame$Hour)
time_city_frame$Percentage = as.numeric(time_city_frame$Percentage)

ggplot(time_city_frame, aes(Hour, Percentage, fill = City)) + 
  geom_bar(stat="identity") + 
  scale_fill_brewer(palette = "Set1") + xlab("Hour") +
  ggtitle("Time Distribution") + scale_x_continuous(breaks = seq(0,23,5)) +
  scale_y_continuous(labels = scales::percent) + theme(plot.title = element_text(hjust = 0.5))

 sum(time_city_frame %>% 
  filter(Hour >= 8 & Hour <= 18) %>% 
  select(Percentage))
 
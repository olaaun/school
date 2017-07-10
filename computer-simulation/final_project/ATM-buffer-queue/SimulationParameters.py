maxArrivals = 500000
maxTime = 12000000
arrival_rate =124 # mean, Mbps
service_rate = 155   # mean, Mbps
packet_size = 53 #byte
lambda_cell = (arrival_rate*10**6)/(packet_size*8) #Arrival rate of cells
service_cell = (service_rate*10**6)/(packet_size*8) #Service rate of cells
seed= 5 #Random seed

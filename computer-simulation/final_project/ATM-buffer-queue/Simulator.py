import simpy
import random
import StatisticalCounter as st
import MonitoredResource as mr
import ATM
from SimulationParameters import *

def main():
    #Setup simulation environment
    random.seed(seed)
    stat_counter = st.StatisticalCounter()
    env = simpy.Environment()
    res = mr.MonitoredResource(stat_counter = stat_counter,env = env, capacity = 1)
    simul = ATM.CellGenerator()
    env.process(simul.generate(env = env, resource=res, stat_counter = stat_counter))
    #Run simulation
    env.run(until = maxTime)

    print("Average number in queue: " + str(stat_counter.calculate_avg_num_in_queue()))
    print("Average number in system: " + str(stat_counter.calculate_avg_num_in_system()))
    print("Average queue wait: " + str(stat_counter.calculate_avg_queue_wait()))
    print("Average system wait: " + str(stat_counter.calculate_avg_system_wait()))

    #Uncomment this line to write results to file, NB: SLOW!
    #stat_counter.write_to_file()



if __name__ == "__main__":
    main()

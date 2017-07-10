import simpy
from StatisticalCounter import StatisticalCounter
import random
from SimulationParameters import *
import math

"""
Generate packets, following a Poisson process
"""
class CellGenerator():
    def generate(self, env, resource, stat_counter):
        for i in range(maxArrivals):
            cell = CellArrival(id = "Packet " + str(i))
            env.process(cell.arrive(env, resource, stat_counter))
            time_next_arrival = random.expovariate(lambda_cell)
            yield env.timeout(time_next_arrival)


    """ Cell arrives, is processed and leaves """
class CellArrival():
    id = None

    def __init__(self, id):
        self.id = id

    def arrive(self, env, res, stat_counter):
        #Request resource
        #Places packet in queue if resource is busy
        with res.request() as request:
            arrive = env.now
            print(self.id + " arrives at time " + str(arrive))
            #Waits until request is granted
            yield request
            queue_wait = env.now-arrive
            stat_counter.add_queue_wait_time(queue_wait)
            print( self.id + " waited in queue " + str(queue_wait))
            #Process packet, before releasing resource
            service_time = 1/service_cell
            yield env.timeout(service_time)
            #res.release(request = request)
            system_wait = env.now - arrive
            stat_counter.add_system_wait_time(system_wait)
            print(self.id + " waited in system " +  str(env.now))

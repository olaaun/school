import simpy
from collections import namedtuple
from SimulationParameters import *

class MonitoredResource(simpy.Resource):

    DataInstance = None
    stat_counter = None

    def __init__(self, stat_counter = stat_counter, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stat_counter = stat_counter
        self.DataInstance = namedtuple("DataInstance", "event_time number_in_queue number_in_resource")

    #Request resource, update statistical counter
    def request(self, *args, **kwargs):
        data_instance = self.get_data_instance()
        self.stat_counter.add_event_data(data_instance)
        return super().request(*args, **kwargs)

    #Release resource, update statistical counter
    def release(self, *args, **kwargs):
        data_instance = self.get_data_instance()
        self.stat_counter.add_event_data(data_instance)
        return super().release(*args, **kwargs)

    #Current simulation state
    def get_data_instance(self):
        return self.DataInstance(event_time = self._env.now, number_in_queue = len(self.queue), number_in_resource =super().count)

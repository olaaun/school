from SimulationParameters import *
from csv import writer

class StatisticalCounter:
    event_data = None
    queue_wait_times = None
    system_wait_times = None

    def __init__(self):
        self.event_data = []
        self.queue_wait_times = []
        self.system_wait_times = []

    def add_event_data(self, entry):
        self.event_data.append(entry)

    def add_queue_wait_time(self, qwt):
        self.queue_wait_times.append(qwt)

    def add_system_wait_time(self, swt):
        self.system_wait_times.append(swt)

    #Average number in queue
    def calculate_avg_num_in_queue(self):
        s = 0
        for i in range(len(self.event_data)-1):
            time_diff = self.event_data[i + 1].event_time - self.event_data[i].event_time
            num_in_queue = self.event_data[i+1].number_in_queue
            s += (time_diff*num_in_queue)
        s = s/self.event_data[-1].event_time
        return s

    #Average number in system
    def calculate_avg_num_in_system(self):
        s = 0
        for i in range(len(self.event_data)-1):
            time_diff = self.event_data[i + 1].event_time - self.event_data[i].event_time
            num_in_sys = self.event_data[i+1].number_in_queue + self.event_data[i+1].number_in_resource
            s += (time_diff*num_in_sys)
        s = s/self.event_data[-1].event_time
        return s

    #Average waiting time in queue
    def calculate_avg_queue_wait(self):
        return sum(self.queue_wait_times)/len(self.queue_wait_times)

    #Average waiting time in system
    def calculate_avg_system_wait(self):
        return sum(self.system_wait_times)/len(self.system_wait_times)


    def write_to_file(self):
        f = writer(open("sys-wait.csv", "w"))
        f.writerow(["SYSWAITTIME", "ARRIVALS"])
        for i in range(len(self.system_wait_times)):
            f.writerow([sum(self.system_wait_times[:i+1])/(i+1), i])
        print("Done with sys_wait")
        t = writer(open("q-wait.csv", "w"))
        t.writerow(["QWAITTIME", "ARRIVALS"])
        for i in range(len(self.queue_wait_times)):
            t.writerow([sum(self.queue_wait_times[:i+1])/(i+1), i])
        print("Done with q_wait")
        s_f = writer(open("sys-num.csv", "w"))
        q_f = writer(open("q-num.csv", "w"))
        s = 0
        q = 0
        s_f.writerow(["SYSNUM", "EVENTS"])
        q_f.writerow(["QNUM", "EVENTS"])
        for i in range(len(self.event_data) - 1):
            time_diff = self.event_data[i + 1].event_time - self.event_data[i].event_time
            num_in_sys = self.event_data[i+1].number_in_queue + self.event_data[i+1].number_in_resource
            num_in_queue = num_in_sys - self.event_data[i+1].number_in_resource
            s += (time_diff*num_in_sys)
            q += (time_diff*num_in_queue)
            s_f.writerow([s/self.event_data[i + 1].event_time, i])
            q_f.writerow([q/self.event_data[i + 1].event_time, i])
        print("Done with sys/q number")

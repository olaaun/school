
/* External definitions for single-server queueing system. */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "lcgrand.h"  /* Header file for random-number generator. */
#include <iostream>
using namespace std;
#define MAX_ARRIVALS 100  /* Limit on queue length. */
#define NUM_SERVERS 5
#define BUSY      1  /* Mnemonics for server's being busy */
#define IDLE      0  /* and idle. */
int next_event_type, num_custs_delayed, num_delays_required, num_events,
    num_in_q, server_status[NUM_SERVERS], queue_limit, num_custs_blocked, arrivals;
float area_num_in_q, area_server_status, mean_interarrival, mean_service,
      sim_time, time_last_event, time_next_event[3], server_times[NUM_SERVERS],
      total_of_delays;
FILE  *infile, *outfile;
void  initialize(void);
void  timing(void);
void  arrive(void);
void  depart(void);
void  report(void);
void  update_time_avg_stats(void);
float expon(float mean);
void set_next_departure(void);
main()  /* Main function. */
{
        /* Open input and output files. */
        outfile = fopen("mm3.out", "w");
        /* Specify the number of events for the timing function. */
        num_events = 2;
        /* Read input parameters. */
        float mean_interarrival_rates [3] = {0.6, 0.75, 0.9};
        for(int i = 0; i < 3; i++) {
                fprintf(outfile, "\n\n-----------------------------\n\n");
                mean_interarrival = 1/mean_interarrival_rates[i];

                /* Initialize the simulation. */
                initialize();
                /* Run the simulation while more delays are still needed. */

                fprintf(outfile, "Single-server queueing system\n\n");
                fprintf(outfile, "Mean service time%16.3f minutes\n\n", mean_service);
                fprintf(outfile, "Number of customers%14d\n\n", num_delays_required);
                fprintf(outfile, "Mean interarrival time%11.3f minutes\n\n",mean_interarrival);

                while (arrivals < MAX_ARRIVALS) {
                        timing();
                        /* Update time-average statistical accumulators. */
                        update_time_avg_stats();
                        /* Invoke the appropriate event function. */
                        switch (next_event_type) {
                        case 1:
                                arrive();
                                break;
                        case 2:
                                depart();
                                break;
                        }
                }
                report();
        }
        /* Invoke the report generator and end the simulation. */

        fclose(outfile);
        return 0;

}
void initialize(void)  /* Initialization function. */
{

        /* Initialize the simulation clock. */
        mean_service = 5;
        arrivals = 0;
        sim_time = 0.0;
        /* Initialize the state variables. */
        for(int i = 0; i < NUM_SERVERS; i++) {
                server_status[i] = IDLE;
                server_times[i] = 1.0e+30;
        }
        num_in_q        = 0;
        time_last_event = 0.0;
        /* Initialize the statistical counters. */
        num_custs_delayed  = 0;
        total_of_delays    = 0.0;
        area_num_in_q      = 0.0;
        area_server_status = 0.0;
        num_custs_blocked = 0;
        /* Initialize event list.  Since no customers are present, the departure
           (service completion) event is eliminated from consideration. */

        time_next_event[1] = sim_time + expon(mean_interarrival);

        time_next_event[2] = 1.0e+30;
}
void timing(void)  /* Timing function. */
{
        int i;
        float min_time_next_event = 1.0e+29;
        next_event_type = 0;
        /* Determine the event type of the next event to occur. */
        for (i = 1; i <= num_events; ++i)
                if (time_next_event[i] < min_time_next_event) {
                        min_time_next_event = time_next_event[i];
                        next_event_type     = i;
                }
        /* Check to see whether the event list is empty. */
        if (next_event_type == 0) {
                /* The event list is empty, so stop the simulation. */
                fprintf(outfile, "\nEvent list empty at time %f", sim_time);
                exit(1);
        }
        /* The event list is not empty, so advance the simulation clock. */
        sim_time = min_time_next_event;
}
void arrive(void)  /* Arrival event function. */
{
        arrivals++;
        float delay;
        /* Schedule next arrival. */
        time_next_event[1] = sim_time + expon(mean_interarrival);
        /* Check to see whether servers are busy. */
        int available_server = -1;
        for(int i = 0; i < NUM_SERVERS; i++) {
                if(server_status[i] == IDLE) {
                        available_server = i;
                }
        }
        if (available_server == -1) {
                num_custs_blocked++;
        }
        else {
                /* Server is idle, so arriving customer has a delay of zero.  (The
                   following two statements are for program clarity and do not affect
                   the results of the simulation.) */
                server_status[available_server] = BUSY;
                /* Schedule a departure (service completion). */
                float service_time = expon(mean_service);
                server_times[available_server] = sim_time + expon(mean_service);
                set_next_departure();

        }
}
void depart(void)  /* Departure event function. */
{
        int i;
        float delay;
        int departing_server = -1;
        float min_time =1.0e+29;
        for(int i = 0; i < NUM_SERVERS; i++) {
                if(server_times[i] < min_time) {
                        departing_server = i;
                        min_time = server_times[i];
                }
        }

        server_status[departing_server]      = IDLE;
        server_times[departing_server] = 1.0e+30;

        set_next_departure();
}
void report(void)  /* Report generator function. */
{
        /* Compute and write estimates of desired measures of performance. */
        fprintf(outfile, "\n\nRoh%10.3f \n\n",
                1/mean_interarrival);
        fprintf(outfile, "Blocking probability %10.3f\n\n",
                (double) num_custs_blocked / arrivals);
        fprintf(outfile, "Time simulation ended%12.3f minutes\n", sim_time);
}
void update_time_avg_stats(void)  /* Update area accumulators for time-average
                                     statistics. */
{
        float time_since_last_event;
        /* Compute time since last event, and update last-event-time marker. */
        time_since_last_event = sim_time - time_last_event;
        time_last_event       = sim_time;
        /* Update area under number-in-queue function. */
        area_num_in_q      += num_in_q * time_since_last_event;
}
void set_next_departure(void)
{
        float min_time_next_event = 1.0e+29;
        for(int i = 0; i < NUM_SERVERS; i++) {
                if(server_times[i] < min_time_next_event) {
                        min_time_next_event = server_times[i];
                }
        }
        time_next_event[2] = min_time_next_event;
}
float expon(float mean)  /* Exponential variate generation function. */
{
        /* Return an exponential random variate with mean "mean". */
        return -mean * log(lcgrand(1));
}

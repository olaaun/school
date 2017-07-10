
/* External definitions for single-server queueing system. */
#include <stdio.h>
#include<string.h>
#include <stdlib.h>
#include <math.h>
#include "lcgrand.h"  /* Header file for random-number generator. */
#include <iostream>
using namespace std;
#define Q_LIMIT 10000  /* Limit on queue length. */
#define BUSY      1  /* Mnemonics for server's being busy */
#define IDLE      0  /* and idle. */
int next_event_type, num_custs_delayed[3], num_delays_required, num_events,
    num_in_q, server_status, input_classes[Q_LIMIT+1];
float mean_interarrival, mean_service,
      sim_time, time_arrival[Q_LIMIT + 1], time_last_event, time_next_event[4],
      total_of_delays, total_of_system_delays[3], type_arrival_rates[3], type_service_rate[3];
FILE  *outfile;
void  initialize(void);
void  timing(void);
void  arrive(int type);
void  depart(void);
void  report(void);
float expon(float mean);
main()  /* Main function. */
{

        outfile = fopen("mm2.out", "w");
        /* Specify the number of events for the timing function. */
        num_events = 3;

        float service_rates [2][3] = {{-1.0, 1.0, 1.0}, {-1.0, 1.0, 1.5}};

        /* Read input parameters. */
        fprintf(outfile, "Single-server queueing system\n\n");
        fprintf(outfile, "Mean service time%16.3f minutes\n\n", 1.0);
        fprintf(outfile, "Number of customers%14d\n\n", 100);
        for(int i = 0; i < 2; i++) {
                fprintf(outfile, "\n\n-----------------------------\n\n");
                memcpy(type_service_rate, service_rates[i], sizeof(type_service_rate));
                /* Write report heading and input parameters. */

                fprintf(outfile, "Mean service time%11.3f minutes (class I), %11.3f minutes (class II)\n\n",
                        type_service_rate[1], type_service_rate[2]);

                /* Initialize the simulation. */
                initialize();
                /* Run the simulation while more delays are still needed. */

                while (num_custs_delayed[1] + num_custs_delayed[2] < num_delays_required) {
                        /* Determine the next event. */
                        timing();
                        /* Invoke the appropriate event function. */
                        switch (next_event_type) {
                        case 1:
                                arrive(1);
                                break;
                        case 2:
                                arrive(2);
                                break;
                        case 3:
                                depart();
                                break;
                        }
                }
                report();
        }

        fclose(outfile);
        return 0;

}
void initialize(void)  /* Initialization function. */
{
        type_arrival_rates[1] = 0.3;
        type_arrival_rates[2] = 0.6;
        mean_service = 1;
        num_delays_required = 100;
        /* Initialize the simulation clock. */
        sim_time = 0.0;
        /* Initialize the state variables. */
        server_status   = IDLE;
        num_in_q        = 0;
        time_last_event = 0.0;
        /* Initialize the statistical counters. */
        num_custs_delayed[1]  = 0;
        num_custs_delayed[2] = 0;
        total_of_delays    = 0.0;
        total_of_system_delays[1] = 0.0;
        total_of_system_delays[2] = 0.0;
        /* Initialize event list.  Since no customers are present, the departure
           (service completion) event is eliminated from consideration. */
        time_next_event[1] = sim_time + expon(type_arrival_rates[1]);
        time_next_event[2] = sim_time + expon(type_arrival_rates[2]);
        time_next_event[3] = 1.0e+30;
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
void arrive(int type_id)  /* Arrival event function. */
{
        float delay;
        /* Schedule next arrival. */
        float arr = expon(type_arrival_rates[type_id]);
        time_next_event[type_id] = sim_time + arr;
        /* Check to see whether server is busy. */
        if (server_status == BUSY) {
                /* Server is busy, so increment number of customers in queue. */
                ++num_in_q;
                /* Check to see whether an overflow condition exists. */
                if (num_in_q > Q_LIMIT) {
                        /* The queue has overflowed, so stop the simulation. */

                        fprintf(outfile, "\nOverflow of the array time_arrival at");
                        fprintf(outfile, " time %f", sim_time);
                        exit(2);
                }
                /* There is still room in the queue, so store the time of arrival of the
                   arriving customer at the (new) end of time_arrival. */
                time_arrival[num_in_q] = sim_time;
                input_classes[num_in_q] = type_id;
        }
        else {
                /* Server is idle, so arriving customer has a delay of zero.  (The
                   following two statements are for program clarity and do not affect
                   the results of the simulation.) */
                delay            = 0.0;
                total_of_delays += delay;
                /* Increment the number of customers delayed, and make server busy. */
                ++num_custs_delayed[type_id];
                server_status = BUSY;
                /* Schedule a departure (service completion). */
                time_next_event[3] = sim_time + expon(type_service_rate[type_id]);
        }
}
void depart(void)  /* Departure event function. */
{
        int i;
        float delay;
        /* Check to see whether the queue is empty. */
        if (num_in_q == 0) {
                /* The queue is empty so make the server idle and eliminate the
                   departure (service completion) event from consideration. */
                server_status      = IDLE;
                time_next_event[3] = 1.0e+30;
        }
        else {
                /* The queue is nonempty, so decrement the number of customers in
                   queue. */
                --num_in_q;
                int type = input_classes[1];

                /* Compute the delay of the customer who is beginning service and update
                   the total delay accumulator. */
                delay            = sim_time - time_arrival[1];
                total_of_delays += delay;
                /* Increment the number of customers delayed, and schedule departure. */
                ++num_custs_delayed[type];
                float serv_t = expon(type_service_rate[type]);
                total_of_system_delays[type] += delay + serv_t;
                time_next_event[3] = time_arrival[1]  +serv_t;
                /* Move each customer in queue (if any) up one place. */
                for (i = 1; i <= num_in_q; ++i) {
                        time_arrival[i] = time_arrival[i + 1];
                        input_classes[i] = input_classes[i+1];
                }
        }
}
void report(void)  /* Report generator function. */
{
        /* Compute and write estimates of desired measures of performance. */
        fprintf(outfile, "\n\nClass 1: \n");
        fprintf(outfile, "Mean delay in system%11.3f minutes\n\n",
                total_of_system_delays[1] / num_custs_delayed[1]);
        fprintf(outfile, "Class 2: \n");
        fprintf(outfile, "Mean delay in system%11.3f minutes\n\n",
                total_of_system_delays[2] / num_custs_delayed[2]);

        fprintf(outfile, "Time simulation ended%12.3f minutes\n", sim_time);
}

float expon(float mean)  /* Exponential variate generation function. */
{
        /* Return an exponential random variate with mean "mean". */

        return -mean * log(lcgrand(1));
}

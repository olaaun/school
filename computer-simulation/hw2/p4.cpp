
/* External definitions for single-server queueing system. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "lcgrand.h"  /* Header file for random-number generator. */
#include <iostream>
using namespace std;
#define Q_LIMIT 100  /* Limit on queue length. */
#define BUSY      1  /* Mnemonics for server's being busy */
#define IDLE      0  /* and idle. */
#define INF 2147483647 /* Set infinity as max int */
int next_event_type, num_custs_delayed[5], num_delays_required, num_events,
    num_in_q[5], server_status[5], queue_limits[5];
float mean_interarrival, mean_service,
      sim_time, time_arrival[5][10000] /*big enough*/, time_last_event, time_next_event[6],
      total_of_delays, total_of_system_delays[5];
FILE  *outfile;
void  initialize(void);
void  timing(void);
void  arrive(int queue);
void  depart(int queue);
void  report(void);
float expon(float mean);
main()  /* Main function. */
{

        outfile = fopen("mm4.out", "w");
        /* Specify the number of events for the timing function. */
        num_events = 5;
        float mean_interarrival_rates [5] = {0.15, 0.3, 0.45,  0.6, 0.75};
        /* Read input parameters. */
        fprintf(outfile, "Single-server queueing system\n\n");
        fprintf(outfile, "Mean service time%16.3f minutes\n\n", 1.0);
        fprintf(outfile, "Number of customers%14d\n\n", 100);
        for(int i = 0; i < 5; i++) {
                fprintf(outfile, "\n\n-----------------------------\n\n");
                mean_interarrival = mean_interarrival_rates[i];
                /* Write report heading and input parameters. */

                fprintf(outfile, "Mean interarrival time%11.3f minutes\n\n",
                        mean_interarrival);

                /* Initialize the simulation. */
                initialize();
                /* Run the simulation while more delays are still needed. */

                while (num_custs_delayed[4] < num_delays_required) {
                        /* Determine the next event. */
                        timing();
                        /* Invoke the appropriate event function. */
                        switch (next_event_type) {
                        case 1:
                                arrive(1);
                                break;
                        case 2:
                                depart(1);
                                break;
                        case 3:
                                depart(2);
                                break;
                        case 4:
                                depart(3);
                                break;
                        case 5:
                                depart(4);
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
        mean_service = 1;
        num_delays_required = 100;
        /* Initialize the simulation clock. */
        sim_time = 0.0;
        /* Initialize the state variables. */
        server_status[1]   = IDLE;
        server_status[2] = IDLE;
        server_status[3]   = IDLE;
        server_status[4] = IDLE;
        num_in_q[1]        = 0;
        num_in_q[2] = 0;
        num_in_q[3] = 0;
        num_in_q[4] = 0;
        time_last_event = 0.0;
        /* Initialize the statistical counters. */
        num_custs_delayed[1]  = 0;
        num_custs_delayed[2]  = 0;
        num_custs_delayed[3]  = 0;
        num_custs_delayed[4]  = 0;
        total_of_delays    = 0.0;
        total_of_system_delays[1] = 0.0;
        total_of_system_delays[2] = 0.0;
        total_of_system_delays[3] = 0.0;
        total_of_system_delays[4] = 0.0;
        queue_limits[1] = INF;
        queue_limits[2] = INF;
        queue_limits[3] = INF;
        queue_limits[4] = INF;
        /* Initialize event list.  Since no customers are present, the departure
           (service completion) event is eliminated from consideration. */
        time_next_event[1] = sim_time + expon(mean_interarrival);

        time_next_event[2] = 1.0e+30;
        time_next_event[3] = 1.0e+30;
        time_next_event[4] = 1.0e+30;
        time_next_event[5] = 1.0e+30;

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
void arrive(int queue)  /* Arrival event function. */
{
        float delay;
        /* Schedule next arrival. */
        if(queue == 1) {
                time_next_event[1] = sim_time + expon(mean_interarrival);
        } /* Check to see whether server is busy. */
        if (server_status[queue] == BUSY) {
                /* Server is busy, so increment number of customers in queue. */

                /* Check to see whether an overflow condition exists. */
                if (num_in_q[queue] + 1 > queue_limits[queue]) {
                        /* The queue has overflowed, so stop the simulation. */
                        cout << "Overflow " << num_in_q[queue] <<endl;
                        return;
                }
                ++num_in_q[queue];
                /* There is still room in the queue, so store the time of arrival of the
                   arriving customer at the (new) end of time_arrival. */

                time_arrival[queue][num_in_q[queue]] = sim_time;
        }
        else {
                /* Server is idle, so arriving customer has a delay of zero.  (The
                   following two statements are for program clarity and do not affect
                   the results of the simulation.) */
                delay            = 0.0;
                total_of_delays += delay;
                /* Increment the number of customers delayed, and make server busy. */
                ++num_custs_delayed[queue];
                server_status[queue] = BUSY;
                /* Schedule a departure (service completion). */
                time_next_event[queue + 1] = sim_time + expon(mean_service);
        }
}
void depart(int queue)  /* Departure event function. */
{
        int i;
        float delay;
        /* Check to see whether the queue is empty. */
        if (num_in_q[queue] == 0) {
                /* The queue is empty so make the server idle and eliminate the
                   departure (service completion) event from consideration. */
                server_status[queue]      = IDLE;
                time_next_event[queue + 1] = 1.0e+30;
        }
        else {
                /* The queue is nonempty, so decrement the number of customers in
                   queue. */
                --num_in_q[queue];

                /* Compute the delay of the customer who is beginning service and update
                   the total delay accumulator. */
                delay            = sim_time - time_arrival[queue][1];
                total_of_delays += delay;
                /* Increment the number of customers delayed, and schedule departure. */
                ++num_custs_delayed[queue];
                float serv_t = expon(mean_service);
                total_of_system_delays[queue] += delay;
                time_next_event[queue + 1] = time_arrival[queue][1]  + serv_t;
                /* Move each customer in queue (if any) up one place. */
                for (i = 1; i <= num_in_q[queue]; ++i) {
                        time_arrival[queue][i] = time_arrival[queue][i + 1];
                }

        }
        if(queue != 4) {arrive(queue + 1); } /* Arrive at next queue */
}
void report(void)  /* Report generator function. */
{
        /* Compute and write estimates of desired measures of performance. */
        fprintf(outfile, "\nQueue 1\n");
        fprintf(outfile, "Mean delay in system%11.3f minutes\n\n",
                total_of_system_delays[1] / num_custs_delayed[1]);
        fprintf(outfile, "Number of cust in queue %13d\n\n",
                num_custs_delayed[1]);
        fprintf(outfile, "\nQueue 2\n");
        fprintf(outfile, "Mean delay in system%11.3f minutes\n\n",
                total_of_system_delays[2] / num_custs_delayed[2]);
        fprintf(outfile, "Number of cust in queue %13d\n\n",
                num_custs_delayed[2]);
        fprintf(outfile, "\nQueue 3\n");
        fprintf(outfile, "Mean delay in system%11.3f minutes\n\n",
                total_of_system_delays[3] / num_custs_delayed[3]);
        fprintf(outfile, "Number of cust in queue %13d\n\n",
                num_custs_delayed[3]);
        fprintf(outfile, "\nQueue 4\n");
        fprintf(outfile, "Mean delay in system%11.3f minutes\n\n",
                total_of_system_delays[4] / num_custs_delayed[4]);
        fprintf(outfile, "Number of cust in queue %13d\n\n",
                num_custs_delayed[4]);
}

float expon(float mean)  /* Exponential variate generation function. */
{
        /* Return an exponential random variate with mean "mean". */

        return -mean * log(lcgrand(1));
}

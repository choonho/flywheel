# Sensor

iperf like network bandwidth and latency check tool

# Server

The sensor.py file works both server and client.

## Server

~~~bash
python sensor.py -s
~~~

## Client

You can check the option by

~~~bash
python sensor.py -c <host> -P <parallel> -t <time>
~~~

# Client Example

~~~bash
sunshout@choonho:~/flywheel/flywheel$ ./sensor.py -c 127.0.0.1 -P 2 -t 10

#################################################
Time                Bandwidth       Latency(ms)
-------------------------------------------------
22:36:02            2.3370 Gbps     0.3570
 +[Thread:0]        1.0840 Gbps
 +[Thread:1]        1.2530 Gbps

22:36:04            2.3995 Gbps     0.0410
 +[Thread:0]        1.1414 Gbps
 +[Thread:1]        1.2582 Gbps

22:36:06            2.3367 Gbps     0.0770
 +[Thread:0]        1.1655 Gbps
 +[Thread:1]        1.1712 Gbps

22:36:08            2.4300 Gbps     0.0601
 +[Thread:0]        1.2043 Gbps
 +[Thread:1]        1.2257 Gbps

22:36:10            2.4333 Gbps     0.0786
 +[Thread:0]        1.2036 Gbps
 +[Thread:1]        1.2297 Gbps


------------ Summary ----------------------------
10 seconds      2.3879 Gbps     0.1227
 +[Thread:0]        1.1602 Gbps
 +[Thread:1]        1.2278 Gbps
~~~

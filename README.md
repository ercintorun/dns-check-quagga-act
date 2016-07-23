# dns-check-quagga-act
One way to  implement Anycast DNS is to use BGP on a DNS server and announce Anycast DNS IP block with BGP. A free solution to have BGP capability on a Linux server is to use Quagga BGPD daemon. This script performs checks a  DNS servers ability to respond to type A DNS queries roughly 60-70 times in a minute. Based on the answer and whether the "bgpd" daemon works, script stops or starts bgpd daemon and logs its action for each control to a log file.  


# Parameters

script_run_time: Determines how many seconds the script should loop
test_domain: The A record DNS server is to be queried with
server_to_test: The DNS server that is to be queried. Default is 127.0.0.1, local server. 

Script run time value is configured to 60 seconds by default. As script will work for only 60 seconds with default settings,executing the script every minute with the help of cron will result in continious/endless control without the effort for daemonizing the script. 

#Logging Level 

Script has 2 logging level you could configure, which are INFO and WARNING. If you would like to keep the log file smalleri, you could change "level=logging.INFO" to "level=logging.WARNING", by which succesful checks does not log anything to log file.

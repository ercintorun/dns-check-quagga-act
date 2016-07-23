# -*- coding: utf-8 -*-
import dns.resolver, psutil, commands, time, logging, datetime

###VARIABLES 
script_run_time = 60 
test_domain = "www.test.com"
server_to_test = ["127.0.0.1"]	

#############
#############
#############
###logging file folder and logging level config
logging.basicConfig(filename='/var/log/dnsscript.log', filemode='a', level=logging.INFO,
                    format='%(asctime)s [%(name)s] %(levelname)s (%(threadName)-10s): %(message)s')

###define dns servers, parameters
anycast_server1 = dns.resolver.Resolver()
anycast_server1.timeout=1.0
anycast_server1.lifetime=1.0
anycast_server1.nameservers = server_to_test	
			
###time to run the script
starttime = time.time()
timeout = time.time()+ script_run_time

###kill process function 
def kill_process(PROCNAME):
	for proc in psutil.process_iter():
		if proc.name() == PROCNAME:
			proc.kill()

###start a loop with an amount of script_run_time value

while True:
	time.sleep(0.8)
	if time.time()> timeout:
		break
	else:
###get all daemon names into list
		daemon_list=[]
		for proc in psutil.process_iter():
			daemon_list.append(proc.name())
###start the control
		if "bgpd" not in daemon_list: 
			try:
				answers = anycast_server1.query(test_domain, "A")
				commands.getoutput ("/etc/init.d/bgpd restart")
				logging.warning("DNS successful, BGP daemon is down, bgpd restarted")
				time.sleep(2) #give bgp 2 second to get up again
			except dns.resolver.NXDOMAIN:
				logging.warning("DNS exception: No such domain, BGP daemon is already down, no change done")
			except dns.resolver.Timeout:
				logging.warning("DNS exception: Timed out while resolving, BGP daemon is already down, no change done ") 
			except dns.exception.DNSException:
				logging.warning("DNS exception: Unhandled exception, BGP daemon is already down, no change done") 
		else:
			try:
				answers = anycast_server1.query(test_domain, "A")
				for data in answers: 
					resolved = data
				logging.info("DNS successful, nothing has been changed, last resolved ip is: "+str(data))
			except dns.resolver.NXDOMAIN:
				kill_process("bgpd")
				logging.warning("DNS exception: No such domain, BGP daemon terminated")
			except dns.resolver.Timeout:
				kill_process("bgpd")
				logging.warning("DNS exception: Timed out while resolving, BGP daemon terminated")
			except dns.exception.DNSException:
				kill_process("bgpd")
				logging.warning("DNS exception: Unhandled exception, BGP daemon terminated")
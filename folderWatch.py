import inotify.adapters

def main():
	i = inotify.adapters.Inotify()
	
	i.add_watch('/opt/python_fun/test_watch/')
	
	for event in i.event_gen():
		processSignal()
		processEvent(event)
		
def readConfig(config_location):
	#TODO read the config from json file provided
	print("______Processing Config_______")
	
def instantiateTaskQueue(queue_config):
	#TODO setup the RabbitMQ task queue to take file tasks
	print("______Configuring Task Queue_______")
	

def processEvent(event):
	print("The Event is: ")
	print(event)
	#TODO process file event
	
def processSignals():
	print("Processing signals...")
	#TODO process signals.
if __name__ == '__main__':
	main()

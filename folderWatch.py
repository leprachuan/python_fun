import inotify.adapters

def main():
	i = inotify.adapters.Inotify()
	
	i.add_watch('/opt/python_fun/test_watch/')
	
	for event in i.event_gen():
		print("The Event is: ")
		print(event)
	
if __name__ == '__main__':
	main()

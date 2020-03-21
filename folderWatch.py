import inotify.adapters

def main():
	i = inotify.adapters.Inotify()
	
	i.add_watch('/opt/python_fun/test_watch/')
	
	with open('/opt/python_fun/test_watch/test_file','w'):
		pass
		for event in i.event_gen(yield_nones=False):
			(_,type_names,path,filename)=event
			
			 print("PATH=[{}] FILENAME=[{}] EVENT_TYPES={}".format(
              path, filename, type_names))
	
if __name__ == '__main__':
	main()

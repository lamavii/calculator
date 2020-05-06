config = open("conf.txt", 'r')
dictionary = {}

for line in config:
	if line[0] == '#' or line[0] == ';' or line[0] == '\n':
		continue
	key = line.split()[0]
	val = ""
	try:
		val = line.split()[1]
		val += " " + line.split()[2]
	except IndexError:
		if val == "":
		 val = "key {" + key + "} has not a value"
	dictionary.update({key : val})

flag = True
while flag:
	command = input()
	try:
		if command.split()[0] == "get" and command.split()[1] == "param":
			try:
				print(command.split()[2] + " : " + dictionary[command.split()[2]])
			except KeyError:
				print("Key {" + command.split()[2] + "} is undefined")
	except IndexError:
		print("Commant {" + command + "} is undefined")
	flag_internal = True
	s = ''
	while flag_internal:
		s = input("Are you want to continue? (y/n)")
		if not(s == 'n' or s == 'y'):
			continue
		else:
			break
	if s == 'n':
		break
	if s == 'y':
		continue


			

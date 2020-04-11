import person, json, random

# save file defaults
SAVE = dict(
	most_holy=dict(),
	most_sinful=dict(),
	last_20_holy_ages=[],
	last_20_sinful_ages=[],
	holy=0,
	sinful=0,
	intro=False,
	day=1
)
try:
	with open("save.json") as f:
		# load save file
		savefile = json.load(f)
		# if a key is missing from the save file it'll be set to the default automatically
		SAVE.update(savefile)
except: pass

# convenience functions
next_person = lambda: person.Person.generate()
avg = lambda l: sum(l)/len(l)

print("Welcome to PearlyGates!")
if not SAVE["intro"]:
	# display story intro fragment
	print()
	print("Saint Peter has retired, and has left you in charge of the gate to heaven.")
	print("Rather than being held to any standard, you are given full freedom to send")
	print("people to heaven or hell based on your arbitrary guidelines.")
	print()
	print("So, let's begin!")
	# don't show it on next startup
	SAVE["intro"]=True
running=True
while running:
	print("It is day {!s}.".format(SAVE["day"]))
	print("Would you like to:")
	print("1) See the dead people?")
	print("2) See stats")
	print("3) Quit")
	choice = None
	while choice is None:
		try:
			choice = int(input("? ").strip())
			assert choice in (1,2,3)
		except:
			print("Choose 1, 2, or 3.")
			choice=None
	if choice==2: # stats
		print("Stats:")
		print("-"*80)
		print("Amount of people sent to heaven all-time: {!s}".format(SAVE["holy"]))
		print("Average age of holy person (over last 20): {!s}".format(avg(SAVE["last_20_holy_ages"])))
		print("Top 5 most common holy traits:")
		# get all traits of people marked "holy"
		holy_traits = list(SAVE["most_holy"].items())
		# sort by occurrences descending
		holy_traits.sort(key=lambda x: -x[1])
		# display top 5
		for trait, count in holy_traits[:5]:
			print(f" - {trait} ({count!s})")
		print("-"*80)
		print("Amount of people sent to hell all-time: {!s}".format(SAVE["sinful"]))
		print("Average age of sinful person (over last 20): {!s}".format(avg(SAVE["last_20_sinful_ages"])))
		print("Top 5 most common sinful traits:")
		# get all traits of people marked "sinful"
		sinful_traits = list(SAVE["most_sinful"].items())
		# sort by occurences descending
		sinful_traits.sort(key=lambda x: -x[1])
		# show top 5
		for trait, count in sinful_traits[:5]:
			print(f" - {trait} ({count!s})")
		print("-"*80)
	elif choice==3:
		print("Goodbye!")
		running = False
	else:
		for i in range(random.randint(7,13)):
			# get new person and show summary
			p = next_person()
			print(p.toString())
			print("Send them to:")
			print("1) Heaven")
			print("2) Hell")
			choice = None
			while choice is None:
				try:
					choice = int(input("? ").strip())
					assert choice in (1,2)
				except:
					print("Choose 1 or 2.")
					choice=None
			if choice==1: # heaven
				print(p.pronoun,"smile"+('' if p.pronoun=="They" else "s"),"at you as",p.pronoun.lower(),"enter"+('' if p.pronoun=="They" else "s")+" the pearly gates.")
				# update stats
				SAVE["holy"]+=1
				SAVE["last_20_holy_ages"]=(SAVE["last_20_holy_ages"]+[p.age])[-20:]
				for trait in p.traits:
					if trait not in SAVE["most_holy"]:
						SAVE["most_holy"][trait]=1
					else:
						SAVE["most_holy"][trait]+=1
			else:
				print(p.pronoun,"scream"+('' if p.pronoun=="They" else "s"),"as",p.pronoun.lower(),"fall"+('' if p.pronoun=="They" else "s")+" into the depths of hell.")
				# update stats
				SAVE["sinful"]+=1
				SAVE["last_20_sinful_ages"]=(SAVE["last_20_sinful_ages"]+[p.age])[-20:]
				for trait in p.traits:
					if trait not in SAVE["most_sinful"]:
						SAVE["most_sinful"][trait]=1
					else:
						SAVE["most_sinful"][trait]+=1
		# dawn of the next day
		SAVE["day"]+=1

with open("save.json","w") as f:
	json.dump(SAVE,f)

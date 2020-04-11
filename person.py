import tracery, json, sys, random, traceback, math

# name generator
NAMES = None
try:
	with open("name.json") as f: NAMES = tracery.Grammar(json.load(f))
except Exception as e:
	if type(e)==FileNotFoundError:
		print("ERROR! name.json not found!",file=sys.stderr)
		print("Download `name.json` and place it in the same folder as `person.py`.",file=sys.stderr)
	traceback.print_exc()
	sys.exit(-1)

# traits list
TRAITS = """Transgender
Homosexual
Christian
Muslim
Hindu
Jewish
Plays video games
Is a jerk to service workers (cashiers, waiters, etc)
Is nice to service workers (cashiers, waiters, etc)
Kicks puppies
Might be a nazi?
Racist
Misogynist
Feminist
Bigoted
Died rich
Died poor""".splitlines()

# list of traits you can't have together
# if a person is generated with more than one of the traits in a tuple,
# they will reroll all but one of those traits
EXCLUSIONARY_TRAITS = [
	("Hindu","Jewish","Muslim"),
	("Is a jerk to service workers (cashiers, waiters, etc)","Is nice to service workers (cashiers, waiters, etc)"),
	("Died rich","Died poor"),
	("Misogynist","Feminist")
]

# average life expectancy
# according to the UN, world life expectancy was ~72.6 in 2019, so we'll go with that
AVERAGE_LIFE_EXPECTANCY=72.6

# pronouns list
# male uses he/him, female uses she/her, and non-binary can use any pronoun in the list below
PRONOUNS = """He
She
They
Ze
Xe
Ve
Vi""".splitlines()

class Person:
	GENDER_DESCRIPTORS = ["Male","Female","Non-binary"]
	def __init__(self,name,age,gender=0,traits=["Boring"]):
		self.name=name
		self.age=age
		self.gender=gender
		self.traits=traits
		# force gender-specific pronouns on binary genders
		if self.gender==0:
			self.pronoun="He"
		elif self.gender==1:
			self.pronoun="She"
		elif self.gender==2:
			# non-binary people get to have whatever pronoun they desire from the list
			self.pronoun=random.choice(PRONOUNS)
	def toString(self):
		# change gender number to gender descriptor
		gender = self.GENDER_DESCRIPTORS[self.gender]
		out=""
		out+=(f"{self.name}, {self.age}\n")
		out+=(f"Gender: {gender}\n")
		c = len(self.traits)
		out+=(f"Traits: ({c!s})\n")
		for trait in self.traits:
			out+=(f" - {trait}\n")
		return out.strip()
	def __str__(self):
		return self.toString()
	@classmethod
	def generate(cls):
		# pick a random gender
		gender = random.randint(0,len(cls.GENDER_DESCRIPTORS)-1)
		tag = "random_name"
		# ~67% chance name is guaranteed to be stereotypical of gender if gender in binary
		if gender==0:
			tag = random.choice(["stereotypical_male_name","stereotypical_male_name","random_name"])
		elif gender==1:
			tag = random.choice(["stereotypical_female_name","stereotypical_female_name","random_name"])
		# generate name from tracery grammar
		name = NAMES.flatten("#"+tag+"#")
		# pick age, skewed towards average life expectancy
		age = random.choice([math.floor,math.ceil])(random.triangular(5,100,AVERAGE_LIFE_EXPECTANCY))
		# pick 3-7 random traits
		traits = [random.choice(TRAITS) for i in range(random.randint(3,7))]
		check = True
		while check:
			check = False
			for trait_exc in EXCLUSIONARY_TRAITS:
				# indexes of conflicting traits
				ind = [i for i, c in enumerate(traits) if c in trait_exc]
				# if person doesn't have anything in the list, go to next
				if not ind: continue
				ind.pop(0) # keep first rolled trait
				if ind: # more than one?
					for i in ind:
						# reroll
						traits[i]=random.choice(TRAITS)
					check = True # check for conflicting traits again
			# don't allow duplicates
			c = len(traits) # length before
			traits = list(set(traits)) # remove duplicates
			while len(traits)<c: # if the list had duplicates
				check = True # make sure to check again after you...
				traits.append(random.choice(TRAITS)) # ...add new traits
		# return object
		return cls(name,age,gender,traits)

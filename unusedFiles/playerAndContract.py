

class Player(object):

	"""A Player is an active Major League Baseball player with the following attributes:

		name: first and last name 					STRING
		team: current team of player 				STRING
		free_agent: True or False 					BOOLEAN
		stats: a players standard mlb statistics    OBJECT
		stats_before_signing: stats before contract OBJECT
		position: a players position(s)        		STRING
		contract: a players Contract 				OBJECT
	
	"""

	def __init__(self, espn_id, name, team, stats, stats_before_signing, position, contract, age_at_signing, service_time):
		#Returns players attributes
		self.espn_id = espn_id
		self.name = name
		self.team = team
		self.stats = stats
		self.stats_before_signing = stats_before_signing
		self.position = position
		self.contract = contract
		self.age_at_signing = age_at_signing
		self.service_time = service_time




class Contract(object):

	"""A active Major League Baseball contract with the following attributes:

		length: Contract length in Years   					INTEGER
		years: Years contract is active 					STRING
		total_value: Total value of Contract 				INTEGER
		current_salary: salary value of current year 		INTEGER
		sign_year: year that the contract was signed      	INTEGER
		age_at_signing: age player signed contract          INTEGER

	"""

	def __init__(self, length, years, total_value, current_salary, avg_value, sign_year):
		#returns contract attributes
		self.length = length
		self.years = years
		self.total_value = total_value
		self.current_salary = current_salary
		self.avg_value = avg_value
		self.sign_year = sign_year
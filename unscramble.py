#!/usr/bin/python2

import logging
import itertools

import util

QWERTY = ["`1234567890"," qwertyuiop"," asdfghjkl;"," zxcvbnm,./"]

"""

things that need to be considered in a typoed message:
 -> duplicate letters
 -> offset letters
 -> misordered letters
 	-> more likely for more distant keys
 	-> I should probably generate a keyDistances table too...
 -> letters followed by offset duplicate

"""

class Unscramblr:
	def __init__(self,scrambled_text):
		self.scrambled_text = scrambled_text

	def setup(self):
		self.generate_typo_proximity_map()
		self.load_the_whole_freakin_dictionary_into_ram()

	def load_the_whole_freakin_dictionary_into_ram(self):
		try:
			with open("wordsEn.txt") as f:
				self.the_dictionary = f.readlines()
		except IOError:
			print("Error loading the dictionary...")
			exit()
		logging.info(self.the_dictionary[1])

	def generate_typo_proximity_map(self):
		self.typoProximityMap = {}
		key_relations = 0

		for i_row in range(len(QWERTY)):
			row = QWERTY[i_row]
			for i_key in range(len(row)):

				thisLetter = [] # multidim -> [distance,list]

				keysWereFound = True

				"""
				I call this following bit the pseudo-ellipse-proximity algorithm.
				An algorithmically correct ellipse might be more accurate.
				Statistics of missed keys would be most accurate, but I didn't find any.
				"""

				m = 1 # iteration count => magniture for key distance
				while keysWereFound:
					keysWereFound = False # be pessemistic

					tier_one = []
					tier_two = []
					tier_thr = []

					# Tier 1 letters - adjacent horizontal
					for val in (i_key-m,i_key+m):
						if util.check_index(val,len(row)):
							keysWereFound = True
							tier_one.append(row[val])

					# Tier 2 letters - adjacent vertical
					for val in (i_row-m,i_row+m):
						if util.check_index(val,len(QWERTY)):
							keysWereFound = True
							tier_one.append(QWERTY[val][i_key])

					# Tier 3 letters - diagonal
					diffs = [x for x in range(1,m)] + [-x for x in range(1,m)]
					for d_valR, d_valK in itertools.product(diffs, repeat=2):
						if d_valR == d_valK:
							continue
						if d_valR + d_valK != m+1:
							continue
						valR = i_row + d_valR
						valK = i_key + d_valK

						if util.check_index(valR,len(QWERTY)):
							if util.check_index(valK,len(row[valR])):
								keysWereFound = True
								tier_thr.append(QWERTY[valR][valK])

					for thing in [tier_one,tier_two,tier_thr]:
						if len(thing) > 0:
							key_relations += len(thing)
							thisLetter.append(thing)

					m+=1

				# end while
		# end keys loop
		logging.info("Processed " + str(key_relations) + " key mistype probability relations")


def main():
	logging.basicConfig(level=logging.DEBUG)
	logging.info("Eric's Unscrambler Script")

	print("Enter message: ")
	msg = raw_input()
	unscramblr = Unscramblr(msg)
	unscramblr.setup()


if __name__ == "__main__":
	main()
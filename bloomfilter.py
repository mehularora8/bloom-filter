"""
This file exports a class that implements a Bloom Filter. 
"""

import hashlib
import mmh3
import numpy as np

class BloomFilter():

	"""
	Initialize with the number of buckets
	and the number of hashes to be used.
	""" 
	def __init__(self, buckets, hashes):
		self.num_buckets = buckets
		self.num_hashes	 = hashes
		self.bucketData  = np.zeros(buckets)
		self.additions 	 = 0

	def insert(self, word):
		"""
		Function to insert strings into the bloom filter. 
		Calls each hash function and marks the corresponding
		bucket as filled.
		"""

		self.additions +=1 

		for i in range(self.num_hashes):
			hash_digest = mmh3.hash(word, i) % self.num_buckets
			self.bucketData[hash_digest] = 1


	def false_positive_probability(self) -> float:
		"""
		Function to calculate the false positive probability if the search function
		returns True. Based on principles of counting. 

		@Return: A float indicating false positive probability. 
		"""

		# Probability of a bit being 0 after one (1) insertion
		prob_one_insertion 	 	 = (1 - (1 / self.num_buckets)) ** self.num_hashes

		# Probability of all the k buckets (each hash) being 0 after n insertions
		prob_multiple_insertions = prob_one_insertion ** self.additions

		# Probability of a false positive is 1 - the above probability
		prob_false_positive  	 = (1 - prob_multiple_insertions) ** self.num_hashes 

		return prob_false_positive


	def search(self, word) -> (bool, float):
		"""
		Function to look up strings in the bloom filter. Hashes the word
		using each of the hash functions and checks if all the corresponding 
		buckets are filled. 

		@Return: Bool representing if the string is in the bloom filter
		@Return: Int representing probability of a false positive
		"""

		for i in range(self.num_hashes):

			if self.bucketData[mmh3.hash(word, i) % self.num_buckets] == 0:
				print("The string \"{}\" is not present in the Bloom filter. \n".format(word))
				return (False, 0)

		# All hashed buckets are filled.
		prob = self.false_positive_probability()
		print("The string \"{1}\" is present in the bloom filter with a false positive probability of {0} \n".format(prob, word)) 
		return (True, prob)
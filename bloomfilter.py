"""
This file exports a class that implements a Bloom Filter. 
"""

import hashlib
import numpy as np

class BloomFilter():

	"""
	Initialize with the number of buckets
	and the number of hashes to be used. Max hashes = 5
	""" 
	def __init__(self, buckets, hashes):
		self.num_buckets = buckets
		self.num_hashes	 = hashes
		self.bucketData  = np.zeros(buckets)
		self.hashes      = self.create_hashes(hashes)
		self.additions 	 = 0

	def create_hashes(self, num_hashes):
		"""
		This function creates a list hash functions
		that can be used to hash strings

		@Return: Array of hash functions
		"""

		# Check for availability
		if num_hashes > 10:
			print("The maximum number of hashes is {}.".format(10))
			return

		def hash1(word):
			h = hashlib.md5(word.encode('utf-8'))
			return hash(h.digest()) % 10

		def hash2(word):
			h = hashlib.sha256(word.encode('utf-8'))
			return hash(h.digest()) % 10

		def hash3(word):
			h = hashlib.blake2b(word.encode('utf-8'))
			return hash(h.digest()) % 10

		def hash4(word):
			h = hashlib.blake2s(word.encode('utf-8'))
			return hash(h.digest()) % 10

		def hash5(word):
			h = hashlib.sha3_512(word.encode('utf-8'))
			return hash(h.digest()) % 10

		def hash6(word):
			h = hashlib.shake_128(word.encode('utf-8'))
			return hash(h.digest()) % 10

		def hash7(word):
			h = hashlib.sha512(word.encode('utf-8'))
			return hash(h.digest()) % 10

		def hash8(word):
			h = hashlib.sha3_384(word.encode('utf-8'))
			return hash(h.digest()) % 10

		def hash9(word):
			h = hashlib.shake_256(word.encode('utf-8'))
			return hash(h.digest()) % 10

		def hash10(word):
			h = hashlib.sha3_224(word.encode('utf-8'))
			return hash(h.digest()) % 10

		hashes = [hash1, hash2, hash3, hash4, hash5, hash6, hash7, hash8, hash9, hash10][:num_hashes]
		
		return hashes


	def insert(self, word):
		"""
		Function to insert strings into the bloom filter. 
		Calls each hash function and marks the corresponding
		bucket as filled.
		"""

		if not self.hashes:
			print("The class has not been instantiated correctly.")
			return 

		self.additions +=1 

		for i in range(len(self.hashes)):
			hash_func = self.hashes[i]
			self.bucketData[hash_func(word) % self.num_buckets] = 1


	def false_positive_probability(self) -> float:
		"""
		Function to calculate the false positive probability if the search function
		returns True. Based on principles of counting. 

		@Return: A float indicating false positive probability. 
		"""

		# Probability of a bit being 0 after one (1) insertion
		p_one_insertion 	  = 1 - (1 / self.num_buckets) ** self.num_hashes

		# Probability of all the k buckets (each hash) being 0 after n insertions
		p_multiple_insertions = p_one_insertion ** self.additions

		# Probability of a false positive is 1 - the above probability
		prob_false_positive   = (1 - p_multiple_insertions) ** self.num_hashes 

		return prob_false_positive


	def search(self, word) -> (bool, float):
		"""
		Function to look up strings in the bloom filter. Hashes the word
		using each of the hash functions and checks if all the corresponding 
		buckets are filled. 

		@Return: Bool representing if the string is in the bloom filter
		@Return: Int representing probability of a false positive
		"""

		if not self.hashes:
			print("The class has not been instantiated correctly.")
			return 

		for i in range(len(self.hashes)):
			hash_func = self.hashes[i]

			if self.bucketData[hash_func(word) % self.num_buckets] == 0:
				print("The string \"{}\" is not present in the Bloom filter. \n".format(word))
				return (False, 0)

		# All hashed buckets are filled.
		prob = self.false_positive_probability()
		print("The string \"{1}\" is present in the bloom filter with a false positive probability of {0} \n".format(prob, word)) 
		return (True, prob)

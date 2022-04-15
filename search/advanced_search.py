import whoosh
import os, os.path
import json
from whoosh import index
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from whoosh import qparser
from whoosh.query import Query

class AdvancedSearch(object):

 	### indexes

	index = 0

	### filters

	ratingMax = 100
	ratingMin = 0

	# has 3 potential values
	# 0 means no filter, 1 means return only non-explicit, 2 means return only explicit
	explicitFilter = 0

	# filter out by kind of return type (artist, album, track)
	returnTypeFilter = ['artist', 'album', 'track']

	# select specific country, all countries list, index picks which one from list based on index
	countryFilter = ""

	# select specific genre
	genreFilter = []

	# instrumental
	instrumental = False

	def __init__(self):
		super(AdvancedSearch, self).__init__()

	def search(self, queryEntered):

		with self.index.searcher() as search:

			q = MultifieldParser(['albumName', 'lyrics', 'trackName', 'artistName', 'label'], schema=self.index.schema)
			q = q.parse(queryEntered)

			#artists = whoosh.query.Term('returnType', 'artist')

			results = search.search(q, limit=None)

			"""
			results = list(filter(self.filterReturnType, results))
			
			if self.explicitFilter == 1:
				results = list(filter(self.filterOutExplicit, results))

			elif self.explicitFilter == 2:
				results = list(filter(self.filterNonExplicit, results))

			results = list(filter(self.filterRating, results))

			# specific to artist
			if self.countryFilter != "":
				results = list(filter(self.filterCountry, results))

			if self.instrumental:
				results = list(filter(self.filterInstrumental, results))

			if self.genreFilter:
				results = list(filter(self.filterGenre, results))
			"""
			
			

			print(results)

	def filterGenre(self, x):

		g = x['genres'].split()
		for ii in self.genreFilter:
			if ii in g:
				return True

		return False

	def filterOutExplicit(self, x):
		if x['returnType'] == 'track' or x['returnType'] == 'album':
			if x['explicit'] == 1:

				return False

		return True

	def filterNonExplicit(self, x):

		if x['returnType'] == 'track' or x['returnType'] == 'album':
			if x['explicit'] == 1:
				return True

		return False

	def filterRating(self, x):
		if x['rating'] >= self.ratingMin and x['rating'] <= self.ratingMax:
			return True
		return False

	def filterCountry(self, x):

		if x['country'] == self.countryFilter:
			return True

		return False

	def filterInstrumental(self, x):

		if x['returnType'] == 'track':
			if x['lyrics'] == "":
				return True

		return False

	def filterReturnType(self, x):

		if x['returnType'] in self.returnTypeFilter:
			return True

		return False

def main():

	advanced = AdvancedSearch()
	advanced.index = index.open_dir('index_dir')
	advanced.search("country")



if __name__ == '__main__':
	main()
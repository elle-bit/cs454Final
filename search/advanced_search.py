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

def createIndex():

	track_file = open('data/with_lyrics.json', 'r')
	track_db = json.load(track_file)
	track_file.close()

	album_file = open('data/a_album.json', 'r')
	album_db = json.load(album_file)
	album_file.close()

	artist_file = open('data/artist.json', 'r')
	artist_db = json.load(artist_file)
	artist_file.close()

	genre_file = open('data/genre.json', 'r')
	genre_db = json.load(genre_file)
	genre_file.close()


	if not os.path.exists('index_dir'):
		os.mkdir('index_dir')


	schema = Schema(returnType=TEXT(stored=True),
						trackName=TEXT(stored=True),
						releaseDate=TEXT(stored=True),
						label=TEXT(stored=True),
						albumName=TEXT(stored=True),
						artistName=TEXT(stored=True),
						artistID=NUMERIC(stored=True),
						albumID=NUMERIC(stored=True),
						trackID=NUMERIC(stored=True),
						country=TEXT(stored=True),
						beginYear=TEXT(stored=True),
						lyrics=TEXT(stored=True),
						explicit=BOOLEAN(stored=True),
						genres=TEXT(stored=True),
						URL=TEXT(stored=True),
						rating=NUMERIC(stored=True))

	ix = create_in("index_dir", schema)
	writer = ix.writer()

	for artistKey in album_db['artist_id']:
		for album in album_db['artist_id'][artistKey]:

			expl = 0
			for trackKey in album_db['artist_id'][artistKey][album]['track_listing']:
				try:
					if track_db['id'][trackKey]['explicit'] == 1:
						expl = 1
						break
				except:
					pass

			genreStr = ''
			for genre in album_db['artist_id'][artistKey][album]['music_genre_list']:
				if genre != 34:
					genreStr += " " + str(genre)


			writer.add_document(returnType='album',
								artistID=artistKey,
								albumID=album,
								label=album_db['artist_id'][artistKey][album]['label'],
								albumName=album_db['artist_id'][artistKey][album]['name'],
								artistName=artist_db['id'][artistKey]['name'],
								explicit=expl,
								releaseDate=album_db['artist_id'][artistKey][album]['release_date'],
								country=artist_db['id'][artistKey]['country'],
								genres=genreStr,
								rating=album_db['artist_id'][artistKey][album]['rating'])

	for trackKey in track_db['id']:

		genreStr = ''
		

		albumKey = str(track_db['id'][trackKey]['album_id'])
		artistKey = str(track_db['id'][trackKey]['artist_id'])

		try:
			for genre in album_db['artist_id'][artistKey][albumKey]['music_genre_list']:
				if genre != 34:
					genreStr += " " + str(genre)

			writer.add_document(trackID=track_db['id'][trackKey]['commontrack_id'],
							trackName=track_db['id'][trackKey]['name'],
							rating=track_db['id'][trackKey]['rating'],
							explicit=track_db['id'][trackKey]['explicit'],
							lyrics=track_db['id'][trackKey]['lyrics'],
							artistID=track_db['id'][trackKey]['artist_id'],
							albumID=track_db['id'][trackKey]['album_id'],
							URL=track_db['id'][trackKey]['share_url'],
							releaseDate=album_db['artist_id'][artistKey][albumKey]['release_date'],
							label=album_db['artist_id'][artistKey][albumKey]['label'],
							genres=genreStr,
							country=artist_db['id'][artistKey]['country'],
							returnType='track')

		except:
			pass

		
	for artistKey in artist_db['id']:

		begin = 2022
		genreStr = ''
		try:
			for albumID in album_db['artist_id'][artistKey]:
				releaseDate = album_db['artist_id'][artistKey][albumID]['release_date']

				if releaseDate != '':
					rel = releaseDate[0:3]
					rel = int(rel)
					if rel < begin:
						begin = rel

				for genre in album_db['artist_id'][artistKey][albumID]['music_genre_list']:
					if genre != 34:
						genreStr += " " + str(genre)
		except:
			pass

		writer.add_document(country=artist_db['id'][artistKey]['country'],
							artistName=artist_db['id'][artistKey]['name'],
							artistID=artistKey,
							rating=artist_db['id'][artistKey]['rating'],
							beginYear=str(begin),
							genres=genreStr,
							returnType='artist')

	writer.commit()

	return

def main():

	# createIndex()

	advanced = AdvancedSearch()
	advanced.index = index.open_dir('index_dir')
	advanced.search("country")



if __name__ == '__main__':
	main()
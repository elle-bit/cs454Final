import os, os.path
import json
from whoosh import index
from whoosh.index import create_in
from whoosh.fields import *

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
	createIndex()


if __name__ == '__main__':
	main()
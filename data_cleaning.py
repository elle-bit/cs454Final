import json
import os

"""module designed to clean data"""


def clean_tracks_lyrics():
	tracklist = {}
	new_track = {}
	count = 0
	with open('tracks.json', 'r') as f:
		data = json.load(f) #deseralize json file into python dictionary
		tracks_data = data.get("track_id")
		new_dict = {}

		for id, t_info in tracks_data.items():
			lyrics = t_info.get("lyrics")
			if lyrics:
				new_lyrics = lyrics.replace('\n', "\\n")
				t_info.update({"lyrics": new_lyrics})
			new_track[id] = t_info


	tracklist.update({'id':new_track})
	with open("all_tracks.json", "w") as nt:
		json.dump(tracklist, nt, indent=3)


def remove_artist_duplicated():
	artists = {}
	a_ids = []

	with open("data/artist.json", "r") as f:
		data = json.load(f)
		data = data.get("id")
		artist_dict = {}

		for id, info in data.items():
			if int(id) not in a_ids:
				a_ids.append(int(id))
				artist_dict[id] = info

		artists.update({'id': artist_dict })
		
		with open("unique_artists.json", "w+") as f:
			json.dump(artists, f, indent=3)


def remove_album_duplicate():
	a_albums = {}
	a_ids = []

	with open("data/a_album.json", "r") as f:
		data = json.load(f)
		data = data.get("artist_id")
		artist_dict = {}

		for id, info in data.items():
			if int(id) not in a_ids:
				a_ids.append(int(id))
				artist_dict[id] = info

		a_albums.update({'artist_id': artist_dict })
		
		with open("unique_albs.json", "w+") as f:
			json.dump(a_albums, f, indent=3)



if __name__ == "__main__":


	# remove_artist_duplicated()
	remove_album_duplicate()

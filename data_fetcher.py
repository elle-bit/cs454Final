import os, re
from api_response import * # user defined module

class MusicDicts():
    """creates a music data object for to store various music attributes in dictionaries"""

    def __init__(self, api_key, exist):
        self.key = api_key
        self.a_id = -1
        self.artist_number = ""
        self.artist_name = ""

        #create dictionaries to be stored for json dump
        self.artist_data = {}
        self.artist_album_track_data = {} 
        self.track_data = {}
        self.lyrics_tracks_data = {}

        if not exist:
            self.artist_data = {'artist_id':{}}
            self.artist_album_track_data = {'id':{}} 
            self.track_data = {'track_id':{}}
            self.lyrics_tracks_data = {'id':{}}

        self.top_artists_ids = []
        
        self._crr_response = None
        self.retry_flag = False

        #to update after each scraper session
        self.fetch_related = set()
        self.retry = []

        #create the regex patter upon instantiation to avoid excess cost
        self.phrase = " This Lyrics is NOT for Commercial use "
        self.copyright = re.compile("\.\.\.\n\n(\*{7})" + self.phrase + "(\*{7})\n" + r"\(\d{12,}\)")

 

    def new_artist_setter(self, artist_number):
        """invoked on each loop of main method, to gather new data"""
        self.retry_flag = False
        self.artist_number = str(artist_number)
        self.a_id = artist_number

        url_section = "artist.get?" + "artist_id=" + self.artist_number
        response_rewrite = get_response(self.key, url_section)
        
        if response_rewrite != {}: 
            self._crr_response = response_rewrite
            #save after we get a response
            self.artist_name = response_rewrite["message"]["body"]["artist"]["artist_name"]
            self._artist_album_init()
            print(self.artist_name)
        
        else:
            print("no artist data")
            self.retry_flag = True
            self.retry.append(self.a_id)
            self.a_id = -1
            self.artist_number = ""

    def _artist_album_init(self):
        """used for each artist to nest sub dicts"""
        self.artist_album_track_data[self.a_id] = {}


    def get_genre_list(self, data):
        """return a list of genre_id"""
        id_list = []
        for each in data["music_genre_list"]:
            id_list.append(each["music_genre"]["music_genre_id"])
        return id_list


    def get_artist_data(self):
        """get various artist attributes and add to the dictionary"""
        related_artists = self.get_related_artist()
        artist_info = self._crr_response["message"]["body"]["artist"]

        artist_aliases = artist_info["artist_alias_list"]
        aliases = []
        alias_count = 0
        for alias in artist_aliases:
            if alias_count == 5: break
            aliases.append(alias.get("artist_alias"))
            alias_count += 1

        self.artist_data[self.a_id] = {
            "name": self.artist_name,
            "alias": aliases,
            "country": artist_info["artist_country"],
            "updated_time": artist_info["updated_time"],
            "begin_year": artist_info["begin_date_year"],
            "end_year": artist_info["end_date_year"],
            "rating" : artist_info["artist_rating"],
            "related_artists": related_artists
            }


    def get_related_artist(self):
        """stored in data object for artists, helper function"""

        related_segment = 'artist.related.get?artist_id=' + self.artist_number
        related_artists = get_response(self.key, related_segment)
        if not related_artists: print("no related artists")
        related_artists_list = related_artists["message"]["body"]["artist_list"]
        
        num_related = related_artists["message"]["header"]["available"]
        num_related = 10 if num_related > 10 else num_related

        related = []
        count = 0
        for artist in related_artists_list:
            if count > 10: break
            ra_id = artist["artist"]["artist_id"]
            
            artist_attrs = {
                "name" : artist["artist"]["artist_name"],
                "id": ra_id,
                "rating": artist["artist"]["artist_rating"]
            }
            related.append(artist_attrs)
            self.fetch_related.add(ra_id)
            count += 1

        if  not related:
            print("no related artists")
        related = sorted(related, key=lambda x: x["rating"], reverse=True)
        return related if related else {}


    def fetch_albums_tracks(self, album_id):
        """get a response object and create an album request"""
        album_request = "album.tracks.get?album_id=" + str(album_id)
        tracks = get_response(self.key, album_request)
        if not tracks: print("no tracks")
        track_list = tracks["message"]["body"]["track_list"]
        tracks_for_album = []
        for track in track_list:
            tv = track.get("track")
            tracks_for_album.append(tv.get("track_id"))
        return tracks_for_album


    def fetch_albums(self):
        """fetch data for albums by invoking a response object and parsing the json """
        url_section = "artist.albums.get?" + "artist_id=" + self.artist_number
        albums_list = get_response(self.key, url_section)
        albums_list = albums_list["message"]["body"]["album_list"]
        album_data = {}

        for album in albums_list:
            album_attrs = album["album"]
            album_id = album["album"]["album_id"]
            album_tracks = self.fetch_albums_tracks(album_id)
            if not album_tracks: print("no album tracks")

            album_data[album_id] = {
                "name": album_attrs["album_name"],
                "label": album_attrs["album_label"],
                "rating": album_attrs["album_rating"],
                "release_date": album_attrs["album_release_date"],
                "music_genre_list": self.get_genre_list(album_attrs["primary_genres"]),
                "track_listing": album_tracks
                }
        self.artist_album_track_data[self.a_id].update(album_data)
 

    def fetch_track_data(self):
        """store various attributes about a track"""
        track_segment = "track.search?q_artist=" + self.artist_name + "&s_track_rating=desc"
        tracks_info = get_response(self.key, track_segment)
        lyrics_flag = False
        if not tracks_info: 
            print("no tracks")
            return None

        num_tracks = tracks_info["message"]["header"]["available"]
        tracks_list = tracks_info["message"]["body"]["track_list"]

        for track in tracks_list:
            _track = track["track"]
            track_id = _track["track_id"]
            lyrics_body = ""
            lyric_indicator = _track["has_lyrics"]
      
            if _track["has_lyrics"]: 
                lyrics_body = self.get_lyrics(track_id)
                if lyrics_body: lyrics_flag = True
                
                if not lyrics_body:
                    print("no lyrics despite indication")
                    lyrics_body = ""

            self.track_data[track_id] = {
                "commontrack_id": _track["commontrack_id"],
                "name": _track["track_name"],
                "artist_id": self.a_id,
                "rating": _track["track_rating"],
                "favorite": _track["num_favourite"],
                "album_id": _track["album_id"],
                "restricted": _track["restricted"],
                "explicit": _track["explicit"],
                "share_url": _track["track_share_url"],
                "lyrics": lyrics_body
                }

            if lyrics_flag:
                self.lyrics_tracks_data[track_id] = self.track_data[track_id]


    def get_lyrics(self, track_id_num):
        """calls on api_response to get the lyrics for the track"""
        lyrics_body = ""
        lyrics_url = "track.lyrics.get?track_id=" +str(track_id_num)
        lyrics_data = get_response(self.key, lyrics_url)
        if lyrics_data:
            lyrics_data = lyrics_data.get("message").get("body").get("lyrics")
            lyrics_body = lyrics_data.get("lyrics_body")
        
        if lyrics_body:
            #replace newline for valid json parsing
            newline_replacement = "\\n"
            lyrics_body = self.copyright.sub('', lyrics_body)
            lyrics_body = lyrics_body.replace('\n', newline_replacement)
        return lyrics_body if lyrics_body else ''


    def top_artist_charts(self):
        """appends top artists to list"""
        top_artist_url = "chart.artists.get?page=1&page_size=100"
        top_artists = get_response(self.key, top_artist_url)
        top_artists = top_artists["message"]["body"]
        top_artists = top_artists.get("artist_list")

        for artist in top_artists:
            artist = artist.get("artist")
            artist_id = artist.get("artist_id")
            self.top_artists_ids.append(artist_id)












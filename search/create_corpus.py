import json
from collections import OrderedDict

class CreateCorpus(object):
    def __init__(self):
        self.create_corpus('data/all_tracks.json', 'track', 'track.json')
        self.create_corpus('data/a_album.json', 'album', 'album.json')
        self.create_corpus('data/artist.json', 'artist', 'artist.json')
        self.create_corpus('data/genre.json', 'genre', 'genre.json')
    
    def create_corpus(self, data_file, data_type, output_name):
        '''create corpus for given file'''
        file = open(data_file, 'r')
        db = json.load(file)
        file.close()
        track_dict = self.add_corpus(db, data_type)
        self.write_to_file(track_dict, output_name)

    def add_corpus(self, db, data_type):
        my_dictionary = {}

        if data_type == 'track' or data_type == 'artist':
            for id in db['id']:
                name = db['id'][id]['name']
                my_dictionary = self.update_dictionary(name, my_dictionary)

        elif data_type == 'album':
            for id in db["artist_id"]:
                album_ids = db["artist_id"][id]
                for a_id in album_ids:
                    album_name = db["artist_id"][id][a_id]['name']
                    my_dictionary = self.update_dictionary(album_name, my_dictionary)
        
        elif data_type == 'genre':
            for id in db:
                genre_name = db[id]['name']
                my_dictionary = self.update_dictionary(genre_name, my_dictionary)

        return dict(OrderedDict(sorted(my_dictionary.items())))

    def update_dictionary(self, data, my_dictionary):
        if data[0] not in my_dictionary:
            my_dictionary[data[0]] = [data]
        else:
            value = list(my_dictionary[data[0]])
            if data not in value:
                value.append(data)
                my_dictionary[data[0]] = value
        return my_dictionary

    def write_to_file(self, data, file_name):
        with open(file_name, 'w') as output_file:
            json.dump(data, output_file, indent=3)
        output_file.close()


def main():
    CreateCorpus()

if __name__ == '__main__':
	main()
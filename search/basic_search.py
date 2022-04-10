import whoosh
import os
import os.path
import json
from whoosh import index
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from whoosh import qparser
from whoosh.query import Query
import create_index

track_synonym = ['track', 'song']
artist_synonym = ['artist', 'creator', 'originator',
                  'designer', 'producer', 'vocalist']
genre_synonym = ['genre', 'type', 'class',
                 'category', 'kind', 'variety', 'group']
album_synonym = ['album', 'cover']


class BasicSearch(object):
    def __init__(self, index_file):
        self.index = open_dir(index_file)
        self.corpus = self.load_corpus(['track', 'album', 'genre', 'artist'])

    ''' corpus of names for track, artist, genre, artist'''

    def load_corpus(self, file_list):
        for file in file_list:
            file_name = 'corpus_data/' + file + '.json'
            with open(file_name, 'r') as f:
                if file == 'track':
                    self.track_corpus = json.load(f)
                elif file == 'album':
                    self.album_corpus = json.load(f)
                elif file == 'genre':
                    self.genre_corpus = json.load(f)
                elif file == 'artist':
                    self.artist_corpus = json.load(f)
                f.close()

    def search(self, query):
        possible_type, key_value = self.determine_type(query.lower())
        if possible_type == 'None':
            key_value = query
            if self.in_corpus('track', key_value):
                self.whoosh_search('trackName', key_value)
            elif self.in_corpus('artist', key_value):
                self.whoosh_search('artistName', key_value)
            elif self.in_corpus('album', key_value):
                self.whoosh_search('albumName', key_value)
            elif self.in_corpus('genre', key_value):
                self.whoosh_search('genres', key_value)
            else:
                self.whoosh_search('lyrics', key_value)

        if possible_type == 'track':
            if self.in_corpus('track', key_value):
                self.whoosh_search('trackName', key_value)
            else:
                print('20 result for <' + query + ">")
        # elif possible_type == 'artist':
        #     if self.in_corpus('artist', key_value):
        #         self.whoosh_search('artistName', key_value)
        #     else:
        #         print('30 result for <' + query + ">")
        # elif possible_type == 'genre':
        # elif possible_type == 'album':

    ''' check if a given name is in any corpus type'''

    def in_corpus(self, data_type, value):
        if data_type == 'track':
            if value in self.track_corpus[value[0]]:
                return True
            return False
        elif data_type == 'artist':
            if value in self.artist_corpus[value[0]]:
                return True
            return False
        elif data_type == 'genre':
            if value in self.genre_corpus[value[0]]:
                return True
            return False
        elif data_type == 'album':
            if value in self.album_corpus[value[0]]:
                return True
            return False

    ''' determine what is the type of the query if possible 
		ex: if a query string is about track_name or others
	'''

    def determine_type(self, query):
        words = query.split()
        if any(x in track_synonym for x in words):
            if 'song name' in query or 'track name' in query:
                removable_words = ['song', 'track', 'name', 'call']
                removable_words += track_synonym
                if 'song' or 'track' in words[0]:
                    for each in removable_words:
                        if each in words:
                            words.remove(each)
                    key_value = ' '.join(words)
                    return ('track', key_value.title())
        else:
            return ('None', query)

    '''search a key_value based on the key_word'''

    def whoosh_search(self, key_word, key_value):
        result_limit = 10
        with self.index.searcher() as searcher:
            query = QueryParser(key_word, self.index.schema).parse(key_value)
            results = searcher.search(query, limit=result_limit)
            self.print_result(results, key_word, key_value, result_limit)

    def print_result(self, results, key_word, key_value, result_limit=None):
        if results:
            print(f"----\nResult FOUND for \"{key_word} = {key_value}\"")
            if key_word != 'genre':
                count = 1
                for r in results:
                    print(r)
                    count += 1
                    if result_limit and count > result_limit:
                        break
        else:
            print(f"----\nResult NOT FOUND for \"{key_word} = {key_value}\"")
            print("None")


def main():
    # create_index.main()
    basic = BasicSearch('index_dir')

    query = 'song name Fancy Like'
    basic.search(query)

    # artist name
    query = 'Jordan Davis feat. Luke Bryan'
    basic.search(query)

    # track name
    query = 'Dream Machine'
    basic.search(query)

    # # album name
    query = 'New Favorite'
    basic.search(query)

    # # genre name
    query = 'Swing'
    basic.search(query)

    # #lyrics
    query = "Maybe, I'm right and maybe, I'm wrong"
    basic.search(query)


if __name__ == '__main__':
    main()

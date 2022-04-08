
"""a set of functions to help preform scraping per desired results"""


def scrape_artists(music_object, a_id):
    """a method to scrape data by their artist Id"""
    music_object.new_artist_setter(a_id)
    if music_object.retry_flag == False:
        music_object.get_artist_data()
        music_object.fetch_albums()  
        music_object.fetch_track_data()

def artist_to_retry(music_object):
    """artists with either a response return failure or embedded api failure, are retried additionally 1 
    time more if api failure and up to three times more if a connection failure"""
    print("RETRY ARTISTS: ")
    for artist_num in music_object.retry:
        print(artist_num)
        music_object.retry.remove(artist_num)
        scrape_artists(music_object, artist_num)
        if music_object.retry_flag:
            print("trying again: ", artist_num)
            music_object.retry.remove(artist_num) #if it fails again, only going to try one additional time
    if music_object.retry: music_object.retry.clear() # just in case something weird occurs


def get_related_artists(music_object, artist_list):
    """in a seperate method to avoid accidental breadth first search"""
    # music_object.fetch_related_artists()
    if music_object.fetch_related:
        print("scraping additional artists")
        for artist_num in music_object.fetch_related:
            if artist_num not in artist_list:
                print(artist_num)
                scrape_artists(music_object, artist_num)
                if not music_object.retry_flag:
                    music_object.total_added_artists += 1
        #check to see if need to retry due to error
        if music_object.retry: artist_to_retry(music_object)
        #just to ensure list cleared to avoid infinite looping
        if music_object.fetch_related: music_object.fetch_related.clear()
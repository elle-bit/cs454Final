from input_out import *
from total_updates import *
from scraper_helper import *



def main(start, end, *a_tup):

    if start and end:
        are_top_scraped(music_data)
        print()
        print("scraping ", end-1, " artists")
        print('scraping data for artist id: ')
        for index in range(start, end):  # hard coded because limit of api calls we can take
            print(index)
            scrape_artists(music_data, index)

        if music_data.retry: artist_to_retry(music_data)
        if music_data.fetch_related:
            get_related_artist(music_data, artists_list)
        
    else: #for when we are not running additional artists
        artist_list = a_tup[0]
        print()
        print("scraping ", len(artist_list), " artists")
        print("SCRAPING DATA FOR ARTIST ID'S ")
        for a in artist_list:
            print(a)
            scrape_artists(music_data, a)

        if music_data.retry: artist_to_retry(music_data)

    write_to_disk(music_data.artist_data, "id", "artist")
    write_to_disk(music_data.artist_album_track_data, "artist_id","a_album")
    write_to_disk(music_data.track_data, "id", "all_tracks")
    write_to_disk(music_data.lyrics_tracks_data, "id", "with_lyrics")



def update_ds_total():
    # get a totals list for each field
    artist_nums = totals_list("artist.json", ["id",""])
    album_nums = totals_list("a_album.json", ["artist_id", "_"])
    track_nums =  totals_list("all_tracks.json",["id",""])
    lyrics_nums = totals_list("with_lyrics.json", ["id","lyrics"])
    
    update_totals([len(artist_nums), len(album_nums), len(track_nums), len(lyrics_nums)])
    write_lists("artist_nums", artist_nums, False)
    write_lists("alb_nums", album_nums, False)
    write_lists("track_nums", track_nums, False)
    write_lists("lyrics_nums", lyrics_nums, False)





if __name__ == '__main__':
    # start_ranges = [x for x in range(0, 401, 100)]
    # max_ranges = [y for y in range(100,500, 100)]


    #start_ranges = [x for x in range(0, 401, 100)]
    #max_ranges = [y for y in range(100,500, 100)]
 
    #CRR EXHAUSTED KEYS
    #de9b4c486aea914d79928445801a6018 #
    #06590d27c8fa785775dc63114810337e #anna
    #2361d89087b1648d87ef8b2ec98ce525 #gabes
    #991d6270a7685921a89ca1089a69c85d #artist
    #905eb3ec64fbf56c69d88ad72db37678 # gmail /
    #c5b947318f5be2ab83fcde6321eb3290 #Gmail2
    #de9b4c486aea914d799284458 #hotmail
    #cb0670ecb75b33f6a375c6e7e9dded1d #pinkii



    #SINGLE KEY RUN

    # main(9502, 9504)
    # main()

    #incremental save incase of 401 or disconnect from the api
    # for x,y in new_zip:
        # print(x, y)
        # main(x, y, False)

   
    key_list = []
    a_key = "c5b947318f5be2ab83fcde6321eb3290"
    global music_data 
    music_data = MusicDicts(a_key, True)
    start_ranges = [x for x in range(9502, 9532, 10)] #Start, stop, step
    max_ranges = [y for y in range(9512, 9542, 10)]  #end, max_end_ step
    new_zip = zip(start_ranges, max_ranges)




    # MULTI KEY RUN **^^ REFORMAT KEY LIST**
    # newZip = zip(start_ranges, max_ranges)

    # for r in zip(newZip, keys_list):
        
    #     ranges, a_key = r #unpack inner zip
    #     start, end = ranges # upack outter zip
        

    #     global music_data 
    #     music_data = MusicData(a_key)
    #     global retry
    #     retry = []

    #     main(start, end, False)


    #if artist list wasnt chunked apart:
    # related_list = get_scraped_related(20, artists_list) #get the related artists based on whats been scraped
    
    related_list = get_block_to_scrape(0, 99, 20)

    for chunk in related_list:
        main(0, 0, chunk)
    update_ds_total()







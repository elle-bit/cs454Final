import os, sys, json
from data_fetcher import * #user defined modules
import total_updates

###PURPOSE###
"""helper module to operate on behalf of music dict to save to disk the scraped data and determine what data to 
scrape based on disk contents"""

def get_scraped_related(chunk_size, artist_list):
    """"""
    related = totals_list('artist.json', ['id', 'related_artists'])
    related = set(related)
    artist_list = totals_list('artist.json', ['id', ""])
    artist_list = set(art_list)

    #want artists in related that are not already in artist_list
    unique_related = related.difference(artist_list)
    unique_related = list(unique_related)
    rl = len(unique_related) #calc before hand for range
    chunked_related = [unique_related[i:i+chunk_size] for i in range(0, rl, chunk_size)]
    write_list("chunked_related", chunked_related, True)
    return chunked_related


def write_to_disk(data, obj_name, data_name):
    """create a new data file if it doesnt exist or append to existing"""
    file_name = data_name + ".json"
    path_file = 'data/' + file_name
    cwd = os.getcwd()

    data_exits = os.path.exists('data/')
    if not data_exits: 
        try:
            os.mkdir(cwd + '/data/')
            os.mkdir(cwd +'/totals/')
        except OSError as err:
            print(err)
            print("\n", "FAILURE TO WRITE")


    exists = os.path.exists(path_file)

    crr_content = {}
    if exists:
        try: 
            with open(path_file) as output_file:
                crr_content = json.load(output_file)        
                old_data = crr_content.get(obj_name)
                old_data.update(data)
                crr_content[obj_name] = old_data
            
        except JSONDecodeError as json_err:
           with open('ill_format.json', "w+") as err_file:
                json.dump(data, err_file, indent=3)

        else:
            with open(path_file, "w") as output_file:
                json.dump(crr_content, output_file, indent=3)

    else: #if path does not exist open in write mode
        json.dump(data, output_file, indent=3)


def are_top_scraped(music_object):
    """if the database hasnt been created, create the db and then scrape the top artists first"""
    top_scraped = True if os.path.exists('data/') else False
    if not top_scraped:
        music_object.top_artist_charts()
        top_artist_list = music_object.top_artists_ids
        for artist_id in top_artist_list:
            if artist_id > 20000:  # only want to s
                print(artist_id)
                scrape_artists(artist_id)
            else: continue

        write_list("top_artists", top_artist_list, False)


def get_block_to_scrape(start_block, num_blocks, chunksize):
    start_ind = (start_block*chunksize) + start_block #get line by calc start * chunk +number of newlines
    max_ind =  start_ind + (chunksize*num_blocks) + (num_blocks-1) #shift by start_ind, add total lines + num of blocks to get
  
    art_list = []
    sublist = []
    num_appened = 0
    with open("totals/chunked_related.txt", "r") as sublists_file:
        for ind, line in enumerate(sublists_file):
            if ind >= start_ind and ind <= max_ind:
                artist_id = line.strip()
                if artist_id.isnumeric():
                    sublist.append(int(artist_id))
                    num_appened += 1
                    if num_appened % chunksize == 0:
                        art_list.append(sublist)
                        sublist = []
    return art_list




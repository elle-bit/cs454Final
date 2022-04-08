from pkgutil import extend_path
from request import *

if __name__ == '__main__':
    genre_data = {}
    genre_data["id"] = {}

    result = get_all_genre("music.genres.get")
    for each in result:
        g_id = each["music_genre"]["music_genre_id"]
        parent_id = each["music_genre"]["music_genre_parent_id"]
        name = each["music_genre"]["music_genre_name"]
        name_extended = each["music_genre"]["music_genre_name_extended"]
        vanity = each["music_genre"]["music_genre_vanity"]

        genre_data["id"][g_id] = {
            "name": name,
            "genre_parent_id": parent_id,
            "name_extended": name_extended,
            "vanity": vanity
        }

    # sort by id
    data = dict(sorted(genre_data["id"].items()))
    
    with open('data/genre.json', 'w') as output_file:
        json.dump(data, output_file, indent=3)
    
    output_file.close()

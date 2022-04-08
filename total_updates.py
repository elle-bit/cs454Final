import os, json


"""A module to update the totals of the db"""
def update_totals(size_list):
	file_name = "totals.txt"
    full_path_file = 'totals/' + file_name
  
    totals_exist = os.path.exists(full_path_file)

    with open(full_path_file, "r+") as total_file:
        if not total_exists:
            totals_file.write(f"Total artists: {size_list[0]}\n")
            totals_file.write(f"Total albums: {size_list[1]}\n")
            totals_file.write(f"Total tracks: {size_list[2]}\n")
            totals_file.write(f"Total with Lyrics: {size_list[3]}")
       
        else:
        	new_totals_list = []
            for idx,line in enumerate(total_file):
                line = line.strip()
                t_line = line.split(": ")
                t_header = t_line[0]
                t_num = int(t_line[-1])
                new_total = size_list[idx]
                updated_line = t_header + ": " + str(new_totals)+ "\n"
                new_totals_list.append(updated_line)
    
    with open(full_path_file, "w") as tf:
        tf.writelines(new_totals_list)


def write_lists(file_name, data_list, sublist_flag):
	"""takes a data list and writes to disk"""

	# for record in added_items:
 #        bisect.insort(data_list, record)


	if sublist_flag:
		with open("totals/" + file_name + ".txt", "a+") as ra:
            for sl in data_list: 
                sl = map_to_strings(sl)
                sl.append("\n")
                ra.writelines(sublist)

    else:
		new_data = map_to_strings(sl)

		with open("totals/"+ file_name + ".txt", 'w') as f_nums:
			f_nums.writelines(new_data)



def map_to_strings(lst):
	return list(map(lambda x: str(x) + "\n" , sub_list))


def totals_list(file_name, **filters ):
	"""gets the list of unique items in the dataset and returns the sorted list"""
	upper, inner = filters
	with open(file_name, "r") as f:
		data = json.load(f)
		data = data.get(upper)
		data_list = []

		if not inner: 
			datalist = data.keys() 
		else:
			for id, info in data.items():
				if inner != "_":
					desired_data = info.get(inner)
					if inner == "related_artists":
						related_artists = [ra.get("id") for ra in desired_data]
						data_list = data_list + related_artists
					else:
						if desired_data != "": data_list.append(id)

				else: #this is the case for albums where inner = "_"
					data_list.append(info.keys())

		#do this for all paths
		data_set = set(data_list)
		data_list = data_set
		data_list = list(map(lambda x: int(x), datalist))
		data_list.sort()

		print(len(data_list))
		return data_list

import os
import shutil
import goldstandard_eval
import numpy as np
import h5py
# first, get the list of xml names from a specified directory
# then, consume the list of xml filenames to get h5 filenames : counts of filenames
# iterate through the h5 filenames, copying h5 files over to a new directory. If count > 1,
IMG_WIDTH = 1152

def fetch_xml_filenames(directory_path):
    result = []
    for file in os.listdir(directory_path):
        if file.endswith('.xml'):
            result.append(file)

    return result

# drops the id off the xml name
# assumes xml_name in form data-year-month-day-run-timestep
def xml_to_h5_filename(xml_name):
    xml_split = xml_name.split('-')
    print("Original Split", xml_split)
    last_group = xml_split[-1]
    xml_split[-1] = last_group[0]
    xml_split = swap_chey(xml_split)
    print(xml_split)
    return '-'.join(xml_split) + '.h5'

def swap_chey(xml_split):
    old_last_group = xml_split[-1]
    xml_split[-1] = xml_split[-2][-1]
    xml_split[-2] = xml_split[-2][0] + old_last_group[0]
    return xml_split

# returns a map of h5 filename to count of labels for that h5 file
def h5_file_counts(xml_names):
    h5_counts = {}
    h5_names = map(xml_to_h5_filename, xml_names)
    for name in h5_names:
        if name in h5_counts:
            h5_counts[name] += 1
        else:
            h5_counts[name] = 1

    return h5_counts


def create_new_h5s(h5_directory, save_directory, xml_directory):
    # keep track of the current counts
    # iterate through the xml names, copying the corresponding h5 file
    # add to the map
    h5_counts = {}
    xml_names = fetch_xml_filenames(xml_directory)
    for name in xml_names:
        h5_name = xml_to_h5_filename(name)
        save_h5_name = h5_name

        if h5_name in h5_counts:
            # for duplicate h5 files
            path_split = os.path.splitext(h5_name)
            save_h5_name = path_split[0] + '_' + str(h5_counts[h5_name]) + path_split[1]
            h5_counts[h5_name] += 1
        else:
            h5_counts[h5_name] = 1
        print(h5_name)

        orig_path = os.path.join(h5_directory, h5_name)
        save_path = os.path.join(save_directory, save_h5_name)
        # copy the h5 file
        shutil.copy2(orig_path, save_path)

        # append the new information to the h5
        xml_full_path = os.path.join(xml_directory, name)
        tc_masks = goldstandard_eval.get_polygons_from_XML(xml_full_path, goldstandard_eval.TC_EVENT)
        ar_masks = goldstandard_eval.get_polygons_from_XML(xml_full_path, goldstandard_eval.AR_EVENT)

        # need to flip
        tc_masks = np.flipud(tc_masks)
        ar_masks = np.flipud(ar_masks)

        new_h5_handle = h5py.File(save_path, 'a')
        new_h5_handle['tc_masks'] = tc_masks
        new_h5_handle['ar_masks'] = ar_masks

#xml_dir = '/project/projectdirs/ClimateNet/xmls_no_rotation_images'
xml_dir = '/project/projectdirs/ClimateNet/xmls_NCAR'
save_dir = '/project/projectdirs/ClimateNet/h5_data_processed/NCAR_temp'
#h5_dir = '/global/cscratch1/sd/amahesh/gb_data/All-Hist'
h5_dir = '/project/projectdirs/ClimateNet/chey_h5'

#print(xml_to_h5_filename(xml_dir + '/data-2001-11-04-02-01479084886.xml'))
create_new_h5s(h5_dir, save_dir, xml_dir)


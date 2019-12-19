import os
import shutil

def remove_overlap(dir1, dir2):
    dir1_xml_set = set([x for x in os.listdir(dir1) if x.endswith('.xml')])
    dir2_xml_set = set([x for x in os.listdir(dir2) if x.endswith('.xml')])
    diff_set = dir1_xml_set.difference(dir2_xml_set)
    return diff_set
    print(diff_set)
    print(len(diff_set))

def copy_set(dir1, dir2, save_dir):
    save_set = remove_overlap(dir1, dir2)
    for filename in save_set:
        orig_path = os.path.join(dir1, filename)
        save_path = os.path.join(save_dir, filename)
        shutil.copy2(orig_path, save_path)

old_set = "/project/projectdirs/ClimateNet/tmq_20191118-165341"
new_set = "/project/projectdirs/ClimateNet/tmq_20191202-173809"
save_dir = "/project/projectdirs/ClimateNet/xmls_NCAR"

copy_set(new_set, old_set, save_dir)


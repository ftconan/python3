# coding=utf-8
import os

def remove_ad_text(dir2, ad_text):
    """
    delete ad text funtion
    1. search file and dir, serarch sub_dir, until sub_dir not exist
    2. remove ad_text from file
    @params: dir2: str   dir
             ad_text: str content
    """
    # dir2 is not dir
    if not os.path.isdir(dir2):
        return

    # dir2 has not seperator, add seperator
    if not dir2.endswith(os.path.sep):
        dir2 += os.path.sep

    # get all file list
    names = os.listdir(dir2)
    # for dir and file
    for name in names:
        # join path
        sub_path = os.path.join(dir2, name)
        #  sub_path is path
        if os.path.isdir(sub_path):
            # fac search
            remove_ad_text(sub_path, ad_text)
        # remove ad text, rename file
        name = name.replace(ad_text, "")
        # join new path
        new_path =  os.path.join(dir2, name)
        # rename file
        os.rename(sub_path, new_path)


if __name__ == '__main__':
    remove_ad_text(r'/home/project/python3', '123')

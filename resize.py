import os
import fnmatch
from PIL import Image, ImageFilter
from threading import Thread
import math
import time


# insert here your paths and number of threads

path = r"I:\Temp\resize_test\src"
dest = r"I:\Temp\resize_test\dst"
number_of_threads = 5

dirss = fnmatch.filter(os.listdir(path), '*.jpg')


def clever_resize(dirs):

    desired_h_size = 1920, 1280
    desired_v_size = 1280, 1920

    for item in dirs:
        my_path = os.path.normpath(path)
        dest_path = os.path.normpath(dest)
        if os.path.isfile(os.path.join(my_path, item)):
            img = Image.open(os.path.join(my_path, item))
            #
            if hasattr(img, '_getexif'):
                orientation = 0x0112
                exif = img._getexif()
                if exif is not None:
                    orientation = exif[orientation]
                    if orientation != 1:
                        rotations = {
                            3: Image.ROTATE_180,
                            6: Image.ROTATE_270,
                            8: Image.ROTATE_90
                        }
                        if orientation in rotations:
                            img = img.transpose(rotations[orientation])
            #
            desired_size = desired_h_size if img.size[0] > img.size[1] else desired_v_size
            # img = img.filter(ImageFilter.UnsharpMask(1, 30, 0)) # uncomment this to get sharpness
            img.thumbnail(desired_size, Image.ANTIALIAS)
            img.save(os.path.join(dest_path, item), quality=100)


def main():
    print('start')

    t1 = time.time()

    one_t_size = math.ceil(len(dirss) / number_of_threads)

    sizes_list = list()

    total_size = len(dirss)
    current_size = int()

    for i in range(number_of_threads):
        if total_size == current_size:
            break
        elif total_size - current_size < one_t_size:
            sizes_list.append(total_size - current_size)
        else:
            sizes_list.append(one_t_size)
        current_size += one_t_size

    print(sizes_list)

    threads = list()

    cur_size = 0
    for i in range(len(sizes_list)):
        if sizes_list[i] != 0:
            threads.append(Thread(target=clever_resize, args=(dirss[cur_size:cur_size+sizes_list[i]],)))
            cur_size += sizes_list[i]

    for i in range(len(sizes_list)):
        threads[i].start()

    for i in range(len(sizes_list)):
        threads[i].join()

    t2 = time.time()

    print('finish')

    print(t2-t1)


if __name__ == '__main__':
    exit(main())
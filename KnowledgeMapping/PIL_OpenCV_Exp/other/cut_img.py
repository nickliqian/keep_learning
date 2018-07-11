from PIL import Image
import os


root_dir = "/home/nick/Desktop/cpic/"
save_dir = root_dir + "cut/"
file_list = os.listdir(root_dir)
# print(file_list)

for file_name in file_list:
    if file_name.endswith(".png"):

        im =Image.open(root_dir + file_name)
        w, h = im.size

        if w < 500:
            for i in range(3):
                im_c = im.crop((0, int(h/3)*i, w, int(h/3)*(i+1)))
                im_name = "{}_{}.{}".format(file_name.split(".")[0], str(i), file_name.split(".")[1])
                im_c.save(save_dir + im_name)
                print("save {}".format(im_name))
        elif 500 < w < 750:
            for i in range(2):
                im_c = im.crop((0, int(h/3)*i, w, int(h/3)*(i+1)))
                im_name = "{}_{}.{}".format(file_name.split(".")[0], str(i), file_name.split(".")[1])
                im_c.save(save_dir + im_name)
                print("save {}".format(im_name))

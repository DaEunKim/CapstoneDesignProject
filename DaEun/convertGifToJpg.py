from PIL import Image

for i in range(6001,9000):
    file_path = "label/image_"+str(i)+".jpg"
    im = Image.open(file_path)
    mypalette = im.getpalette()
    #print(mypalette)
    #im.putpalette(mypalette)
    new_im = Image.new("RGBA", im.size)
    new_im.paste(im)
    new_im.save("label_jpg/image_"+str(i)+".jpg")
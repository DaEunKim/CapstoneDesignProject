from PIL import Image
for i in range(18131,21401):
    file_path = "label/image_"+str(i)+".jpg"
    im = Image.open(file_path)
    mypalette = im.getpalette()
    print(mypalette)
    #im.putpalette(mypalette)
    new_im = Image.new("RGBA", im.size)
    new_im.paste(im)
    new_im.save("Images/001/image_"+str(i)+".jpg")
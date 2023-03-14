import pytsk3

image_path = "/path/to/image.dd"
offset = 0 # or the offset of the MFT in the image
img = pytsk3.Img_Info(image_path)
fs = pytsk3.FS_Info(img, offset=offset)
mft = fs.open_meta(inode=0)

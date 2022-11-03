from curses import raw
import rawpy
import imageio
import os

dir_in_str = os.path.dirname(__file__)+"/pyin/"
dir_out_str = os.path.dirname(__file__)+"/pyout/"

print(f"Copy input files to {os.path.dirname(__file__)}/pyin/")
print("Select input format:")
print("1) .RW2")
print("2) .CR2")
print("3) Custom")
print("Enter file format. 1, 2, 3")

in_type = input()
if in_type == "1":
    conv_from = ".RW2"
elif in_type == "2":
    conv_from = ".CR2"
else:
    print("Enter file extention")
    conv_from = input()

print("Select output format:")
print("1) .TIFF")
print("2) .JPG")
print("3) .PNG")
print("4) Custom")
print("Enter file format. 1, 2, 3, 4")

f_type = input()

if f_type == "1":
    file_type = ".TIFF"
elif f_type == "2":
    file_type = ".JPG"
    print("Enter quality 1~100 (eg. 98)")
    quality = input()
elif f_type == "3":
    file_type = ".PNG"
else :
    print("Enter file extention")
    file_type = input()

directory = os.fsencode(dir_in_str)

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(conv_from):
        raw = rawpy.imread(dir_in_str+filename)
        rgb = raw.postprocess(gamma = (6,6), use_camera_wb = True, bright = 1.0, output_bps = 16, output_color = rawpy.ColorSpace.sRGB)
        out_file = os.path.splitext(os.path.basename(filename))[0]
        filename_out = out_file+file_type
        
        if f_type == "1":
            imageio.imsave(dir_out_str+filename_out, rgb)
        elif f_type == "2":
            imageio.imsave(dir_out_str+filename_out, rgb, quality = quality)
        elif f_type == "3":
            imageio.imsave(dir_out_str+filename_out, rgb,) 
        else:
            imageio.imsave(dir_out_str+filename_out, rgb)
            
        print(f"converted {filename} to {filename_out}")
        
        os.system(f'exec exiftool -tagsFromFile "{dir_in_str+filename}" "{dir_out_str+filename_out}"')
        print(f"Copied metadata from {dir_in_str+filename} to {dir_out_str+filename_out}")
        os.system(f'rm {dir_out_str+filename_out+"_original"}')
        print(f"Removed duplicate files")

print(f"Converted files written to {dir_out_str}")
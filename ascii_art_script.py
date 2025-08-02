import cv2
import os,subprocess

#os module is to handle the file path and subprocess module is to pipe the output to 'less' text viewer

# ASCII characters from darkest to lightest
ASCII_CHARS = "MWB80#Qdb@m&Uk%Xh$ZwqpaoIunCf1YJtxzLvil{}c?][<>+r*)(j\\/|!^~\":;'-.`,_ "


def resize_image(image, new_width=100):
    height, width = image.shape
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)  # Adjust for font ratio
    resized = cv2.resize(image, (new_width, new_height))
    return resized


def grayify(image):
    #if img has alpha channel,use it as a mask
    if len(image.shape) == 3 and image.shape[2] == 4:
        alpha = image[:,:,3]
        mask = cv2.threshold(alpha, 128, 255, cv2.THRESH_BINARY)[1]
        image = image[:,:,:3] #drop the alpha channel
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.bitwise_and(gray, gray, mask = mask)
        return gray
    else:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def pixel_to_colored_ascii(pixel):   
    ascii_index = int(pixel)*len(ASCII_CHARS) // 256 
    char = ASCII_CHARS[ascii_index] 

    #maps to ansi 256 grayscale(range 232 to 255)  

    ansi_gray = min(255, max(232, 232 + int(pixel / 11)))  
    return f"\033[38;5;{ansi_gray}m{char}\033[0m"



def remove_background(gray_image, threshold=245):
    # Make very bright areas into "background" (set to 255)
    _, mask = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY_INV)
    return cv2.bitwise_and(gray_image, gray_image, mask=mask)


def pixels_to_ascii(image,use_grayscale = False):
    ascii_str = ""
    for row in image:
        for pixel in row:
            if pixel == 0:
                ascii_str += " "  # treat full-black as blank
            else:
                if use_grayscale:
                    ascii_str += pixel_to_colored_ascii(int(pixel))
                else:

                    ascii_index = int(pixel)*len(ASCII_CHARS) // 256
                    ascii_str += ASCII_CHARS[ascii_index]
                    #pixel assortment checked for robust grouping
        ascii_str += "\n"
    return ascii_str

def image_to_ascii(path, width=100, background_threshold=245):
    if not path.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
        print("Unsupported format. Use .png, .jpg, or .bmp.")
        return
    image = cv2.imread(path, cv2.IMREAD_UNCHANGED) #now loads with alpha channel

    if image is None:
        print("Could not load image. Check the path.")
        return

    gray = grayify(image)
    bg_removed = remove_background(gray, background_threshold)
    resized = resize_image(bg_removed, width)

    use_grayscale = input("Use ANSI grayscale color (y/n)?: ").strip().lower() 

    if use_grayscale == "y":
        ascii_art = pixels_to_ascii(resized,use_grayscale = True)
        subprocess.run(["less","-R"], input = ascii_art.encode())
    else:
        ascii_art = pixels_to_ascii(resized)
        subprocess.run(["less"], input = ascii_art.encode())

def get_image_path():
    #promting to either enter full path or the filename which is put inside the test_images folder provided,.png only
    choice = input("provide the full path?(y/n): ").strip().lower()
    if choice == 'y':
        return os.path.expanduser(input("Enter full image path: ").strip())
    else:
        filename = input("Enter image filename (e.g., cat.png): ").strip()
        base_path = os.path.join(os.path.dirname(__file__), "test_images")
        return os.path.join(base_path, filename)


if __name__ == "__main__":
    print("======ASCII ART TOOL(python + opencv)======\n")
    image_path = get_image_path()
    image_width = int(input("Set width: "))
    image_to_ascii(image_path, width=image_width,background_threshold = 245)



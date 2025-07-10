import cv2
import os,subprocess

#os module is to handle the file path and subprocess module is to pipe the output to 'less' text viewer

# ASCII characters from darkest to lightest
ASCII_CHARS = "@%#*+=-:. "

def resize_image(image, new_width=100):
    height, width = image.shape
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)  # Adjust for font ratio
    resized = cv2.resize(image, (new_width, new_height))
    return resized

def grayify(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def remove_background(gray_image, threshold=245):
    # Make very bright areas into "background" (set to 255)
    _, mask = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY_INV)
    return cv2.bitwise_and(gray_image, gray_image, mask=mask)

def pixels_to_ascii(image):
    ascii_str = ""
    for row in image:
        for pixel in row:
            if pixel == 0:
                ascii_str += " "  # treat full-black as blank
            else:
                ascii_str += ASCII_CHARS[pixel // 25]
        ascii_str += "\n"
    return ascii_str

def image_to_ascii(path, width=100, background_threshold=245):
    image = cv2.imread(path)
    if image is None:
        print("Could not load image. Check the path.")
        return

    gray = grayify(image)
    bg_removed = remove_background(gray, background_threshold)
    resized = resize_image(bg_removed, width)
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
    print("ASCII ART FROM PNG (python + opencv)\n")
    image_path = get_image_path()
    image_to_ascii(image_path, width=110,background_threshold = 245)


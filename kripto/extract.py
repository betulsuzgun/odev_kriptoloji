from PIL import Image

def extract_message(image_path):
    img = Image.open(image_path)
    data = img.getdata()
    binary_msg = ''
    for pixel in data:
        for value in pixel[:3]:
            binary_msg += str(value & 1)

    chars = [binary_msg[i:i+8] for i in range(0, len(binary_msg), 8)]
    message = ''
    for ch in chars:
        if ch == '11111110':
            break
        message += chr(int(ch, 2))
    return message

# Örnek kullanım
if __name__ == "__main__":
    message = extract_message("input_image.png")
    print("Çözülen mesaj:")
    print(message)

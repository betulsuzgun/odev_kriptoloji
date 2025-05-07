from PIL import Image

def embed_message(image_path, output_path, message):
    img = Image.open(image_path)
    binary_msg = ''.join(format(ord(c), '08b') for c in message) + '1111111111111110'  # End delimiter
    data = iter(img.getdata())
    new_pixels = []

    for i in range(0, len(binary_msg), 3):
        pixel = list(next(data))
        for j in range(3):
            if i + j < len(binary_msg):
                pixel[j] = pixel[j] & ~1 | int(binary_msg[i + j])
        new_pixels.append(tuple(pixel))

    for pixel in data:
        new_pixels.append(pixel)

    stego_img = Image.new(img.mode, img.size)
    stego_img.putdata(new_pixels)
    stego_img.save(output_path)
    print(f"Mesaj başarıyla '{output_path}' dosyasına gizlendi.")

# Örnek kullanım
if __name__ == "__main__":
    message = input("Gizlemek istediğiniz mesajı girin (160 karaktere kadar): ")
    if len(message) > 160:
        print("Maksimum 160 karakter girilmelidir.")
    else:
        embed_message("input_image.png", "input_image.png", message)

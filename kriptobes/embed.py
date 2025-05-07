import cv2
import numpy as np

def embed_message_in_image(input_image_path, output_image_path, message):
    # Görseli oku
    image = cv2.imread(input_image_path)
    
    # Mesajı ikili (binary) hale getir
    message_bin = ''.join(format(ord(c), '08b') for c in message)
    message_length = len(message_bin)

    # Görselde kullanılacak pikselleri hazırlıyoruz
    data_idx = 0
    for row in range(image.shape[0]):
        for col in range(image.shape[1]):
            if data_idx < message_length:
                # Kırmızı kanalını al ve mesaj bitlerini yerleştir
                pixel = image[row, col]
                red_channel = pixel[2]
                
                # En düşük anlamlı bit yerine mesajı yerleştir
                new_red = (red_channel & 0xFE) | int(message_bin[data_idx])
                image[row, col][2] = new_red
                
                data_idx += 1

    # Filtreleme (Gaussian)
    image = cv2.GaussianBlur(image, (5, 5), 0)

    # Çıktıyı kaydet
    cv2.imwrite(output_image_path, image)
    print("Mesaj başarıyla gömüldü ve filtre uygulandı!")

# Kullanım örneği
embed_message_in_image('input_image.jpg', 'stego_image.jpg', 'Bu bir gizli mesajdır!')

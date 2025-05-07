import cv2
import numpy as np

def message_to_bits(message):
    message += "###"
    return ''.join(format(ord(c), '08b') for c in message)

def embed_message(img_path, out_path, message):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("❌ input_image.jpg yüklenemedi.")
        return

    h, w = img.shape
    h -= h % 8
    w -= w % 8
    img = img[:h, :w]

    bits = message_to_bits(message)
    bit_index = 0

    stego_img = np.copy(img)

    for i in range(0, h, 8):
        for j in range(0, w, 8):
            if bit_index >= len(bits):
                break

            block = stego_img[i:i+8, j:j+8].astype(np.float32)
            if block.shape != (8, 8):
                continue

            dct_block = cv2.dct(block)

            coeff = int(dct_block[4, 3])
            coeff = (coeff & ~1) | int(bits[bit_index])
            dct_block[4, 3] = coeff
            bit_index += 1

            idct_block = cv2.idct(dct_block)
            stego_img[i:i+8, j:j+8] = idct_block

    cv2.imwrite(out_path, np.uint8(stego_img))
    print("✅ Mesaj başarıyla gömüldü:", out_path)

if __name__ == "__main__":
    embed_message("input_image.jpg", "stego.jpg", "DCT içinde gizli mesaj")

import cv2
import numpy as np

def extract_message(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("❌ stego.jpg yüklenemedi.")
        return

    h, w = img.shape
    h -= h % 8
    w -= w % 8
    img = img[:h, :w]

    bits = ""
    message = ""

    for i in range(0, h, 8):
        for j in range(0, w, 8):
            block = img[i:i+8, j:j+8].astype(np.float32)
            if block.shape != (8, 8):
                continue

            dct_block = cv2.dct(block)
            coeff = int(dct_block[4, 3])
            bits += str(coeff & 1)

            # 8 bitlik blok oluşunca karaktere çevir
            if len(bits) >= 8:
                byte = bits[:8]
                bits = bits[8:]
                char = chr(int(byte, 2))
                message += char
                if message.endswith("###"):
                    print("🔍 Çıkarılan Mesaj:", message[:-3])
                    return

    print("⚠️ Mesaj sonu bulunamadı.")
    print("Tahmini mesaj:", message)

if __name__ == "__main__":
    extract_message("stego.jpg")

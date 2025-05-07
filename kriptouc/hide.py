import cv2
import numpy as np

def message_to_bits(message):
    message += "###"
    return ''.join(format(ord(c), '08b') for c in message)

def calculate_complexity(block):
    transitions = np.sum(block[:, :-1] != block[:, 1:]) + np.sum(block[:-1, :] != block[1:, :])
    total = 2 * block.shape[0] * (block.shape[1] - 1)
    return transitions / total

def embed_message(img_path, out_path, message):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    h, w = img.shape
    bits = message_to_bits(message)
    bit_index = 0
    threshold = 0.3

    stego = np.copy(img)
    for bit_plane in range(7, -1, -1):
        plane = ((stego >> bit_plane) & 1).astype(np.uint8)
        for i in range(0, h, 8):
            for j in range(0, w, 8):
                if bit_index + 64 > len(bits):
                    continue
                block = plane[i:i+8, j:j+8]
                if block.shape != (8, 8):
                    continue
                complexity = calculate_complexity(block)
                # ...
            if bit_index >= len(bits):
                break

        # 🛠️ MASK düzeltildi burada:
        mask = np.uint8(~(1 << bit_plane) & 0xFF)
        stego = (stego & mask) | ((plane << bit_plane) & 0xFF)

        if bit_index >= len(bits):
            break
# ...


    cv2.imwrite(out_path, stego)
    print("✅ Mesaj başarıyla gömüldü:", out_path)

if __name__ == "__main__":
    embed_message("input.png", "stego.png", "BPCS yöntemiyle gizli mesaj")

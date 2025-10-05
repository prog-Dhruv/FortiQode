import matplotlib.pyplot as plt
import numpy as np
from cryptography.fernet import Fernet

def is_in_orientation_zone(x, y):
    """Checks if a coordinate is within any of the 15x15 orientation squares."""
    in_top_left = (x < 15 and y < 15)
    in_top_right = (x >= 85 and y < 15)
    in_bottom_left = (x < 15 and y >= 85)
    return in_top_left or in_top_right or in_bottom_left

def extract_binary_data(img, start_x=20, start_y=20, num_bits=10000):
    """
    Extracts binary bits from the image, skipping orientation squares.
    Default num_bits is large to capture full ciphertext.
    """
    binary_data = ""
    x, y = start_x, start_y
    height, width = img.shape

    while len(binary_data) < num_bits and y < height:
        if x >= width:
            x = start_x
            y += 1
            continue
        if not is_in_orientation_zone(x, y):
            pixel = img[y, x]
            bit = '1' if pixel < 0.5 else '0'  # Black (0) => '1', White (1) => '0'
            binary_data += bit
        x += 1

    return binary_data

def binary_to_ciphertext(binary_data):
    """Converts binary string back into the encrypted text (ciphertext)."""
    chars = []
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        if len(byte) < 8:
            break
        chars.append(chr(int(byte, 2)))
    return ''.join(chars)

def decrypt_text(ciphertext, key, stop_marker="_pineapple"):
    """
    Decrypts ciphertext with the given symmetric key.
    Removes stop marker before returning plaintext.
    """
    cipher = Fernet(key)
    try:
        decrypted = cipher.decrypt(ciphertext.encode()).decode()
        return decrypted.replace(stop_marker, "")
    except Exception as e:
        return f"[Decryption Failed] {str(e)}"

# --- Main Execution ---

# Load the image (as grayscale)
image_path = "qr_like_encrypted.png"
img = plt.imread(image_path)

# Convert float values to range 0–1 if needed (matplotlib loads PNGs as float32)
if img.ndim == 3:
    img = img[:, :, 0]  # If RGBA, take only one channel

# Extract binary from QR-like image
binary_data = extract_binary_data(img, start_x=20, start_y=20, num_bits=10000)

# Convert to ciphertext string
ciphertext = binary_to_ciphertext(binary_data)

# Supply the SAME symmetric key used for encryption
key_str = input("Enter the symmetric key used for encryption: ").strip()
key = key_str.encode()

# Decrypt to recover original message
extracted_text = decrypt_text(ciphertext, key)

print("\nExtracted & Decrypted Message:")
print(extracted_text)
    
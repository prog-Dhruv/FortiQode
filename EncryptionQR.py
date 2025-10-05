from matplotlib import pyplot as plt
import numpy as np
import random
from cryptography.fernet import Fernet

# --- Encryption Helpers ---
def generate_key():
    """Generate a new symmetric key (store this securely for decryption)."""
    return Fernet.generate_key()

def encrypt_text(text, key):
    """Encrypts text using AES symmetric key (Fernet)."""
    cipher = Fernet(key)
    return cipher.encrypt(text.encode()).decode()  # Return string


# --- QR Helpers ---
def draw_orientation_square(matrix, top_left_x, top_left_y, size=15):
    # Ensure there's space for the border
    border = 1

    # Outer white border
    matrix[top_left_y-border:top_left_y+size+border, 
           top_left_x-border:top_left_x+size+border] = 1

    # Outer black square
    matrix[top_left_y:top_left_y+size, top_left_x:top_left_x+size] = 0  

    # Middle white square
    matrix[top_left_y+2:top_left_y+size-2, top_left_x+2:top_left_x+size-2] = 1  

    # Inner black square
    matrix[top_left_y+4:top_left_y+size-4, top_left_x+4:top_left_x+size-4] = 0  
 


def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)

def is_in_orientation_zone(x, y):
    in_top_left = (x < 15 and y < 15)
    in_top_right = (x >= 85 and y < 15)
    in_bottom_left = (x < 15 and y >= 85)
    return in_top_left or in_top_right or in_bottom_left

def embed_data(matrix, binary_data, used_mask, start_x=20, start_y=20):
    x, y = start_x, start_y
    height, width = matrix.shape
    for bit in binary_data:
        if x >= width:
            x = start_x
            y += 1
        if y >= height:
            break
        if not is_in_orientation_zone(x, y):
            matrix[y, x] = 0 if bit == '1' else 1
            used_mask[y, x] = True
        x += 1

def fill_with_gibberish(matrix, used_mask):
    height, width = matrix.shape
    for y in range(height):
        for x in range(width):
            if not used_mask[y, x] and not is_in_orientation_zone(x, y):
                matrix[y, x] = random.randint(0, 1)

def create_qr_like_image(size=100, text="Hello", key=None):
    salt = "_pineapple"
    if len(text) + len(salt) > 200:
        raise ValueError("Input text plus marker must be 200 characters or fewer.")

    # --- Encrypt text before binary encoding ---
    encrypted_text = encrypt_text(text + salt, key)

    # Convert encrypted text to binary
    binary_data = text_to_binary(encrypted_text)

    img = np.ones((size, size), dtype=np.uint8)
    used_mask = np.zeros((size, size), dtype=bool)

    # Orientation markers
    draw_orientation_square(img, 0, 0)
    draw_orientation_square(img, size - 15, 0)
    draw_orientation_square(img, 0, size - 15)
    used_mask[0:15, 0:15] = True
    used_mask[0:15, 85:100] = True
    used_mask[85:100, 0:15] = True

    # Embed encrypted data
    embed_data(img, binary_data, used_mask, start_x=20, start_y=20)

    # Fill remaining with random bits
    fill_with_gibberish(img, used_mask)

    return img, encrypted_text

# --- Main Execution ---
if __name__ == "__main__":
    # Generate symmetric key (keep this safe!)
    key = generate_key()
    print(f"Generated Symmetric Key (store safely): {key.decode()}")

    input_text = input("Enter text ≤192 characters: ")[:192]

    qr_like_img, encrypted_text = create_qr_like_image(text=input_text, key=key)

    # Show QR-like image
    plt.imshow(qr_like_img, cmap='gray', interpolation='nearest')
    plt.title('Encrypted QR-like 100x100 Image')
    plt.axis('off')
    plt.show()

    # Save QR-like image
    output_filename = "qr_like_encrypted.png"
    plt.imsave(output_filename, qr_like_img, cmap='gray', format='png')
    print(f"Image saved as: {output_filename}")

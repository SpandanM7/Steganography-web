import numpy as np
from PIL import Image
import random

def embed_data(image_path, data, output_image_path):
    img = Image.open(image_path).convert('L')
    img_array = np.array(img)
    
    bitstream = ''.join(format(byte, '08b') for byte in data.encode())
    bitstream_length = len(bitstream)
    length_bits = format(bitstream_length, '032b')
    full_bitstream = length_bits + bitstream
    
    random.seed(42)
    height, width = img_array.shape
    bits_index = 0
    
    for i in range(height):
        for j in range(width):
            if bits_index < len(full_bitstream):
                img_array[i, j] = (img_array[i, j] & 254) | int(full_bitstream[bits_index])
                bits_index += 1
            else:
                break

    modified_image = Image.fromarray(img_array)
    modified_image.save(output_image_path)

def binary_to_text(binary_string):
    chars = [chr(int(binary_string[i:i+8], 2)) for i in range(0, len(binary_string), 8)]
    return ''.join(chars)

def retrieve_data(image_path):
    img = Image.open(image_path).convert('L')
    img_array = np.array(img, dtype=np.uint8)

    extracted_bits = []
    length_bits = []
    
    for i in range(32):
        pixel_value = img_array[i // img_array.shape[1], i % img_array.shape[1]]
        bit = pixel_value & 1
        length_bits.append(str(bit))
    
    bitstream_length = int(''.join(length_bits), 2)
    bits_extracted = 0
    
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            if bits_extracted >= bitstream_length + 32:
                break
            if bits_extracted >= 32:
                pixel_value = img_array[i, j]
                bit = pixel_value & 1
                extracted_bits.append(str(bit))
            bits_extracted += 1

    binary_string = ''.join(extracted_bits)
    hidden_text = binary_to_text(binary_string)
    return hidden_text
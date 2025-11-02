from PIL import Image


def _text_to_bin(text: str) -> str:
    return "".join(format(ord(c), "08b") for c in text)


def _bin_to_text(binary: str) -> str:
    chars = [binary[i : i + 8] for i in range(0, len(binary), 8)]
    return "".join([chr(int(c, 2)) for c in chars])


# ENCODE TEXT INTO IMAGE
def encode_text_into_image(
    input_image_path: str, output_image_path: str, secret_text: str
) -> bool:
    try:
        img = Image.open(input_image_path)
        img = img.convert("RGB")
        binary_text = _text_to_bin(secret_text) + "1111111111111110"
        data_index = 0
        data_len = len(binary_text)

        pixels = list(img.getdata())
        new_pixels = []

        for pixel in pixels:
            r, g, b = pixel
            if data_index < data_len:
                r = (r & ~1) | int(binary_text[data_index])
                data_index += 1
            if data_index < data_len:
                g = (g & ~1) | int(binary_text[data_index])
                data_index += 1
            if data_index < data_len:
                b = (b & ~1) | int(binary_text[data_index])
                data_index += 1
            new_pixels.append((r, g, b))

        img.putdata(new_pixels)
        img.save(output_image_path)
        return True
    except Exception as e:
        print("LSB Encode Error:", e)
        return False


# DECODE TEXT FROM IMAGE
def decode_text_from_image(image_path: str) -> str | None:
    try:
        img = Image.open(image_path)
        img = img.convert("RGB")
        pixels = list(img.getdata())
        binary_text = ""

        for pixel in pixels:
            r, g, b = pixel
            binary_text += str(r & 1)
            binary_text += str(g & 1)
            binary_text += str(b & 1)

        all_bytes = [binary_text[i : i + 8] for i in range(0, len(binary_text), 8)]
        decoded_text = ""
        for byte in all_bytes:
            if byte == "11111111":
                if decoded_text.endswith(chr(255)):
                    break
            decoded_text += chr(int(byte, 2))

        decoded_text = decoded_text.replace(chr(255), "")
        return decoded_text
    except Exception as e:
        print("LSB Decode Error:", e)
        return None

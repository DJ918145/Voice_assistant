import easyocr

def read_txt():
    ans = ""
    reader = easyocr.Reader(['en']) 
    image_path = ".\image.jpg" 
    results = reader.readtext(image_path)
    print("\nDetected Text:\n")
    for _, text, _ in results:
        ans = ans + text
    return ans

from PIL import Image
import pytesseract
import pandas as pd

# Path to the image file
image_path = 'C:\Users\ismae\Pictures\Metadata'

# Open the image file
img = Image.open(image_path)

# Extract text from the image
extracted_text = pytesseract.image_to_string(img)

# Extract metadata (EXIF data)
exif_data = img._getexif()

# Convert EXIF data to a readable format
exif = {
    ExifTags.TAGS[k]: v
    for k, v in exif_data.items()
    if k in ExifTags.TAGS
}

# Print the extracted text
print("Extracted Text:")
print(extracted_text)

# Print the metadata
print("\nMetadata:")
for tag, value in exif.items():
    print(f"{tag}: {value}")

# Save extracted text to a file
with open('extracted_text.txt', 'w') as f:
    f.write(extracted_text)

# Save metadata to a CSV file
meta_df = pd.DataFrame(list(exif.items()), columns=['Tag', 'Value'])
meta_df.to_csv('extracted_metadata.csv', index=False)

print("Extracted text saved to 'extracted_text.txt'.")
print("Extracted metadata saved to 'extracted_metadata.csv'.")

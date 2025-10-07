#First install those packages
#pip install rembg pillow
#pip install onnxruntime


import os
import io
from rembg import remove
from PIL import Image

# === CONFIGURATION ===
INPUT_FOLDER = "/content/drive/MyDrive/PicsWithBackground/"       # Folder containing your images
OUTPUT_FOLDER = "/content/drive/MyDrive/PicsWithoutBackground"     # Folder to save results
USE_WHITE_BACKGROUND = True         # Set to False for transparent PNGs
# ======================

# Create output folder if it doesn’t exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Get all image files (jpg, jpeg, png, etc.)
valid_exts = (".jpg", ".jpeg", ".png", ".webp")
files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(valid_exts)]

if not files:
    print("⚠️ No images found in", INPUT_FOLDER)
else:
    print(f"🧠 Found {len(files)} image(s) in '{INPUT_FOLDER}' — processing...\n")

for file_name in files:
    input_path = os.path.join(INPUT_FOLDER, file_name)
    file_root, _ = os.path.splitext(file_name)

    # Set output file extension
    if USE_WHITE_BACKGROUND:
        output_path = os.path.join(OUTPUT_FOLDER, f"{file_root}_white_bg.jpg")
    else:
        output_path = os.path.join(OUTPUT_FOLDER, f"{file_root}_no_bg.png")

    try:
        # Read input image
        with open(input_path, "rb") as inp_file:
            input_data = inp_file.read()

        # Remove background
        output_data = remove(input_data)

        if USE_WHITE_BACKGROUND:
            # Apply white background
            image = Image.open(io.BytesIO(output_data)).convert("RGBA")
            white_bg = Image.new("RGBA", image.size, (255, 255, 255, 255))
            final_image = Image.alpha_composite(white_bg, image).convert("RGB")
            final_image.save(output_path, "JPEG", quality=95)
        else:
            # Save with transparency
            with open(output_path, "wb") as out_file:
                out_file.write(output_data)

        print(f"✅ Processed: {file_name} → {os.path.basename(output_path)}")

    except Exception as e:
        print(f"❌ Error processing {file_name}: {e}")

print("\n🎉 Done! Check your output folder:", OUTPUT_FOLDER)
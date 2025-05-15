import cv2
import sys

# File paths
file_paths = ['image1.jpg', 'image2.jpg', 'image3.jpg', 'image4.jpg']

# Load images and validate
images = []
for path in file_paths:
    img = cv2.imread(path)
    if img is None:
        print(f"❌ Failed to load image: {path}")
        sys.exit(1)
    images.append(img)

# Create stitcher
stitcher = cv2.Stitcher_create()

# Stitch
status, stitched = stitcher.stitch(images)

# Check result
if status == cv2.Stitcher_OK:
    print("✅ Stitching successful.")
    cv2.imwrite('stitched_output.jpg', stitched)
else:
    print("❌ Stitching failed with status code:", status)

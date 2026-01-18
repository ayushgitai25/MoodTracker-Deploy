import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Define paths
train_dir = 'data/train'
emotion = 'happy'  # Let's check a happy face

# Construct path to a specific folder
folder_path = os.path.join(train_dir, emotion)

try:
    # Get list of images in the 'happy' folder
    images = os.listdir(folder_path)
    
    if len(images) > 0:
        print(f"✅ Found {len(images)} images in {emotion} folder.")
        
        # Pick the first image
        img_path = os.path.join(folder_path, images[0])
        img = mpimg.imread(img_path)
        
        # Show it
        plt.imshow(img, cmap='gray')
        plt.title(f"Sample: {emotion}")
        plt.axis('off')
        plt.show()
    else:
        print(f"⚠️ The folder 'data/train/{emotion}' exists but is empty.")

except FileNotFoundError:
    print("❌ ERROR: Could not find the folder. Check your path!")
    print(f"Expected to find: {os.path.abspath(folder_path)}")
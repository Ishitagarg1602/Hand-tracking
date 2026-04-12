import os
import random
import shutil

images_dir = "dataset/images"
labels_dir = "dataset/labels"

# Create target directories
for subset in ["train", "val"]:
    os.makedirs(os.path.join(images_dir, subset), exist_ok=True)
    os.makedirs(os.path.join(labels_dir, subset), exist_ok=True)

# Find all image files that are right in the images_dir
image_files = [f for f in os.listdir(images_dir) if f.endswith(".jpg") and os.path.isfile(os.path.join(images_dir, f))]

# Shuffle the data securely for a randomized split
random.seed(42)
random.shuffle(image_files)

# 80% train, 20% validation split
split_idx = int(len(image_files) * 0.8)
train_files = image_files[:split_idx]
val_files = image_files[split_idx:]

def move_files(files, subset):
    moved_images = 0
    moved_labels = 0
    for img_file in files:
        base_name = os.path.splitext(img_file)[0]
        
        # Move image
        src_img = os.path.join(images_dir, img_file)
        dst_img = os.path.join(images_dir, subset, img_file)
        shutil.move(src_img, dst_img)
        moved_images += 1
        
        # Move corresponding label if it exists
        label_file = f"{base_name}.txt"
        src_label = os.path.join(labels_dir, label_file)
        dst_label = os.path.join(labels_dir, subset, label_file)
        
        if os.path.exists(src_label):
            shutil.move(src_label, dst_label)
            moved_labels += 1
            
    return moved_images, moved_labels

train_img, train_lbl = move_files(train_files, "train")
val_img, val_lbl = move_files(val_files, "val")

print(f"Data split complete!")
print(f"Train subset: {train_img} images, {train_lbl} labels")
print(f"Val subset: {val_img} images, {val_lbl} labels")

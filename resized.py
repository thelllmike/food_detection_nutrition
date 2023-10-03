from PIL import Image
import os

# List of all your images directories
image_directories = [
    'apple_pie', 'baby_back_ribs', 'baklava', 'beef_carpaccio', 'beef_tartare',
    'beet_salad', 'beignets', 'bibimbap', 'bread_pudding', 'breakfast_burrito',
    'bruschetta', 'caesar_salad', 'cannoli', 'carrot_cake', 'ceviche', 'cheesecake',
    'chicken_curry', 'chicken_quesadilla', 'chicken_wings', 'chocolate_cake',
    'chocolate_mousse', 'churros', 'club_sandwich', 'crab_cakes', 'creme_brulee',
    'croque_madame', 'cup_cakes', 'deviled_eggs', 'donuts', 'dumplings', 'eggs_benedict',
    'escargots', 'falafel', 'filet_mignon', 'fish_and_chips', 'foie_gras', 'french_fries',
    'french_onion_soup', 'french_toast', 'fried_calamari', 'fried_rice', 'frozen_yogurt',
    'garlic_bread', 'gnocchi', 'greek_salad', 'grilled_cheese_sandwich', 'grilled_salmon',
    'guacamole', 'gyoza', 'hamburger', 'hot_and_sour_soup', 'hot_dog', 'huevos_rancheros',
    'hummus', 'ice_cream', 'lasagna', 'lobster_bisque', 'lobster_roll_sandwich',
    'macaroni_and_cheese', 'macarons', 'miso_soup', 'mussels', 'nachos', 'omelette',
    'onion_rings', 'oysters', 'pad_thai', 'paella', 'pancakes', 'panna_cotta',
    'peking_duck', 'pho', 'pizza', 'pork_chop', 'poutine'
]

# Desired size
desired_size = (256, 256)  # Setting the desired image size to 256x256

# Iterate over all specified directories
for images_path in image_directories:
    # Check if the specified directory exists
    if not os.path.exists(images_path):
        print(f"Directory {images_path} does not exist. Skipping.")
        continue
    
    print(f"Resizing images in {images_path} ...")
    
    # Iterate over all subdirectories and files in the given directory
    for root, dirs, files in os.walk(images_path):
        for file in files:
            if file.endswith(".jpg"):  # or use another image extension if needed
                image_path = os.path.join(root, file)
                try:
                    with Image.open(image_path) as img:
                        img_resized = img.resize(desired_size)  # Removed Image.ANTIALIAS
                        img_resized.save(image_path)  # Overwriting the original image file
                except Exception as e:
                    print(f"Error resizing {image_path}: {e}")

print("Resizing Completed")

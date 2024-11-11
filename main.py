import requests
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

output_folder = "downloaded_images"
os.makedirs(output_folder, exist_ok=True)

# Generate all URLs
urls = []
for i in range(1, 50):
    for j in range(1, 50):
        for fmt in ["png", "gif"]:
            url = f"https://www.cameronsworld.net/img/content/{i}/{j}.{fmt}"
            urls.append(url)

def download_image(url):
    try:
        
        image_name = f"{url.split('/')[-2]}_{os.path.basename(url)}"
        
        # GET request to the URL
        response = requests.get(url, timeout=10)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Save the image file
            with open(os.path.join(output_folder, image_name), "wb") as f:
                f.write(response.content)
            print(f"Downloaded {image_name}")
        else:
            print(f"Failed to download {url}, status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

# Download images using multithreading
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(download_image, url) for url in urls]
    for future in as_completed(futures):
        future.result()  # Handle any exceptions that may arise

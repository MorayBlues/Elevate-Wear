import cloudinary
import os
import cloudinary.uploader
from dotenv import load_dotenv
load_dotenv()
cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET")
)

def upload_image(file):
    result = cloudinary.uploader.upload(file)
    return result['secure_url']
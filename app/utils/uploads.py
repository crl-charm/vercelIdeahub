import os
import uuid
import logging
from flask import current_app
from werkzeug.utils import secure_filename

logger = logging.getLogger(__name__)

def get_upload_folder():
    """Get upload folder from config, create if needed"""
    folder = current_app.config.get('UPLOAD_FOLDER', os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static', 'uploads', 'menu'))
    os.makedirs(folder, exist_ok=True)
    return folder

def allowed_file(filename):
    """Check if file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config.get('ALLOWED_UPLOAD_EXTENSIONS', {'png', 'jpg', 'jpeg', 'gif', 'webp'})

def validate_and_save_image(file):
    """Validate and save image file with error handling"""
    try:
        max_size = current_app.config.get('UPLOAD_MAX_FILE_SIZE', 5 * 1024 * 1024)
        
        if not file or file.filename == '':
            return None, "No file provided"
        
        if not allowed_file(file.filename):
            return None, "File type not allowed. Use: PNG, JPG, JPEG, GIF, WebP"
        
        # Check file size
        file.seek(0, 2)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > max_size:
            return None, f"File too large. Max size: {max_size / 1024 / 1024:.0f}MB"
        
        if file_size == 0:
            return None, "File is empty"
        
        # Additional security: Check file header (magic bytes)
        file_header = file.read(16)
        file.seek(0)
        
        allowed_headers = {
            b'\x89PNG\r\n\x1a\n',  # PNG
            b'\xff\xd8\xff',        # JPEG
            b'GIF87a',             # GIF
            b'GIF89a',             # GIF
            b'RIFF',               # WebP (starts with RIFF)
        }
        
        is_valid_header = any(file_header.startswith(header) for header in allowed_headers)
        if not is_valid_header:
            logger.warning(f"Rejected file with invalid header: {file_header[:10]}")
            return None, "Invalid file format"
        
        # Generate unique filename with UUID
        ext = secure_filename(file.filename).rsplit('.', 1)[1].lower()
        unique_filename = f"menu_{uuid.uuid4().hex}.{ext}"
        
        upload_folder = get_upload_folder()
        filepath = os.path.join(upload_folder, unique_filename)
        
        # Try to optimize image if PIL available
        try:
            from PIL import Image
            img = Image.open(file)
            
            # Convert RGBA to RGB if necessary
            if img.mode == 'RGBA':
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                rgb_img.paste(img, mask=img.split()[3])
                img = rgb_img
            
            # Resize if too large (max 1200px)
            if img.width > 1200:
                ratio = 1200 / img.width
                new_height = int(img.height * ratio)
                img = img.resize((1200, new_height), Image.Resampling.LANCZOS)
            
            img.save(filepath, quality=85, optimize=True)
        except ImportError:
            # Fallback: save without optimization
            file.seek(0)
            file.save(filepath)
        except Exception as e:
            logger.warning(f"Image optimization failed, saving raw: {e}")
            file.seek(0)
            file.save(filepath)
        
        return f"/static/uploads/menu/{unique_filename}", None
        
    except Exception as e:
        logger.error(f"Image save error: {e}")
        return None, f"Error saving file: {str(e)}"

def delete_old_image(image_url):
    """Delete old image file when updating"""
    if not image_url:
        return
    try:
        if image_url.startswith('/static/uploads/menu/'):
            filename = image_url.replace('/static/uploads/menu/', '')
            filepath = os.path.join(get_upload_folder(), filename)
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.info(f"Deleted old image: {filename}")
    except Exception as e:
        logger.warning(f"Error deleting old image: {e}")

from __future__ import annotations

from flask import Blueprint, jsonify, request, render_template, current_app
import os
import uuid
from werkzeug.utils import secure_filename
import logging

from app.repositories.menu_repository import MenuRepository
from app.services.menu_service import MenuService
from app.utils.auth import admin_required, login_required
from app.core.socketio_handlers import emit_menu_update

menu_bp = Blueprint("menu", __name__, url_prefix="/admin/menu")

_service = MenuService(repo=MenuRepository())

logger = logging.getLogger(__name__)

# Valid categories
VALID_CATEGORIES = ["Main Dish", "Snack", "Beverages"]

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



@menu_bp.route("", methods=["GET"])
@login_required
def menu_page() -> str:
    items = _service.list_all()
    return render_template("admin/menu.html", items=items, categories=VALID_CATEGORIES)


@menu_bp.route("/api/items", methods=["GET"])
@login_required
def api_list_items() -> tuple:
    items = _service.list_available()
    return jsonify({"success": True, "data": items}), 200


@menu_bp.route("/api/items/all", methods=["GET"])
@login_required
def api_all_items() -> tuple:
    items = _service.list_all()
    return jsonify({"success": True, "data": items}), 200


@menu_bp.route("/api/categories", methods=["GET"])
@login_required
def api_get_categories() -> tuple:
    return jsonify({"success": True, "data": VALID_CATEGORIES}), 200


@menu_bp.route("/api/items", methods=["POST"])
@login_required
def api_create_item() -> tuple:
    category = request.form.get("category", "").strip()
    
    # Validate category
    if category not in VALID_CATEGORIES:
        return jsonify({"success": False, "error": f"Category must be one of: {', '.join(VALID_CATEGORIES)}"}), 400
    
    # Validate required fields
    name = request.form.get("name", "").strip()
    price = request.form.get("price", "").strip()
    
    if not name:
        return jsonify({"success": False, "error": "Item name is required"}), 400
    
    if not price:
        return jsonify({"success": False, "error": "Price is required"}), 400
    
    try:
        price = float(price)
        if price < 0:
            return jsonify({"success": False, "error": "Price must be positive"}), 400
    except ValueError:
        return jsonify({"success": False, "error": "Price must be a valid number"}), 400
    
    # Handle image upload
    image_url = None
    if 'image' in request.files:
        image_url, error = validate_and_save_image(request.files['image'])
        if error:
            return jsonify({"success": False, "error": error}), 400
    
    # Create item
    result = _service.create(
        name=name,
        price=price,
        category=category,
        description=request.form.get("description", "").strip() or None,
        image_url=image_url,
    )
    if result.get("success"):
        emit_menu_update('create', result.get("data", {}))
    return jsonify(result), 201


@menu_bp.route("/api/items/<int:item_id>", methods=["PATCH"])
@login_required
def api_update_item(item_id: int) -> tuple:
    from app.models.menu_item import MenuItem
    from app import db
    
    category = request.form.get("category", "").strip()
    
    if category and category not in VALID_CATEGORIES:
        return jsonify({"success": False, "error": f"Category must be one of: {', '.join(VALID_CATEGORIES)}"}), 400
    
    # Validate price if provided
    price = request.form.get("price", "").strip()
    if price:
        try:
            price = float(price)
            if price < 0:
                return jsonify({"success": False, "error": "Price must be positive"}), 400
        except ValueError:
            return jsonify({"success": False, "error": "Price must be a valid number"}), 400
    else:
        price = None
    
    # Handle image upload
    image_url = None
    old_image_url = None
    
    if 'image' in request.files and request.files['image'].filename:
        # Get old image URL for cleanup
        item = db.session.get(MenuItem, item_id)
        if item:
            old_image_url = item.image_url
        
        # Save new image
        image_url, error = validate_and_save_image(request.files['image'])
        if error:
            return jsonify({"success": False, "error": error}), 400
        
        # Delete old image after successful save
        if old_image_url:
            delete_old_image(old_image_url)
    
    # Update item
    result = _service.update(
        item_id=item_id,
        name=request.form.get("name", "").strip() or None,
        price=price,
        category=category if category else None,
        description=request.form.get("description", "").strip() or None,
        image_url=image_url,
    )
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    if result.get("success"):
        emit_menu_update('update', {'item_id': item_id, **result.get("data", {})})
    return jsonify(result), 200


@menu_bp.route("/api/items/<int:item_id>/availability", methods=["PATCH"])
@login_required
def api_toggle_availability(item_id: int) -> tuple:
    result = _service.toggle_availability(item_id)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    if result.get("success"):
        emit_menu_update('availability_toggle', {'item_id': item_id, **result.get("data", {})})
    return jsonify(result), 200


@menu_bp.route("/api/items/<int:item_id>", methods=["DELETE"])
@login_required
def api_delete_item(item_id: int) -> tuple:
    from app.models.menu_item import MenuItem
    from app import db
    
    # Get item to retrieve image URL for cleanup
    item = db.session.get(MenuItem, item_id)
    image_url = item.image_url if item else None
    
    # Delete from database
    result = _service.delete(item_id)
    
    # Delete image file if delete was successful
    if isinstance(result, dict) and result.get("success"):
        if image_url:
            delete_old_image(image_url)
        emit_menu_update('delete', {'item_id': item_id})
    
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 200


@menu_bp.route("/api/menu-items", methods=["GET"])
@login_required
def api_menu_items_alias() -> tuple:
    items = _service.list_all()
    return jsonify({"success": True, "data": items}), 200

"""
Socket.IO event handlers for real-time updates across inventory, menu, expenses, and receivables
"""
from flask_socketio import emit
from app import socketio


# Inventory Events
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit('connected', {'data': 'Connected to server'})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnect"""
    pass


def emit_inventory_update(event_type, item_data):
    """Broadcast inventory updates to all connected clients
    
    Args:
        event_type: 'create', 'update', 'delete', 'stock_change'
        item_data: dict containing item information
    """
    socketio.emit('inventory_update', {
        'event': event_type,
        'data': item_data
    })


def emit_menu_update(event_type, item_data):
    """Broadcast menu updates to all connected clients
    
    Args:
        event_type: 'create', 'update', 'delete', 'availability_toggle'
        item_data: dict containing menu item information
    """
    socketio.emit('menu_update', {
        'event': event_type,
        'data': item_data
    })


def emit_expenses_update(event_type, expense_data):
    """Broadcast expense updates to all connected clients
    
    Args:
        event_type: 'create', 'delete'
        expense_data: dict containing expense information
    """
    socketio.emit('expenses_update', {
        'event': event_type,
        'data': expense_data
    })


def emit_receivables_update(event_type, receivable_data):
    """Broadcast receivables updates to all connected clients
    
    Args:
        event_type: 'create', 'mark_paid', 'update'
        receivable_data: dict containing receivable information
    """
    socketio.emit('receivables_update', {
        'event': event_type,
        'data': receivable_data
    })


def emit_inventory_low_stock(payload: dict) -> None:
    socketio.emit("inventory_low_stock", payload)


def emit_receivable_marked_paid(receivable_id: int) -> None:
    socketio.emit("receivable_marked_paid", {"receivable_id": receivable_id})


def emit_debt_due_reminder(payload: dict) -> None:
    socketio.emit("debt_due_reminder", payload)


def emit_daily_sales_closed(payload: dict) -> None:
    socketio.emit("daily_sales_closed", payload)

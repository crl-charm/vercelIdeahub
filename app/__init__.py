from flask import Flask, request, g
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from flask_socketio import SocketIO
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
import logging
import os

# Create database object
db = SQLAlchemy()
_sqlalchemy_db = db
socketio = SocketIO(cors_allowed_origins="*")  # Will be overridden by CORS
csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address)


def create_app():

    import sys
    import os

    # Set up static folder - Flask should serve from root-level static directory
    static_folder = os.path.join(os.path.dirname(__file__), '..', 'static')
    app = Flask(__name__, static_folder=static_folder, static_url_path='/static')

    # Fix 1: config.py is outside the app folder, so import it properly
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from config import Config
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    socketio.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)

    # Configure CORS restrictively
    CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)

    # Configure logging
    configure_logging(app)

    # Register security middleware
    register_security_middleware(app)

    # import routes
    from app.routes.session_routes import session_bp
    from app.routes.order_routes import order_bp
    from app.routes.sales_routes import sales_bp
    from app.routes.sales_balance import sales_bp as sales_balance_bp
    from app.routes.user_routes import user_bp
    from app.routes.auth_routes import bp as auth_bp
    from app.routes.dashboard_routes import bp as dashboard_bp
    from app.routes.boardroom_routes import boardroom_bp
    from app.routes.admin_routes import admin_bp
    from app.routes.lounge_routes import lounge_bp
    from app.routes.inventory import inventory_bp
    from app.routes.receivables import receivables_bp
    from app.routes.expenses import expenses_bp
    from app.routes.staff_performance import staff_performance_bp
    from app.routes.analytics import analytics_bp
    from app.routes.reservations import reservations_bp
    from app.routes.receipts import receipts_bp
    from app.routes.menu import menu_bp
    from app.routes.qr_order import qr_bp, order_bp as qr_order_bp
    from app.controllers.analytics_controller import AnalyticsController
    from app.controllers.performance_controller import PerformanceController
    from app.controllers.finance_controller import FinanceController
    from app.controllers.management_controller import ManagementController

    # register routes
    app.register_blueprint(session_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(sales_bp)
    app.register_blueprint(sales_balance_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(boardroom_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(lounge_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(receivables_bp)
    app.register_blueprint(expenses_bp)
    app.register_blueprint(staff_performance_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(reservations_bp)
    app.register_blueprint(receipts_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(qr_bp)
    app.register_blueprint(qr_order_bp)

    # Import Socket.IO handlers to register events
    from app.core import socketio_handlers

    controllers = [
        AnalyticsController(db),
        PerformanceController(db),
        FinanceController(db),
        ManagementController(db),
    ]
    for controller in controllers:
        controller.register(app)

    @app.route("/")
    def home():
        return render_template("landing.html")

    return app


def configure_logging(app):
    """Configure comprehensive logging for security and debugging"""
    if not app.debug:
        # Production logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('app.log'),
                logging.StreamHandler()
            ]
        )

        # Security-specific logger
        security_logger = logging.getLogger('security')
        security_logger.setLevel(logging.INFO)
        security_handler = logging.FileHandler('security.log')
        security_handler.setFormatter(logging.Formatter(
            '%(asctime)s - SECURITY - %(levelname)s - %(message)s'
        ))
        security_logger.addHandler(security_handler)
    else:
        # Development logging
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )


def register_security_middleware(app):
    """Register security middleware and error handlers"""

    @app.before_request
    def security_headers():
        """Add security headers to all responses"""
        for header, value in app.config.get('SECURITY_HEADERS', {}).items():
            g.security_headers = getattr(g, 'security_headers', {})
            g.security_headers[header] = value

    @app.after_request
    def apply_security_headers(response):
        """Apply security headers to response"""
        security_headers = getattr(g, 'security_headers', {})
        for header, value in security_headers.items():
            response.headers[header] = value
        return response

    @app.errorhandler(404)
    def not_found_error(error):
        """Handle 404 errors securely"""
        if request.path.startswith('/api/'):
            return {'error': 'Resource not found'}, 404
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors without leaking information"""
        db.session.rollback()
        if request.path.startswith('/api/'):
            return {'error': 'Internal server error'}, 500
        return render_template('500.html'), 500

    @app.errorhandler(403)
    def forbidden_error(error):
        """Handle 403 errors"""
        if request.path.startswith('/api/'):
            return {'error': 'Forbidden'}, 403
        return render_template('403.html'), 403

        
import logging
import os
from app import create_app, db
from sqlalchemy.exc import OperationalError
from flask_migrate import upgrade

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    try:
        # 尝试删除现有的数据库文件
        if os.path.exists('instance/app.db'):
            os.remove('instance/app.db')
            logger.info("Removed existing database file")
    except Exception as e:
        logger.warning(f"Error removing database file: {e}")

    try:
        # 确保 instance 目录存在
        os.makedirs('instance', exist_ok=True)
        
        # 创建所有表
        with create_app().app_context():
            db.create_all()
            logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

if __name__ == '__main__':
    logger.info("Starting application...")
    try:
        init_db()
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        
    app = create_app()
    print("Starting server...")
    print("Access URLs:")
    print("Local:    http://127.0.0.1:3000")
    print("External: http://0.0.0.0:3000")
    app.run(host='0.0.0.0', port=3000, debug=True)
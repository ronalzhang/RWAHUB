import logging
import os
from app import create_app, db
from sqlalchemy.exc import OperationalError
from flask_migrate import upgrade
import sqlite3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_db_tables():
    """验证数据库表是否存在"""
    try:
        app = create_app()
        with app.app_context():
            # 尝试连接数据库
            conn = sqlite3.connect('instance/app.db')
            cursor = conn.cursor()
            
            # 检查表是否存在
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            logger.info(f"现有的数据库表: {tables}")
            
            # 如果没有找到必要的表，重新创建
            required_tables = {'assets', 'users', 'trades', 'dividend_records'}
            existing_tables = {table[0] for table in tables}
            
            if not required_tables.issubset(existing_tables):
                logger.warning(f"缺少必要的表，现有表: {existing_tables}")
                return False
                
            return True
    except Exception as e:
        logger.error(f"验证数据库表时出错: {e}")
        return False
    finally:
        try:
            conn.close()
        except:
            pass

def init_db():
    try:
        # 确保 instance 目录存在
        os.makedirs('instance', exist_ok=True)
        logger.info("Instance 目录已创建")
        
        # 检查数据库文件权限
        db_path = 'instance/app.db'
        if os.path.exists(db_path):
            try:
                # 检查文件权限
                os.access(db_path, os.W_OK)
                logger.info("数据库文件可写")
                # 尝试删除现有数据库
                os.remove(db_path)
                logger.info("已删除现有数据库文件")
            except Exception as e:
                logger.error(f"处理现有数据库文件时出错: {e}")
                raise

        # 创建应用上下文
        app = create_app()
        with app.app_context():
            # 尝试创建所有表
            db.create_all()
            logger.info("数据库表创建完成")
            
            # 验证表是否真的创建成功
            if not verify_db_tables():
                raise Exception("数据库表验证失败")
                
    except Exception as e:
        logger.error(f"初始化数据库时出错: {e}")
        raise

if __name__ == '__main__':
    logger.info("启动应用...")
    success = False
    
    for attempt in range(3):  # 最多尝试3次
        try:
            init_db()
            success = True
            logger.info("数据库初始化成功")
            break
        except Exception as e:
            logger.error(f"第 {attempt + 1} 次尝试初始化数据库失败: {e}")
    
    if not success:
        logger.error("所有数据库初始化尝试都失败了")
        
    app = create_app()
    print("启动服务器...")
    print("访问地址:")
    print("本地:    http://127.0.0.1:3000")
    print("外部:    http://0.0.0.0:3000")
    app.run(host='0.0.0.0', port=3000, debug=True)
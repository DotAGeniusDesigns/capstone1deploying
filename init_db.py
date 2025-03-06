"""
Database initialization script for Fortune Teller app.
Run this script manually if you need to reset and initialize the database completely.
"""
import os
import logging
from flask import Flask
from flask_migrate import Migrate
from models import db, User, DailyFortune, MBTITrait, ChineseZodiac
from seed_mbti import seed_mbti_data
from seed_chinese_zodiac import seed_chinese_zodiac_data
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def init_database():
    """Initialize the database from scratch"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key')

    # Get database URL from environment
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///site.db')
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    bcrypt = Bcrypt(app)
    
    with app.app_context():
        try:
            # Drop all tables and recreate them
            logger.info("Dropping all tables...")
            db.drop_all()
            logger.info("Creating all tables...")
            db.create_all()
            
            # Seed MBTI data
            logger.info("Seeding MBTI data...")
            seed_mbti_data(db)
            
            # Seed Chinese Zodiac data
            logger.info("Seeding Chinese Zodiac data...")
            seed_chinese_zodiac_data(db)
            
            # Create admin user if needed
            username = os.getenv('ADMIN_USERNAME', 'admin')
            if not User.query.filter_by(username=username).first():
                from datetime import datetime
                
                # Create admin user
                admin_password = os.getenv('ADMIN_PASSWORD', 'password123')  # Should be set in environment
                hashed_password = bcrypt.generate_password_hash(admin_password).decode('utf-8')
                
                admin = User(
                    username=username,
                    email=os.getenv('ADMIN_EMAIL', 'admin@example.com'),
                    password=hashed_password,
                    name='Administrator',
                    birthday=datetime.strptime('1990-01-01', '%Y-%m-%d').date(),
                    role='admin'
                )
                db.session.add(admin)
                db.session.commit()
                logger.info(f"Admin user '{username}' created")
            
            logger.info("Database initialization complete!")
            return True
            
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            return False

if __name__ == "__main__":
    success = init_database()
    if success:
        print("Database initialized successfully!")
    else:
        print("Database initialization failed. Check the logs for details.") 
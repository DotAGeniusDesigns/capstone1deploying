from app import app, db, bcrypt
from models import User, MBTITrait, ChineseZodiac
from datetime import date

def seed_database():
    """
    Seeds the database with initial data for testing
    """
    with app.app_context():
        # Create admin user
        if User.query.filter_by(username='admin').first() is None:
            admin_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
            admin_user = User(
                name='Admin User',
                birthday=date(1990, 1, 1),
                username='admin',
                email='admin@example.com',
                password=admin_password,
                mbti='INTJ',
                chinese_zodiac='Horse',
                role='admin'
            )
            db.session.add(admin_user)
            
        # Create test user
        if User.query.filter_by(username='testuser').first() is None:
            user_password = bcrypt.generate_password_hash('test123').decode('utf-8')
            test_user = User(
                name='Test User',
                birthday=date(1992, 5, 15),
                username='testuser',
                email='test@example.com',
                password=user_password,
                mbti='ENFP',
                chinese_zodiac='Monkey',
                role='user'
            )
            db.session.add(test_user)
        
        # Add MBTI traits if not already present
        if MBTITrait.query.count() == 0:
            mbti_traits = [
                MBTITrait(
                    type='INTJ',
                    strengths='Strategic, analytical, independent, determined, knowledgeable, curious',
                    weaknesses='Arrogant, dismissive of emotions, overly critical, combative, socially clueless'
                ),
                MBTITrait(
                    type='ENFP',
                    strengths='Enthusiastic, creative, sociable, free-spirited, energetic, optimistic',
                    weaknesses='Disorganized, impractical, easily stressed, overly emotional, unfocused'
                ),
                # Add more as needed
            ]
            db.session.add_all(mbti_traits)
        
        # Add Chinese Zodiac info if not already present
        if ChineseZodiac.query.count() == 0:
            zodiac_info = [
                ChineseZodiac(
                    sign='Horse',
                    yearly_fortune_2024='A year of potential advancement and recognition in your career. Focus on building strong relationships and maintain a balanced approach to work and personal life.'
                ),
                ChineseZodiac(
                    sign='Monkey',
                    yearly_fortune_2024='A year filled with creativity and unexpected opportunities. Your quick thinking will help you adapt to changing circumstances, but remember to follow through on your commitments.'
                ),
                # Add more as needed
            ]
            db.session.add_all(zodiac_info)
        
        db.session.commit()
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_database() 
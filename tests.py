import unittest
from app import app, db
from models import User, DailyFortune, MBTITrait, ChineseZodiac
from datetime import datetime, date, timedelta
from flask_bcrypt import Bcrypt
import json
import os

class FortuneTellingAppTests(unittest.TestCase):
    """Test suite for the Fortune Telling Web Application"""

    def setUp(self):
        """Setup test environment before each test"""
        # Configure test database
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        
        self.app = app.test_client()
        self.bcrypt = Bcrypt(app)
        
        # Create database tables
        with app.app_context():
            db.create_all()
            self._create_test_data()
            
    def tearDown(self):
        """Clean up after each test"""
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def _create_test_data(self):
        """Create test data for the database"""
        # Create test user with admin role
        admin_password = self.bcrypt.generate_password_hash('testadmin123').decode('utf-8')
        admin_user = User(
            name='Admin User',
            birthday=date(1990, 1, 1),
            username='admin',
            email='admin@test.com',
            password=admin_password,
            mbti='INTJ',
            chinese_zodiac='Horse',
            role='admin'
        )
        
        # Create regular test user
        user_password = self.bcrypt.generate_password_hash('testuser123').decode('utf-8')
        regular_user = User(
            name='Test User',
            birthday=date(1992, 5, 15),
            username='testuser',
            email='user@test.com',
            password=user_password,
            mbti='ENFP',
            chinese_zodiac='Monkey',
            role='user'
        )
        
        # Create test MBTI trait
        intj_trait = MBTITrait(
            type='INTJ',
            strengths='Strategic, analytical, independent, dedicated',
            weaknesses='Overly critical, dismissive of emotions, perfectionistic'
        )
        
        enfp_trait = MBTITrait(
            type='ENFP',
            strengths='Enthusiastic, creative, sociable, free-spirited',
            weaknesses='Disorganized, overly optimistic, trouble focusing'
        )
        
        # Create test Chinese Zodiac
        horse_zodiac = ChineseZodiac(
            sign='Horse',
            yearly_fortune_2024='A year of potential advancement and recognition.'
        )
        
        monkey_zodiac = ChineseZodiac(
            sign='Monkey',
            yearly_fortune_2024='A year of innovation and unexpected opportunities.'
        )
        
        # Create test daily fortune
        today = datetime.now().date()
        taurus_fortune = DailyFortune(
            zodiac_sign='taurus',
            date=today,
            fortune='Today is a day for practical planning and financial decisions.'
        )
        
        gemini_fortune = DailyFortune(
            zodiac_sign='gemini',
            date=today,
            fortune='Communication is highlighted today. Express your ideas clearly.'
        )
        
        db.session.add_all([admin_user, regular_user, intj_trait, enfp_trait, 
                            horse_zodiac, monkey_zodiac, taurus_fortune, gemini_fortune])
        db.session.commit()
    
    # Test User Authentication
    def test_login_success(self):
        """Test successful login"""
        response = self.app.post('/login', data={
            'username': 'testuser',
            'password': 'testuser123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful', response.data)
    
    def test_login_wrong_password(self):
        """Test login with incorrect password"""
        response = self.app.post('/login', data={
            'username': 'testuser',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login Unsuccessful', response.data)
    
    def test_signup(self):
        """Test user registration"""
        response = self.app.post('/signup', data={
            'name': 'New User',
            'birthday': '1995-03-15',
            'username': 'newuser',
            'email': 'new@test.com',
            'password': 'newpassword123',
            'confirm_password': 'newpassword123',
            'mbti': 'ISFJ'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your account has been created', response.data)
        
        # Verify user was added to database
        with app.app_context():
            user = User.query.filter_by(username='newuser').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.email, 'new@test.com')
            self.assertEqual(user.role, 'user')
    
    # Test Role-Based Access Control
    def test_admin_access(self):
        """Test admin access to generate fortunes page"""
        # Login as admin
        self.app.post('/login', data={
            'username': 'admin',
            'password': 'testadmin123'
        })
        # Access admin-only page
        response = self.app.get('/generate_fortunes', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Generate Today\'s Fortune', response.data)
    
    def test_regular_user_cannot_access_admin_page(self):
        """Test regular user cannot access admin-only pages"""
        # Login as regular user
        self.app.post('/login', data={
            'username': 'testuser',
            'password': 'testuser123'
        })
        # Try to access admin-only page
        response = self.app.get('/generate_fortunes', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You do not have permission', response.data)
    
    # Test User Profile Editing
    def test_edit_account(self):
        """Test editing user account details"""
        # Login first
        self.app.post('/login', data={
            'username': 'testuser',
            'password': 'testuser123'
        })
        
        # Edit account
        response = self.app.post('/edit_account', data={
            'name': 'Updated User',
            'birthday': '1992-05-15',
            'username': 'testuser',
            'email': 'updated@test.com',
            'mbti': 'INFJ'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your account has been updated successfully', response.data)
        
        # Verify changes in database
        with app.app_context():
            user = User.query.filter_by(username='testuser').first()
            self.assertEqual(user.name, 'Updated User')
            self.assertEqual(user.email, 'updated@test.com')
            self.assertEqual(user.mbti, 'INFJ')
    
    # Test Fortune Generation
    def test_daily_fortune_access(self):
        """Test accessing daily fortune page"""
        # Login first
        self.app.post('/login', data={
            'username': 'testuser',
            'password': 'testuser123'
        })
        
        # Access daily fortune page
        response = self.app.get('/daily_fortune', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # The page should contain the user's zodiac sign (Taurus for May 15)
        self.assertIn(b'taurus', response.data.lower())

if __name__ == '__main__':
    unittest.main() 
from models import db, ChineseZodiac

# Sample Chinese Zodiac data
chinese_zodiac_data = [
    {
        "sign": "Rat",
        "yearly_fortune_2024": "The year 2024 will bring Rat natives opportunities for growth and success in their careers."
    },
    {
        "sign": "Ox",
        "yearly_fortune_2024": "Ox natives will find stability and steady progress in 2024, especially in personal relationships."
    },
    {
        "sign": "Tiger",
        "yearly_fortune_2024": "Tigers will experience dynamic changes and should embrace new adventures in 2024."
    },
    {
        "sign": "Rabbit",
        "yearly_fortune_2024": "Rabbit natives will find peace and harmony in 2024, making it a great year for introspection."
    },
    {
        "sign": "Dragon",
        "yearly_fortune_2024": "2024 is a year of power and influence for Dragons, with significant achievements on the horizon."
    },
    {
        "sign": "Snake",
        "yearly_fortune_2024": "Snakes will need to focus on personal development and healing in 2024 to achieve inner peace."
    },
    {
        "sign": "Horse",
        "yearly_fortune_2024": "Horses will find success in social and professional spheres, with plenty of opportunities for networking."
    },
    {
        "sign": "Sheep",
        "yearly_fortune_2024": "Sheep natives will experience emotional fulfillment and should focus on creative projects in 2024."
    },
    {
        "sign": "Monkey",
        "yearly_fortune_2024": "Monkeys will find excitement and innovation in 2024, making it a great year for new ventures."
    },
    {
        "sign": "Rooster",
        "yearly_fortune_2024": "Roosters will see financial growth and should focus on long-term investments in 2024."
    },
    {
        "sign": "Dog",
        "yearly_fortune_2024": "Dogs will experience loyalty and strong bonds in relationships, making 2024 a year of love and trust."
    },
    {
        "sign": "Pig",
        "yearly_fortune_2024": "Pigs will find prosperity and joy in 2024, with opportunities for both personal and professional growth."
    }
]

def seed_chinese_zodiac_data(db_instance=None):
    """Seed the Chinese Zodiac table"""
    if db_instance is None:
        # This is for standalone execution
        from app import app, db
        with app.app_context():
            _perform_seeding(db)
    else:
        # This is when called from another module
        _perform_seeding(db_instance)
        
def _perform_seeding(db_instance):
    # Clear existing data
    db_instance.session.query(ChineseZodiac).delete()
    
    # Insert new data
    for zodiac in chinese_zodiac_data:
        new_zodiac = ChineseZodiac(
            sign=zodiac['sign'],
            yearly_fortune_2024=zodiac['yearly_fortune_2024']
        )
        db_instance.session.add(new_zodiac)
    
    db_instance.session.commit()
    print("Chinese Zodiac data seeded successfully!")

# Allow running as a standalone script
if __name__ == "__main__":
    seed_chinese_zodiac_data()

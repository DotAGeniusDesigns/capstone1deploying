from models import db, MBTITrait
from app import app

# Complete MBTI data
mbti_data = [
    {
        "type": "INTJ",
        "strengths": "Strategic, Logical, Efficient.",
        "weaknesses": "Arrogant, Judgmental, Overly Analytical."
    },
    {
        "type": "INTP",
        "strengths": "Innovative, Analytical, Objective.",
        "weaknesses": "Absent-minded, Condescending, Insensitive."
    },
    {
        "type": "ENTJ",
        "strengths": "Confident, Efficient, Strategic.",
        "weaknesses": "Stubborn, Dominant, Intolerant."
    },
    {
        "type": "ENTP",
        "strengths": "Innovative, Enthusiastic, Confident.",
        "weaknesses": "Argumentative, Insensitive, Intolerant."
    },
    {
        "type": "INFJ",
        "strengths": "Insightful, Inspiring, Decisive.",
        "weaknesses": "Sensitive, Private, Perfectionistic."
    },
    {
        "type": "INFP",
        "strengths": "Empathetic, Creative, Open-Minded.",
        "weaknesses": "Overly Idealistic, Self-Critical, Reserved."
    },
    {
        "type": "ENFJ",
        "strengths": "Charismatic, Altruistic, Empathetic.",
        "weaknesses": "Overly Idealistic, Intense, Overly Sensitive."
    },
    {
        "type": "ENFP",
        "strengths": "Curious, Observant, Energetic.",
        "weaknesses": "Overly Idealistic, Disorganized, Easily Stressed."
    },
    {
        "type": "ISTJ",
        "strengths": "Responsible, Reliable, Organized.",
        "weaknesses": "Stubborn, Insensitive, Judgmental."
    },
    {
        "type": "ISFJ",
        "strengths": "Supportive, Reliable, Patient.",
        "weaknesses": "Humble, Reluctant to Change, Overly Altruistic."
    },
    {
        "type": "ESTJ",
        "strengths": "Dedicated, Strong-Willed, Organized.",
        "weaknesses": "Inflexible, Judgmental, Stubborn."
    },
    {
        "type": "ESFJ",
        "strengths": "Supportive, Reliable, Sociable.",
        "weaknesses": "Overly Concerned with Social Status, Inflexible, Reluctant to Innovate."
    },
    {
        "type": "ISTP",
        "strengths": "Optimistic, Energetic, Practical.",
        "weaknesses": "Stubborn, Insensitive, Risky."
    },
    {
        "type": "ISFP",
        "strengths": "Charming, Imaginative, Passionate.",
        "weaknesses": "Fiercely Independent, Easily Stressed, Unpredictable."
    },
    {
        "type": "ESTP",
        "strengths": "Bold, Rational, Practical.",
        "weaknesses": "Insensitive, Impatient, Risk-Prone."
    },
    {
        "type": "ESFP",
        "strengths": "Bold, Original, Practical.",
        "weaknesses": "Easily Bored, Risk-Prone, Unfocused."
    }
]

def seed_mbti():
    with app.app_context():
        db.create_all()
        for trait in mbti_data:
            mbti_trait = MBTITrait(
                type=trait['type'],
                strengths=trait['strengths'],
                weaknesses=trait['weaknesses']
            )
            db.session.add(mbti_trait)
        db.session.commit()

if __name__ == '__main__':
    seed_mbti()

# models.py
import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
load_dotenv()

Base = declarative_base()

# SQLAlchemy setup
# Decide DB location
if os.environ.get("RENDER", "").lower() == "true":
    db_path = "/tmp/quiz.db"  # ✅ Writable in Render
else:
    db_path = os.path.join(os.path.dirname(__file__), "quiz.db")  # ✅ Local path
# SQLAlchemy setup
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    # ✅ Use PostgreSQL on Render
    engine = create_engine(DATABASE_URL)
else:
    # ✅ Use SQLite for local development
    db_path = os.path.join(os.path.dirname(__file__), "quiz.db")
    engine = create_engine(f"sqlite:///{db_path}")

Session = sessionmaker(bind=engine)

# Question Table
class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    prompt = Column(String)
    option_0 = Column(String)
    option_1 = Column(String)
    option_2 = Column(String)
    option_3 = Column(String)
    correct = Column(Integer)

# User Attempt Table
class UserAttempt(Base):
    __tablename__ = 'user_attempts'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    score = Column(Integer)

# Create tables and optionally populate if empty
def init_db():
    Base.metadata.create_all(engine)
    session = Session()
    if session.query(Question).count() == 0:
        questions = [
            Question(
                prompt="Why is the person who judges others without self-reflection inexcusable?",
                option_0="Because they know the law too well",
                option_1="Because they pray too little",
                option_2="Because they pass judgment while doing the same things",
                option_3="Because they are uneducated in Scripture",
                correct=2
            ),
            Question(
                prompt="What leads people to repentance according to Romans 2:4?",
                option_0="Fear of hell",
                option_1="God's goodness",
                option_2="Peer pressure",
                option_3="The Law of Moses",
                correct=1
            ),
            Question(
                prompt="What does stubbornness and an unrepentant heart store up?",
                option_0="Hope for the future",
                option_1="Earthly blessings",
                option_2="God's wrath",
                option_3="Greater understanding",
                correct=2
            ),
            Question(
                prompt="How will God judge each person, as stated in Romans 2:6?",
                option_0="According to their nationality",
                option_1="According to their deeds",
                option_2="According to their family lineage",
                option_3="According to their church attendance",
                correct=1
            ),
            Question(
                prompt="What reward is promised to those who seek glory, honor, and immortality?",
                option_0="Peace and prosperity",
                option_1="Eternal life",
                option_2="Earthly riches",
                option_3="Leadership over nations",
                correct=1
            ),
            Question(
                prompt="What will happen to those who are self-seeking and disobedient to the truth?",
                option_0="They will be given second chances endlessly",
                option_1="They will receive God's mercy",
                option_2="They will face wrath and indignation",
                option_3="They will inherit the kingdom",
                correct=2
            ),
            Question(
                prompt="According to Romans 2:11, what is true about God's judgment?",
                option_0="God judges by appearance",
                option_1="God shows no partiality",
                option_2="God favors the Israelites",
                option_3="God delays justice",
                correct=1
            ),
            Question(
                prompt="Who will be justified before God according to Romans 2:13?", 
                option_0="Only those who hear the law",
                option_1="Only the circumcised",
                option_2="The doers of the law",
                option_3="The teachers of the law",
                correct=2
            ),
            Question(
                prompt="What does Paul say about Gentiles who do not have the law?",
                option_0="They are automatically condemned",
                option_1="They are to be avoided",
                option_2="They can show the law written on their hearts",
                option_3="They must convert to Judaism",
                correct=2
            ),
            Question(
                prompt="Who is the real Jew according to Romans 2:29?", 
                option_0="One who descends from Abraham",
                option_1="One who is born in Israel",
                option_2="One inwardly, whose heart is circumcised by the Spirit",
                option_3="One who knows Hebrew",
                correct=2
            ),
            # Add remaining 8 questions similarly...
        ]
        session.add_all(questions)
        session.commit()
        print("✅ Questions added.")
    else:
        print("Questions already exist.")

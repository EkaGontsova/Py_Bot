import sqlalchemy as sq
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func


Base = declarative_base()


class Word(Base):
    __tablename__ = 'words'

    id = sq.Column(sq.Integer, primary_key=True)
    word = sq.Column(sq.String)
    translate = sq.Column(sq.String)


def create_session():
    DSN = ''
    engine = create_engine(DSN)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def delete_word(word):
    session = create_session()
    session.query(Word).filter_by(word=word).delete()
    session.commit()
    session.close()


def add_new_word(word, translate):
    session = create_session()
    new_word = Word(word=word, translate=translate)
    session.add(new_word)
    session.commit()
    session.close()


def get_random_pair():
    session = create_session()
    pair = session.query(Word).order_by(func.random()).first()
    session.close()
    return pair.word, pair.translate


if __name__ == "__main__":
    engine = create_engine('postgresql://postgres:AlexOvosh1984@localhost:5432/Py_HW')
    session = create_session()

    add_new_word("Лес", "Forest")
    add_new_word("Утро", "Morning")
    add_new_word("Вечер", "Evening")
    add_new_word("Небо", "Sky")
    add_new_word("Солнце", "Sun")
    add_new_word("Ночь", "Night")
    add_new_word("Река", "River")
    add_new_word("Гора", "Mountain")
    add_new_word("Луна", "Moon")
    add_new_word("Море", "Sea")

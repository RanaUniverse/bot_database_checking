"""This is special for checking different things"""

import random

from faker import Faker

from sqlmodel import Session

from database_code.table_part import (
    NotePart,
    UserPart,
)
from database_code.make_database import create_db_and_engine, engine


fake = Faker()


def make_fake_user():
    """
    When i will call this, it will make new fake user_part row
    """
    new_user = UserPart(
        user_id=random.randrange(1, 10000000, 5),
        username=fake.name().replace(" ", ""),
    )
    print(new_user)


def make_fake_note():
    """
    i will use NotePart to make a new note
    """
    new_note = NotePart(
        note_title="This is title",
        note_content="This is note subject completely without any issue",
    )
    print(new_note)


def add_some_user():
    """add some user to the database only user"""

    new_user = UserPart(
        user_id=random.randrange(0, 10000000, 5),
        username="_".join(fake.words(3)),
        first_name=fake.first_name().title(),
        last_name=fake.last_name().title(),
        email_id=fake.email(),
        phone_no=fake.phone_number(),
    )
    with Session(engine) as session:
        session.add(new_user)
        session.commit()


def add_some_note():

    title = " ".join(fake.words(3))
    content = fake.sentence(25)

    new_note = NotePart(
        note_title=title,
        note_content=content,
        # user_id=1
    )

    with Session(engine) as session:
        session.add(new_note)
        session.commit()


def main():
    create_db_and_engine()
    # add_some_user()
    # add_some_note()


if __name__ == "__main__":
    main()

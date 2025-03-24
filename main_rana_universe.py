"""This is special for checking different things"""

import random

from faker import Faker

from sqlmodel import Session, select

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


def select_all_user():
    """
    search on user table about some user
    """
    with Session(engine) as session:
        statement = select(UserPart)
        results = session.exec(statement)
        users = results.all()
        print(users)


def select_all_note():
    """
    lets search for each note obj
    """
    with Session(engine) as session:
        statement = select(NotePart)
        results = session.exec(statement)
        notes = results.all()
        print(notes)


def find_one_user():
    """
    lets find one row in the user table
    """
    with Session(engine) as session:
        statement = select(UserPart).where(UserPart.first_name == "Tinaaa")
        results = session.exec(statement).first()
        print(results)


def search_notes_of_a_user():
    """'
    it will search for all the notes a user has own
    """
    user_id = 32
    with Session(engine) as session:
        statement = select(NotePart).where(NotePart.user_id == user_id)
        results = session.exec(statement)
        his_notes = results.all()
        for _ in his_notes:
            print(_.note_title)


def add_user_and_note():
    """
    add a user and make a fake note to add to this user.
    """
    new_user = UserPart(
        user_id=random.randrange(0, 10000000, 5),
        username="_".join(fake.words(3)),
        first_name=fake.first_name().title(),
        last_name=fake.last_name().title(),
        email_id=fake.email(),
        phone_no=fake.phone_number(),
    )

    title = " ".join(fake.words(3))
    content = fake.sentence(25)
    new_user.note_count += 1

    new_note = NotePart(
        note_title=title,
        note_content=content,
        user=new_user,
    )

    with Session(engine) as session:
        session.add(new_note)
        session.commit()


def find_note_for_a_old_user():
    """
    it will take  a user id and then add a ntoe to it
    """
    user_id = 60426503
    # This is which come from telegram

    with Session(engine) as session:
        statement = select(UserPart).where(UserPart.user_id == user_id)
        results = session.exec(statement)
        user_row = results.first()
        if user_row:
            print(user_row.notes)
        else:
            print("No user found in this id")


def main():
    create_db_and_engine()
    # add_some_user()
    # add_some_note()

    # select_all_user()
    # select_all_note()
    # find_one_user()
    # search_notes_of_a_user()

    add_user_and_note()
    # add_new_note_for_a_old_user()
    find_note_for_a_old_user()


if __name__ == "__main__":

    for _ in range(0):
        print(_)
        main()

    main()

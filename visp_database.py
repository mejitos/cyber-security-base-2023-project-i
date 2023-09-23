# Script to generate small mock database for the VISP application
#
# This has nothing to do with the actual assignment of creating
# security vulnerabilities. This is just a utility to create some
# kind of actual user experience.
import json
import os
import random
import time
import uuid


DATABASE_FILENAME = 'database.json'
DATABASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(DATABASE_DIRECTORY, DATABASE_FILENAME)

USERS = [
    {
        'username': 'bob',
        'password': '$2b$12$vfhWnLkrnoQ6/FHkpArvz.ysVcUjacObJl330Liw9r2B9A60Zwf0C',
    },
    {
        'username': 'alice',
        'password': '$2b$12$9qM3gaLB1YTQyXc/k.clp.1sjOlH.JnfD6pc9E5U.6xyLP7huP79G',
    }
]

TITLES = [
    'Golden Hour Sunrise',
    'Urban Jungle',
    'Majestic Mountain Peak',
    'Seaside Serenity',
    'Desert Mirage',
    'Tropical Paradise',
    'Starry Night Sky',
    'Flower Field Bliss',
    'Breathtaking Waterfall',
    'Sunset Silhouette',
    'Northern Lights Magic',
    'Wildflower Meadow',
    'Cherry Blossom Dream',
    'Misty Forest',
    'Midnight Moon',
]

DESCRIPTIONS = [
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
    'Integer euismod lobortis lectus eu tincidunt. Proin sed lorem ipsum.',
    'Praesent eleifend convallis tellus eget maximus.',
    'Sed auctor placerat arcu, vel molestie ex ullamcorper nec.',
    'Nulla eros odio, tincidunt id lacinia id, aliquet eget justo.'
    'Nunc porttitor sit amet tellus vel ultrices. Duis mi quam, ultrices sed justo sed, hendrerit tempor metus.',
    'Donec porta posuere odio nec suscipit. Mauris at condimentum sem. Etiam ac lobortis enim.',
    'Suspendisse malesuada turpis at condimentum efficitur.',
    'Morbi nibh sem, porta vel aliquet sed, hendrerit auctor enim. Etiam id augue lorem.',
    'Etiam sed vehicula lectus, et varius dui. Aliquam vel nisl non augue maximus sagittis eu quis dui. Quisque porta justo quam.',
]


def load_database() -> dict:
    """Loads database from pre-defined JSON file

    Returns
        Dictionary containing the database.
    """
    database = None

    try:
        with open(DATABASE_PATH, 'r') as database_file:
            database = json.loads(database_file.read())
    except:
        pass

    return database


def save_database(database: dict):
    """Saves database to pre-defined JSON file

    Arguments
        database: Dictionary containing the database.
    """
    with open(DATABASE_PATH, 'w') as database_file:
        database_file.write(json.dumps(database, indent=4))


def create_database() -> dict:
    """Create database file with pseudo-random data

    Will overwrite any existing database files.

    Returns
        The generated database.
    """
    MIN_IMAGES = 3
    MAX_IMAGES = 7
    database = {'users': {}, 'images': {}}

    for user in USERS:
        user = {**user, 'id': str(uuid.uuid4())}
        database['users'][user['id']] = user

        for _ in range(random.randint(MIN_IMAGES, MAX_IMAGES)):
            title = random.choice(TITLES)
            image = {
                'id': str(uuid.uuid4()),
                'timestamp': int(time.time()),
                'title': title,
                'description': random.choice(DESCRIPTIONS),
                'filename': f'{title}.png',
                'shared': random.randint(0, 100) < 33,
                'owner': user['id'],
            }
            database['images'][image['id']] = image

    save_database(database)

    return database


if __name__ == '__main__':
    create_database()

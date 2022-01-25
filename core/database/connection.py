from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config


class DatabaseConnection:
    connection = None
    session = None

    @staticmethod
    def get_session():
        if DatabaseConnection.connection is None:
            DatabaseConnection()

            connection_string = f"postgresql://{Config.DATABASE_USER}:{Config.DATABASE_PORT}@{Config.DATABASE_HOST}:" \
                                f"{Config.DATABASE_PASSWORD}/{Config.DATABASE_NAME}"
            engine = create_engine(connection_string, echo=True, future=True)
            DatabaseConnection.session = sessionmaker(bind=engine)

        return DatabaseConnection.session

    def __init__(self):
        if DatabaseConnection.connection is not None:
            raise Exception("Error: Only one MongoConnect object can be created")
        else:
            DatabaseConnection.connection = self

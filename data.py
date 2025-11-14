import os
import mysql.connector
from mysql.connector import errorcode

# Read MySQL connection info from environment variables with sensible defaults
DB_CONFIG = {
    'user': os.environ.get('MYSQL_USER', 'root'),
    'password': os.environ.get('MYSQL_PASSWORD', ''),
    'host': os.environ.get('MYSQL_HOST', '127.0.0.1'),
    'port': int(os.environ.get('MYSQL_PORT', 3306)),
    'database': os.environ.get('MYSQL_DATABASE', 'event_management'),
    'charset': 'utf8mb4',
}


def ensure_database_and_tables():
    """Create the database (if missing) and required tables.

    This mirrors the original SQLite schema but uses MySQL-compatible DDL and
    CREATE TABLE IF NOT EXISTS so it is safe to run multiple times.
    """
    # Connect without specifying database to allow creating it if missing
    tmp_cfg = DB_CONFIG.copy()
    db_name = tmp_cfg.pop('database')

    try:
        cnx = mysql.connector.connect(**tmp_cfg)
        cursor = cnx.cursor()

        # Create database if not exists
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` DEFAULT CHARACTER SET utf8mb4")
        cnx.database = db_name

        # Create tables
        TABLES = {}
        TABLES['Venue'] = (
            "CREATE TABLE IF NOT EXISTS Venue ("
            "  VenueID INT AUTO_INCREMENT PRIMARY KEY,"
            "  VenueName VARCHAR(255) NOT NULL,"
            "  Location VARCHAR(255) NOT NULL,"
            "  Capacity INT NOT NULL"
            ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"
        )

        TABLES['Organizer'] = (
            "CREATE TABLE IF NOT EXISTS Organizer ("
            "  OrganizerID INT AUTO_INCREMENT PRIMARY KEY,"
            "  OrganizerName VARCHAR(255) NOT NULL,"
            "  ContactInfo VARCHAR(255)"
            ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"
        )

        TABLES['Event'] = (
            "CREATE TABLE IF NOT EXISTS Event ("
            "  EventID INT AUTO_INCREMENT PRIMARY KEY,"
            "  EventName VARCHAR(255) NOT NULL,"
            "  EventDate DATE NOT NULL,"
            "  EventTime TIME NOT NULL,"
            "  VenueID INT,"
            "  OrganizerID INT,"
            "  FOREIGN KEY (VenueID) REFERENCES Venue(VenueID) ON DELETE SET NULL,"
            "  FOREIGN KEY (OrganizerID) REFERENCES Organizer(OrganizerID) ON DELETE SET NULL"
            ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"
        )

        TABLES['Participant'] = (
            "CREATE TABLE IF NOT EXISTS Participant ("
            "  ParticipantID INT AUTO_INCREMENT PRIMARY KEY,"
            "  ParticipantName VARCHAR(255) NOT NULL,"
            "  Email VARCHAR(255) NOT NULL,"
            "  Phone VARCHAR(50)"
            ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"
        )

        TABLES['Registration'] = (
            "CREATE TABLE IF NOT EXISTS Registration ("
            "  RegistrationID INT AUTO_INCREMENT PRIMARY KEY,"
            "  EventID INT,"
            "  ParticipantID INT,"
            "  RegistrationDate DATE NOT NULL,"
            "  FOREIGN KEY (EventID) REFERENCES Event(EventID) ON DELETE CASCADE,"
            "  FOREIGN KEY (ParticipantID) REFERENCES Participant(ParticipantID) ON DELETE CASCADE"
            ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"
        )

        TABLES['Ticket'] = (
            "CREATE TABLE IF NOT EXISTS Ticket ("
            "  TicketID INT AUTO_INCREMENT PRIMARY KEY,"
            "  EventID INT,"
            "  ParticipantID INT,"
            "  TicketType VARCHAR(100) NOT NULL,"
            "  PurchaseDate DATE NOT NULL,"
            "  FOREIGN KEY (EventID) REFERENCES Event(EventID) ON DELETE CASCADE,"
            "  FOREIGN KEY (ParticipantID) REFERENCES Participant(ParticipantID) ON DELETE CASCADE"
            ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"
        )

        for name, ddl in TABLES.items():
            cursor.execute(ddl)

        cnx.commit()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            raise RuntimeError('Something is wrong with your MySQL user name or password')
        else:
            raise
    finally:
        try:
            cursor.close()
        except Exception:
            pass
        try:
            cnx.close()
        except Exception:
            pass


if __name__ == '__main__':
    ensure_database_and_tables()

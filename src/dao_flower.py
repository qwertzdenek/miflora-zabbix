import time
import mysql.connector

class FlowerEntry:
    def __init__(self, temperature, moisture, conductivity, light, battery, time=int(time.time())):
        self.temperature = temperature
        self.moisture = moisture
        self.conductivity = conductivity
        self.light = light
        self.battery = battery
        self.time = time

    def to_string(self):
        print(self.temperature, self.moisture, self.conductivity, self.light)

class FlowerDAO:
    def __init__(self):
        self.conn = mysql.connector.connect(user='zabbix', password='password',
                                            unix_socket='/var/run/mysqld/mysqld.sock', database='zabbix')
        self.create_schema()


    def store(self, new_entry):
        """
        Store new data entry.
        """
        c = self.conn.cursor()
        data = (new_entry.time, new_entry.temperature, new_entry.moisture,
             new_entry.conductivity, new_entry.light, new_entry.battery)
        c.execute("INSERT INTO flower_journal VALUES (%s, %s, %s, %s, %s, %s)", data)
        self.conn.commit()
        c.close()


    def load(self, count=1):
        """
        Load last count entries.
        """
        c = self.conn.cursor()
        if count == None:
            c.execute("SELECT temperature, moisture, conductivity, light, battery, time FROM flower_journal ORDER BY time DESC")
        else:
            c.execute("SELECT temperature, moisture, conductivity, light, battery, time FROM flower_journal ORDER BY time DESC LIMIT %s", [count])
        db_entries = c.fetchall()
        result = list()
        for db_entry in reversed(db_entries):
            result_entry = FlowerEntry(db_entry[0], db_entry[1], db_entry[2],
                                       db_entry[3], db_entry[4], time=db_entry[5])
            result.append(result_entry)
        c.close()
        return result


    def create_schema(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS flower_journal (
            time int NOT NULL,
            temperature int,
            moisture int,
            conductivity int,
            light int,
            battery int,
            PRIMARY KEY (time)
          )''')
        c.close()


    def close(self):
        self.conn.close()


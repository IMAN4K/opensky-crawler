# MIT License

# Copyright (c) 2022 Iman Ahmadvand

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from readline import read_init_file
import psycopg2 as psql
import os
from settings import Settings


class Database:
    def __init__(self) -> None:
        self._connection = None
        self._configuration = {
            "host": "localhost",
            "port": "5432",
            "database": "postgres",
            "user": "postgres"
        }
        self.connect()

        if self._connection:
            self.execute(os.path.join(os.path.dirname(
                os.path.abspath(__file__)), 'schema', 'S0.sql'))

    def loadSettings(self, descriptor):
        settings = Settings(descriptor, 'Database')

        configuration = settings.load()
        if len(configuration.keys()) == 0:
            settings.save(self._configuration)
        else:
            self._configuration = configuration

        self.connect()

        if self._connection:
            self.execute(os.path.join(os.path.dirname(
                os.path.abspath(__file__)), 'schema', 'S0.sql'))

    def connect(self):
        if not os.getenv('PGPASSWORD'):
            print("Please set the PGPASSWORD environment variable!")

        try:
            self._connection = psql.connect(
                host=self._configuration["host"],
                port=self._configuration["port"],
                database=self._configuration["database"],
                user=self._configuration["user"],
                password=123456
            )
        except Exception as e:
            print(e)

    def importCSV(self, path):
        try:
            cur = self._connection.cursor()
            cur.execute("""
            COPY "StateVectors"
            FROM '{0}'
            DELIMITER ','
            CSV HEADER;
            """.format(path))
            self._connection.commit()
            cur.close()
        except Exception as e:
            print(e)

    def execute(self, path):
        with open(path) as f:
            try:
                cur = self._connection.cursor()
                cur.execute(f.read())
                self._connection.commit()
                cur.close()
            except Exception as e:
                print(e)

    def start(self):
        if self._connection:
            self.execute(os.path.join(os.path.dirname(
                os.path.abspath(__file__)), 'schema', 'S1.sql'))

from pathlib import Path
from py_dpz_database_tools import pydpzsqlalchemytools
import unittest
import json

project_path = Path(__file__).parents[1]
json_path = project_path.joinpath('config.json')

with open(json_path, 'r') as f:
    config = json.load(f)

table_names = config['APP']['TEST_TABLES']
source_user_name = config['TEST_SOURCE_DATABASE']['USERNAME']
source_password = config['TEST_SOURCE_DATABASE']['PASSWORD']
source_schema_name = config['TEST_SOURCE_DATABASE']['SCHEMA']
source_server_name = config['TEST_SOURCE_DATABASE']['HOST']
source_database_name = config['TEST_SOURCE_DATABASE']['DB']
target_user_name = config['TEST_TARGET_DATABASE']['USERNAME']
target_password = config['TEST_TARGET_DATABASE']['PASSWORD']
target_schema_name = config['TEST_TARGET_DATABASE']['SCHEMA']
target_server_name = config['TEST_TARGET_DATABASE']['HOST']
target_database_name = config['TEST_TARGET_DATABASE']['DB']

sql_source_database = pydpzsqlalchemytools.PyDpzSqlAlchemyTools(
    schema_name=source_schema_name,
    server_name=source_server_name,
    database_name=source_database_name,
    user_name=source_user_name,
    user_password=source_password,
)

sql_target_database = pydpzsqlalchemytools.PyDpzSqlAlchemyTools(
    schema_name=target_schema_name,
    server_name=target_server_name,
    database_name=target_database_name,
    user_name=target_user_name,
    user_password=target_password,
)


class TestDatabaseUtils(unittest.TestCase):

    def test_simple_select_of_current_user(self):
        sql_source_database.windows_logon()
        sql_source_database.set_server_name("MIHQCORPDDB01\MIHQCOPRDDB01")
        sql_source_database.connect_to_server()
        expected = [('US\\svc_performancee_t',)]
        actual = sql_source_database.select_data("SELECT CURRENT_USER")
        sql_source_database.windows_logoff()

        sql_source_database.set_server_name("localhost")
        server_name = sql_source_database.get_server_name()
        self.assertEqual(server_name, "localhost")
        self.assertEqual(expected, actual)

    def test_select_of_source_database(self):
        sql_source_database.windows_logon()
        sql_source_database.connect_to_server()
        expected = [(1,)]
        actual = sql_source_database.select_data("SELECT 1")
        sql_source_database.windows_logoff()
        self.assertEqual(expected, actual)

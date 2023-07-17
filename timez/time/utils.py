# utils for tzr.py ($TimeZoneReminder)


import datetime
# import logging
import os
import pytz
import re
import shutil
import sqlite3
import time
from dateutil.tz import tzoffset, tzlocal, tz
from pprint import pprint


# logging.basicConfig(filename='tzr.log', level=logging.DEBUG, filemode='a',
#                     format='%(levelname)s - %(message)s')


class InfoBase:
    def __init__(self):
        self.n = 0

    def __repr__(self):
        return f'tzrContactBook.db/contact table contains {len(InfoBase.select_all())} entries'

    def __str__(self):
        return f'You have {len(InfoBase.select_all())} entries saved in your Contact base'

    @staticmethod
    def create_table():
        with sqlite3.connect('tzrContactBook.db') as conn:
            cursor = conn.cursor()

            cursor.execute("""CREATE TABLE if not exists contact (contact_name VARCHAR(255) PRIMARY KEY,
                                                                  platform VARCHAR(255), 
                                                                  comment VARCHAR(255), 
                                                                  location VARCHAR(255),
                                                                  zone_name VARCHAR(255), 
                                                                  utc_offset FLOAT)""")
            conn.commit()

    @staticmethod
    def transfer_to_sql(contact_name, platform, comment, location, zone_name, utc_offset):
        with sqlite3.connect('tzrContactBook.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO contact(contact_name, platform, comment, location, zone_name, utc_offset)"
                " VALUES (?, ?, ?, ?, ?, ?)", (contact_name, platform, comment, location, zone_name, utc_offset))
            conn.commit()

    @staticmethod
    def select_column(column_name):
        with sqlite3.connect('tzrContactBook.db') as conn:
            cursor = conn.cursor()
            cursor.execute('select %s from contact' % column_name)
            data_ = cursor.fetchall()
            conn.commit()
            return [x[0] for x in data_]

    @staticmethod
    def select_row(column: str, key_word) -> []:
        """Filter contact table by 1 field: contact_name/platform/time_zone or utc_offset
        Return selected rows as [(), (), ..]"""
        # Never do this - insecure! using Python's string operations to assemble queries is not safe
        # , as they are vulnerable to SQL injection attacks
        with sqlite3.connect('tzrContactBook.db') as conn:
            cursor = conn.cursor()
            if column == 'utc_offset':
                cursor.execute('SELECT * FROM contact WHERE %s = "%f"' % (column, key_word))  # because float
            else:
                cursor.execute('SELECT * FROM contact WHERE %s = "%s"' % (column, key_word))
            data_ = cursor.fetchall()
            conn.commit()
            return data_

    @staticmethod
    def delete_row(key):
        try:
            conn = sqlite3.connect('tzrContactBook.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM contact WHERE contact_name = "%s"' % key)
            conn.commit()
            conn.close()
        except sqlite3.Error as error:
            print("Failed to delete record from contact table", error)

        finally:
            if conn:
                conn.close()

    @staticmethod
    def select_all():
        with sqlite3.connect('tzrContactBook.db') as conn:
            cursor = conn.cursor()
            cursor.execute('select * from contact')
            data_ = cursor.fetchall()
            conn.commit()
        return data_

    @staticmethod
    def print_contact_table():
        """Available by entering secret command 000 in the main menu of TimeZoneReminder"""
        print('table: contact / tzrContactBook.db: ')
        headers = ('contact_name', 'platform', 'comment', 'location', 'zone_name', 'utc_offset')
        print('{0:15} | {1:10} | {2:50} | {3:8}  | {4:11}  | {5:9} '.format(headers[0],
              headers[1], headers[2], headers[3], headers[4], headers[5]))
        print('_' * 130)
        content = InfoBase.select_all()
        for entry in sorted(content):
            # print(*entry, sep=' | ')
            print('{0:15} | {1:10} | {2:50} | {3:8}  | {4:11}  | {5:9} '.format(entry[0],
                  entry[1], entry[2], entry[3], str(entry[4]), str(entry[5])))
            print()
        print(f'Number of entries: {len(content)}')

    @staticmethod
    def specify_destination():
        """Supporting method for def export_contact_book()"""
        path = input("Specify path to location for saving Contacts' Book:> ")
        folder = input('Enter name for folder(if necessary to create):> ')
        windows = input('Is Windows - your OS ? y/n:> ')
        if windows == 'y':
            full_path = os.path.join(path, folder).strip() + '\\'
        else:
            full_path = os.path.join(path, folder).strip() + '/'
        if not os.access(full_path, os.F_OK):
            try:
                os.mkdir(full_path)
            except OSError:
                print(f'Cannot create {full_path} so let`s use {os.getcwd()}.')
                return os.getcwd()
        return full_path

    @staticmethod
    def create_csv_from_sql():
        """Write .csv-file with data from tzrContactBook.db inside working directory;
        Supporting method for def export_contact_book()"""
        data = InfoBase.select_all()
        file_name = 'tzr_contacts.csv'
        with open(file_name, 'w', encoding='utf-8') as out_file:
            out_file.write("Time Zone Reminder / Contacts' Book\n")
            out_file.write('contact_name,platform,comment,location,zone_name,utc_offset\n')
            for row in sorted(data):
                out_file.write(';'.join(list(map(str, row))) + '\n')
        return file_name

    @staticmethod
    def export_contact_book():
        """Get path for saving exported data and copy original .csv-file there;
        Check if export file exists in designated location; Remove original .csv-file"""
        file_name = InfoBase.create_csv_from_sql()
        dst_folder = InfoBase.specify_destination()
        try:
            shutil.copy(file_name, dst_folder)
            if 'tzr_contacts.csv' in os.listdir(dst_folder):
                print(f'{file_name} is successfully saved to {dst_folder}.')
                os.remove(file_name)
        except Exception as e:
            # logging.debug(e)
            print(f'Cannot save file to {dst_folder} so {file_name} is successfully saved to {os.getcwd()}')


def timer(func):
    def wrapper(func_argument):
        start = time.time()
        func(func_argument)
        end = time.time()
        # logging.info('def convert_time() ran ' + str(end - start) + ' seconds')
    return wrapper


class TimeKeeper:
    def __init__(self):
        self.command = ''
        self.call = 0

    tz_olson = {'UTC': 'Etc/UTC',
                'ART': 'America/Argentina/Buenos_Aires',
                'CST': 'US/Central',
                'EST': 'US/Eastern',
                'IST': 'Asia/Kolkata',
                'JST': 'Asia/Tokyo',
                'MSK': 'Europe/Moscow',
                'PST': 'US/Pacific',
                'TURKEY': 'Europe/Istanbul'
                }

    def __repr__(self):
        return 'TZR app recognizes following short names for time zones:'

    def __str__(self):
        return TimeKeeper.tz_olson

    @staticmethod
    def calculate_time(time_obj, time_interval: list) -> str:
        """ how much time will it be in ..2 hours?
        """
        # logging.info(f'***def calculate_time({time.strftime("%H:%M", time_obj)}, {time_interval})')
        time0 = list(map(int, time.strftime("%H:%M", time_obj).split(':')))
        hours, minutes = time0[0], time0[1]
        hours2, minutes2 = hours + time_interval[0], minutes + time_interval[1]
        time2 = datetime.timedelta(hours=hours2, minutes=minutes2)
        # logging.debug(str(time2)[:5])
        return str(time2)[:5]

    @staticmethod
    def get_current_time(tz_data) -> str:
        """convert current local time into another time zone"""
        # logging.info('***def get_current_time(tz_data)')
        # logging.debug(f'tz_data={tz_data}')
        try:
            offset = datetime.timedelta(hours=float(tz_data))
            tz_ = datetime.timezone(offset)
            return datetime.datetime.now(tz_).strftime('%d-%m-%Y %H:%M')
        except ValueError:
            try:
                tz_ = pytz.timezone(TimeKeeper.tz_olson[tz_data.upper()])
                return datetime.datetime.now(tz_).strftime('%d-%m-%Y %H:%M')
            except KeyError:
                print(f'there are no {tz_data.upper()} time zone in my database. Try again with offset')

    @staticmethod
    def date_constructor(zone_info, date: list, time0: list):
        """Return time zone-aware object"""
        # logging.info(f'***def date_constructor({zone_info}, {date}, {time0})')
        if isinstance(zone_info, float):
            # time from local time zone
            return datetime.datetime(date[0], date[1], date[2], time0[0], time0[1], 0,
                                     tzinfo=tzoffset(None, int(zone_info * 3600)))
        try:
            # if user provided offset
            return datetime.datetime(date[0], date[1], date[2], time0[0], time0[1], 0,
                                     tzinfo=tzoffset(None, int(float(zone_info) * 3600)))  # in seconds
        except ValueError:
            try:
                # if user entered valid zone name
                tz_from_pytz = pytz.timezone(TimeKeeper.tz_olson[zone_info.upper()])
                return tz_from_pytz.localize(datetime.datetime(date[0], date[1], date[2], time0[0], time0[1]))
            except KeyError:
                print(f'there are no {zone_info} time zone in my database. Try again with offset to UTC')

    @staticmethod
    def define_tzfrom_tzto_time(from_local=''):
        """Supporting method for def convert_time()
        Return tz_from: float  or str,
        tz_to: float or str or <class dateutil.tz.tzlocal>,
        _time: str"""
        tz_from, tz_to = None, None
        if not from_local:
            from_local = input('convert local time? y/n ')
        if from_local.lower() == 'y':
            tz_from = float(datetime.datetime.now().astimezone().strftime('%z')) / 100  # get local offset
            tz_to = input('Enter the destination time zone: name or offset to UTC/GMT:> ')
        elif from_local.lower() != 'n':
            print('Wrong command!')
            TimeKeeper.define_tzfrom_tzto_time()
        else:
            tz_from = input('Enter the original time zone: name or offset to UTC/GMT:> ')
            tz_to = tz.tzlocal()  # get local tz from PC
        _time = input('Enter time in format 00:00:> ')
        return tz_from, tz_to, _time

    @timer
    def convert_time(self):
        """Convert time and print result"""
        # logging.info('***def convert_time')
        self.call += 1
        time_params = TimeKeeper.define_tzfrom_tzto_time()
        tz_from, tz_to, time_ = time_params[0], time_params[1], time_params[2]
        # logging.debug(f'tz_from={tz_from}, tz_to={tz_to}, time_={time_}')
        time0 = list(map(int, time_.split(':')))
        # logging.debug(f'time0: {time0}')
        try:
            message = 'IncorrectInput: hour must be in 0..23 and minute must be in 0..59'
            assert (0 <= time0[0] <= 23 and 0 <= time0[1] <= 59), message

            date = list(map(int, datetime.datetime.now().strftime('%Y-%m-%d').split('-')))  # [2022, 6, 29]
            # logging.debug(date)
            dt = TimeKeeper.date_constructor(tz_from, date, time0)
            # logging.debug(f'datetime aware constructed: {dt}')
            if not dt:
                return False
            dt_utc = dt.astimezone(pytz.utc)
            # logging.debug(f' UTC {dt_utc}')
            if isinstance(tz_from, float):  # i.d. from local time
                try:  # if user provided offset
                    hours = int(str(float(tz_to)).split('.')[0])
                    minutes = int(str(float(tz_to)).split('.')[1])
                    offset_ = datetime.timedelta(hours=hours, minutes=minutes)
                    tz_from_offset = datetime.timezone(offset_, name='UNKNOWN')
                    dt_converted = dt_utc.astimezone(tz=tz_from_offset)
                except ValueError:  # if user entered valid zone name
                    if tz_to.upper() in list(TimeKeeper.tz_olson.keys()):
                        tz_pytz = pytz.timezone(TimeKeeper.tz_olson[tz_to.upper()])
                        dt_converted = dt_utc.astimezone(tz_pytz)
                    else:
                        print(f'there are no {tz_to.upper()} time zone in my database. Try again with offset to UTC')
                        return False
                print(f" [{dt.strftime('%H:%M %d-%m-%Y')}] your local time = "
                      f"[{dt_converted.strftime('%H:%M %d-%m-%Y')}] {tz_to} time zone.")
            else:  # to local
                dt_converted = dt_utc.astimezone(tz_to)
                print(f"[{dt.strftime('%H:%M %d-%m-%Y')}] {tz_from} time zone = "
                      f"[{dt_converted.strftime('%H:%M %d-%m-%Y')}] your local time.")
        except AssertionError as error:
            print(error)
            TimeKeeper.convert_time(self)

    @staticmethod
    def tz_from_input(time_zone: str):
        if time_zone.isalpha():
            zone_name = time_zone.upper()
            utc_offset = None
        elif re.match('[-+]?[0-9.]', time_zone):
            zone_name = None
            utc_offset = float(time_zone)
        else:
            return None, None
        return zone_name, utc_offset

    @staticmethod
    def time_operation_0(time_period: list) -> str:
        """0-display the time that will come after a certain time period"""
        current_local_time = time.localtime()
        print(f"In {time_period[0]} hours {time_period[1]} minutes it'll be:")
        return TimeKeeper.calculate_time(current_local_time, time_period)

    @staticmethod
    def calculate_tzfrom_tzto_time(time_data: list, from_local=''):
        """Return tz_from: float  or str,
        tz_to: float or str or <class dateutil.tz.tzlocal>,
        _time: str"""
        if from_local.lower() == 'y':
            tz_from = float(datetime.datetime.now().astimezone().strftime('%z')) / 100  # get local offset
            tz_to = time_data[0]
        else:
            tz_from = time_data[0]
            tz_to = tz.tzlocal()  # get local tz from PC
        return tz_from, tz_to, time_data[1]

    @staticmethod
    def time_operation_2(time_data: list, from_local):  # ([tz, time] , 'y')
        time_params = TimeKeeper.calculate_tzfrom_tzto_time(time_data, from_local=from_local)
        tz_from, tz_to, time_ = time_params[0], time_params[1], time_params[2]
        time0 = list(map(int, time_.split(':')))
        date = list(map(int, datetime.datetime.now().strftime('%Y-%m-%d').split('-')))  # [2022, 6, 29]
        dt = TimeKeeper.date_constructor(tz_from, date, time0)
        if not dt:
            return False
        dt_utc = dt.astimezone(pytz.utc)
        if isinstance(tz_from, float):  # i.d. from local time
            try:  # if user provided offset
                hours = int(str(float(tz_to)).split('.')[0])
                minutes = int(str(float(tz_to)).split('.')[1])
                offset_ = datetime.timedelta(hours=hours, minutes=minutes)
                tz_from_offset = datetime.timezone(offset_, name='UNKNOWN')
                dt_converted = dt_utc.astimezone(tz=tz_from_offset)
            except ValueError:  # if user entered valid zone name
                if tz_to.upper() in list(TimeKeeper.tz_olson.keys()):
                    tz_pytz = pytz.timezone(TimeKeeper.tz_olson[tz_to.upper()])
                    dt_converted = dt_utc.astimezone(tz_pytz)
                else:
                    print(f'there are no {tz_to.upper()} time zone in my database. Try again with offset to UTC')
                    return False
            return f" [{dt.strftime('%H:%M %d-%m-%Y')}] your local time = " \
                   f"[{dt_converted.strftime('%H:%M %d-%m-%Y')}] {tz_to} time zone."
        else:  # to local
            dt_converted = dt_utc.astimezone(tz_to)
            return f"[{dt.strftime('%H:%M %d-%m-%Y')}] {tz_from} time zone = " \
                   f"[{dt_converted.strftime('%H:%M %d-%m-%Y')}] your local time."

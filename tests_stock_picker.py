# -*- coding: utf-8 -*-
"""
Created on 11th May, 2019

@author: Shalini Jha
"""

import pytest
import stock_picker
import datetime
import csv
import math

VALID_CSV_PATH = "tests_data_stock_picker.csv"
INVALID_CSV_PATH = "invalid_csv.csv"

test_case = {'ABB': {datetime.datetime(2019, 1, 1, 0, 0): 1319.2,
                     datetime.datetime(2019, 1, 2, 0, 0): 1319.25,
                     datetime.datetime(2019, 1, 3, 0, 0): 1308.95,
                     datetime.datetime(2019, 1, 4, 0, 0): 1303.65,
                     datetime.datetime(2019, 1, 7, 0, 0): 1301.8,
                     datetime.datetime(2019, 1, 8, 0, 0): 1299.4},
             'ACC': {datetime.datetime(2019, 1, 1, 0, 0): 1488.8,
                     datetime.datetime(2019, 1, 2, 0, 0): 1483.95,
                     datetime.datetime(2019, 1, 3, 0, 0): 1452.25,
                     datetime.datetime(2019, 1, 4, 0, 0): 1469.1,
                     datetime.datetime(2019, 1, 7, 0, 0): 1477.95},
             'INFY': {datetime.datetime(2019, 1, 1, 0, 0): 665.05,
                      datetime.datetime(2019, 1, 2, 0, 0): 669.05,
                      datetime.datetime(2019, 1, 3, 0, 0): 669.15,
                      datetime.datetime(2019, 1, 4, 0, 0): 661.05,
                      datetime.datetime(2019, 1, 7, 0, 0): 671.7},
             'MRF': {datetime.datetime(2019, 1, 1, 0, 0): 66801,
                     datetime.datetime(2019, 1, 2, 0, 0): 66700,
                     datetime.datetime(2019, 1, 3, 0, 0): 67000,
                     datetime.datetime(2019, 1, 4, 0, 0): 66560,
                     datetime.datetime(2019, 1, 7, 0, 0): 67000},
             'TCS': {datetime.datetime(2019, 1, 1, 0, 0): 1902.8,
                     datetime.datetime(2019, 1, 2, 0, 0): 1923.3,
                     datetime.datetime(2019, 1, 3, 0, 0): 1899.95,
                     datetime.datetime(2019, 1, 4, 0, 0): 1876.85,
                     datetime.datetime(2019, 1, 7, 0, 0): 1897.9}}

test_case1 = {'ABB': {
    datetime.datetime(2019, 1, 7, 0, 0): 131.8,
    datetime.datetime(2019, 1, 8, 0, 0): 129.4},
    'ACC': {datetime.datetime(2019, 1, 2, 0, 0): 1483.95,
            datetime.datetime(2019, 1, 3, 0, 0): 1452.25},
    'INFY': {datetime.datetime(2019, 1, 1, 0, 0): 665.05,
             datetime.datetime(2019, 1, 2, 0, 0): 669.05,
             datetime.datetime(2019, 1, 3, 0, 0): 669.15,
             datetime.datetime(2019, 1, 4, 0, 0): 661.05},
    'MRF': {datetime.datetime(2019, 1, 2, 0, 0): 66700,
            datetime.datetime(2019, 1, 3, 0, 0): 67000,
            datetime.datetime(2019, 1, 4, 0, 0): 66560},
    'TCS': {datetime.datetime(2019, 1, 1, 0, 0): 902.8,
            datetime.datetime(2019, 1, 2, 0, 0): 123.3,
            datetime.datetime(2019, 1, 4, 0, 0): 176.85,
            }}

result_dictionary = {'%%%': {datetime.datetime(2019, 1, 1, 0, 0): 1488.8},
                     '****': {datetime.datetime(2019, 1, 7, 0, 0): 197.9},
                     'ABB': {datetime.datetime(2019, 1, 7, 0, 0): 131.8,
                             datetime.datetime(2019, 1, 8, 0, 0): 129.4},
                     'ACC': {datetime.datetime(2019, 1, 2, 0, 0): 1483.95,
                             datetime.datetime(2019, 1, 3, 0, 0): 1452.25},
                     'INFY': {datetime.datetime(2019, 1, 1, 0, 0): 665.05,
                              datetime.datetime(2019, 1, 2, 0, 0): 669.05,
                              datetime.datetime(2019, 1, 3, 0, 0): 669.15,
                              datetime.datetime(2019, 1, 4, 0, 0): 661.05},
                     'MRF': {datetime.datetime(2019, 1, 2, 0, 0): 66700.0,
                             datetime.datetime(2019, 1, 3, 0, 0): 67000.0,
                             datetime.datetime(2019, 1, 4, 0, 0): 66560.0,
                             datetime.datetime(2019, 1, 7, 0, 0): 67000.0},
                     'TCS': {datetime.datetime(2019, 1, 1, 0, 0): 902.8,
                             datetime.datetime(2019, 1, 2, 0, 0): 123.3,
                             datetime.datetime(2019, 1, 4, 0, 0): 176.85},
                     '^^^^': {datetime.datetime(2019, 1, 4, 0, 0): 1469.1}}

list_of_words = ['ABB', 'ABBB', 'ACC', 'ACCE', 'TCS', 'SCCT', 'INFY', 'YFNI', 'MRF', 'RMF']

empty_list = []

no_symbol_in_list = ['POIK', 'JHDBM', 'LKIUY', 'KKJDLD', 'ASDF']

word = 'ABB'

result = {'AAB', 'AABB', 'AB', 'ABA', 'ABAB', 'ABB', 'ABBA', 'ABBB', 'ABBC', 'ABBD', 'ABBE', 'ABBF', 'ABBG', 'ABBH',
          'ABBI', 'ABBJ', 'ABBK', 'ABBL', 'ABBM', 'ABBN', 'ABBO', 'ABBP', 'ABBQ', 'ABBR', 'ABBS', 'ABBT', 'ABBU',
          'ABBV', 'ABBW', 'ABBX', 'ABBY', 'ABBZ', 'ABC', 'ABCB', 'ABD', 'ABDB', 'ABE', 'ABEB', 'ABF', 'ABFB',
          'ABG', 'ABGB', 'ABH', 'ABHB', 'ABI', 'ABIB', 'ABJ', 'ABJB', 'ABK', 'ABKB', 'ABL', 'ABLB', 'ABM', 'ABMB'
    , 'ABN', 'ABNB', 'ABO', 'ABOB', 'ABP', 'ABPB', 'ABQ', 'ABQB', 'ABR', 'ABRB', 'ABS', 'ABSB', 'ABT', 'ABTB',
          'ABU', 'ABUB', 'ABV', 'ABVB', 'ABW', 'ABWB', 'ABX', 'ABXB', 'ABY', 'ABYB', 'ABZ', 'ABZB', 'ACB', 'ACBB',
          'ADB', 'ADBB', 'AEB', 'AEBB', 'AFB', 'AFBB', 'AGB', 'AGBB', 'AHB', 'AHBB', 'AIB', 'AIBB', 'AJB', 'AJBB',
          'AKB', 'AKBB', 'ALB', 'ALBB', 'AMB', 'AMBB', 'ANB', 'ANBB', 'AOB', 'AOBB', 'APB', 'APBB', 'AQB', 'AQBB',
          'ARB', 'ARBB', 'ASB', 'ASBB', 'ATB', 'ATBB', 'AUB', 'AUBB', 'AVB', 'AVBB', 'AWB', 'AWBB', 'AXB', 'AXBB',
          'AYB', 'AYBB', 'AZB', 'AZBB', 'BAB', 'BABB', 'BB', 'BBB', 'CABB', 'CBB', 'DABB', 'DBB', 'EABB', 'EBB',
          'FABB', 'FBB', 'GABB', 'GBB', 'HABB', 'HBB', 'IABB', 'IBB', 'JABB', 'JBB', 'KABB', 'KBB', 'LABB',
          'LBB', 'MABB', 'MBB', 'NABB', 'NBB', 'OABB', 'OBB', 'PABB', 'PBB', 'QABB', 'QBB', 'RABB', 'RBB', 'SABB',
          'SBB', 'TABB', 'TBB', 'UABB', 'UBB', 'VABB', 'VBB', 'WABB', 'WBB', 'XABB', 'XBB', 'YABB', 'YBB', 'ZABB',
          'ZBB'}

result1 = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
           'W', 'X', 'Y', 'Z'}

start_date = datetime.datetime(2019, 1, 1, 0, 0)

end_date = datetime.datetime(2019, 1, 3, 0, 0)

symbol = 'TCS'

result_dates = [datetime.datetime(2019, 1, 1, 0, 0),
                datetime.datetime(2019, 1, 2, 0, 0),
                datetime.datetime(2019, 1, 3, 0, 0)]

Correct_list = ['ABB', 'ACC', 'TCS', 'MRF']


class TestGetData():
    def test_with_valid_file_path(self):
        assert stock_picker.get_data(VALID_CSV_PATH) == test_case

    def test_with_none_path(self):
        with pytest.raises(TypeError):
            stock_picker.get_data(None)

    def test_with_invalid_csv_path(self):
        with pytest.raises(OSError):
            stock_picker.get_data("")

    def test_with_missing_values_in_csv_file(self):
        assert stock_picker.get_data(INVALID_CSV_PATH) == result_dictionary


class TestKnown():
    def test_with_list_of_words(self):
        assert stock_picker.known(test_case, list_of_words) == {'ABB', 'ACC', 'MRF', 'TCS', 'INFY'}

    def test_with_empty_list(self):
        assert stock_picker.known(test_case, empty_list) == set()

    def test_with_no_symbol_in_list(self):
        assert stock_picker.known(test_case, no_symbol_in_list) == set()


class TestEdits1():
    def test_with_words(self):
        assert stock_picker.edits1(word) == result

    def test_with_empty_string(self):
        assert stock_picker.edits1('') == result1


class TestCorrection():
    def test_with_correct_symbol(self):
        assert stock_picker.correction('ABB', test_case) == {'ABB'}

    def test_with_two_corrections_symbol(self):
        assert stock_picker.correction('ABC', test_case) == {'ABB', 'ACC'}

    def test_with_one_posible_correction_symbol(self):
        assert stock_picker.correction('ACCC', test_case) == {'ACC'}

    def test_with_incorrect_symbol(self):
        assert stock_picker.correction('#$5^', test_case) == set()


class TestWalkDays():
    def test_with_start_date_and_end_date(self):
        assert list(stock_picker.walk_days(start_date, end_date)) == result_dates

    def test_with_start_date_is_greater_than_end_date(self):
        assert list(stock_picker.walk_days(end_date, start_date)) == []


class TestBuyandSell():
    def test_with_dates_in_dataset(self):
        result = stock_picker.buy_and_sell(test_case, symbol, start_date, end_date)
        assert math.isclose(result[0], 1908.6833333333334)
        assert math.isclose(result[1], 12.738360700393617)
        assert result[2] == '03-Jan-2019'
        assert result[3] == '02-Jan-2019'
        assert math.isclose(result[4], 2334.999999999991)

    def test_with_when_startdate_is_greater_than_enddate(self):
        assert stock_picker.buy_and_sell(test_case, symbol, end_date, start_date) is None

    def test_with_when_startdate_is_not_in_dataset(self):
        result = stock_picker.buy_and_sell(test_case, symbol, datetime.datetime(2019, 1, 5, 0, 0),
                                           datetime.datetime(2019, 1, 7, 0, 0))
        assert math.isclose(result[0], 1883.8666666666668)
        assert math.isclose(result[1], 12.15322316644172)
        assert result[2] == '05-Jan-2019'
        assert result[3] == '07-Jan-2019'
        assert math.isclose(result[4], 2105.000000000018)

    def test_with_when_startdate_is_before_earliest_date(self):
        result = stock_picker.buy_and_sell(test_case, symbol, datetime.datetime(2018, 12, 30, 0, 0),
                                           datetime.datetime(2019, 1, 7, 0, 0))
        assert math.isclose(result[0], 1893.5)
        assert math.isclose(result[1], 17.64067270070318)
        assert result[2] == '04-Jan-2019'
        assert result[3] == '02-Jan-2019'
        assert math.isclose(result[4], 4645.000000000005)

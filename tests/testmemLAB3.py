# tests/test_memory.py
import unittest
from src1.db1.backend1.memoryLAB3 import FlatTable
from src1.db1.backend1.errorsLAB3 import InvalidRoomsAmountError,InvalidHouseNumberError,InvalidSquareError,InvalidCostError,DuplicateIDError 


class TestMemory(unittest.TestCase):
    def setUp(self):
        self.flat_table=FlatTable()
        self.assertIsInstance(self.flat_table,FlatTable)
        
    def test_create_record(self):
        cases=[
            (1,2,"Marble Avenue",60,48,10.5),
            (2,4,"Greenbloom Street",22,87,48.3),
            (3,1,"Campbell Street",5,31,8.6),
            (4,1,"Rollway Lane",8,26,7.1),
            (5,3,"Orange Cross",29,70,26.5),
            (6,2,"Tompson Street",88,54,14.9),
            (7,2,"Royal Cross",40,45.6,17.7),
            (8,2,"Limestone Avenue",117,38.3,13.2),
            (9,4,"Waldorf Lane",1,100.6,66.2),
            (10,2,"St Mary Road",5,40,12.2),
            (11,3,"Lovelace Lane",2,61,43.5),
            (12,2,"Redoak Road",19,50,28),
            (13,3,"Westwick Street",52,69,42),
            (14,5,"Pacific Avenue",220,122,92.6),
            (15,2,"Windblow Street",132,53,20),
            (16,1,"Medowbrook Highway",44,23,4.7)
            ]
        for test_data in cases:
            with self.subTest(test_data=test_data):
                record = self.flat_table.create_record(*test_data)
                self.assertEqual(record, test_data)


    def test_create_record_rooms_amount_below1(self):
        cases = [
            (1,-2,"Marble Avenue",60,48,10.5),
            (2,0,"Greenbloom Street",22,87,48.3),
            (3,-444,"Campbell Street",5,31,8.6),
            (4,-1,"Rollway Lane",8,26,7.1)
        ]
        error_message = "Поле кол-ва комнат не может содержать значение менее 1"
        for test_data in cases:
            with self.subTest(test_data=test_data):
                with self.assertRaises(InvalidRoomsAmountError) as context:
                    self.flat_table.create_record(*test_data)

        self.assertEqual(str(context.exception), error_message)
    def test_create_record_house_number_below1(self):
        cases=[
            (1,2,"Marble Avenue",-60,48,10.5),
            (2,4,"Greenbloom Street",-22,87,48.3),
            (3,1,"Campbell Street",0,31,8.6),
            (4,1,"Rollway Lane",-8,26,7.1),
        ]
        error_message = "Поле номера дома не может содержать значение менее 1"
        for test_data in cases:
            with self.subTest(test_data=test_data):
                with self.assertRaises(InvalidHouseNumberError) as context:
                    self.flat_table.create_record(*test_data)
        self.assertEqual(str(context.exception), error_message)

    def test_create_record_negative_square(self):
        cases=[
            (1,2,"Marble Avenue",60,-48,10.5),
            (2,4,"Greenbloom Street",22,-87,48.3),
            (3,1,"Campbell Street",5,-31,8.6),
            (4,1,"Rollway Lane",8,-26,7.1)
        ]
        error_message = "Поле площади квартиры не может содержать значение менее 0"
        for test_data in cases:
            with self.subTest(test_data=test_data):
                with self.assertRaises(InvalidSquareError) as context:
                    self.flat_table.create_record(*test_data)

        self.assertEqual(str(context.exception), error_message)

    def test_create_record_negative_cost(self):
        cases=[
            (1,2,"Marble Avenue",60,48,-10.5),
            (2,4,"Greenbloom Street",22,87,-48.3),
            (3,1,"Campbell Street",5,31,-8.6),
            (4,1,"Rollway Lane",8,26,-7.1)
        ]
        error_message = "Поле стоимости квартиры не может содержать значение менее 0"
        for test_data in cases:
            with self.subTest(test_data=test_data):
                with self.assertRaises(InvalidCostError) as context:
                    self.flat_table.create_record(*test_data)

        self.assertEqual(str(context.exception), error_message)



    def test_create_record_duplicate_id(self):
        test_data_1 = (1,2,"Marble Avenue",60,48,10.5)
        test_data_2 = (1,4,"Greenbloom Street",22,87,48.3)
        error_message = "Запись с ID 1 уже существует"
        self.flat_table.create_record(*test_data_1)

        with self.assertRaises(DuplicateIDError) as context: # AssertionError: DuplicateIDError not raised
            self.flat_table.create_record(*test_data_2)

        self.assertEqual(str(context.exception), error_message)    

    def test_select_record(self):
        # Подготовка тестовых данных для проверки функции select_record.
        test_datas = [
            (1,2,"Marble Avenue",60,48,10.5),
            (2,4,"Greenbloom Street",22,87,48.3),
            (3,1,"Campbell Street",5,31,8.6),
            (4,1,"Rollway Lane",8,26,7.1),
            (5,3,"Orange Cross",29,70,26.5),
            (6,2,"Tompson Street",88,54,14.9),
            (7,2,"Royal Cross",40,45.6,17.7),
            (8,2,"Limestone Avenue",117,38.3,13.2),
            (9,4,"Waldorf Lane",1,100.6,66.2),
            (10,2,"St Mary Road",5,40,12.2),
            (11,3,"Lovelace Lane",2,61,43.5),
            (12,2,"Redoak Road",19,50,28),
            (13,3,"Westwick Street",52,69,42),
            (14,5,"Pacific Avenue",220,122,92.6),
            (15,2,"Windblow Street",132,53,20),
            (16,1,"Medowbrook Highway",44,23,4.7)

        ]

        for test_data in test_datas:
            self.flat_table.create_record(*test_data)
        cases = [
            {
                "name": "Выбор без фильтров",
                "filters": {},
                "expected": test_datas,
            },
            {
                "name": "Фильтр по ID",
                "filters": {"flat_id": 1},
                "expected": [test_datas[0]],
            },
            {
                "name": "Фильтр по кол-ву комнат",
                "filters": {"rooms_amount": 3},
                "expected": [test_datas[4],test_datas[10],test_datas[12]],
            },
            {
                "name": "Фильтр по улице",
                "filters": {"street": "St Mary Road"},
                "expected": [test_datas[9]],
            },
            {
                "name": "Фильтр по номеру дома",
                "filters": {"house_number": 19},
                "expected": [test_datas[11]],
            },
            {
                "name": "Фильтр по площади",
                "filters": {"square": 122},
                "expected": [test_datas[13]],
            },
            {
                "name": "Фильтр по стоимости",
                "filters": {"cost": 13.2},
                "expected": [test_datas[7]],
            },
        ]
        for case in cases:
            with self.subTest(
                case=case["name"], filters=case["filters"], expected=case["expected"]
            ):
                records = self.flat_table.select_record(**case["filters"])
                self.assertEqual(records, case["expected"])


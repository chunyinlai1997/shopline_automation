import unittest
from selenium import webdriver
from unittest.mock import Mock
import preorder

class TestPreorderMethods(unittest.TestCase):

    def test_period_type_handler(self):
        preorder_instance = preorder.Preorder()
        period_type = "A"
        result = preorder_instance.period_type_handler(period_type)
        self.assertEqual(result, ("此商品為預購商品，大約3-5工作天到貨（尚有庫存不代表有現貨）", "Pre-order product. Start shipping in 3-5 working days (NOT IN STOCK)"))

    def test_xls_to_list(self):
        preorder_instance = preorder.Preorder()
        mock_workbook = Mock()
        mock_worksheet = Mock()
        mock_workbook.sheet_by_index.return_value = mock_worksheet
        mock_worksheet.nrows = 3
        mock_worksheet.ncols = 2
        mock_worksheet.cell_value.side_effect = [
            "value_0_0", "value_0_1",
            "value_1_0", "value_1_1",
            "value_2_0", "value_2_1"
        ]
        with unittest.mock.patch("xlrd.open_workbook", return_value=mock_workbook):
            result = preorder_instance.xls_to_list("dummy_path")
        expected_result = [
            ["value_0_0", "value_0_1"],
            ["value_1_0", "value_1_1"],
            ["value_2_0", "value_2_1"]
        ]
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()

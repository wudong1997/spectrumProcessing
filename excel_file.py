import xlrd


class xl_file:
    file_name = ''
    sheet_name = ''
    table = None

    def __init__(self, file_name, sheet_name):
        self.file_name = file_name
        self.sheet_name = sheet_name

    def read_excel(self):
        try:
            data = xlrd.open_workbook(self.file_name)
            self.table = data.sheet_by_name(self.sheet_name)
        except Exception as msg:
            error_message = msg
            print(error_message)

    def get_column(self, column_name):
        """
        获取指定列名的数据
        :param column_name: 列名
        """
        column_index = None
        # 计算指定列名编号
        for i in range(self.table.ncols):
            if str(self.table.cell_value(0, i)) == column_name:
                column_index = i
                break
        rad_list = self.table.col_values(column_index)[1:]
        return rad_list

    def get_row(self, row_name):
        """
        获取指定行名的数据
        :param row_name: 行名
        :return:
        """
        row_index = None
        # 计算指定列名编号
        for i in range(self.table.nrows):
            if str(self.table.cell_value(i, 0)) == row_name:
                row_index = i
                break
        rad_list = self.table.row_values(row_index)[1:]
        return rad_list

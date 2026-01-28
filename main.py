from Utils.HandleCSV import HandleCSV
from openpyxl.reader.excel import load_workbook

# Press the green button in the gutter to run the script.
def append_tables(act_list, new_table):
    for table_row in new_table[1:]:
        act_list.append(table_row)

def get_titles(num_worksheet):
    title_row = 11
    row_ini = title_row
    column_ini = 1
    ws = wb.worksheets[num_worksheet]
    # Cuántas columnas tiene la tabla?

    column_act = column_ini
    cl = ws.cell(row=row_ini, column=column_ini)
    while cl.value is not None:
        column_act += 1
        cl = ws.cell(row=row_ini, column=column_act)

    titles = ["Type", "Name"]
    num_columns = column_act
    for row in wb.worksheets[num_worksheet].iter_rows(min_row=title_row, max_col=num_columns - 1, max_row=title_row):
        for cell in row:
            titles.append(cell.value)
    return titles

if __name__ == '__main__':
    wb = load_workbook('resources/Dataedo Data Dictionary.xlsx')

    tables_list = [get_titles(10)]
    functions_list = []
    procedures_list = []
    views_list = []
    all_list = []
    for sheet in wb.worksheets[4:]:
        ws = sheet
        row_ini = 11
        column_ini = 1
        # Cuántas columnas tiene la tabla?
        row_act = row_ini
        column_act = column_ini
        cl = ws.cell(row=row_ini, column=column_ini)
        while cl.value is not None:
            column_act += 1
            cl = ws.cell(row=row_ini, column=column_act)

        # Cuántas filas tiene la tabla?
        cl = ws.cell(row=row_ini, column=column_ini)
        while cl.value is not None:
            row_act += 1
            cl = ws.cell(row=row_act, column=column_ini)

        # Obtener el dato de toda la tabla
        num_filas = row_act
        num_columns = column_act
        new_list = []
        new_row = ["Type", "Name"]
        titles_row = 11
        for row in ws.iter_rows(min_row=titles_row, max_col=num_columns-1, max_row=titles_row):
            for cell in row:
                new_row.append(cell.value)
        new_list.append(new_row)

        for row in ws.iter_rows(min_row=titles_row + 1, max_col=num_columns-1, max_row=num_filas-1):
            new_row = [ws.cell(row=1, column=1).value, ws.cell(row=5, column=2).value]
            for cell in row:
                new_row.append(cell.value)
            new_list.append(new_row)

        if ws.cell(row=1, column=1).value == "Table:":
            append_tables(tables_list, new_list)
        elif ws.cell(row=1, column=1).value == "View:":
            append_tables(views_list, new_list)
        elif ws.cell(row=1, column=1).value == "Function:":
            append_tables(functions_list, new_list)
        elif ws.cell(row=1, column=1).value == "Procedure:":
            append_tables(procedures_list, new_list)
        for e in new_list:
            all_list.append(e)

    HandleCSV.write_csv("./resources/all_list_full.csv", all_list)
    HandleCSV.write_csv("./resources/table_list_full.csv", tables_list)
    HandleCSV.write_csv("./resources/views_list_full.csv", views_list)
    HandleCSV.write_csv("./resources/functions_list_full.csv", functions_list)
    HandleCSV.write_csv("./resources/procedures_list_full.csv", procedures_list)



import csv


class HandleCSV:
    def read_csv(csv_doc: str):
        """
        Lee un archivo csv y devuelve la matriz de datos.

        :param csv_doc: Documento csv.
        :return: Arreglo de datos del csv_doc.
        """
        datos = []
        with open(csv_doc, encoding='latin-1') as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                datos.append(row)
        f.close()
        return datos

    def write_csv(csv_doc: str, rows):
        """
        Lee un archivo csv y escribe las filas.

        :param csv_doc: Documento csv.
        :return: None
        """
        # DELETE FROM `sistema_bpm` WHERE FECHA_APLICACION = '00-00-0000';
        with open(csv_doc, 'w', encoding='latin-1', newline='') as f:
            writer = csv.writer(f)
            for row in rows:
                try:
                    writer.writerow(row)
                except UnicodeEncodeError or UnicodeDecodeError:
                    new_row = []
                    for element in row:
                        element = str(element).encode('cp1252')
                        new_row.append(element)
                    writer.writerow(new_row)
            f.close()
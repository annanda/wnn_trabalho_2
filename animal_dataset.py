import csv
from collections import OrderedDict
import rows

VALOR_DIVISAO = 10021

class AnimalDataset:
    def __init__(self, path_to_dataset):
        self.x_train = []
        self.y_train = []
        self.x_test = []
        self.y_test = []

        with open(path_to_dataset, 'r') as csv_file:
            examples = list(csv.reader(csv_file, delimiter=','))
            examples = examples[1:]  # remove header
            x = []
            y = []
            for row in examples:
                example = [int(feature) for feature in row[:-1]]
                x.append(example)
                y.append(row[-1])
            self.x_train = x[:VALOR_DIVISAO]
            self.x_test = x[VALOR_DIVISAO:]
            self.y_train = y[:VALOR_DIVISAO]
            self.y_test = y[VALOR_DIVISAO:]
            # self.transform_test_labels()

    def transform_test_labels(self):
        # classifier = {
        #     'Return_to_owner': 0,
        #     'Euthanasia': 1,
        #     'Adoption': 2,
        #     'Transfer': 3,
        #     'Died': 4
        # }
        new_y_test = []
        for row in self.y_test:
            y = [0, 0, 0, 0, 0]
            y[int(row)] = 1
            new_y_test.append(y)
        self.y_test = new_y_test


class AnimalTestDataset:
    def __init__(self, path_to_dataset):
        self.x = []
        self.ids = []

        with open(path_to_dataset, 'r') as csv_file:
            examples = list(csv.reader(csv_file, delimiter=','))
            examples = examples[1:]  # remove header

            for row in examples:
                example = [int(feature) for feature in row[1:]]  # ignore id
                idi = int(row[0])
                self.x.append(example)
                self.ids.append(idi)

    def export_exact_predictions_to_csv(self, filename, ids, predictions):
        new_rows = []

        # classifier = {
        #     'Return_to_owner': 0,
        #     'Euthanasia': 1,
        #     'Adoption': 2,
        #     'Transfer': 3,
        #     'Died': 4
        # }

        for i, prediction in enumerate(predictions):
            # ID	Adoption	Died	Euthanasia	Return_to_owner	Transfer
            # print(type(prediction))
            # print(prediction == '3')
            # print(int(prediction == '3'))

            new_row = OrderedDict({})
            new_row['ID'] = ids[i]
            new_row['Adoption'] = int(prediction == '2')
            new_row['Died'] = int(prediction == '4')
            new_row['Euthanasia'] = int(prediction == '1')
            new_row['Return_to_owner'] = int(prediction == '0')
            new_row['Transfer'] = int(prediction == '3')

            new_rows.append(new_row)

        new_rows.sort(key=lambda e: e['ID'])
        # print(new_rows)

        new_fields = [(key, rows.fields.UnicodeField) for key in new_rows[0].keys()]
        table_to = rows.Table(fields=OrderedDict(new_fields))
        for row in new_rows:
            table_to.append(row)

        rows.export_to_csv(table_to, filename)

    def export_prob_predictions_to_csv(self, filename, ids, predictions):
        new_rows = []

        # classifier = {
        #     'Return_to_owner': 0,
        #     'Euthanasia': 1,
        #     'Adoption': 2,
        #     'Transfer': 3,
        #     'Died': 4
        # }
        # print(predictions)
        # count = [0, 0, 0, 0]
        # m = []
        for i, prediction in enumerate(predictions):
            # ID	Adoption	Died	Euthanasia	Return_to_owner	Transfer
            # print(type(prediction))
            # print(prediction == '3')
            # print(int(prediction == '3'))

            new_row = OrderedDict({})
            # print(prediction[0])
            # print(type(prediction[0]))

            # print numpy.argmax(prediction)
            # m.append(numpy.argmax(prediction))
            # if numpy.argmax(prediction) == 0:
            #     count[0]+=1
            # if numpy.argmax(prediction) == 1:
            #     count[1]+=1
            # if numpy.argmax(prediction) == 2:
            #     count[2]+=1
            # if numpy.argmax(prediction) == 3:
            #     count[3]+=1

            new_row['ID'] = ids[i]
            new_row['Adoption'] = prediction[2]
            new_row['Died'] = prediction[4]
            new_row['Euthanasia'] = prediction[1]
            new_row['Return_to_owner'] = prediction[0]
            new_row['Transfer'] = prediction[3]

            new_rows.append(new_row)
        # print(count)
        # print(set(m))
        new_rows.sort(key=lambda e: e['ID'])
        # print(new_rows)

        new_fields = [(key, rows.fields.Field) for key in new_rows[0].keys()]
        table_to = rows.Table(fields=OrderedDict(new_fields))
        for row in new_rows:
            table_to.append(row)

        rows.export_to_csv(table_to, filename)
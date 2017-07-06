import csv
from collections import OrderedDict, Counter
import rows


class AnimalDataset:
    def __init__(self, path_to_dataset, number_exemples=None):
        self.x_train = []
        self.y_train = []
        self.x_test = []
        self.y_test = []
        self.number_exemples = number_exemples
        self.number_exemples_test = None
        self.valor_divisao = None

        with open(path_to_dataset, 'r') as csv_file:
            examples = list(csv.reader(csv_file, delimiter=','))
            examples = examples[1:]  # remove header
            x = []
            y = []
            for row in examples:
                example = [int(feature) for feature in row[:-1]]
                x.append(example)
                y.append(row[-1])
            self.valor_divisao = self.percentage(90, len(y))
            self.x_train = x[:self.valor_divisao]
            self.x_test = x[self.valor_divisao:]
            self.y_train = y[:self.valor_divisao]
            self.y_test = y[self.valor_divisao:]
            self.analise_dataset_train()
            print len(x)
            print len(self.y_train)
            # self.balance_dataset_train()
            # self.balance_dataset_test()
            # self.analise_dataset_train()

    def percentage(self, percent, whole):
        return int((percent * whole) / 100.0)

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

    def transform_train_labels(self):
        new_y_train = []
        for row in self.y_train:
            y = [0, 0, 0, 0, 0]
            y[int(row)] = 1
            new_y_train.append(y)
        self.y_train = new_y_train

    def analise_dataset_train(self):
        exemplos = Counter(self.y_train)
        print exemplos.most_common(5)

        teste_exemplos = Counter(self.y_test)
        print teste_exemplos.most_common(5)

    def balance_dataset_train(self):
        new_x_train = []
        new_y_train = []
        if self.number_exemples:
            number_exemples = self.number_exemples
        else:
            contador = Counter(self.y_train)
            number_exemples = contador.most_common()[-1][-1]
            self.number_exemples = number_exemples
        quantidies = {
            '0': 0,
            '1': 0,
            '2': 0,
            '3': 0,
            '4': 0}
        for i, item in enumerate(self.y_train):
            if quantidies[item] >= number_exemples:
                continue
            else :
                new_x_train.append(self.x_train[i])
                new_y_train.append(item)
                quantidies[item] += 1
        self.x_train = new_x_train
        self.y_train = new_y_train

    def balance_dataset_test(self):
        new_x_test = []
        new_y_test = []
        contador = Counter(self.y_test)
        number_exemples = contador.most_common()[-1][-1]
        quantidies = {
            '0': 0,
            '1': 0,
            '2': 0,
            '3': 0,
            '4': 0}
        for i, item in enumerate(self.y_test):
            if quantidies[item] >= number_exemples:
                continue
            else:
                new_x_test.append(self.x_test[i])
                new_y_test.append(item)
                quantidies[item] += 1
        self.x_test = new_x_test
        self.y_test= new_y_test


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

if __name__ == '__main__':
    source_file = 'dataset/new'
    print '------------ CAT ----------------------'
    dataset_cat = AnimalDataset(source_file + '_train_cat.csv')
    print dataset_cat.valor_divisao
    print '------------ DOG ----------------------'
    dataset_dog = AnimalDataset(source_file + '_train_dog.csv')
    print dataset_dog.valor_divisao
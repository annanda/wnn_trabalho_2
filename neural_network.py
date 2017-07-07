from PyWANN.WiSARD import WiSARD
from sklearn.metrics import log_loss, confusion_matrix
from animal_dataset import AnimalDataset
import csv

# source_type = ''
source_file = 'dataset/new'
output_file = 'wnn'


def apply_wisard(source_file, num_bits_addr, bleaching, randomize_positions, animal, number_examples):
    if animal == 'cat':
        dataset = AnimalDataset(source_file + '_train_cat.csv', number_examples)
    else:
        dataset = AnimalDataset(source_file + '_train_dog.csv', number_examples)

    if number_examples is None:
        number_examples = dataset.number_exemples

    scores = [number_examples]
    w = WiSARD(num_bits_addr, bleaching, randomize_positions)
    w.fit(dataset.x_train, dataset.y_train)
    predicted = w.predict_proba(dataset.x_test)
    expected = [int(y) for y in dataset.y_test]
    score = log_loss(expected, predicted)
    scores.append(score)
    print("{},{}".format(number_examples, score))

    predicted_class = []
    for element in predicted:
        max_value = max(element)
        idx_max_value = list(element).index(max_value)
        predicted_class.append(idx_max_value)


    #     'Return_to_owner': 0,
    #     'Euthanasia': 1,
    #     'Adoption': 2,
    #     'Transfer': 3,
    #     'Died': 4

    matrix = confusion_matrix(expected, predicted_class)
    print matrix
    return scores


if __name__ == '__main__':
    num_bits_addr = 34
    bleaching = True
    randomize_positions = True
    total = []
    # for i in xrange(3186, 10020):
    animal = 'dog'
    scores_cat = apply_wisard(source_file, num_bits_addr, bleaching, randomize_positions, animal, 29)
    total.append(scores_cat)

    # with open('resultado_dog_exemples.csv', 'w') as csv_file:
    #     for item in total:
    #         rowwriter = csv.writer(csv_file, delimiter=',')
    #         rowwriter.writerow(item)





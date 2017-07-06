from PyWANN.WiSARD import WiSARD
from sklearn.metrics import log_loss
from animal_dataset import AnimalDataset, AnimalTestDataset
import csv

# source_type = ''
source_file = 'dataset/new'
output_file = 'wnn'


def apply_wisard(source_file, num_bits_addr, bleaching, randomize_positions):
    dataset = AnimalDataset(source_file + '_train_cat.csv')
    cat_testset = AnimalTestDataset(source_file + '_cat_test.csv')
    bits_memoria_max = 36
    score_total = []
    for i in xrange(bits_memoria_max, 16, -1):
        scores = [i]
        w = WiSARD(i, bleaching, randomize_positions)
        w.fit(dataset.x_train + dataset.x_test, dataset.y_train + dataset.y_test)
        predicted = w.predict_proba(dataset.x_test)
        # predicted_on_cats = w.predict_proba(cat_testset.x)
        expected = dataset.y_test
        score = log_loss(expected, predicted)
        scores.append(score)
        print("Logloss on cats: {}, memoria: {}".format(score, i))

        ###########################################

        dataset = AnimalDataset(source_file + '_train_dog.csv')
        dog_testset = AnimalTestDataset(source_file + '_dog_test.csv')

        w_2 = WiSARD(num_bits_addr, bleaching, randomize_positions)
        w_2.fit(dataset.x_train + dataset.x_test, dataset.y_train + dataset.y_test)
        predicted = w_2.predict_proba(dataset.x_test)
        # predicted_on_dogs = w_2.predict_proba(dog_testset.x)
        expected = dataset.y_test
        score = log_loss(expected, predicted)
        scores.append(score)
        print("Logloss on dogs: {}, memoria: {}".format(score, i))

        # dog_testset.export_prob_predictions_to_csv(output_file + '_memoria_' + str(i) + '.csv', cat_testset.ids + dog_testset.ids,
        #
        #                                       list(predicted_on_cats) + list(predicted_on_dogs))
    #
        score_total.append(scores)
    return score_total


if __name__ == '__main__':
    num_bits_addr = 34
    bleaching = True
    randomize_positions = True
    scores = apply_wisard(source_file, num_bits_addr, bleaching, randomize_positions)

    with open('resultado_memoria_2.csv', 'w') as csv_file:
        for score in scores:
            rowwriter = csv.writer(csv_file, delimiter=',')
            rowwriter.writerow(score)





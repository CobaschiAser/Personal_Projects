import json
import os
import random


def load_data(directory, part):
    train_documents = []
    train_labels = []
    test_documents = []
    test_labels = []

    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            f = os.path.join(root, name)
            msg = open(f, "r")
            if part in f:
                test_labels.append(1 if 'spm' in f else 0)
                test_documents.append(msg.read())
            else:
                train_labels.append(1 if 'spm' in f else 0)
                train_documents.append(msg.read())
            msg.close()

    print("Data loaded")
    return train_documents, train_labels, test_documents, test_labels


def flip_coin():
    random_number = random.random()
    if random_number < 0.5:
        return 0
    return 1


def flip_coin_test(directory, part):
    train_documents, train_labels, test_documents, test_labels = load_data(directory, part)

    flip_coin_correct = 0
    print("Flip_coin")
    c = 1
    for doc, label in zip(test_documents, test_labels):
        flip_coin_prediction = flip_coin()
        print(c)
        c += 1
        if label == flip_coin_prediction:
            flip_coin_correct += 1

    return flip_coin_correct / len(test_labels)


def always_zero_test(directory, part):
    train_documents, train_labels, test_documents, test_labels = load_data(directory, part)

    print("Always_zero: ")
    always_zero_correct = 0
    c = 1
    for doc, label in zip(test_documents, test_labels):
        print(c)
        c += 1
        if label == 0:
            always_zero_correct += 1

    return always_zero_correct / len(test_labels)


if __name__ == "__main__":
    data_directory = 'lingspam_public'

    flip_coin_file = 'results/filp_coin.json'
    flip_coin_accuracy = flip_coin_test(data_directory, "part10")

    always_zero_file = 'results/always_zero.json'
    always_zero_accuracy = always_zero_test(data_directory, "part10")

    with open(flip_coin_file, 'w') as file:
        json.dump(flip_coin_accuracy, file)

    with open(always_zero_file, 'w') as file:
        json.dump(always_zero_accuracy, file)

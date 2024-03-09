import os
import re
from collections import defaultdict
from math import log
import json


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

    return train_documents, train_labels, test_documents, test_labels


def preprocess_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    return text.split()


def train_naive_bayes(documents, labels):
    class_probs = [0, 0]
    word_probs = [[], []]
    vocabulary = []

    total_documents = len(documents)
    c = 1
    for doc, label in zip(documents, labels):
        print("c: " + str(c))
        c += 1
        words = preprocess_text(doc)
        class_probs[label] += 1.0

        for word in words:
            if word in vocabulary:
                index = vocabulary.index(word)
                word_probs[label][index] += 1.0
            else:
                vocabulary.append(word)
                word_probs[label].append(1)
                word_probs[(label + 1) % 2].append(0)

    d = 0
    for label in range(2):
        class_probs[label] /= total_documents
        d += 1
        e = 0
        total_word_count = sum(word_probs[label])
        for index in range(len(vocabulary)):
            e += 1
            word_probs[label][index] = (word_probs[label][index] + 1) / (total_word_count + len(vocabulary))
            print("d: " + str(d) + " e: " + str(e))
    return class_probs, word_probs, vocabulary


def load_trained_bayes(part):
    with open('bayes_naive_files\class_' + part + '.json', 'r') as filehandle:
        class_probs = json.loads(filehandle.read())
    with open('bayes_naive_files\words_' + part + '.json', 'r') as filehandle:
        word_probs = json.loads(filehandle.read())
    with open('bayes_naive_files\\vocab_' + part + '.json', 'r') as filehandle:
        vocabulary = json.loads(filehandle.read())

    return class_probs, word_probs, vocabulary


def predict_naive_bayes(document, class_probs, word_probs, vocabulary):
    words = preprocess_text(document)
    scores = [log(score) for score in class_probs]

    for label in range(2):
        for word in words:
            try:
                index = vocabulary.index(word)
                scores[label] += log(word_probs[label][index])
            except:
                continue

    if scores[0] > scores[1]:
        return 0
    else:
        return 1


def train_and_test(directory, part):
    train_documents, train_labels, test_documents, test_labels = load_data(directory, part)
    class_probs, word_probs, vocabulary = load_trained_bayes(part)

    # pentru a scrie datele
    '''output_class_probs = 'bayes_naive_files\class_' + part + '.json'
    output_word_probs = 'bayes_naive_files\words_' + part + '.json'
    output_vocab_probs = 'bayes_naive_files\\vocab_' + part + '.json'

    with open(output_class_probs, 'w') as file:
        json.dump(class_probs, file)
    with open(output_word_probs, 'w') as file:
        json.dump(word_probs, file)
    with open(output_vocab_probs, 'w') as file:
        json.dump(vocabulary, file)
    '''
    correct = 0
    prediction_number = 1
    for doc, label in zip(test_documents, test_labels):
        prediction = predict_naive_bayes(doc, class_probs, word_probs, vocabulary)
        if label == prediction:
            correct += 1
        prediction_number += 1

    return correct / len(test_labels)


def leave_one_out(directory):
    accuracy_file = '/results/bayes_naive_accuracies.json'
    part_set = ["part" + str(i) for i in range(1, 11)]
    accuracy_sum = 0
    index = 1
    accuracy_dict = {}
    for part in part_set:
        part_accuracy = train_and_test(directory, part)
        accuracy_sum += part_accuracy
        if part not in accuracy_dict.keys():
            accuracy_dict[part] = part_accuracy
        index += 1

    #with open(accuracy_file, 'w') as file:
    #    json.dump(accuracy_dict, file)

    return accuracy_sum / len(part_set)


if __name__ == "__main__":
    data_directory = 'lingspam_public'

    accuracy = leave_one_out(data_directory)
    print("Leave one Out accuracy: " + str(accuracy))

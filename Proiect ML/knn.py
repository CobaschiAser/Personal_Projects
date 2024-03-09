from Levenshtein import distance as lev
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


# preprocesarea: fiecare fisier e transformat intr-o lista de cuvinte,
# cand calculez distanta intre 2 fisiere(instante), calculez distanta Levenshtein intre cele 2 liste de cuvinte respective

def get_key(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    return text


def preprocess_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    return text.split()


def train_knn(documents, labels):
    docs_with_labels = {}
    processed_docs = []
    for doc, label in zip(documents, labels):
        word_key = get_key(doc)
        processed_docs.append(preprocess_text(doc))
        if word_key not in docs_with_labels.keys():
            docs_with_labels[word_key] = label

    return docs_with_labels, processed_docs


def predict_knn(document, documents_set, docs_with_labels, k, processed_docs):
    predict_word = preprocess_text(document)
    predict_list = []
    for i in range(len(documents_set)):
        word = processed_docs[i]
        predict_list.append([documents_set[i], lev(predict_word, word)])

    sorted_list = sorted(predict_list, key=lambda x: x[1])
    one_sum = 0
    for i in range(k):
        one_sum += docs_with_labels[get_key(sorted_list[i][0])]

    if one_sum <= k / 2:
        return 0
    else:
        return 1


def train_and_test(directory, part, k):
    train_documents, train_labels, test_documents, test_labels = load_data(directory, part)
    print(len(test_documents))
    docs_with_labels, processed_docs = train_knn(train_documents, train_labels)
    correct = 0
    prediction_number = 0
    for doc, label in zip(test_documents, test_labels):
        prediction = predict_knn(doc, train_documents, docs_with_labels, k, processed_docs)
        prediction_number += 1
        if label == prediction:
            correct += 1

    return correct / len(test_labels)


def leave_one_out(directory, k):
    accuracy_file = 'results\knn_accuracies.json'
    part_set = ["part" + str(i) for i in range(1, 11)]
    accuracy_sum = 0
    index = 1
    accuracy_dict = {}
    for part in part_set:
        part_accuracy = train_and_test(directory, part, k)
        index += 1
        accuracy_sum += part_accuracy
        if part not in accuracy_dict.keys():
            accuracy_dict[part] = part_accuracy

    with open(accuracy_file, 'w') as file:
        json.dump(accuracy_dict, file)

    return accuracy_sum / len(part_set)


if __name__ == "__main__":
    data_directory = 'lingspam_public'
    accuracy = leave_one_out(data_directory, 1001)
    print("Leave one Out accuracy: " + str(accuracy))


# K = 3 accuracy  0.9759450171821306
# K = 1001 accuracy 0.8419243986254296
# K = 1001 "cvloo accuracy" :  0.8448977554573409

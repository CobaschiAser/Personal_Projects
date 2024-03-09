import os
import re
from collections import defaultdict
from math import log
import json


def load_parts(directory):
    parts = [[], [], [], [], [], [], [], [], [], []]
    labels = [[], [], [], [], [], [], [], [], [], []]
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            f = os.path.join(root, name)
            msg = open(f, "r")
            for i in reversed(range(1, 11)):
                part_str = f"part{i}"
                if part_str in f:
                    parts[i - 1].append(msg.read())
                    labels[i - 1].append(1 if 'spm' in f else 0)
                    break
            msg.close()
    return parts, labels


def preprocess_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    return text.split()


def train_naive_bayes_bonus(documents, labels):
    class_probs = [0, 0, 0]
    word_probs = [[], [], []]
    vocabulary = []

    total_documents = len(documents)

    #c = 1
    for doc, label in zip(documents, labels):
        #print(c)
        #c += 1
        words = preprocess_text(doc)
        class_probs[label] += 1.0

        for word in words:
            if word in vocabulary:
                index = vocabulary.index(word)
                word_probs[label][index] += 1.0
            else:
                vocabulary.append(word)
                word_probs[label].append(1)
                for i in range(3):
                    if i != label:
                        word_probs[i].append(0)

    for label in range(3):
        print(label)
        class_probs[label] /= total_documents

        total_word_count = sum(word_probs[label])
        for index in range(len(vocabulary)):
            word_probs[label][index] = (word_probs[label][index] + 1) / (total_word_count + len(vocabulary))

    return class_probs, word_probs, vocabulary


def split_test_train(parts, labels, index):
    train_doc = parts[:index] + parts[index + 1:]
    train_label = labels[:index] + labels[index + 1:]
    test_doc = parts[index]
    test_label = labels[index]

    return train_doc, train_label, test_doc, test_label


def test_split(data_directory):
    parts, labels = load_parts(data_directory)
    for part_index in range(2, 10):
        print("For part" + str(part_index + 1))
        train_doc, train_label, test_doc, test_label = split_test_train(parts, labels, part_index)
        print(len(train_doc))
        print(len(train_label))
        print(len(test_doc))
        print(len(test_label))


def leave_one_out(data_directory):
    accuracy_file = 'results\\bonus_accuracies.json'

    accuracy_dict = {}
    accuracy_sum = 0

    for part_index in range(2, 10):
        parts, labels = load_parts(data_directory)
        train_doc, train_label, test_doc, test_label = split_test_train(parts, labels, part_index)
        print(len(train_doc))
        print(len(train_label))
        print(len(test_doc))
        print(len(test_label))
        for i in range(len(train_label[0])):
            train_label[0][i] = 2
        for i in range(len(train_label[1])):
            train_label[1][i] = 2
        docs = [d for docs in train_doc for d in docs]
        labels = [l for lab in train_label for l in lab]
        print("Training for part " + str(part_index+1) + " started")
        class_probs, word_probs, vocabulary = train_naive_bayes_bonus(docs, labels)
        print("Training for part " + str(part_index+1) + " ready")
        with open('bonus_files\\class_part' + str(part_index+1) + '.json', 'w+') as filehandle:
            json.dump(class_probs, filehandle)
        with open('bonus_files\\words_part' + str(part_index+1) + '.json', 'w+') as filehandle:
            json.dump(word_probs, filehandle)
        with open('bonus_files\\vocab_part' + str(part_index+1) + '.json', 'w+') as filehandle:
            json.dump(vocabulary, filehandle)

        '''with open('bonus_class.txt', 'r') as filehandle:
           class_probs = json.loads(filehandle.read())
        with open('bonus_words.txt', 'r') as filehandle:
           word_probs = json.loads(filehandle.read())
        with open('bonus_vocab.txt', 'r') as filehandle:
           vocabulary = json.loads(filehandle.read())
        '''
        correct = 0
        total = 0
        # c = 1
        for document, true_label in zip(test_doc, test_label):
            # print(c)
            # c += 1
            words = preprocess_text(document)
            scores = [log(score) for score in class_probs]

            for label in range(3):
                for word in words:
                    try:
                        index = vocabulary.index(word)
                        scores[label] += log(word_probs[label][index])
                    except:
                        continue

            if scores[0] > scores[1] and scores[0] > scores[2]:
                prediction = 0
            elif scores[1] > scores[0] and scores[1] > scores[2]:
                prediction = 1
            else:
                prediction = 2

            if prediction != 2:
                total += 1
                if prediction == true_label:
                    correct += 1

        current_accuracy = correct / total
        key = 'part' + str(part_index + 1)
        if key not in accuracy_dict:
            accuracy_dict[key] = current_accuracy
        print("Accuracy for part " + str(part_index+1) + " is: " + str(accuracy_dict[key]))
        accuracy_sum += accuracy_dict[key]

    cvloo_accuracy = accuracy_sum / len(accuracy_dict.keys())

    accuracy_dict["cvloo"] = cvloo_accuracy
    print("CVLOO accuracy: " + str(accuracy_dict["cvloo"]))

    with open(accuracy_file, 'w') as file:
        json.dump(accuracy_dict, file)


if __name__ == "__main__":
    data_directory = 'lingspam_public'
    test_split(data_directory)
    leave_one_out(data_directory)


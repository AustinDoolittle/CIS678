import argparse
import pprint
import time
import math
import operator
import matplotlib.pyplot as plot
import numpy as np
import networkx as nx

#trains the classifier
def Train(filename, verbose=True):
    start_time = time.time();
    vocab = {}
    categories = {}

    #read the lines from the file
    trainFile = open(filename)
    trainFileLines = trainFile.readlines()
    trainFileLen = len(trainFileLines)
    trainFile.close()
    counter = 1

    #iterate over the lines
    for line in trainFileLines:
        lineSplit = line.split(' ', 1)
        category = lineSplit[0]
        content = lineSplit[1].rstrip().split(' ')
        if verbose:
            print str(counter) + "/" + str(trainFileLen)+ " Category: " + category

        #get store the count of that category
        if category not in categories:
            categories[category] = {
                'count': 1,
                'words': {},
                'wordcount': 0,
                'probability': 0
            }
        else:
            categories[category]['count'] += 1

        #iterate over the words in the document and add their counts to the category dictionay
        for word in content:
            categories[category]['wordcount'] += 1
            if word not in vocab:
                vocab[word] = 1
            else:
                vocab[word] += 1
            if word not in categories[category]['words']:
                categories[category]['words'][word] = {
                    'count': 1,
                    'probability': 0
                }
            else:
                categories[category]['words'][word]['count'] += 1
        counter += 1


    print str(trainFileLen) + " documents in training set"
    print str(len(vocab)) + " words in vocabulary"

    print 'Calculating Probabilities'

    #iterate over the category dictionary and calculate the Probabilities
    vocabLength = len(vocab)
    for c in categories:
        categories[c]['probability'] = math.log(((categories[c]['count']**2) + 0.0) / trainFileLen)
        categories[c]['def_probability'] = math.log(1.0 / (categories[c]['wordcount'] + vocabLength))
        for w in categories[c]["words"]:
            categories[c]['words'][w]['probability'] = math.log((categories[c]['words'][w]['count'] + 1.0) / (categories[c]['wordcount'] + vocabLength))

    print "Training time: " + str(time.time() - start_time)
    if verbose:
        print ''
    return vocab, categories

#Test against a file containing test data
def Test(vocab, data, filename, verbose):
    start_time = time.time();

    #read all the lines from the test file
    testfile = open(filename)
    testfileLines = testfile.readlines()
    testfileLen = len(testfileLines)
    testfile.close()
    correct = 0
    counter = 0

    analytics = {}

    for category in data:
        analytics[category] = {
            "correct": 0,
            "wrong_guesses": {},
            "count": 0
        }

    vocabLength = len(vocab)

    for line in testfileLines:
        #iterate over the words in the file, calculate their Probabilities and the overall probability for the category on that document
        lineSplit = line.split(' ', 1)
        actual_category = lineSplit[0]
        content = lineSplit[1].rstrip().split(' ')
        products = {}
        for cat in data:
            def_probability = data[cat]['def_probability']
            products[cat] = data[cat]['probability']
            for word in content:
                if word in data[cat]['words']:
                    products[cat] += data[cat]['words'][word]['probability']
                elif word in vocab:
                    data[cat]['words'][word] = {
                        'probability': def_probability
                    }
                    products[cat] += def_probability

        #determine which category has the highest word probabilities
        guess_category = max(products, key=products.get)
        if verbose:
            #pp.pprint(products)
            print str(counter+1) + "/" + str(testfileLen) + " Guess: " + guess_category + ", Actual: " + actual_category + (" RIGHT" if guess_category == actual_category else " WRONG")

        #store analytical data
        if guess_category == actual_category:
            correct += 1
            analytics[actual_category]["correct"] += 1
        else:
            if guess_category not in analytics[actual_category]["wrong_guesses"]:
                analytics[actual_category]["wrong_guesses"][guess_category] = 1
            else:
                analytics[actual_category]["wrong_guesses"][guess_category] += 1

        analytics[actual_category]["count"] += 1
        counter += 1

    total_time = time.time() - start_time
    print "Testing Time: " + str(total_time)
    print "Accuracy: " + str(((correct + 0.0) / testfileLen) * 100) + "%"

    return analytics

def Graph(results, analytics, vocab):
    #Accuracy for each category bar Graph
    accuracies = {}
    pie_chart_stats = {}
    most_mistaken = {}
    for cat in analytics:
        accuracies[cat] = (analytics[cat]["correct"] / (analytics[cat]["count"] + 0.1)) * 100
        pie_chart_stats[cat] = {}
        total_wrong = analytics[cat]["count"] - analytics[cat]["correct"]
        max_error = ''
        for error in analytics[cat]['wrong_guesses']:
            pie_chart_stats[cat][error] = ((analytics[cat]['wrong_guesses'][error] + 0.0) / total_wrong) * 100
            if max_error == '' or analytics[cat]['wrong_guesses'][error] > analytics[cat]['wrong_guesses'][max_error]:
                max_error = error
        most_mistaken[cat] = max_error


    accuracies = sorted(accuracies.items(), key=lambda x: x[1], reverse=True)

    x = [val[0] for val in accuracies]
    y = [val[1] for val in accuracies]

    y_pos = np.arange(len(x))
    plot.bar(y_pos, y, align='center', alpha=0.5)
    plot.xticks(y_pos, x, rotation=90)
    plot.ylabel("Accuracy (%)")
    plot.xlabel("Category")
    plot.title("Accuracy by Category")
    plot.tight_layout()
    plot.draw()
    plot.savefig('accuracies.png')


    #pie chart for each category with incorrect guesses
    for cat in pie_chart_stats:
        labels = pie_chart_stats[cat].keys()
        values = pie_chart_stats[cat].values()
        plot.figure()
        plot.pie(values, labels=labels, autopct='%%%.2f')
        plot.axis('equal')
        plot.title(cat + " Misclassification Frequency")
        plot.savefig(cat + "_pie.png")
    plot.draw()

    #Directed Graph of the most mistaken
    plot.figure()
    dg = nx.DiGraph()
    dg.add_edges_from(most_mistaken.items())
    nx.draw(dg, with_labels=True)
    plot.savefig('dir_graph.png')

    #highest probability word in each category
    most_probs = {}
    highest_vocab = sorted(vocab.items(), key=operator.itemgetter(1), reverse=True)[:100]
    highest_vocab = [x[0] for x in highest_vocab]
    word_write_count = 25
    for cat in categories:
        #sorted_probs = sortd(categories[cat]['words'].items(), key=operator.itemgetter(1))
        sorted_probs = sorted(categories[cat]['words'].items(), key=operator.itemgetter(1), reverse=True)
        sorted_probs = [x[0] for x in sorted_probs]
        highest_uniques = []
        for word in sorted_probs:
            if word not in highest_vocab:
                highest_uniques.append((word, categories[cat]['words'][word]['probability']))
                if len(highest_uniques) == word_write_count:
                    break
        most_probs[cat] = highest_uniques

    highest_uniques_file = open('highest_uniques_file.csv', 'w')
    highest_uniques_file.write('category')
    for i in range(word_write_count):
        highest_uniques_file.write(',' + str(i+1))
    highest_uniques_file.write('\n')

    for cat in most_probs:
        highest_uniques_file.write(cat)
        for word in most_probs[cat]:
            is_copy = False
            for cat2 in most_probs:
                if cat2 == cat:
                    continue
                for word2 in most_probs[cat2]:
                    if word2[0] == word[0]:
                        is_copy = True
                        break
                if is_copy:
                    break
            if is_copy:
                highest_uniques_file.write(',_' + word[0] + '_')
            else:
                highest_uniques_file.write(',' + word[0])
        highest_uniques_file.write('\n')

    highest_uniques_file.close()

    plot.show()

#begin main function

#setup the argument parser
docs = {}
parser = argparse.ArgumentParser()
parser.add_argument('-tr', '--train', help='The file to train with')
parser.add_argument('-te', '--test', help='The file to test with')
parser.add_argument('-v', '--verbose', help='Prints out more information during the training and testing process', action='store_true')
args = parser.parse_args()

#get train file
if args.train is not None:
    train_file = args.train
else:
    train_file = 'forumTraining-stemmed.data'

print "-- Beginning Training --\n"

#train
vocabulary, categories = Train(train_file, args.verbose)

print "-- Training Complete --"
print "======================="
print "-- Beginning Testing --\n"

#get test file
if args.test is not None:
    test_file = args.test
else:
    test_file = 'forumTest-stemmed.data'

#test
analytics = Test(vocabulary, categories, test_file, args.verbose)

print "-- Testing Complete --"
print "======================="
print "-- Beginning Analytics --\n"

#display analytics
Graph(categories, analytics, vocabulary)

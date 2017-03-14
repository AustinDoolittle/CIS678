import argparse
import math
import sys
import random as rand
import timeit
import os

__verbose = False
__leaf_count = 0
__vertices_count = 0
__max_depth = 0
__ifthen_count = 0

def Entropy(s):
    counts = {}
    total_size = len(s)
    for line in s:
        if line['class'] not in counts:
            counts[line['class']] = 1
        else:
            counts[line['class']] += 1

    retval = 0
    for c in counts:
        temp = (counts[c] + 0.0) / total_size
        retval += temp * math.log(temp, 2)

    return -retval

def MSQ_Entropy(s, feat, real_val):
    retval = 0
    for line in s:
        retval += (real_val - line['features'][feat]) ** 2
    return retval / len(s)

def Gain(s, a, real_val=None):
    total_size = len(s)

    if real_val is not None:
        retval = MSQ_Entropy(s, a, real_val)
        return Entropy(s) - retval, real_val
    else:
        feat_vals = {}
        for line in s:
            if line['features'][a] not in feat_vals:
                feat_vals[line['features'][a]] = 1
            else:
                feat_vals[line['features'][a]] += 1

        retval = 0
        for val in feat_vals:
            retval += ((feat_vals[val] + 0.0) / total_size) * Entropy([x for x in s if x['features'][a] == val])

        return Entropy(s) - retval, feat_vals.keys()


def MySplit(line):
    retval = line.split(',')
    return [x.strip() for x in retval]

def LoadData(filename):
    with open(filename) as f:
        data = f.readlines()

    #remove newlines
    data = [d.strip() for d in data]

    #get classes
    class_count = int(data[0])
    classes = []
    for c in data[1].split(','):
        classes.append(c)

    #get features and their values
    feature_count = int(data[2])
    features = {}
    feature_list = []
    index = feature_count + 3
    for line in data[3:index]:   #start at data index 3
        feat_data = MySplit(line)
        feature_list.append(feat_data[0])
        if feat_data[1] == "real":
            features[feat_data[0]] = {
                'is_real': True
            }
        else:
            features[feat_data[0]] = {
                'is_real': False,
                'classes': feat_data[2:]
            }

    index += 1

    retval = []

    for line in data[index:]:
        line_data = MySplit(line)
        temp = {}
        for f in range(0, feature_count):
            if features[feature_list[f]]['is_real']:
                temp[feature_list[f]] = float(line_data[f])
            else:
                temp[feature_list[f]] = line_data[f]

        retval.append({
            'features': temp,
            'class': line_data[feature_count]
        })

    rand.shuffle(retval)
    split_index = int(.75 * len(retval))
    train = retval[:split_index]
    test = retval[split_index:]
    return train, test, classes, features

def GenerateTree(s, features, used_features=[], depth_count=0):
    global __verbose
    global __leaf_count
    global __max_depth
    global __vertices_count

    if depth_count > __max_depth:
        __max_depth = depth_count

    __vertices_count += 1

    class_counts = {}
    feature_list = [x for x in features.keys() if x not in used_features]

    for line in s:
        if line['class'] not in class_counts:
            class_counts[line['class']] = 1
        else:
            class_counts[line['class']] += 1

    most_likely_class = max(class_counts, key=class_counts.get)

    if len(class_counts) == 1:
        #we only have one class, return it
        __leaf_count += 1
        if __verbose:
            print "1 class, creating leaf, Depth: " + str(depth_count) + ",  New Leafcount: " + str(__leaf_count)

        return {
            'is_leaf': True,
            'class': class_counts.keys()[0]
        }
    elif len(feature_list) == 0:
        #we are out of features to test for, return the most popular class
        __leaf_count += 1
        if __verbose:
            print "No more features, creating leaf, Depth: " + str(depth_count) + ", New Leafcount: " + str(__leaf_count)

        return {
            'is_leaf': True,
            'class': most_likely_class
        }
    else:
        #split on the feature with the highest gain\
        if __verbose:
            print "Calculating Best Feature"

        gains = {}
        val_list = {}
        for f in feature_list:
            if features[f]['is_real']:
                if __verbose:
                    print "\tCalculating Thresholds"

                thresholds = []
                s_sorted = sorted(s, key=lambda x: x['features'][f])
                last_class = s_sorted[0]['class']
                last_val = s_sorted[0]['features'][f]
                for k in range(1,len(s_sorted)):
                    if last_class != s_sorted[k]['class']:
                        thresholds.append((last_val + s_sorted[k]['features'][f]) / 2)
                        last_class = s_sorted[k]['class']
                    last_val = s_sorted[k]['features'][f]

                if __verbose:
                    print "\tNum thresholds: " + str(len(thresholds))
                    print "\tCalculating Gains..."
                thresholds = dict(zip(thresholds, [Gain(s,f,x) for x in thresholds]))
                max_val = max(thresholds, key=thresholds.get)
                if __verbose:
                    print "\tBest threshold: " + str(thresholds[max_val]) + "\n"
                gains[f], val_list[f] = thresholds[max_val], max_val
            else:

                gains[f], val_list[f] = Gain(s, f)

        split_feat = max(gains, key=gains.get)

        retval = {
            'feature': split_feat,
            'is_leaf': False,
            'branches': {}
        }

        new_used_features = used_features + [split_feat]

        if features[split_feat]['is_real']:
            retval['is_real'] = True
            retval['split_val'] = val_list[split_feat]
            under_thresh = [x for x in s if x['features'][split_feat] < val_list[split_feat]]
            over_thresh =[x for x in s if x['features'][split_feat] >= val_list[split_feat]]
            if len(under_thresh) > 0:
                if __verbose:
                    print "Creating split on " + split_feat + ", Depth: " + str(depth_count)
                retval['branches']['under'] = GenerateTree(under_thresh, features, new_used_features, depth_count + 1)
            else:
                __leaf_count += 1
                if __verbose:
                    print "No more training examples, creating leaf, Depth: " + str(depth_count) + ", New Leafcount: " + str(__leaf_count)
                retval['branches']['under'] = {
                    'is_leaf': True,
                    'class': most_likely_class
                }

            if len(over_thresh) > 0:
                if __verbose:
                    print "Creating split on " + split_feat + ", Depth: " + str(depth_count)
                retval['branches']['over'] = GenerateTree(over_thresh, features, new_used_features, depth_count + 1)
            else:
                __leaf_count += 1
                if __verbose:
                    print "No more training examples, creating leaf, Depth: " + str(depth_count) + ", New Leafcount: " + str(__leaf_count)
                retval['branches']['over'] = {
                    'is_leaf': True,
                    'class': most_likely_class
                }
        else:
            retval['is_real'] = False
            for val in features[split_feat]['classes']:
                temp = [x for x in s if x['features'][split_feat] == val]
                if len(temp) > 0:
                    if __verbose:
                        print "Creating split on " + split_feat + ", Depth: " + str(depth_count)
                    retval['branches'][val] = GenerateTree(temp, features, new_used_features, depth_count + 1)
                else:
                    __leaf_count += 1
                    if __verbose:
                        print "No more training examples, creating leaf, Depth: " + str(depth_count) + ", New Leafcount: " + str(__leaf_count)
                    retval['branches'][val] = {
                        'is_leaf': True,
                        'class': most_likely_class
                    }

        return retval

def TestTree(test_data, tree, features):
    analytics = {
        'classes': {},
        'correct': 0,
        'total': len(test_data)
    }
    for line in test_data:
        c = Classify(line, tree, features)
        if line['class'] not in analytics['classes']:
            analytics['classes'][line['class']] = {
                'count': len([x for x in test_data if x['class'] == line['class']]),
                'correct': 0,
                'misclass': {}
            }

        if c == line['class']:
            analytics['correct'] += 1
            analytics['classes'][c]['correct'] += 1
        else:
            if c not in analytics['classes'][line['class']]['misclass']:
                analytics['classes'][line['class']]['misclass'][c] = 1
            else:
                analytics['classes'][line['class']]['misclass'][c] += 1

    return analytics

def TestForest(test_data, forest, features):
    analytics = {
        'classes': {},
        'correct': 0,
        'total': len(test_data)
    }
    for line in test_data:
        class_counts = {}
        for tree in forest:
            c = Classify(line, tree[0], tree[1])
            if c not in class_counts:
                class_counts[c] = 1
            else:
                class_counts[c] += 1
        max_class = max(class_counts, key=class_counts.get)
        if line['class'] not in analytics:
            analytics['classes'][line['class']] = {
                'count': len([x for x in test_data if x['class'] == line['class']]),
                'correct': 0,
                'misclass': {}
            }

        if max_class == line['class']:
            analytics['correct'] += 1
            analytics['classes'][max_class]['correct'] += 1
        else:
            if max_class not in analytics['classes'][line['class']]['misclass']:
                analytics['classes'][line['class']]['misclass'][max_class] = 1
            else:
                analytics['classes'][line['class']]['misclass'][max_class] += 1

    return analytics


def GenerateForest(train_data, features, tree_count):
    global __leaf_count
    global __max_depth
    global __vertices_count
    trees = []
    for i in range(0,tree_count):
        sub_data = GetSubset(train_data, .1)
        sub_features = {i: features[i] for i in GetSubset(features.keys(), .1)}
        print "\tCreating tree " + str(i+1) + "/" + str(tree_count)
        if __verbose:
            print "\t\tSubset size: " + str(len(sub_data))
            print "\t\tFeature list size: " + str(len(sub_features))
        trees.append((GenerateTree(sub_data, sub_features), sub_features))
        __leaf_count = 0
        __max_depth = 0
        __vertices_count = 0
    return trees

def Classify(data_line, tree, features):
    if tree['is_leaf']:
        return tree['class']
    else:
        if features[tree['feature']]['is_real']:
            if data_line['features'][tree['feature']] < tree['split_val']:
                return Classify(data_line, tree['branches']['under'], features)
            else:
                return Classify(data_line, tree['branches']['over'], features)
        else:
            return Classify(data_line, tree['branches'][data_line['features'][tree['feature']]], features)

def GetSubset(list, threshold=0):
    return [list[i] for i in rand.sample(xrange(len(list)), rand.randrange(math.floor(len(list) * threshold), len(list)))]

#TODO
def CreateIfThen(tree, features):
    global __ifthen_count

    if tree['is_leaf']:
        return str(__ifthen_count) + ". Classified as " + tree['class'] + '\n\n'
    else:
        counter = 0
        retstr = str(__ifthen_count) + ". Split on " + tree['feature'] + '\n'
        appstr = ""
        for k in tree['branches']:
            __ifthen_count += 1
            if tree['is_real']:
                retstr += "\t" + k + " " + str(tree['split_val']) + ": Go To " + str(__ifthen_count) + "\n"
            else:
                retstr += "\t" + k + ": Go To " + str(__ifthen_count) + "\n"
            appstr += CreateIfThen(tree['branches'][k], features)
        return retstr + "\n" + appstr


#begin main function
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Use Decision trees to classify datasets")
    parser.add_argument("--data", "-d", dest='filename', default='car.data')
    parser.add_argument("--verbose", "-v", dest='verbose', action="store_true", default=False)
    parser.add_argument("--lorax", "-l", dest="lorax", action="store_true", default=False)
    parser.add_argument("--treecount", "-t", default="10", type=int)


    args = parser.parse_args()
    __verbose = args.verbose;

    train_data, test_data, classes, features = LoadData(args.filename)

    if args.lorax:
        print "~~I am the Lorax. I speak for the trees. I speak for the trees for the trees have no tongues~~\n"

        print "Generating Forest"
        train_start = timeit.default_timer()
        forest = GenerateForest(train_data, features, args.treecount)
        train_end = timeit.default_timer()
        print "Forest Generation time: " + str(train_end - train_start) + "\n"

        print "Starting Testing..."
        test_start = timeit.default_timer()
        results = TestForest(test_data, forest, features)
        test_end = timeit.default_timer()
        print "Testing time: " + str(test_end - test_start) + "\n"

        print "~~Results~~"
        print "Tree Count: " + str(len(forest))
        print "Accuract: " + str(round(((results['correct'] + 0.0) / results['total']) * 100, 3)) + "%"

    else:
        print "Generating Tree..."
        train_start = timeit.default_timer()
        tree = GenerateTree(train_data, features)
        train_end = timeit.default_timer()
        print "Train time: " + str(train_end - train_start) + '\n'

        print "Starting Testing..."
        test_start = timeit.default_timer()
        results = TestTree(test_data, tree, features)
        test_end = timeit.default_timer()
        print "Test time: " + str(test_end - test_start) + '\n'

        print "~~Results~~"
        print "Leaf Count: " + str(__leaf_count) 
        print "Height: " + str(__max_depth) 
        print "Vertices Count: " + str(__vertices_count)
        print "Accuracy: " + str(round(((results['correct'] + 0.0) / results['total']) * 100, 3)) + "%"

        #create If Then document
        ifthen_filename, junk = os.path.splitext(args.filename)
        ifthen_result = CreateIfThen(tree, features)
        fp = open(ifthen_filename + ".ift", 'w')
        fp.write(ifthen_result)
        fp.close()

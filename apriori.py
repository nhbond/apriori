__author__      = "Nathan H. Bond"

import numpy as np
import itertools
import csv

def read_csv(filename):
    data = []
    with open(f'./{filename}') as fid:
        reader = csv.reader(fid, delimiter=',', quotechar='"')
        for row in reader:
            # filter out empty strings from row
            data.append(set(filter(None, row)))
    return data

def apriori_itemsets(minsup, filename): #minsup, minconf , minlift,
    # dataset loaded from csv
    dataset = read_csv(filename)
    # create set and compute support counts for 1-itemset
    one_item_set = {}
    last_infrequent = []
    # create set of all 1-itemsets and their respective counts
    for transaction in dataset:
        # freeze each subset
        for item in transaction:
            # convert to list, convert list to set, freeze set
            frozen = frozenset([item])
            # add/increment subset in dictionary
            one_item_set[frozen] = one_item_set.get(frozen, 0) + 1

    # prune 1-itemset items below minsup and add to infrequent set
    keys = list(one_item_set.keys())
    for item in keys:
        if one_item_set[item] / len(dataset) < minsup:
            last_infrequent.append(item)
            one_item_set.pop(item)
        else:
            # set itemset value to support instead of support count
            one_item_set[item] = one_item_set[item] / len(dataset)
    # list of all frequent n-itemsets, initialized with 1-itemset
    frequent_n_sets = [one_item_set]
    
    # if no more frequent n-itemsets can be produced, exit loop
    max_itemset = False
    # generate candidate n-itemsets
    while not max_itemset:
        candidate = {}
        infrequent = set()
        last_frequent = [set(x) for x in list(frequent_n_sets[-1])]
        # generate candidate n-itemsets
        for i in range(len(last_frequent)):
            for j in range(i,len(last_frequent)):
                test = last_frequent[i].union(last_frequent[j])
                if len(test) == len(last_frequent[i]) + 1:
                    candidate[frozenset(test)] = 0
        # prune sets with infrequent subsets, add to infrequent set
        keys = list(candidate.keys())
        for subset in keys:
            for item in last_infrequent:
                if item.issubset(subset):
                    infrequent.add(subset)
                    candidate.pop(subset)
                    break
        # count itemsets in dataset
        for transaction in dataset:
            # check if candidate itemset exists in transaction
            for subset in candidate:
                if subset.issubset(transaction):
                    # add/increment subset in candidate dictionary if it exists
                    candidate[subset] = candidate.get(subset, 0) + 1
        # prune sets below minsup, add to infrequent set
        keys = list(candidate.keys())
        for item in keys:
            if candidate[item] / len(dataset) < minsup:
                infrequent.add(item)
                candidate.pop(item)
            else:
                # set itemset value to support instead of support count
                candidate[item] = candidate[item] / len(dataset)
        if not len(candidate):
            max_itemset = True
        frequent_n_sets.append(candidate)
        last_infrequent = list(infrequent)
    return frequent_n_sets


def apriori_rules(minconf, minlift, itemsets):
    rules = []
    for itemset in itemsets:
        for subset in itemset:
            items = set(subset)
            for r in range(1,len(items)):
                combinations = itertools.combinations(items, r)
                for combination in combinations:
                    item = frozenset(combination)
                    antecedent = item
                    antecedent_sup = itemsets[len(antecedent)-1][antecedent]
                    consequent = frozenset(antecedent.symmetric_difference(items))
                    consequent_sup = itemsets[len(consequent)-1][consequent]
                    itemset_sup = itemsets[len(subset)-1][subset]
                    confidence = itemset_sup / antecedent_sup
                    lift = confidence / consequent_sup
                    # ensure conf(x->y) > minconf and lift(x->y) > minlift for good rule selection
                    if confidence >= minconf and lift >= minlift:
                        rules.append((len(subset), lift, confidence, itemset_sup, set(antecedent), set(consequent)))
    return rules

def apriori(minsup, minconf, minlift, filename):
    # generate frequent n-itemsets
    itemsets = apriori_itemsets(minsup, filename)
    # mine valid association rules
    rules = apriori_rules(minconf, minlift, itemsets)
    # sort rules by number of items, then lift, then conf, then support then the length of the consequent in descending order
    sorted_rules = sorted(rules, key=lambda x : (x[0], x[1], x[2], x[3], len(x[5])), reverse=True)
    return sorted_rules

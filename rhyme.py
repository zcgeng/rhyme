# -*- coding=UTF-8 -*-
import sys, os
import pickle
from pypinyin import Style, lazy_pinyin

cluster_strict = [[i] for i in range(22)]
# cluster_normal = [[0],[1,21],[2],[3],[4],[5,18],[6,7],[8],[9],[10,11],[12],[13],[14],[15],[7,16],[17,20],[19]]

def gen_groups(file_path='dict/group.txt'):
    groups = {}
    with open(file_path) as f:
        for line in f:
            l = line.strip().split(' ')
            groups[int(l[0])] = l[1:]
    return groups

def gen_clusters(groups, cluster_mapping):
    clusters = {}
    for i in range(len(cluster_mapping)):
        clusters[i] = []
        for g in cluster_mapping[i]:
            clusters[i] += groups[g]
    return clusters

def gen_index(clusters):
    index = {}
    for key in clusters:
        for value in clusters[key]:
            index[value] = key
    return index

def get_tags(rhyme_index, word):
    try:
        cluster_ids = [str(rhyme_index[i]) for i in lazy_pinyin(word)[::-1]]
        tag2 = '_'.join(cluster_ids[:2])
        if len(cluster_ids) > 2:
            tag3 = '_'.join(cluster_ids[:3])
            return [tag3,tag2]
        else:
            return [tag2]
    except Exception as e:
        print(word, e)
        return ''


def gen_dictionary(rhyme_index, words):
    dictionary = {}
    for w in words:
        tags = get_tags(rhyme_index, w)
        for tag in tags:
            if tag not in dictionary:
                dictionary[tag] = list()
            dictionary[tag].append(w)
    return dictionary

def init(filepath):
    print("词库初始化中...")
    words = []
    with open(filepath) as f:
        for line in f:
            words.append(line.strip())
    rhyme_dict = gen_dictionary(rhyme_index, words)
    with open('dict/rhyme_dict.pkl', 'wb') as f:
        pickle.dump(rhyme_dict, f)
    print("词库初始化完成")

if __name__ == '__main__':
    groups = gen_groups()
    clusters = gen_clusters(groups, cluster_strict)
    rhyme_index = gen_index(clusters)

    help_message = """Usage:
    python3 {} init /path/to/dictionary --  Generate the dictionary
    python3 {} get XXX  --  Get a rhyme
    """.format(sys.argv[0], sys.argv[0])

    if len(sys.argv) < 2:
        print(help_message)
        exit(0)

    if sys.argv[1] == 'init':
        filepath = ''
        if len(sys.argv) < 3:
            filepath = 'dict/30wdict_utf8.txt'
        else:
            filepath = sys.argv[2]
        init(filepath)

    elif sys.argv[1] == 'get':
        if not os.path.exists('dict/rhyme_dict.pkl'):
            init('dict/30wdict_utf8.txt')

        d = None
        with open('dict/rhyme_dict.pkl', 'rb') as f:
            d = pickle.load(f)
        word = sys.argv[2]
        print(word)
        tags = get_tags(rhyme_index,word)
        print(d[tags[0]])
    else:
        print(help_message)
        exit(0)

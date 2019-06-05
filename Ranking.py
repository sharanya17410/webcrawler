from sklearn.feature_extraction.text import TfidfVectorizer
from scipy import spatial
from sklearn.metrics.pairwise import cosine_similarity
from collections import OrderedDict
from itertools import islice
import numpy as np
import operator,re, math, json


def calculate_pt(word_array, reldoc, doc):
    pt = []
    for word in word_array:
        rel_pre = rel_abs = 0.0
        for document in reldoc:
            if word in doc[document]:
                rel_pre += 1
            else:
                rel_abs += 1
        rel_pre += 0.5
        rel_abs += 0.5
        pt.append(rel_pre / (rel_pre + rel_abs))
    return pt

def calculate_ut(word_array, reldoc, doc):
    ut = []
    for word in word_array:
        non_rel_pre = non_rel_abs = 0.0
        for document in list(set(doc) - set(reldoc)):
            if word in document:
                non_rel_pre += 1
            else:
                non_rel_abs += 1
        non_rel_pre += 0.5
        non_rel_abs += 0.5
        ut.append(non_rel_pre / (non_rel_pre + non_rel_abs))
    return ut

def calculate_ct(pt,ut):
    ct = []
    for i in range(len(pt)):
        ct.append(math.log(((pt[i] * (1 - ut[i])) / (ut[i] * (1 - pt[i])))))
    return ct

def calculate_rsv(ct,tf_array,doc):
    rsv = []
    tfrow = len(tf_array)
    tfcol = len(tf_array[0])
    for i in range(len(doc)):
        rsvval = 0
        for j in range(tfcol):
            if tf_array[tfrow - 1, j] > 0 and tf_array[i, j] > 0:
                rsvval += ct[j]
        rsv.append(rsvval)
    return rsv


def print_result(rsv, doc):
    final_mydic = {}
    for idx, i in enumerate(doc):
        final_mydic.update({i.split(':-')[0]: rsv[idx]})
    d_descending = OrderedDict(sorted(final_mydic.items(), key=operator.itemgetter(1), reverse=True))
    count = 1
    for key, value in d_descending.items():
        if count > 8:
            break
        if value > 0 and key != ("=> " + search_query):
            print(count, value, key)
            count +=1

if __name__ == "__main__":
    vect = TfidfVectorizer(min_df=1)
    file = open(r'E:\desktop\iirpackage\bookdetails.json')
    data = json.load(file)
    doc = []
    for idx, i in enumerate(data['Books']):
        doc.append(i['Name'] + ":-" + i['Description'])
    search_query = input("Enter Query : ")
    doc.append( "=> " + search_query)
    tfidf = vect.fit_transform(doc)
    weights = (tfidf * tfidf.T).A
    dist = cosine_similarity(weights)
    cos_sim = np.round(dist, 4)
    mydic = {}
    for idx,i in enumerate(doc):
        mydic.update({idx: cos_sim[len(cos_sim) - 1, idx]})
    sorted_mydic = sorted(mydic.items(), key=operator.itemgetter(1), reverse=True)
    top_k_doc = 6
    reldoc = [ i[0] for i in islice(sorted_mydic, top_k_doc)]
    del reldoc[0]
    tf_array = tfidf.toarray()
    word_array = vect.get_feature_names()
    ut = calculate_ut(word_array,reldoc,doc)
    pt = calculate_pt(word_array,reldoc,doc)
    ct = calculate_ct(pt,ut)
    rsv = calculate_rsv(ct,tf_array,doc)
    print_result(rsv,doc)

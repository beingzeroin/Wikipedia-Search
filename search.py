import math
import Stemmer
import bisect
import operator
import re
import time

stem = Stemmer.Stemmer('english')

files_type = ['index/secondary_title', 'index/secondary_body', 'index/secondary_info', 'index/secondary_ext', 'index/secondary_ref', 'index/secondary_cat']

stop_words = []
f = open('stopwords_list.txt', 'r')
for line in f.readlines():
    line = line.split('\n')[0]
    stop_words.append(line)
stop_words = set(stop_words)

details = open('index/details', 'r')

counts = details.readline().strip('\n').split(';')
sec_counts = {}
i = 0
for i in range(6):
    sec_counts[i] = counts[i]
    i += 1

total_count = int(details.readline().strip('\n'))

document_names = {}
f = open("titles_list", "r")
for line in f.readlines():
    if ':' in line:
        document_names[line.split(':')[0]] = line.split(':')[1].strip('\n')

sec_index = [[], [], [], [], [], []]
for i in range(6):
    path = files_type[i]
    f = open(path, "r")
    for line in f.readlines():
        sec_index[i].append(line.strip('\n'))

queries = input("$ Number of queries:")
print
for i in range(queries):

    ranked_docs = {}
    
    inp = raw_input("Enter search query:")
    tim = time.time()
    query = []
    fields = {}
    if ':' in inp:   #Field queries
        f = inp.split(',')
        for i in f:
            words = i.split(':')[1].lower()
            words = words.split(' ')
            for w in words:
                word = stem.stemWord(w)
                fields[word] = [0 for x in range(6)]
                field = i.split(':')[0]
                if field == 't':
                    fields[word][0] = 1
                elif field == 'b':
                    fields[word][1] = 1
                elif field == 'i':
                    fields[word][2] = 1
                elif field == 'e':
                    fields[word][3] = 1
                elif field == 'r':
                    fields[word][4] = 1
                else:
                    fields[word][5] = 1
                query.append(word)
    else:
        query = [s.strip() for s in re.findall('\d+|[A-Za-z]+', inp.lower())]

        for word in query:
            if len(word) == 1:
                try:
                    float(word)
                except ValueError:
                    query.remove(word)
        query = [stem.stemWord(s) for s in query if s not in stop_words]
        for word in query:
            fields[word] = [1 for i in range(6)]

    
    for word in query:
        for i in range(6):

            if fields[word][i] == 0:
                continue
             
            idx = bisect.bisect(sec_index[i], word)
            if idx == sec_counts[i]:
                continue
            
            if word == sec_index[i][idx-1]:
                path = "index/primary_" + files_type[i].split('/')[1].split('_')[1] + '_' + str(idx)
            else:
                path = "index/primary_" + files_type[i].split('/')[1].split('_')[1] + '_' + str(idx+1)
            
            f = open(path, "r")
            for line in f.readlines():
                if line.split('--')[0].split(':')[0] == word:
                    line = line.strip('\n')
                    doc_count = int(line.split('--')[0].split(':')[1])
                     
                    if int(total_count/doc_count) >= 45:
                        postings = line.split('--')[1].split(';')
                        
                        temp = []
                        for post in postings:
                            if len(post) > 0:
                                temp.append((post.split(':')[0], int(post.split(':')[1])))
                        
                        idf_num = float(total_count - doc_count + 0.5)
                        idf_den = float(doc_count + 0.5)
                        idf = float(math.log(float(idf_num/idf_den)))

                        for j in range(min(5000, doc_count)):
                            try: 
                                tf = float(temp[j][1])
                            except IndexError:
                                break
                            
                            score = 0
                            for word in query:
                                num = float(tf * 2.6)
                                den = float(tf + 1.6)
                                score += float(idf * float(num/den))

                            if i == 0:    #Different weights for different fields
                                score = score*(2 ** 8)
                            elif i == 1:
                                score = score*(2 ** 2)
                            elif i == 2:
                                score = score*(2 ** 4)
                            elif i == 3:
                                score = score*(2 ** 3)
                            elif i == 4:
                                score = score*(2 ** 1)
                            elif i == 5:
                                score = score*(2 ** 4)


                            if (document_names[temp[j][0]] == "Wikipedia" and word != "Wikipedia") or (document_names[temp[j][0]] == "Category" and word != "Category") or (document_names[temp[j][0]] == "File" and word != "File") or (document_names[temp[j][0]] == "Template" and word != "Template") or (document_names[temp[j][0]] == "Portal" and word != "Portal"):
                                continue

                            if temp[j][0] in ranked_docs:
                                ranked_docs[temp[j][0]] += score
                            else:
                                ranked_docs[temp[j][0]] = score
                    break
        
    ranked_docs = sorted(ranked_docs.items(), key=operator.itemgetter(1), reverse=True)  #Sort docs based on score

    if len(ranked_docs) == 0:
        print "No documents retrieved\n"
        continue

    ct = 0
    print
    for i in ranked_docs:
        if ct == 10:
            break

        doc_id = int(i[0], 0)
        doc_name = document_names[i[0]]
        score = i[1]
 
        print str(doc_id), ",", doc_name, ",", str(score)
        ct += 1
    end = time.time()
    print"\nTime taken: " ,  str(end - tim), "s\n"

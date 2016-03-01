import xml.sax
import re
import Stemmer
import sys
import os

titles = open("titles_list", "w")
index_title = open("index/title_1", "w")
index_body = open("index/body_1", "w")
index_info = open("index/info_1", "w")
index_ref = open("index/ref_1", "w")
index_ext = open("index/ext_1", "w")
index_cat = open("index/cat_1", "w")

title = {}
body = {}
info = {}
ref = {}
ext = {}
cat = {}

stop_words = []

doc_count = 1
file_no = 1
total_count = 0

class Wiki_Handler(xml.sax.ContentHandler):

    def __init__(self):

        xml.sax.ContentHandler.__init__(self)
        self.elements = []
        self.current = ""
        self.parent = ""
        self.content = ""
    
    def startElement(self, name, attrs):

        self.elements.append(name)
        if self.current is not None:
            self.parent = self.current
        self.current = name

    def endElement(self, name):
        
        global index_title
        global index_body
        global index_info
        global index_ref
        global index_ext
        global index_cat

        global title
        global body
        global info
        global ref
        global ext
        global cat

        global doc_count
        global file_no
        global total_count
        global title_count

        if name == "page":
            total_count += 1
                
            if doc_count == 2000: #Maximum number of docs per file

                for i in sorted(title.keys()):
                    s = i + ':' + title[i] + '\n'
                    index_title.write(s)
                for i in sorted(info.keys()):
                    s = i + ':' + info[i] + '\n'
                    index_info.write(s)
                for i in sorted(ref.keys()):
                    s = i + ':' + ref[i] + '\n'
                    index_ref.write(s)
                for i in sorted(ext.keys()):
                    s = i + ':' + ext[i] + '\n'
                    index_ext.write(s)
                for i in sorted(cat.keys()):
                    s = i + ':' + cat[i] + '\n'
                    index_cat.write(s)
                for i in sorted(body.keys()):
                    s = i + ':' + body[i] + '\n'
                    index_body.write(s)
            
                doc_count = 0

                title.clear()
                body.clear()
                info.clear()
                ref.clear()
                ext.clear()
                cat.clear()
            
                index_title.close()
                index_body.close()
                index_info.close()
                index_ref.close()
                index_ext.close()
                index_cat.close()

            if doc_count == 0:
                file_no += 1
                t = "index/title_" + str(file_no)
                b = "index/body_" + str(file_no)
                i = "index/info_" + str(file_no)
                r = "index/ref_" + str(file_no)
                e = "index/ext_" + str(file_no)
                c = "index/cat_" + str(file_no)
                index_title = open(t, "w")
                index_body = open(b, "w")
                index_info = open(i, "w")
                index_ref = open(r, "w")
                index_cat = open(c, "w")
                index_ext = open(e, "w")
        
            doc_count += 1
            print total_count

        elif name == "title":
            self.title = self.content
            self.title = re.sub('amp;', '', self.title)
            self.title = re.sub('&quot;', '', self.title)

        elif name == "id" and self.parent == "page":
            self.doc_id = re.sub('\n', '', self.content)
            titles.write(hex(int(self.doc_id)) + ":" + self.title)

        elif name == "text":
            self.text = self.content
            self.parse()
            self.make_index()
    
        self.elements.pop()
        if self.elements:
            self.current = self.parent
            if len(self.elements) == 1:
                self.parent = ""
        else:
            self.current = ""
        self.content = ""
            
    def make_index(self):

        doc_id = int(self.doc_id)
        
        word_list = set(self.info)
        for word in word_list:
            if word not in info:
                info[word] = "1--" + str(hex(doc_id)) + ":" + str(self.info.count(word)) + ";"
            else:
                l = len(str(info[word].split('--')[0]))
                count = int(info[word].split('--')[0]) + 1
                temp = info[word][l:]
                info[word] = str(count) + temp + str(hex(doc_id)) + ":" + str(self.info.count(word)) + ";"

        word_list = set(self.body)
        for word in word_list:
            if word not in body:
                body[word] = "1--" + str(hex(doc_id)) + ":" + str(self.body.count(word)) + ";"
            else:
                l = len(str(body[word].split('--')[0]))
                count = int(body[word].split('--')[0]) + 1
                temp = body[word][l:]
                body[word] = str(count) + temp + str(hex(doc_id)) + ":" + str(self.body.count(word)) + ";"

        word_list = set(self.ref)
        for word in word_list:
            if word not in ref:
                ref[word] = "1--" + str(hex(doc_id)) + ":" + str(self.ref.count(word)) + ";"
            else:
                l = len(str(ref[word].split('--')[0]))
                count = int(ref[word].split('--')[0]) + 1
                temp = ref[word][l:]
                ref[word] = str(count) + temp + str(hex(doc_id)) + ":" + str(self.ref.count(word)) + ";"

        word_list = set(self.ext)
        for word in word_list:
            if word not in ext:
                ext[word] = "1--" + str(hex(doc_id)) + ":" + str(self.ext.count(word)) + ";"
            else:
                l = len(str(ext[word].split('--')[0]))
                count = int(ext[word].split('--')[0]) + 1
                temp = ext[word][l:]
                ext[word] = str(count) + temp + str(hex(doc_id)) + ":" + str(self.ext.count(word)) + ";"

        word_list = set(self.cat)
        for word in word_list:
            if word not in cat:
                cat[word] = "1--" + str(hex(doc_id)) + ":" + str(self.cat.count(word)) + ";"
            else:
                l = len(str(cat[word].split('--')[0]))
                count = int(cat[word].split('--')[0]) + 1
                temp = cat[word][l:]
                cat[word] = str(count) + temp + str(hex(doc_id)) + ":" + str(self.cat.count(word)) + ";"

        word_list = set(self.title)
        for word in word_list:
            if word not in title:
                title[word] = "1--" + str(hex(doc_id)) + ":" + str(self.title.count(word)) + ";"
            else:
                l = len(str(title[word].split('--')[0]))
                count = int(title[word].split('--')[0]) + 1
                temp = title[word][l:]
                title[word] = str(count) + temp + str(hex(doc_id)) + ":" + str(self.title.count(word)) + ";"

    def parse(self):

        global stop_words

        self.info = ""
        self.body = ""
        self.ref = ""
        self.ext = ""
        self.cat = ""
        
        lines = self.text.split('\n')
        flag = 0

        for line in lines:

            if "{{Infobox" in line or "{{ Infobox" in line:
                flag = 1

            elif "==Reference" in line or "== Reference" in line:
                flag = 2

            elif "==External" in line or "== External" in line:
                flag = 3
           
            elif "[[Category" in line:
                flag = 4

            elif flag == 4:
                break

            elif line.find("==") == 0:
                flag = 5

            if flag == 1:
                self.info += line + "\n"
                if "}}" in line:
                    flag = 5
            elif flag == 2:
                self.ref += line + "\n"
            elif flag == 3:
                self.ext += line + "\n"
            elif flag == 4:
                c = line.split(":")
                try:
                    self.cat += c[1][:-2].strip() + "\n"
                except:
                    pass
            elif flag == 5:
                self.body += line + "\n"
        
        stem = Stemmer.Stemmer('english')
        
        regex = '\d+|[A-Za-z]+'

        parse_info = [s.strip() for s in re.findall(regex, self.info.lower()) if len(s)>0]
        self.info = []
        for s in parse_info:
            s = stem.stemWord(s)
            if s not in stop_words:
                self.info.append(s)

        parse_body = [s.strip() for s in re.findall(regex, self.body.lower()) if len(s)>0]
        self.body = []
        for s in parse_body:
            s = stem.stemWord(s)
            if s not in stop_words:
                self.body.append(s)

        parse_ref = [s.strip() for s in re.findall(regex, self.ref.lower()) if len(s)>0]
        self.ref = []
        for s in parse_ref:
            s = stem.stemWord(s)
            if s not in stop_words:
                self.ref.append(s)

        parse_ext = [s.strip() for s in re.findall(regex, self.ext.lower()) if len(s)>0]
        self.ext = []
        for s in parse_ext:
            s = stem.stemWord(s)
            if s not in stop_words:
                self.ext.append(s)

        parse_cat = [s.strip() for s in re.findall(regex, self.cat.lower()) if len(s)>0]
        self.cat = []
        for s in parse_cat:
            s = stem.stemWord(s)
            if s not in stop_words:
                self.cat.append(s)

        parse_title = [s.strip() for s in re.findall(regex, self.title.lower()) if len(s)>0]
        self.title = []
        for s in parse_title:
            s = stem.stemWord(s)
            if s not in stop_words:
                self.title.append(s)


    def characters(self, content):

        unicode_string = content.encode("utf-8").strip()
        if unicode_string:
            self.content += unicode_string + '\n'

def merge_files():

    global file_no
    global total_count

    files_type = ['index/title_', 'index/body_', 'index/info_', 'index/ext_', 'index/ref_', 'index/cat_']
    divide_files = ""
    file_count = 0

    for files in files_type:

        if file_count != 0:
            divide_files += str(file_count) + ';'
            s.write(index.split(':')[0] + '\n')

        idx_count = 0
        file_count = 1
        ct = 0
        file_ptr = [0]*file_no
        line = [0]*file_no
        for i in range(file_no):
            f = files + str(i+1)
            file_ptr[i] = open(f, "r")
            line[i] = file_ptr[i].readline().split('\n')[0]
        
        prim = "index/primary_" + files.split('/')[1] + str(file_count)
        sec = "index/secondary_" + files.split('/')[1][:-1]
        s = open(sec, "w")
        f = open(prim, "w")
        subl = []

        while ct != file_no:
            idx = []
            for i in range(file_no):
                if i not in subl:
                    idx.append((line[i].split(':')[0], i))
            idx.sort()

            a = []
            a.append(idx[0][1])
            for i in range(1, len(idx)):
                if idx[i][0] == idx[0][0]:
                    a.append(idx[i][1])
                else:
                    break;
            
            posting_count = 0
            for i in a:
                try:
                    posting_count += int(line[i].split(':')[1].split('--')[0])
                except IndexError:
                    continue
            
            index = idx[0][0] + ':' + str(posting_count) + '--'
            for i in a:
                if len(line[i]) > 0:
                    temp = line[i].split('--')[1]
                    index += temp
            index += '\n'
            
            temp = []
            parsed = index.split('--')[1].split(';')[:-1]
            for item in parsed:
               temp.append((int(item.split(':')[1]), item.split(':')[0]))
            temp = sorted(temp, reverse=True)

            index = index.split('--')[0] + '--'
            for item in temp:
                index += item[1] + ':' + str(item[0]) + ';'
            index += '\n'
            
            f.write(index)
            idx_count += 1

            if idx_count == 3000:  #Index limit per file
                idx_count = 0
                file_count += 1
                prim = "index/primary_" + files.split('/')[1] + str(file_count)
                f.close()
                f = open(prim, "w")
                s.write(index.split(':')[0] + '\n')
            
            for i in a:
                line[i] = file_ptr[i].readline().split('\n')[0]
                if line[i] == "":
                    ct += 1
                    subl.append(i)

    if file_count != 0:
        divide_files += str(file_count) + ';'
        s.write(index.split(':')[0] + '\n')
    
    for i in range(file_no):
        file_ptr[i].close()
    f.close()
    s.close()

    for files in files_type:
        for i in range(1, file_no+1):
            path = files + str(i)
            os.remove(path)

    details = open("index/details", "w")
    details.write(divide_files.strip(':') + '\n')
    details.write(str(total_count) + '\n')

def main(dump_file):

    global stop_words

    global index_title
    global index_body
    global index_info
    global index_ref
    global index_ext
    global index_cat

    global title
    global body
    global info
    global ref
    global ext
    global cat

    global file_no

    f = open("stopwords_list.txt", "r")
    for lines in f.readlines():
        line = lines.split('\n')[0]
        stop_words.append(line)
    stop_words = set(stop_words)

    data = open(dump_file)
    xml.sax.parse(data, Wiki_Handler())

    
    for i in sorted(title.keys()):
        s = i + ':' + title[i] + '\n'
        index_title.write(s)

    for i in sorted(info.keys()):
        s = i + ':' + info[i] + '\n'
        index_info.write(s)

    for i in sorted(ref.keys()):
        s = i + ':' + ref[i] + '\n'
        index_ref.write(s)

    for i in sorted(ext.keys()):
        s = i + ':' + ext[i] + '\n'
        index_ext.write(s)

    for i in sorted(cat.keys()):
        s = i + ':' + cat[i] + '\n'
        index_cat.write(s)

    for i in sorted(body.keys()):
        s = i + ':' + body[i] + '\n'
        index_body.write(s)

    
    title.clear()
    body.clear()
    info.clear()
    ref.clear()
    ext.clear()
    cat.clear()
    
    index_title.close()
    index_body.close()
    index_info.close()
    index_ref.close()
    index_ext.close()
    index_cat.close()

    merge_files()

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print "Usage: python index.py <name_of_dump>"
        sys.exit()

    main(sys.argv[1])

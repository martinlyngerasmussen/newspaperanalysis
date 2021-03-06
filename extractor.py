
import os
import json
import re
from helps import ParallelBucket


def list_folder(path):
    if os.path.isdir(path):
        for fname in os.listdir(path):
            yield path+'/'+fname
    else:
        print(path), ' is not a folder !!'

def process_file(_file, output_folder):
    def nonblank_lines(f):
        for l in f:
            line = l.rstrip()
            if line:
                yield line

    output = open(output_folder+os.path.split(_file)[1].split('.')[0]+'.json', 'w')
    with open(_file, encoding="ISO-8859-1") as _f:
        article = {}
        f = nonblank_lines(_f)
        for line in f:
            if re.search(r"Document ", line):
                article['title'] = next(f).strip()
                line = next(f).strip()
                
            if re.search(r"words", line):
                article['date'] = next(f).strip()
                line = next(f).strip()
                
               
                line = next(f).strip()
                line = next(f).strip()
                line = next(f).strip()
                line = next(f).strip()
                line = next(f).strip()                
            
                
                text = ''
                while not re.search(r"FIN", line):
                    text += line+' ' # add the next line to the text, basically concatenate
                    line = next(f).strip().replace('\"', '')
                    
                article['body'] = text
                output.write(json.dumps(article)+'\n')

def main():
    articles = []
    input_folder = './data/input/'
    output_folder = './data/output/'

    bucket = ParallelBucket()
    for _file in list_folder(input_folder):
        print("Processing file ", _file, '.....')
        #process_file(_file, output_folder)
        #exit()
        bucket.add_job(process_file, args=(_file, output_folder))
    bucket.joinall()


if __name__ == '__main__':
    main()

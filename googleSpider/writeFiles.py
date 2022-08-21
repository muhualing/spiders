from MySQLProvider import results
import os

lines = ['\t'.join(result) for result in results]

file_path = os.path.join(os.getcwd(),"urls.txt")
with open(file_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
    # f.writelines(result[0] + "\t" + result[1] + "\t" + result[2])
    # file1 = open(file_path, 'r', encoding='utf-8')
    # Lines = file1.readlines()

    # count = 0
    # queries = []
    # for line in Lines:
    #     count += 1
    #     queries.append(line.split('\t')[0])
    # return queries[start:]    
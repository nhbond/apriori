import time
from apriori import apriori

# set source and destination file names
#   source is a csv file of itemsets
#   destination is the file to write the mined rules
source = 'src/testset.csv'
destination = 'dst/rules.txt'

# measure runtime
start = time.time() # start timer
# support = 0.15, confidence = 0.80, lift = 1.00
rules = apriori(0.15, 0.80, 1.00, source)
end = time.time() # stop timer
print(f'\033[1mruntime:\033[0m {round((end-start),2)}s')

# write rules to file
with open(destination, 'w') as f:
    for rule in rules:
      f.write(f'{rule[4]}  ⇒  {rule[5]}\t||\tRule Specs: len={rule[0]}, lift={round(rule[1],2)}, conf={round(rule[2],2)}, sup={round(rule[3],2)}\n')
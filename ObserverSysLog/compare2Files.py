"""
with open('f1.txt', 'r') as file1:
    with open('f2.txt', 'r') as file2:
        same = set(file1).intersection(file2)

same.discard('\n')

with open('some_output_file.txt', 'w') as file_out:
    for line in same:
        file_out.write(line)
"""
import difflib, sys
# accoun Tri
#./rippled submit sh1LrEHjJyMGi9JLUHeyvKKAGSuRL '{"Account" : "rBor3Awo22JCTB21gJejAyHZhQBXq7c29N", "TransactionType" : "LogTransaction", "TransactionContent" :  "tri dep trai"}'
secretAcc = 'sh1LrEHjJyMGi9JLUHeyvKKAGSuRL'
accID = 'rBor3Awo22JCTB21gJejAyHZhQBXq7c29N'


with open('f1.txt','r') as f1, open('f2.txt','r') as f2:
    diff = difflib.ndiff(f1.readlines(),f2.readlines())    
    for line in diff:
#        if line.startswith('-'):
#            sys.stdout.write(line)
#        elif line.startswith('+'):
#            sys.stdout.write('\t\t'+line)  
	if line.startswith('+'):
		line = line[2:len(line)-1]
		sys.stdout.write(line)
		msg = './rippled submit ' + secretAcc + '{"Account" : "' + accID + '", "TransactionType" : "LogTransaction", "TransactionContent" :  "' + line + '"}\''
		print msg

import re

def read_vf_file(file_name): 
    with open(file_name, 'r') as file: 
        vf_data = file.read()

    return vf_data

def extract_vf_identity(vf_data): 
    protein_identity = []
    r=re.findall('(Query.*?\n)Matrix',vf_data,re.DOTALL)
    for k in r:
        protein_identity.append(k)

    return protein_identity

def main(): 
    record=[]
    
    vf_file_path = input("Enter Your text file:  ")
    vf_data = read_vf_file(vf_file_path)

    matched = extract_vf_identity(vf_data)

    for score_data in matched:
        
        score= re.finditer('Score* = *([1-9]\d*(\.\d+)?) bits* \(([^)]+)\)',score_data)
        identity=re.finditer('Identities* = [-+]?[0-9]+/[-+]?[0-9]+ \(([^)]+)\)',score_data)
        #name=re.finditer('>VFG*([0-9][0-9][0-9][0-9][0-9][0-9]) \(([^)]+)\)',score_data)
        
        pname=list(re.finditer(r'Query= core.*\_Gene[0-9]\d*(\.\d+)?\n',score_data))
        
        for i,j in zip(score,identity):
           i=i.group(3)
           j=j.group(1).strip("%")
           #k=k.group() 
           if int(i) >= 100 and int(j) >= 30 :
               record.append(pname[0].group())
    
    with open("Filter_protein.txt","w") as f:
        for line in record:
            f.write(line)

    lines_seen = set() 
    outfile = open('output.csv', "w")
    infile = open('Filter_protein.txt', "r")

    for line in infile:
        if line not in lines_seen: 
            outfile.write(line)
            lines_seen.add(line)
    outfile.close()

    
if __name__ == '__main__': 
    main()
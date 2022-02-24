#TDB Practical Assignment 1
#Python Code to Detect if a schedule is Conflict Serializable

from get_graph import Graph

try:
    #function definition to identify if two instructions are conflicting
    def isConflicting(instruction_1, instruction_2):
        if instruction_1 == "____" or instruction_2 == "____":
            return False
        op1, op2 = instruction_1[0], instruction_2[0]
        data_1, data_2 = instruction_1[2], instruction_2[2]
        if data_1 == data_2:
            if op1 == 'W' or op2 =='W':
                return True
        else:
            return False

    #get input file
    input_file = input("Enter file:")

    #get number of transactions from input file
    with open(input_file) as f:
        no_of_transactions = int(f.readline())

    #make 2-D array of lists for different transactions
    ls = [[] for _ in range(no_of_transactions)]

    #populate these lists
    with open(input_file) as f:
        #skip first line
        for _ in range(1):
            temp = f.readline()
        line = f.readline()
        while line:
            data = line.split(":")
            transaction_no = int(data[0][1])
            count = 0
            for i in range(len(ls)):
                if i == (transaction_no - 1):
                    ls[i].append(data[1][:-2])
                else:
                    ls[i].append("____")
            line = f.readline()

    #print the schedule
    print("------------------- SCHEDULE : -------------------")
    for list_ in ls:
        print(list_)

    #create a directed graph
    g = Graph(no_of_transactions)

    #get length of transactions
    L = len(ls[0])
    for transaction_id in range(no_of_transactions):
        for i in range(L):
            instruction = ls[transaction_id][i]
            for j in range(no_of_transactions):
                if j == transaction_id:
                    continue
                else:
                    for k in range(i + 1, L):
                        if isConflicting(instruction, ls[j][k]):
                            g.addEdge(transaction_id, j)

    print("\n------------------- RESULT: -------------------")
    if g.isCyclic():
        print("Given schedule is NOT CONFLICT SERIALIZABLE")
    else:
        print("Given schedule is CONFLICT SERIALIZABLE")

except:
    print("Error!")
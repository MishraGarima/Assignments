input_log = []
def read_log():
    input_file = input("Enter file:")
    with open(input_file) as f:
        line = f.readline()
        while line:
            #print(line)
            input_log.append(line.strip())
            line = f.readline()

def display_table(table_list):
    width = 110
    temp = 0
    for row_ in table_list:
        if temp<2:
            print("-" * width)
            temp = temp + 1
        print("|", end='')
        for ele in row_:
            print(f" {ele}".ljust(18) + "|", end="")
        print()

    print("Number of commit operations are:", no_of_commits)
    print("Redo transactions are:", " ".join(RedoT))
    print("Undo transactions are:", " ".join(UndoT))


#print("--    ARIES Analysis table  -- ")
#print("Type it in format like this without barckets  -->>>     write_item,T1,D,20")
#print("At the end for system crash type : crash")

lines = []
read_log()
for line in input_log:
    l = list(list(map(str,line.split(","))))
    if line != ['crash']:
        lines.append(l)
    else:
        break

transaction_table = [["Lsn_no", "Last_no", "Trans_id", "Type", "Page_id"]]
dict = {}
lsn_no = 1
last_no = 0
no_of_commits = 0
checkpointreached = 0  # not reached checkpoint as yet
beforecheckpointcommitedT = []
RedoT = []
UndoT = []

#work on each transaction
for trans in lines:

    # write/update
    if len(trans) == 4:
        # print("write")
        # lets get the last_no  by[-1]
        if (dict.get(trans[1])) != None:
            last_no = (dict.get(trans[1]))[-1]
        else:
            # print ("N")
            last_no = 0
        # now letts append the lsn_no and we have the lsn_no
        dict.setdefault(trans[1], []).append(lsn_no)

        # now lets append to the transaction_table
        transaction_table.append([lsn_no, last_no, trans[1], trans[0], trans[2]])
        lsn_no += 1

        if checkpointreached == 1 and (trans[1] not in UndoT):
            UndoT.append(trans[1])

    # commit
    if len(trans) == 2 and trans[0] != "start_transaction":

        if (dict.get(trans[1])) != None:
            last_no = (dict.get(trans[1]))[-1]
        else:
            last_no = 0
        dict.setdefault(trans[1], []).append("C")
        transaction_table.append([lsn_no, last_no, trans[1], trans[0], "-"])
        lsn_no += 1
        no_of_commits += 1

        if checkpointreached == 0:
            beforecheckpointcommitedT.append(trans[1])
        else:
            RedoT.append(trans[1])
            UndoT.remove(trans[1])

    # system crash
    if len(trans) == 1 and trans[0] == "checkpoint":
        transaction_table.append([lsn_no, " ", " ", "Checkpoint", " "])
        lsn_no += 1
        checkpointreached = 1

display_table(transaction_table)
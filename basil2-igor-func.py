def igor_out(values) : 
    '''
    Takes in the values of each gate from some output. This needs to be turned into an array. 
    WARNING! This is specific to Basil2 device in 2019-DEC bonding scheme (no c8 used). 
    Prints out the setdqd() function to be pasted into IGOR window. 
    Also prints the do2d function for a 50mv window around the centre of c5, c9
    '''
    gates = ["c2", "c3", "c4", "c5", "c6", "c7", "c9"] 
    print("function setdqd()")
    for gate, value in zip(gates, values):
        print("setval(\"" + gate + "\", ", value,")")
    print("end\n")
    c5 = values[3]
    c9 = values[6]
    print("c5 start at {} and end at {}".format(c5 + 25, c5 - 25))
    print("c9 start at {} and end at {}\n".format(c9 + 25, c9 - 25))
    print("do2d(\"c5\", {}, {}, 50, 0, \"c9\", {}, {}, 50, 0)".format(c5 + 25, c5 - 25, c9 + 25, c9 - 25))

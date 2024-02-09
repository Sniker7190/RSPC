import sys, re, time, json

print(sys.argv)

INSTS = [
    "RST",
    "RTV",
    "ADD",
    "SUB",
    "MUL",
    "AND",
    "OR",
    "XOR",
    "PLO",
    "PLI",
    "FLO",
    "FLI",
    "JMP",
    "JMN"
]

ONE = [
    "PLI",
    "FLI",
    "PLO",
    "FLO",
    "JMP"
]

def Close():
    for g in range(10):
        print("[WARNING] Closing in " + str(10 - g))
        time.sleep(1)

def BinInt(INTC):
    Int = INTC + 1
    O = ""
    if Int > 64:
        O = O + "1"
        Int = Int - 64
    else:
        O = O + '0'
    if Int > 32:
        O = O + "1"
        Int = Int - 32
    else:
        O = O + '0'
    if Int > 16:
        O = O + "1"
        Int = Int - 16
    else:
        O = O + '0'
    if Int > 8:
        O = O + "1"
        Int = Int - 8
    else:
        O = O + '0'
    if Int > 4:
        O = O + "1"
        Int = Int - 4
    else:
        O = O + '0'
    if Int > 2:
        O = O + "1"
        Int = Int - 2
    else:
        O = O + '0'
    if Int > 1:
        O = O + "1"
        Int = Int - 1
    else:
        O = O + "0"
    return O

def GetItemInList(Find, List):
    for i in range(len(List)):
        if List[i] == Find:
            return(i)

def CommandCompiler(Asm):
    SOC = 'summon falling_block ~1 ~3 ~1 {"BlockState":{"Name":"redstone_block"},"Passengers":[{"id":"falling_block","BlockState":{"Name":"activator_rail"},"Passengers":[{"id":"armor_stand","Health":0,"Passengers":['
    END = ']}]}]}'
    FINAL = SOC
    YVAL = " 7 "
    BINS = []
    Asm = Asm.split("\n")
    for a in range(len(Asm)):
        asmp = Asm[a].split(" ")
        try:
            BINS.append(BinInt(int(GetItemInList(asmp[0], INSTS) + 1) + 64))
            if GetItemInList(asmp[0], ONE) == None:
                BINS.append(BinInt(int(asmp[1])))
                BINS.append(BinInt(int(asmp[2])))
            else:
                BINS.append(BinInt(int(asmp[1])))
        except:
            x = 0
    for m in range(len(BINS)):
        for n in range(len(BINS[m])):
            if n != 0 or m != 0:
                FINAL = FINAL + ","
            if BINS[m][n] == "1":
                bl = ' redstone_block"}'
            else:
                bl = ' stone"}'
            FINAL = FINAL + '{"id":"command_block_minecart","Command":"setblock ' + str(n * 2) + YVAL + str(m * 4) + bl
    FINAL = FINAL + END
    try:
        i = open("command.txt", "x")
        i.write(FINAL)
        i.close()
    except:
        i = open("command.txt", "w")
        i.write(FINAL)
        i.close()
    print("[INFO] Compiled correctly! Length of command is " + str(len(FINAL)))
    Close()

def BinCompiler(ASM):
    BIN = ""
    asm = ASM.split("\n")
    for a in range(len(asm) - 1):
        asmp = asm[a].split(" ")
        BIN = BIN + chr(GetItemInList(asmp[0], INSTS) + 64)
        if GetItemInList(asmp[0], ONE) == None:
            BIN = BIN + chr(int(asmp[1]))
            BIN = BIN + chr(int(asmp[2]))
        else:
            BIN = BIN + chr(int(asmp[1]))
    
    try:
        i = open("prog.bin", "x")
        i.write(BIN)
        i.close()
    except:
        i = open("prog.bin", "w")
        i.write(BIN)
        i.close()
    time.sleep(0.6)
    print("[INFO] Binary compiling complete. Now writing minecraft command.")
    CommandCompiler(ASM)


def ParseTokens(TokensJson):
    OUT = ""
    JS = json.loads(TokensJson)
    VARS = []
    VAR_ALLOCATION = []
    for c in range(len(JS)):
        for d in range(len(JS[c])):
            try:
                if JS[c][d]["keyword"] == "var":
                    VARS.append(JS[c][d + 1]["var_name"])
                    VAR_ALLOCATION.append(len(VAR_ALLOCATION) + 1)
                    OUT = OUT + "RST " + str(len(VAR_ALLOCATION)) + " " + str(JS[c][3]["value"]) + "\n"
                if JS[c][d]["keyword"] == "plout":
                    OUT = OUT + "PLO " + str(GetItemInList(JS[c][d + 1]["var_name"], VARS) + 1) + "\n"
            except:
                x = 1
        try:
            Opa = ""
            if JS[c][1]["oparator"] == "+=":
                Opa = "ADD "
            if JS[c][1]["oparator"] == "-=":
                Opa = "SUB "
            if JS[c][1]["oparator"] == "==":
                Opa = "RTV "
            if JS[c][1]["oparator"] == "=":
                Opa = "RST "
            if JS[c][1]["oparator"] == "*=":
                Opa = "MUL "
            VarInd = GetItemInList(JS[c][0]["var_use"], VARS)
            VarInd += 1
            if not Opa == "RST ":
                VarInd1 = GetItemInList(JS[c][2]["value"], VARS)
                VarInd1 += 1
            else:
                VarInd1 = int(JS[c][2]["value"])
            OUT = OUT + Opa + str(VarInd) + " " + str(VarInd1) + "\n"
        except:
            x1 = 1

    try:
        i = open("inst.txt", "x")
        i.close()
    except:
        i = open("inst.txt", "w")
        i.write(OUT)
        i.close()
    time.sleep(0.6)
    print("[INFO] Tokens have been parsed. Compiled to assembly. Now compiling to binary.")
    BinCompiler(OUT)

def Tokenize(lines):
    VARS = []
    TOKENED = "["
    for a in range(len(lines)):
        ls = lines[a].split(" ")
        if ls[0] == "var":
            if not a == 0:
                TOKENED = TOKENED + ","
            TOKENED = TOKENED + '[{"keyword":"var"}'
            TOKENED = TOKENED + ',{"var_name":"'+ ls[1] + '"}'
            TOKENED = TOKENED + ',{"oparator":"'+ ls[2] + '"}'
            TOKENED = TOKENED + ',{"value":"'+ ls[3] + '"}]'
            VARS.append(ls[1])
        if ls[0] == "plout":
            if not a == 0:
                TOKENED = TOKENED + ","
            TOKENED = TOKENED + '[{"keyword":"plout"}'
            TOKENED = TOKENED + ',{"var_name":"'+ ls[1] + '"}]'
        if ls[0] == "loop":
            if not a == 0:
                TOKENED = TOKENED + ","
            TOKENED = TOKENED + '[{"keyword":"plout"}'
            TOKENED = TOKENED + ',{"looptimes":"'+ ls[1] + '"}]'
        for b in range(len(VARS)):
            if ls[0] == VARS[b]:
                if not a == 0:
                    TOKENED = TOKENED + ","
                TOKENED = TOKENED + '[{"var_use":"'+ ls[0] + '"}'
                TOKENED = TOKENED + ',{"oparator":"'+ ls[1] + '"}'
                TOKENED = TOKENED + ',{"value":"'+ ls[2] + '"}]'
    TOKENED = TOKENED + ']'
    print("[INFO] Tokenizing complete. Now parsing tokens.")
    time.sleep(0.7)
    ParseTokens(TOKENED)

def CodeComp(code):
    LINES = []
    for i in range(len(code)):
        code[i] = re.sub("\n", "", code[i])
        sp = code[i].split(";")
        for h in range(len(sp) - 1):
            LINES.append(sp[h])
    for b in range(len(LINES)):
        while LINES[b][0] == " ":
            LINES[b] = re.sub(" ", "", LINES[b], 1)
    if True == ";":
        print("[ERROR] Last letter of code.txt is not ';'")
    else:
        print("[INFO] Lexing is complete. Now tokenizing.")
        time.sleep(0.5)
        Tokenize(LINES)

try:
    code = open("Input/code.txt").readlines()
    CodeComp(code)
except:
    print("[ERROR] Code file not found.")
    Close()

#code = open("Input/code.txt").readlines()
#CodeComp(code)
#!/usr/bin/env python
# coding: utf-8


import csv
from collections import defaultdict


def get_dictionary(file_name: str) -> dict:

    # open CSV file 
    with open(file_name, 'r') as csv_file:
        
        # get an ordered dictionary of the data
        ordered_dict = csv.DictReader(csv_file)
        
        # turn it into a common dictionary by putting it in a list
        into_dictionary = list(ordered_dict)
            
        # return the dictionary by itself
        return into_dictionary[0]


def read_operator_table(file_name: str):
    
    table: list = []
    
    # open CSV file 
    with open(file_name, 'r') as csv_file:
        
        # set up reader
        csv_reader = csv.reader(csv_file)
            
        # go over the rows and add them to table
        for row in csv_reader:
            table.append(row)

        # return table
        return table


def read_symbol_table(file_name: str, column_name: str) -> list:

    # set up variables 
    columns: defaultdict = defaultdict(list)
    symbol_list: list = []

    # open CSV file 
    with open(file_name, 'r') as csv_file:

        # set up reader
        csv_reader = csv.DictReader(csv_file)

        # go over the rows
        for row in csv_reader: 
            
            # create a dict that has the row category as a key and the items
            # in the row category are placed in a list as the value
            for (key, value) in row.items(): 
                columns[key].append(value) 
    
    # make a list of the values
    symbol_list = columns[column_name]
    
    # return symbol_list
    return symbol_list


def read_token_list(file_name: str) -> list:
    
    # set up variables 
    columns: defaultdict = defaultdict(list)
    token_list: list = []

    # open CSV file 
    with open(file_name, 'r') as csv_file:

        # set up reader
        csv_reader = csv.DictReader(csv_file)

        # go over the rows
        for row in csv_reader: 
            
            # create a dict that has the row category as a key and the items
            # in the row category are placed in a list as the value
            for (key, value) in row.items(): 
                columns[key].append(value) 
        
    # make a list of the values
    token_list = columns["Token"]
    
    # return token_list
    return token_list


def push_down_automata(symbols_list: list) -> list: # symbols: list
    
    # quad variables
    quad: list = [0, 0, 0, 0]
    quad_list: list = []
    quad_flag: bool = True
    quad_counter: int = 2
        
    # PDA stack
    push_down_stack: list = ["^"]
        
    # terminals stacks
    symbol_terminals: list = []
    pda_terminals: list = []
        
    # symbols lists
    symbols: list = symbols_list
    symbols_initial: list = []
    symbols_initial = symbols.copy()
    
    # symbols current
    symbols_current_left: int = 0
        
    # operators
    current_operator: str = push_down_stack[0]
    previous_operator: str = push_down_stack[0]
        
    # indexes
    current_index: int = 0
    previous_index: int = 0
        
    # index counters
    index_counter_current: int = 0
    index_counter_previous: int = 0
        
    # index tracker
    print_index_tracker: int = 0
        
    # temporary tracking
    current_temporary: str = ""
    temp_counter: int = 1
    temp_string: str = "temp"
        
    # PDA handling
    pushing_down: bool = True
    break_flag: int = 0
    length_count: int = 0
    
    # fix-up stack and variables
    fix_up_list: list = []
    label_counter: int = 1
    label_string: str = "L"
    label_current: str = ""
        
    # left brace
    current_left_brace: str = ""
    left_brace_tracker: int = 0
        
    # class name
    class_name_tracker: int = 0
    class_name: str = ""
    
    # reserved
    reserved: list = list(get_dictionary("Reserved_Words.csv"))[1:]
    reserved_tracker: int = 0
        
    # current if and then
    symbols_current_if: int = 0
    symbols_current_then: int = 0
    pda_current_if: int = 0
    pda_current_then: int = 0
        
    # then flag
    then_flag: int = 0
        
    # precedence table
    precedence_table: list = read_operator_table("Operator_Precedence_Table.csv")
        
    # operators
    operator_list: list = precedence_table[0]

        
    # ------------------------------------------------------ START -------------------------------------------------

    
    while pushing_down:
        
        # we keep track index and character (symbol)
        for index, symbol in enumerate(symbols):
            
            # check if symbol is in operator list or not
            if symbol not in operator_list:

                push_down_stack.append(symbol)

            elif symbol in operator_list:

                previous_operator = current_operator
                current_operator = symbol
                
                push_down_stack.append(symbol)
                symbol_terminals.append(symbol)
                
                if symbol == "print":
                    print_index_tracker = symbol_terminals.index(symbol)
             
            # check to see if symbol is a special case
            if symbol == "class":
                class_name_tracker = 1
                
            if class_name_tracker:
                class_name = symbols[index + 1]
                class_name_tracker = 0
                
            if symbol == "{":
                current_left_brace = symbol
                left_brace_tracker = index
                
            if symbol in reserved:
                reserved_tracker = index
                
            if symbol == "if":
                symbols_current_if = index
                
            if symbol == "then":
                symbols_current_then = index
                
            # get current and precious index
            current_index = operator_list.index(current_operator)
            previous_index = operator_list.index(previous_operator)
            

            # ----------------------------------------- ( < ) -------------------------------------------------------
            
            # if we have '<' then we yield precedence
            if precedence_table[previous_index][current_index] == "<":
                pass

            # ----------------------------------------- ( = ) -------------------------------------------------------
                
            # if we have '=' then we have equal precedence so we continue
            elif precedence_table[previous_index][current_index] == "=":
                
                # pop parenthesis if no longer needed in Symbols
                if symbol_terminals[symbol_terminals.index(current_operator) - 1] == "(" and current_operator == ")":
                    break

            # ----------------------------------------- ( > ) -------------------------------------------------------
                    
            # if we have '>' then we take precedence
            elif precedence_table[previous_index][current_index] == ">":
                pda_terminals = symbol_terminals.copy()
                
                # setting index_counters
                index_counter_current = index
                index_counter_previous = index - 2
            
                # ------------------------------------ SYMBOLS ------------------------------------------------------
                
                # we go through the tokens in the range and move backwards to avoid index issues
                for item in reversed(range(index_counter_previous - 1, index)):
                    
                    symbols.pop(item)
                    index_counter_current -= 1
                    
                # we add the temp token to symbols
                symbols.insert(index_counter_current, temp_string + str(temp_counter))
                
                # we update current_temporary
                current_temporary = temp_string + str(temp_counter)
                
                # pop parenthesis if no longer needed in Symbols
                symbol_terminals.remove(previous_operator)
                if symbol_terminals[symbol_terminals.index(current_operator) - 1] == "(" and current_operator == ")":
                    symbols.pop(symbols.index(current_temporary) - 1)
                    symbols.pop(symbols.index(current_temporary) + 1) 
                
                # ----------------------------------------- PDA -------------------------------------------------------
                
                # setting index_counters
                index_counter_current = index
                index_counter_previous = index - 2
                
                # we go through the tokens in the range and move backwards to avoid index issues
                for item in reversed(range(index_counter_previous, index + 1)):
        
                    # if quad_flag is on then we create the flag by adjusting the counter
                    # to get the correct index for the quad list
                    if quad_flag:
                        quad[quad_counter] = push_down_stack[item]
                    
                        if quad_counter == 2:
                            quad_counter -= 2
                        
                        elif quad_counter == 0:
                            quad_counter += 1
                            
                        elif quad_counter == 1:
                            quad_counter += 2
                            
                        elif quad_counter == 3:
                            quad_flag = False      
                            
                    # pop item
                    push_down_stack.pop(item)
                    
                    # update current index counter
                    index_counter_current -= 1
                    
                # ------------------------------ COMPARISSON OPERATORS -----------------------------------------------
                
                # we update the quad assuming we have comparisson operators
                if "<" in quad:
                    quad[quad_counter] = '-'
                    temp_counter -= 1
                    
                elif ">" in quad:
                    quad[quad_counter] = '-'
                    temp_counter -= 1
                
                elif "=" not in quad:
                    quad[quad_counter] = temp_string + str(temp_counter)
                    
                else:
                    quad[quad_counter] = "-"
                
                # add temp to PDA
                push_down_stack.insert(index_counter_current + 1, temp_string + str(temp_counter))
                
                # pop parenthesis if no longer needed in PDA
                pda_terminals.remove(previous_operator)
                if pda_terminals[pda_terminals.index(current_operator) - 1] == "(" and current_operator == ")":
                    push_down_stack.pop(push_down_stack.index(current_temporary) - 1)
                    push_down_stack.pop(push_down_stack.index(current_temporary) + 1)            
                    
                # input quad rearrangement
                if quad[2] == 'input':
                    quad[0] = quad[2]
                    quad[2] = "-"
                    temp_counter -= 1
                
                # reset variables for next round
                quad_counter = 2
                temp_counter += 1
                quad_list.append(quad)
                quad = [0, 0, 0, 0]
                
                # -------------------------------- IF THEN statement is complete ----------------------------------------------------
    
                # REMOVE items between if then
                for if_index, item in enumerate(pda_terminals):
                
                    if item == "if":
                        pda_current_if = if_index
                        
                    elif item == "then":
                        pda_current_then = if_index
        
                # check PDA rweminals and remove items from symbols
                if len(pda_terminals) >= 3 and (pda_terminals[pda_current_if] == "if" and pda_terminals[pda_current_then] == "then"):

                    symbols_current_then -= 2
                
                    for item in reversed(range(symbols_current_if + 1, symbols_current_then)):
                        symbols.pop(item)
                        then_flag = 1
                    
                    # if we have a symbol 'then' we add the corresponding quad along with fix-up labels
                    if then_flag:
                        quad_list.append(["THEN", label_string + str(label_counter), previous_operator, "-"])
                        fix_up_list.append(label_string + str(label_counter))
                        label_current = label_string + str(label_counter)
                        label_counter += 1
                
                # ---------------------------------------- END current loop ---------------------------------------------------------
                break
                
                
            # if no operators remain inbetween the braces pop anything between them and themselves
            elif current_operator == "}" and current_left_brace:
                
                # pop if then from stack
                for if_index, item in enumerate(symbol_terminals):
                
                    if item == "if":
                        symbols_current_if = if_index
                        
                    elif item == "then":
                        symbols_current_then = if_index
                        
                    elif item == "{":
                        symbols_current_left = if_index
                
                # pop the print string
                if len(symbol_terminals) >= 4 and (symbol_terminals[print_index_tracker] == "print" and symbol_terminals[-2] == "{" and symbol_terminals[-1] == "}"):
                    
                    for item in range(left_brace_tracker + 1, index):
                        quad_list.append(["print", symbols[item], "-", "-"])
            
                # if then popped from the stack
                if fix_up_list and (symbol_terminals[symbols_current_if] == "if" and symbol_terminals[symbols_current_then] == "then"):
                    
                    quad_list.append([fix_up_list[-1], "-", "-", "-"])
                    fix_up_list.pop()
                
                # remove empty braces
                if current_operator == symbol_terminals[-1] and symbols_current_left:
                    
                    for item in reversed(range(left_brace_tracker, index + 1)):
                        symbols.pop(item)
                        
                    break
                    
                # remove final if then if it exists
                if symbol_terminals[symbols_current_left] == "{" and symbol_terminals[-1] == "}":
                    
                    for item in reversed(range(left_brace_tracker, index + 1)):
                        symbols.pop(item)
                    
                    
            # no conditions are met
            else:
                pass
                
            length_count = len(symbols)
            
        # -------------------------- End of for loop -------------------------------
        
        # if the length of symbols didn't change add 1 to break_flag
        if len(symbols) == length_count:
            break_flag += 1
            
        # reset variables for next round
        previous_operator = push_down_stack[0]
        current_operator = push_down_stack[0]
        push_down_stack = ["^"]
        symbol_terminals = []
        pda_terminals =[]
        current_temporary = ""
        current_left_brace = ""
        print_index_tracker = 0
        then_flag = 0
        symbols_current_if = 0
        symbols_current_then = 0
        symbols_current_left = 0
        
        # if length of symbols is 2 or less we have popped all the items
        if len(symbols) <= 2:
            pushing_down = False
        
        # a back-up measure to avoid infinite loops
        if break_flag == 10:
            break
            
    # ---------------------------------- End of while loop --------------------------
    
    # return the quads generated
    return quad_list


def assembly_code(quad_list: list) -> list:
    
    # set up variables needed
    assembly_list: list = []
    fix_up_list: list = []
    current_code: list = []
    string: str = ""

    # we run through all the quads and get the assembly equivalent
    for quad in quad_list:
        
        # we check the operator and only look at the first 3 items in the quad
        for operator in quad[:-3]:
            
            if operator[0] == "L":
                operator = "L"
            
            match operator:
                
                case "+":
                    
                    current_code.append("mov ax, [" + quad[1] + "]")
                    current_code.append("add ax, [" + quad[2] + "]")
                    current_code.append("mov [" + quad[3] + "], ax")
                    
                    assembly_list.append(current_code)
                
                case "-":
                    
                    current_code.append("mov ax, [" + quad[1] + "]")
                    current_code.append("sub ax, [" + quad[2] + "]")
                    current_code.append("mov [" + quad[3] + "], ax")
                    
                    assembly_list.append(current_code)
                    
                case "*":
                    
                    current_code.append("mov ax, [" + quad[1] + "]")
                    
                    if quad[2].isdigit():
                        current_code.append("imul ax, [" + quad[2] + "]")
                        
                    else:
                        current_code.append("mul byte [" + quad[2] + "]")
                        
                    current_code.append("mov [" + quad[3] + "], ax")
                    assembly_list.append(current_code)
                
                case "/":
                    
                    current_code.append("mov dx, 0")
                    current_code.append("mov ax, [" + quad[1] + "]")
                    current_code.append("mov bx, [" + quad[2] + "]")
                    current_code.append("div bx")
                    current_code.append("mov [" + quad[3] + "], ax")
                    
                    assembly_list.append(current_code)
                
                case "=":
                    current_code.append("mov ax, [" + quad[2] + "]")
                    current_code.append("mov [" + quad[1] + "], ax")
                    current_code.append("nop")
                    
                    assembly_list.append(current_code)
                
                case ">":
                    
                    current_code.append("mov ax, [" + quad[1] + "]")
                    current_code.append("cmp ax, [" + quad[2] + "]")
                    
                    assembly_list.append(current_code)
                
                case "<":
                    
                    current_code.append("mov ax, [" + quad[1] + "]")
                    current_code.append("cmp ax, [" + quad[2] + "]")
                    
                    assembly_list.append(current_code)
                
                case "<=":
                    
                    current_code.append("mov ax, [" + quad[1] + "]")
                    current_code.append("cmp ax, [" + quad[2] + "]")
                    
                    assembly_list.append(current_code)
                    
                case ">=":
                    
                    current_code.append("mov ax, [" + quad[1] + "]")
                    current_code.append("cmp ax, [" + quad[2] + "]")
                    
                    assembly_list.append(current_code)
                    
                case "==":
                    
                    current_code.append("mov ax, [" + quad[1] + "]")
                    current_code.append("cmp ax, [" + quad[2] + "]")
                    
                    assembly_list.append(current_code)
                    
                case "!=":
                    
                    current_code.append("mov ax, [" + quad[1] + "]")
                    current_code.append("cmp ax, [" + quad[2] + "]")
                    
                    assembly_list.append(current_code)
                
                case "THEN":
                    
                    if quad[2] == "<":
                        string = "JGE"
                        
                    elif quad[2] == ">":
                        string = "JLE"
                        
                    elif quad[2] == "<=":
                        string = "JG"
                        
                    elif quad[2] == ">=":
                        string = "JL"
                        
                    elif quad[2] == "==":
                        string = "JNE"
                        
                    elif quad[2] == "!=":
                        string = "JE"
                    
                    current_code.append(string + " " + quad[1])
                    
                    fix_up_list.append(quad[1])
                    assembly_list.append(current_code)
                    
                case "L":
                    print("LABEL")
                    current_code.append("nop")
                    assembly_list.append(current_code)
                    
                case "print":
                    current_code.append("mov ax, [" + quad[1] + "]")
                    current_code.append("mov [" + quad[1] + "], ax")
                    current_code.append("mov ax, [" + quad[1] + "]")
                    current_code.append("call ConvertIntegerToString")
                    current_code.append("mov ax, [" + quad[1] + "]")
                    current_code.append("mov eax, 4")
                    current_code.append("mov ebx, 1")
                    current_code.append("mov ecx, Result")
                    current_code.append("mov edx, ResultEnd")
                    current_code.append("int 80h")
                    
                    assembly_list.append(current_code)
                    
                case "input":
                    current_code.append("call PrintString")
                    current_code.append("call GetAnInteger")
                    current_code.append("mov ax, [ReadInt]")
                    current_code.append("mov ["+ quad[1] + "], ax")
                    
                    assembly_list.append(current_code)
                
                case unknown_command:
                    print("Invalid Input:", operator)
                    
        # reset variable for next round
        current_code = []
        
        # --------------------------------- End nested loop -----------------------------------
        
    return [assembly_list, fix_up_list]


def assembly_literals(assembly: list) -> list:
    
    
    # bracket variables
    left_bracket: str = "["
    right_bracket: str = "]"
    left_bracket_index: int = 0
    right_bracket_index: int = 0
    
    # str variables
    list_to_str: list = []
    str_replacement: str = ""
        
    # assembly variables
    assembly_list: list = []
    assembly_list.extend(assembly[0])
    assembly_counter: int = 0
        
    # fix up variables
    fix_up_counter: int = 0
    fix_up_list: list = []
        
    # jump variables
    jump_list: list = ["JG", "JL", "JGE", "JLE", "JNE", "JE"]
        
    # body variable
    body_list: list = []

    # if the list with the asm code includes also has a fix-up list then initialize it
    if len(assembly) > 1:
        fix_up_list = assembly[1]
    
    
    # we go through the list that contains all the lists
    for index_1, assembly in enumerate(assembly_list):
        
        # we go through each individual list
        for index_2, item in enumerate(assembly):
            
            # get the index for the left and right bracket
            try:
                left_bracket_index = item.index(left_bracket)
                right_bracket_index = item.index(right_bracket)
                
            # item doesn't have brackets
            except (IndexError, ValueError) as error:
                pass
            
            # we check if the asm code is greater than the left bracket index that an actual left bracket exists in item
            if len(item) > left_bracket_index and "[" in item:
                
                # we go through each character in the asm code
                for character in range(left_bracket_index + 1, right_bracket_index):
                    
                    # if we have a digit then we remove the brackets and end the loop
                    if item[character].isdigit():
            
                        list_to_str.extend(assembly_list[index_1][index_2])
                
                        list_to_str.remove(left_bracket)
                        list_to_str.remove(right_bracket)
                        str_replacement = "".join(list_to_str)
                        
                        assembly[index_2] = str_replacement
                        
                        break
                        
                    # otherwise we end the loop
                    else:
                        break
                        
                # we reset the variables for the next round
                list_to_str = []
                str_replacement = ""
                
            # otherwise we have a NOP operation
            else:
                pass
            
        # --------------------------------- End nested loop -----------------------------------

    # we go through all the lists in the assembly_list
    for assembly in assembly_list:
        
        # we go through each item in assembly
        for item in assembly:
            
            # if NOT nop add space to the code and make it it's own list
            if item != "nop":
                body_list.append(["    " + item])
                
            # if nop is the only asm code in assembly it means we have items in the fix-up list
            elif len(assembly) == 1 and item == "nop":
                body_list.append([fix_up_list[fix_up_counter][-2:] + ":", item])
                fix_up_counter += 1
            
            # otherwise add add space to the asm code
            else:
                body_list.append(["    " + item])
                
    # we go through body_list
    for index, item in enumerate(body_list):
        
        # if we have a label we hoin it with nop
        if item[0][0] == "L":
            body_list[index] = [" ".join(item)]
        
    # we return body_list
    return body_list


# ----------------------------- generate the asm file --------------------------------------------------------


def initialize_asm_file(file_name: str):
    
    with open(file_name, "w") as file:
        
        file.write("")


def write_asm_header(file_name: str):
    
    asm_keys: str = ""
    program_name: str = read_symbol_table("Symbol_Table.csv", "Symbol")[0]
    
    asm_keys = f"""; Program Name: {program_name}\n
sys_exit	equ	1
sys_read	equ	3
sys_write	equ	4
stdin		equ	0	; default keyboard
stdout		equ	1	; default terminal screen
stderr		equ	3
"""
    
    with open(file_name, "a") as file:
        
        file.write(asm_keys)


def write_asm_data(file_name: str):
    
    asm_keys: str = ""
    symbol_table_tokens: list = read_symbol_table("Symbol_Table.csv", "Symbol")[1:]
    symbol_table_values: list = read_symbol_table("Symbol_Table.csv", "Value")[1:]
    symbol_table_combo: list = []
        
    symbol_table_combo = list(zip(symbol_table_tokens,symbol_table_values))
    
    constant_header: str = """; -------------------------- declare constants ------------------------------------

section .data
    
"""
        
    constant: str = """    userMsg         db     'Input an integer: '
    lenUserMsg      equ    $-userMsg
    newline         db     0xA
    Ten             DW     10
    num times 6     db     'ABCDEF'
    numEnd          equ    $-num
    Result          db     'Output: '
    ResultValue     db     'aaaaa'
                    db     0xA
    ResultEnd       equ    $-Result
    
"""
    
    # we fill out the variables from the symbol table along with their values
    with open(file_name, "a") as file:

        file.write("\n")
        file.write(constant_header)
    
        for item in symbol_table_combo:

            if item[1] == "":
                file.write("    " + (item[0] + "\tdw\t00000\n"))
                
            elif item[0].isdigit():
                    pass
            
            else:
                file.write("    " + item[0] + "\tdw\t" + item[1] + "\n")

        file.write(constant)


def write_asm_bss(file_name: str):
    
    variables: str = """; -------------------------- uninitiated variables ---------------------------------

section .bss 

    TempChar        RESB    1
    testchar        RESB    1
    ReadInt         RESW    1              
    tempint         RESW    1             
    negflag         RESB    1 
    
"""
    
    with open(file_name, "a") as file:
        
        file.write(variables)


def write_asm_start(file_name: str):
    
    main_program: str = """; -------------------------- Main program -----------------------------------------

global _start   

section .text

_start:
    
"""
        
    with open(file_name, "a") as file:
        
        file.write(main_program)


def write_asm_body(file_name: str):
    
    quads: list = push_down_automata(read_token_list("Token_Classification_Table.csv"))
    assembly_list: list = assembly_code(quads)
    body: list = assembly_literals(assembly_list)
    
    with open(file_name, "a") as file:
        
        for line in body:
        
            for item in line:
                    
                file.write(item + "\n")


def write_asm_end(file_name: str):
    
    end_program: str = """; -------------------------- End Main program -------------------------------------

fini:

    mov eax,sys_exit
    xor ebx,ebx
    int 80h
    
"""
    with open(file_name, "a") as file:
        
        file.write(end_program)


def write_asm_functions(file_name: str):
    
    functions: str = """; ------------------------------ functions ----------------------------------------

PrintString:

    push    ax
    push    dx

    ; prompt user

    mov eax, 4
    mov ebx, 1
    mov ecx, userMsg
    mov edx, lenUserMsg
    int 80h
    pop     dx 
    pop     ax
    ret

;End PrintString


GetAnInteger:

    mov eax, 3
    mov ebx, 2
    mov ecx, num
    mov edx, 6
    int 0x80


;End GetAnInteger


ConvertStringToInteger:

    mov ax, 0
    mov [ReadInt], ax 
    mov ecx, num
    mov bx,0
    mov bl, byte [ecx]

Next:

    sub bl,'0'
    mov ax, [ReadInt]
    mov dx, 10
    mul dx
    add ax, bx
    mov [ReadInt], ax
    mov bx, 0
    add ecx, 1
    mov bl, byte[ecx]
    cmp bl,0xA
    jne Next
    ret

;End GetAnInteger


ConvertIntegerToString:

    mov ebx, ResultValue + 4

ConvertLoop:

    sub dx,dx
    mov cx,10
    div cx
    add dl,'0'
    mov [ebx], dl
    dec ebx
    cmp ebx, ResultValue
    jge ConvertLoop

    ret

; End ConvertIntegerToString
"""
        
    with open(file_name, "a") as file:
        
        file.write(functions)


# ----------------------------- asm file complete -------------------------------------------------


def write_asm_file(file_name: str):
    
    # run all the functions to create the asm file
    initialize_asm_file(file_name)
    write_asm_header(file_name)
    write_asm_data(file_name)
    write_asm_bss(file_name)
    write_asm_start(file_name)
    write_asm_body(file_name)
    write_asm_end(file_name)
    write_asm_functions(file_name)
    
    print(f".asm file created. File name is: {file_name}")


def syntax_analyzer(file_name: str) -> str:

    # run all the functions to get the output of the suntax analyzer
    quads = push_down_automata(read_token_list("Token_Classification_Table.csv"))
    assembly_list = assembly_code(quads)
    
    write_asm_file(file_name)
    
    return "Syntax Analysis Complete."


if __name__ == "__main__":
    syntax_analyzer("asm_file.txt")
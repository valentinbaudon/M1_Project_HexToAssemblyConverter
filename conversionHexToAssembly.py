import json
import math
import os
import sys
from time import sleep
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal

CurrentInstruction = 0
TotalInstructions = 1


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


Logo = resource_path("Logo.png")


# Thread qui met à jour la valeur de la barre de progression
class ProgressThread(QtCore.QThread):
    progress_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def run(self):
        while 1:
            self.progress_signal.emit(int(CurrentInstruction / TotalInstructions * 100))
            sleep(0.1)


# Fonction qui lit le fichier d'entrée et écrit chaque instruction en binaire
def writeBinaryInstructions(filepath):
    global TotalInstructions
    global CurrentInstruction
    CurrentInstruction = 0
    TotalInstructions = 1
    STMfile = open(filepath)
    STMfileLines = STMfile.readlines()
    data_STMfile = ""
    addresses = []
    for STMfileLine in STMfileLines:
        data_STMfile += STMfileLine[12:-3]
        addresses.append(STMfileLine[4:12])
    data_binary = ""
    # Boucle qui convertit l'hexadécimal au binaire
    for c in data_STMfile:
        data_binary += str(bin(int(c, 16))[2:].zfill(4))
    data_big_endian = ""
    # Boucle qui convertit les données de Little Endian en Big Endian
    for i in range(0, len(data_binary) - 15, 8):
        data_big_endian = data_big_endian + data_binary[i:i + 8]
    i = 0
    data_reformatted = ""
    # Boucle qui reformatte les données par groupe de 32 bits
    while i < len(data_big_endian) - 31:
        tmp = data_big_endian[i:i + 32]
        data_reformatted += tmp[24:] + tmp[16:24] + tmp[8:16] + tmp[:8]
        i += 32
    instructions_file = open(resource_path("ConversionFiles\\instructions_file.txt"), "w")
    i = 0
    # Boucle qui écrit le fichier de sortie avec chaque instruction
    while i < len(data_reformatted) - 31:
        tmp = data_reformatted[i:i + 32]
        if tmp[0:3] == "111" and tmp[3:5] != "00":
            instructions_file.write(addresses[math.floor(i / 256)] + tmp + '\n')
            i += 32
        else:
            instructions_file.write(addresses[min(round(i / 256), len(addresses) - 1)] + tmp[:16] + '\n')
            i += 16


# Fonction qui détermine si une instruction est 16 bits ou 32 bits
def is32bits(instruction):
    if instruction[0:3] == '111' and instruction[3:5] != "00":
        return True
    else:
        return False


# Fonction qui lit le JSON et retourne les arguments d'une instruction avec leurs valeurs
def GetDictField_16(json_file, line, index):
    finalString = ""
    try:
        fields = json_file[str(line[:index])]['fields']
    except:
        return ""
    keys = fields.keys()
    newBit = dict()
    for i in range(len(fields)):
        tmp = fields[list(keys)[i]]
        var1 = 15 - int(tmp[0])
        var2 = 15 - int(tmp[1])
        if var1 > var2:
            newTab = [var1, var2]
        else:
            newTab = [var2, var1]
        newBit[list(fields.keys())[i]] = newTab
    newDict = dict()
    for i in range(len(newBit)):
        tmp = newBit[list(keys)[i]]
        newDict[list(newBit.keys())[i]] = int(line[tmp[1]:tmp[0] + 1], 2)
    for j in range(len(newDict) - 1):
        key = list(keys)[j]
        if key[0] == 'R':
            match key[1]:
                case "n":
                    finalString += 'Rn' + str(newDict[list(keys)[j]]) + ', '
                case "m":
                    finalString += 'Rm' + str(newDict[list(keys)[j]]) + ', '
                case "d":
                    finalString += 'Rd' + str(newDict[list(keys)[j]]) + ', '
                case "t":
                    finalString += 'Rt' + str(newDict[list(keys)[j]]) + ', '
        if key[:3] == 'imm':
            finalString += '#' + str(newDict[list(keys)[j]]) + ', '
    key = list(keys)[-1]
    if key[0] == 'R':
        match key[1]:
            case "n":
                finalString += 'Rn' + str(newDict[list(keys)[-1]])
            case "m":
                finalString += 'Rm' + str(newDict[list(keys)[-1]])
            case "d":
                finalString += 'Rd' + str(newDict[list(keys)[-1]])
            case "t":
                finalString += 'Rt' + str(newDict[list(keys)[-1]])
    if key[:3] == 'imm':
        finalString += '#' + str(newDict[list(keys)[-1]])
    return finalString


# Fonction qui écrit les instructions détaillées dans un fichier de sortie
def write_described_instruction_16(descr_file, json_file, line, index, code, address):
    match code:
        case "Compact":
            descr_file.write("0x" + str(hex(int(address, 16)))[2:].zfill(8) + " : " + json_file[str(line[:index])][
                'instruction'] + ' : ' + GetDictField_16(json_file, line, index) + "\n")
        case "Classique":
            descr_file.write("0x" + str(hex(int(address, 16)))[2:].zfill(8) + " : " + json_file[str(line[:index])][
                'meaning'] + ' : ' + GetDictField_16(json_file, line, index) + "\n")
        case "Classic":
            descr_file.write("0x" + str(hex(int(address, 16)))[2:].zfill(8) + " : " + json_file[str(line[:index])][
                'meaning'] + ' : ' + GetDictField_16(json_file, line, index) + "\n")
        case "Integral":
            descr_file.write(
                "0x" + str(hex(int(address, 16)))[2:].zfill(8) + " : " + line[:-1] + ' : ' +
                json_file[str(line[:index])][
                    'meaning'] + " : " + GetDictField_16(json_file, line, index) + "\n")


# Fonction qui lit le JSON et retourne les arguments d'une instruction avec leurs valeurs
def GetDictField_32(json_file, line, instruction):
    finalString = ""
    fields = json_file[str(instruction)]['fields']
    keys = fields.keys()
    newBit = dict()
    for i in range(len(fields)):
        tmp = fields[list(keys)[i]]
        var1 = 31 - int(tmp[0])
        var2 = 31 - int(tmp[1])
        if var1 > var2:
            newTab = [var1, var2]
        else:
            newTab = [var2, var1]
        newBit[list(fields.keys())[i]] = newTab
    newDict = dict()
    for i in range(len(newBit)):
        tmp = newBit[list(keys)[i]]
        newDict[list(newBit.keys())[i]] = int(line[tmp[1]:tmp[0] + 1], 2)
    for j in (range(len(newDict) - 1, 0, -1)):
        key = list(keys)[j]
        match key[0]:
            case 'R':
                match key[1]:
                    case "n":
                        finalString += 'Rn' + str(newDict[list(keys)[j]]) + ', '
                    case "m":
                        finalString += 'Rm' + str(newDict[list(keys)[j]]) + ', '
                    case "d":
                        finalString += 'Rd' + str(newDict[list(keys)[j]]) + ', '
                    case "t":
                        finalString += 'Rt' + str(newDict[list(keys)[j]]) + ', '
            case 'W':
                finalString += 'W' + str(newDict[list(keys)[j]]) + ', '
            case 'T':
                finalString += 'T' + str(newDict[list(keys)[j]]) + ', '
            case 'U':
                finalString += 'U' + str(newDict[list(keys)[j]]) + ', '
        match key[:2]:
            case 'tb':
                finalString += 'tb' + str(newDict[list(keys)[j]]) + ', '
            case 'sh':
                finalString += 'tb' + str(newDict[list(keys)[j]]) + ', '
        match key[:3]:
            case 'imm':
                finalString += '#' + str(newDict[list(keys)[j]]) + ', '
            case 'Rt2':
                finalString += 'Rt2 ' + str(newDict[list(keys)[j]]) + ', '
            case 'CRd':
                finalString += 'CRd' + str(newDict[list(keys)[j]]) + ', '
            case 'CRm':
                finalString += 'CRm ' + str(newDict[list(keys)[j]]) + ', '
            case 'CRn':
                finalString += 'CRm ' + str(newDict[list(keys)[j]]) + ', '
        match key[:4]:
            case 'type':
                finalString += 'type:' + str(newDict[list(keys)[j]]) + ', '
            case 'SYSm':
                finalString += 'SYSm:' + str(newDict[list(keys)[j]]) + ', '
            case 'mask':
                finalString += 'mask:' + str(newDict[list(keys)[j]]) + ', '
            case 'cond':
                finalString += 'cond:' + str(newDict[list(keys)[j]]) + ', '
            case 'RdLo':
                finalString += 'RdLo:' + str(newDict[list(keys)[j]])
            case 'RdHi':
                finalString += 'RdHi:' + str(newDict[list(keys)[j]])
            case 'opc1':
                finalString += 'opc1:' + str(newDict[list(keys)[j]])
            case 'opc2':
                finalString += 'opc2:' + str(newDict[list(keys)[j]])
        match key[:6]:
            case 'option':
                finalString += 'option:' + str(newDict[list(keys)[j]]) + ', '
            case 'rotate':
                finalString += 'rotate:' + str(newDict[list(keys)[j]]) + ', '
            case 'coproc':
                finalString += 'coproc:' + str(newDict[list(keys)[j]]) + ', '
        if key[:5] == 'shift':
            finalString += 'shift:' + str(newDict[list(keys)[j]]) + ', '
        elif key[:7] == 'sat_imm':
            finalString += 'sat_imm:' + str(newDict[list(keys)[j]]) + ', '
        elif key[:7] == 'widthm1':
            finalString += 'widthm1:' + str(newDict[list(keys)[j]]) + ', '
        elif key[:13] == 'register_list':
            finalString += 'register_list:' + str(newDict[list(keys)[j]]) + ', '
    key = list(keys)[-1]
    match key[0]:
        case 'R':
            match key[1]:
                case "n":
                    finalString += 'Rn' + str(newDict[list(keys)[-1]]) + ', '
                case "m":
                    finalString += 'Rm' + str(newDict[list(keys)[-1]]) + ', '
                case "d":
                    finalString += 'Rd' + str(newDict[list(keys)[-1]]) + ', '
                case "t":
                    finalString += 'Rt' + str(newDict[list(keys)[-1]]) + ', '
        case 'W':
            finalString += 'W' + str(newDict[list(keys)[-1]]) + ', '
        case 'T':
            finalString += 'T' + str(newDict[list(keys)[-1]]) + ', '
        case 'U':
            finalString += 'U' + str(newDict[list(keys)[-1]]) + ', '
    match key[:2]:
        case 'tb':
            finalString += 'tb' + str(newDict[list(keys)[-1]]) + ', '
        case 'sh':
            finalString += 'tb' + str(newDict[list(keys)[-1]]) + ', '
    match key[:3]:
        case 'imm':
            finalString += '#' + str(newDict[list(keys)[-1]]) + ', '
        case 'Rt2':
            finalString += 'Rt2 ' + str(newDict[list(keys)[-1]]) + ', '
        case 'CRd':
            finalString += 'CRd' + str(newDict[list(keys)[-1]]) + ', '
        case 'CRm':
            finalString += 'CRm ' + str(newDict[list(keys)[-1]]) + ', '
        case 'CRn':
            finalString += 'CRm ' + str(newDict[list(keys)[-1]]) + ', '
    match key[:4]:
        case 'type':
            finalString += 'type:' + str(newDict[list(keys)[-1]]) + ', '
        case 'SYSm':
            finalString += 'SYSm:' + str(newDict[list(keys)[-1]]) + ', '
        case 'mask':
            finalString += 'mask:' + str(newDict[list(keys)[-1]]) + ', '
        case 'cond':
            finalString += 'cond:' + str(newDict[list(keys)[-1]]) + ', '
        case 'RdLo':
            finalString += 'RdLo:' + str(newDict[list(keys)[-1]])
        case 'RdHi':
            finalString += 'RdHi:' + str(newDict[list(keys)[-1]])
        case 'opc1':
            finalString += 'opc1:' + str(newDict[list(keys)[-1]])
        case 'opc2':
            finalString += 'opc2:' + str(newDict[list(keys)[-1]])
    match key[:6]:
        case 'option':
            finalString += 'option:' + str(newDict[list(keys)[-1]]) + ', '
        case 'rotate':
            finalString += 'rotate:' + str(newDict[list(keys)[-1]]) + ', '
        case 'coproc':
            finalString += 'coproc:' + str(newDict[list(keys)[-1]]) + ', '
    if key[:5] == 'shift':
        finalString += 'shift:' + str(newDict[list(keys)[-1]]) + ', '
    elif key[:7] == 'sat_imm':
        finalString += 'sat_imm:' + str(newDict[list(keys)[-1]]) + ', '
    elif key[:7] == 'widthm1':
        finalString += 'widthm1:' + str(newDict[list(keys)[-1]]) + ', '
    elif key[:13] == 'register_list':
        finalString += 'register_list:' + str(newDict[list(keys)[-1]]) + ', '
    return finalString


# Fonction qui écrit les instructions détaillées dans un fichier de sortie
def write_described_instruction_32(descr_file, json_file, line, instruction, code, address):
    match code:
        case "Compact":
            descr_file.write("0x" + str(hex(int(address, 16)))[2:].zfill(8) + " : " + json_file[str(instruction)]['instruction'] + ' : ' + GetDictField_32(json_file, line, instruction) + "\n")
        case "Classique":
            descr_file.write("0x" + str(hex(int(address, 16)))[2:].zfill(8) + " : " + json_file[str(instruction)]['meaning'] + ' : ' + GetDictField_32(json_file, line, instruction) + "\n")
        case "Classic":
            descr_file.write("0x" + str(hex(int(address, 16)))[2:].zfill(8) + " : " + json_file[str(instruction)]['meaning'] + ' : ' + GetDictField_32(json_file, line, instruction) + "\n")
        case "Integral":
            descr_file.write("0x" + str(hex(int(address, 16)))[2:].zfill(8) + " : " + line[:-1] + ' : ' + json_file[str(instruction)]['meaning'] + " : " + GetDictField_32(json_file, line, instruction) + "\n")


# Fonction qui lit les bits et lance l'écriture des instructions.
# Elle contient aussi l'arbre de décision
def describe_instructions(code):
    global TotalInstructions
    global CurrentInstruction
    file = open(resource_path("ConversionFiles\\instructions_file.txt"), "r")
    assembly_description = open(resource_path("ConversionFiles\\Assembly.txt"), "w")
    lines = file.readlines()
    TotalInstructions = len(lines)
    json_16 = json.load(open(resource_path("ConversionFiles\\Json_Decoding_ARM_16bit.json"), "r"))
    json_32 = json.load(open(resource_path("ConversionFiles\\Json_Decoding_ARM_32bit.json"), "r"))
    for binary_line in lines:
        address = binary_line[:8]
        line = binary_line[8:-1]
        CurrentInstruction += 1
        if is32bits(line):
            if line == "11111111111111111111111111111111":
                assembly_description.write("0x" + str(hex(int(address, 16)))[2:].zfill(8) + " : UNDEFINED or UNPREDICTABLE\n")
            else:
                # Load/Store
                if line[:7] == "1110100":
                    # Load/Store Multiple
                    if line[7:9] == "01" and line[11] == "0":
                        write_described_instruction_32(assembly_description, json_32, line, "1110100010x0", code, address)
                    elif line[7:9] == "01" and line[11] == "1" and line[10] != "0" and line[12:16] != "1101":
                        write_described_instruction_32(assembly_description, json_32, line, "1110100010x1", code, address)
                    elif line[7:9] == "01" and line[11] == "1" and line[10] == "0" and line[12:16] == "1101":
                        write_described_instruction_32(assembly_description, json_32, line, "1110100010111101", code, address)
                    elif line[7:9] == "10" and line[11] == "0" and line[10] != "0" and line[12:16] != "1101":
                        write_described_instruction_32(assembly_description, json_32, line, "1110100100x0", code, address)
                    elif line[7:9] == "10" and line[11] == "0" and line[10] == "0" and line[12:16] == "1101":
                        write_described_instruction_32(assembly_description, json_32, line, "1110100100101101", code, address)
                    elif line[7:9] == "10" and line[11] == "1":
                        write_described_instruction_32(assembly_description, json_32, line, "1110100100x1", code, address)
                    # Load/Store dual or exclusive, table branch
                    elif line[7:9] == "00" and line[10:12] == "00":
                        write_described_instruction_32(assembly_description, json_32, line, "111010000100", code, address)
                    elif line[7:9] == "00" and line[10:12] == "01":
                        write_described_instruction_32(assembly_description, json_32, line, "111010000101", code, address)
                    elif (line[7] == "0" and line[10:12] == "10") or (line[7] == "1" and line[11] == "0"):
                        write_described_instruction_32(assembly_description, json_32, line, "111010000110", code, address)
                    elif (line[7] == "0" and line[10:12] == "11" and line[12:16] != "1111") or (line[7] == "1" and line[11] == "1" and line[12:16] != "1111"):
                        write_described_instruction_32(assembly_description, json_32, line, "111010000111", code, address)
                    elif (line[7] == "0" and line[10:12] == "11" and line[12:16] == "1111") or (line[7] == "1" and line[11] == "1" and line[12:16] == "1111"):
                        write_described_instruction_32(assembly_description, json_32, line, "1110100xx1x11111", code, address)
                    elif line[7:9] == "01":
                        if line[10:12] == "00" and line[24:28] == "0100":
                            write_described_instruction_32(assembly_description, json_32, line, "111010001100xxxxxxxx11110100", code, address)
                        elif line[10:12] == "00" and line[24:28] == "0101":
                            write_described_instruction_32(assembly_description, json_32, line, "111010001100xxxxxxxx11110101", code, address)
                        elif line[10:12] == "01":
                            match line[24:28]:
                                case "0000":
                                    write_described_instruction_32(assembly_description, json_32, line, "111010001101xxxx111100000000", code, address)
                                case "0001":
                                    write_described_instruction_32(assembly_description, json_32, line, "111010001101xxxx111100000001", code, address)
                                case "0100":
                                    write_described_instruction_32(assembly_description, json_32, line, "111010001101xxxxxxxx111101001111", code, address)
                                case "0101":
                                    write_described_instruction_32(assembly_description, json_32, line, "111010001101xxxxxxxx111101011111", code, address)
                                case _:
                                    assembly_description.write("0x" + address + " : " + line + " : UNDEFINED or UNPREDICTABLE\n")
                        else:
                            assembly_description.write("0x" + address + " : " + line + " : UNDEFINED or UNPREDICTABLE\n")
                    else:
                        assembly_description.write("0x" + address + " : " + line + " : UNDEFINED or UNPREDICTABLE\n")
                # Data processing (shifted register)
                elif line[:7] == "1110101":
                    match line[7:11]:
                        case "0000":
                            if line[20:24] != "1111":
                                write_described_instruction_32(assembly_description, json_32, line, "11101010000", code, address)
                            elif line[20:24] == "1111" and line[11] == "1":
                                write_described_instruction_32(assembly_description, json_32, line, "111010100001xxxxxxxx1111", code, address)
                            else:
                                assembly_description.write("0x" + address + " : " + line + " : UNDEFINED or UNPREDICTABLE\n")
                        case "0001":
                            write_described_instruction_32(assembly_description, json_32, line, "11101010001", code, address)
                        case "0010":
                            if line[12:16] != "1111":
                                write_described_instruction_32(assembly_description, json_32, line, "11101010010", code, address)
                            else:
                                if line[26:28] == "00" and line[17:20] == "000" and line[24:26] == "00":
                                    write_described_instruction_32(assembly_description, json_32, line, "11101010010x1111x000xxxx0000", code, address)
                                elif line[26:28] == "00" and line[17:20] != "000" and line[24:26] != "00":
                                    write_described_instruction_32(assembly_description, json_32, line, "11101010010x1111xxxxxxxxxx00", code, address)
                                elif line[26:28] == "01":
                                    write_described_instruction_32(assembly_description, json_32, line, "11101010010x1111xxxxxxxxxx01", code, address)
                                elif line[26:28] == "10":
                                    write_described_instruction_32(assembly_description, json_32, line, "11101010010x1111xxxxxxxxxx10", code, address)
                                elif line[26:28] == "11":
                                    if line[17:20] == "000" and line[24:26] == "00":
                                        write_described_instruction_32(assembly_description, json_32, line, "11101010010x1111x000xxxx0011", code, address)
                                    else:
                                        write_described_instruction_32(assembly_description, json_32, line, "11101010010x1111xxxxxxxxxx11", code, address)
                                else:
                                    assembly_description.write("0x" + address + " : " + line + " : UNDEFINED or UNPREDICTABLE\n")
                        case "0011":
                            if line[12:16] != "1111":
                                write_described_instruction_32(assembly_description, json_32, line, "11101010011", code, address)
                            else:
                                write_described_instruction_32(assembly_description, json_32, line, "11101010011x1111", code, address)
                        case "0100":
                            if line[20:24] != "1111":
                                write_described_instruction_32(assembly_description, json_32, line, "11101010100", code, address)
                            elif line[20:24] == "1111" and line[11] == "1":
                                write_described_instruction_32(assembly_description, json_32, line, "111010101001xxxxxxxx1111", code, address)
                            else:
                                assembly_description.write("0x" + address + " : " + line + " : UNDEFINED or UNPREDICTABLE\n")
                        case "0110":
                            write_described_instruction_32(assembly_description, json_32, line, "11101010110", code, address)
                        case "1000":
                            if line[20:24] != "1111":
                                write_described_instruction_32(assembly_description, json_32, line, "11101011000", code, address)
                            elif line[20:24] == "1111" and line[11] == "1":
                                write_described_instruction_32(assembly_description, json_32, line, "111010110001xxxxxxxx1111", code, address)
                            else:
                                assembly_description.write("0x" + address + " : " + line + " : UNDEFINED or UNPREDICTABLE\n")
                        case "1010":
                            write_described_instruction_32(assembly_description, json_32, line, "11101011010", code, address)
                        case "1011":
                            write_described_instruction_32(assembly_description, json_32, line, "11101011011", code, address)
                        case "1101":
                            if line[20:24] != "1111":
                                write_described_instruction_32(assembly_description, json_32, line, "11101011101", code, address)
                            elif line[20:24] == "1111" and line[11] == "1":
                                write_described_instruction_32(assembly_description, json_32, line, "111010111011xxxxxxxx1111", code, address)
                            else:
                                assembly_description.write("0x" + address + " : " + line + " : UNDEFINED or UNPREDICTABLE\n")
                        case "1111":
                            write_described_instruction_32(assembly_description, json_32, line, "11101011110", code, address)
                        case _:
                            assembly_description.write("0x" + address + " : " + line + " : UNDEFINED or UNPREDICTABLE\n")
                # Data processing (modified immediate)
                elif line[:5] == "11110" and line[16] == "0":
                    if line[6] == "0":
                        match line[7:11]:
                            case "0000":
                                if line[20:24] != "1111":
                                    write_described_instruction_32(assembly_description, json_32, line, "11110x00000", code, address)
                                else:
                                    write_described_instruction_32(assembly_description, json_32, line, "11110x00000xxxxxxxxx1111", code, address)
                            case "0001":
                                write_described_instruction_32(assembly_description, json_32, line, "11110x00001", code, address)
                            case "0010":
                                if line[12:16] != "1111":
                                    write_described_instruction_32(assembly_description, json_32, line, "11110x00010", code, address)
                                else:
                                    write_described_instruction_32(assembly_description, json_32, line, "11110x00010x1111", code, address)
                            case "0011":
                                if line[12:16] != "1111":
                                    write_described_instruction_32(assembly_description, json_32, line, "11110x00011", code, address)
                                else:
                                    write_described_instruction_32(assembly_description, json_32, line, "11110x00011x1111", code, address)
                            case "0100":
                                if line[20:24] != "1111":
                                    write_described_instruction_32(assembly_description, json_32, line, "11110x00100", code, address)
                                else:
                                    write_described_instruction_32(assembly_description, json_32, line, "11110x00100xxxxxxxxx1111", code, address)
                            case "1000":
                                if line[20:24] != "1111":
                                    write_described_instruction_32(assembly_description, json_32, line, "11110x01000", code, address)
                                else:
                                    write_described_instruction_32(assembly_description, json_32, line, "11110x01000xxxxxxxxx1111", code, address)
                            case "1010":
                                write_described_instruction_32(assembly_description, json_32, line, "11110x01010", code, address)
                            case "1011":
                                write_described_instruction_32(assembly_description, json_32, line, "11110x01011", code, address)
                            case "1101":
                                if line[20:24] != "1111":
                                    write_described_instruction_32(assembly_description, json_32, line, "11110x01101", code, address)
                                else:
                                    write_described_instruction_32(assembly_description, json_32, line, "11110x01101xxxxxxxxx1111", code, address)
                            case "1110":
                                write_described_instruction_32(assembly_description, json_32, line, "11110x01110", code, address)
                            case _:
                                assembly_description.write("0x" + address + " : " + line + " : UNDEFINED or UNPREDICTABLE\n")
                    # Data processing (plain binary immediate)
                    else:
                        match line[7:12]:
                            case "00000":
                                if line[12:16] != "1111":
                                    write_described_instruction_32(assembly_description, json_32, line, "11110x10000011110", code, address)
                                else:
                                    write_described_instruction_32(assembly_description, json_32, line, "11110x100000xxxx0", code, address)
                            case "00100":
                                write_described_instruction_32(assembly_description, json_32, line, "11110x100100xxxx0", code, address)
                            case "01010":
                                if line[12:16] != "1111":
                                    write_described_instruction_32(assembly_description, json_32, line, "11110x101010xxxx0", code, address)
                                else:
                                    write_described_instruction_32(assembly_description, json_32, line, "11110x1010101111", code, address)
                            case "01100":
                                write_described_instruction_32(assembly_description, json_32, line, "11110x101100xxxx0", code, address)
                            case "10000":
                                write_described_instruction_32(assembly_description, json_32, line, "1111001100x0xxxx0xxxxxxxxx0", code, address)
                            case "10010":
                                if line[17:20] != "000" and line[24:26] != "00":
                                    write_described_instruction_32(assembly_description, json_32, line, "1111001100x0xxxx0xxxxxxxxx0", code, address)
                                else:
                                    assembly_description.write("0x" + address + " : " + line + " : UNDEFINED or UNPREDICTABLE\n")
                            case "10100":
                                write_described_instruction_32(assembly_description, json_32, line, "111100110100xxxx0xxxxxxxxx0", code, address)
                            case "10110":
                                if line[12:16] != "1111":
                                    write_described_instruction_32(assembly_description, json_32, line, "111100110110xxxx0xxxxxxxxx0", code, address)
                                else:
                                    write_described_instruction_32(assembly_description, json_32, line, "11110011011011110xxxxxxxxx0", code, address)
                            case "11000":
                                write_described_instruction_32(assembly_description, json_32, line, "1111001110x0xxxx0xxxxxxxxx0", code, address)
                            case "11010":
                                if line[17:20] != "000" and line[24:26] != "00":
                                    write_described_instruction_32(assembly_description, json_32, line, "1111001110x0xxxx0xxxxxxxxx0", code, address)
                                else:
                                    assembly_description.write("0x" + address + " : " + line + " : UNDEFINED or UNPREDICTABLE\n")
                            case "11100":
                                write_described_instruction_32(assembly_description, json_32, line, "111100111100xxxx0xxxxxxxxx0", code, address)
                            case _:
                                assembly_description.write("0x" + address + " : " + line + " : UNDEFINED or UNPREDICTABLE\n")
                # Branches and miscellaneous control
                elif line[:5] == "11110" and line[16] == "1":
                    if line[17:20] in ["000", "010"]:
                        if line[6:10] != "111":
                            write_described_instruction_32(assembly_description, json_32, line, "11110xxxxxxxxxxx10x0", code, address)
                        elif line[5:12] == "011100":
                            write_described_instruction_32(assembly_description, json_32, line, "11110011100", code, address)
                        elif line[5:12] == "011111":
                            write_described_instruction_32(assembly_description, json_32, line, "11110011111", code, address)
                        elif line[5:12] == "0111010":
                            if line[21:24] == "000":
                                if line[24:28] == "1111":
                                    write_described_instruction_32(assembly_description, json_32, line, "111100111010xxxx10x1x0001111", code, address)
                                match line[24:]:
                                    case "00000000":
                                        write_described_instruction_32(assembly_description, json_32, line, "111100111010xxxx10x0x00000000000", code, address)
                                    case "00000001":
                                        write_described_instruction_32(assembly_description, json_32, line, "111100111010xxxx10x0x00000000001", code, address)
                                    case "00000010":
                                        write_described_instruction_32(assembly_description, json_32, line, "111100111010xxxx10x0x00000000010", code, address)
                                    case "00000011":
                                        write_described_instruction_32(assembly_description, json_32, line, "111100111010xxxx10x0x00000000011", code, address)
                                    case "00000100":
                                        write_described_instruction_32(assembly_description, json_32, line, "111100111010xxxx10x0x00000000100", code, address)
                                    case _:
                                        assembly_description.write("0x" + address + " : " + line + " : UNDEFINED or UNPREDICTABLE\n")
                            else:
                                assembly_description.write("0x" + address + " : " + line + " : UNDEFINED or UNPREDICTABLE\n")
                        elif line[5:12] == "0111011":
                            match line[24:28]:
                                case "0010":
                                    write_described_instruction_32(assembly_description, json_32, line, "111100111011xxxx10x0xxxx0010", code, address)
                                case "0100":
                                    write_described_instruction_32(assembly_description, json_32, line, "111100111011xxxx10x0xxxx0100", code, address)
                                case "0101":
                                    write_described_instruction_32(assembly_description, json_32, line, "111100111011xxxx10x0xxxx0101", code, address)
                                case "0110":
                                    write_described_instruction_32(assembly_description, json_32, line, "111100111011xxxx10x0xxxx0110", code, address)
                                case _:
                                    assembly_description.write("0x" + address + " : " + line + " : UNDEFINED or UNPREDICTABLE\n")
                        else:
                            assembly_description.write("0x" + address + " : " + line + " : UNDEFINED or UNPREDICTABLE\n")
                    elif line[17:20] in ["001", "011"]:
                        write_described_instruction_32(assembly_description, json_32, line, "11110xxxxxxxxxxx10x1", code, address)
                    elif line[17:20] in ["101", "111"]:
                        write_described_instruction_32(assembly_description, json_32, line, "11110xxxxxxxxxxx11x1", code, address)
                    else:
                        assembly_description.write("0x" + address + " : " + line + " : UNDEFINED or UNPREDICTABLE\n")
                # Store single data item
                elif line[:8] == "11111000" and line[11] == "0":
                    if line[8:12] == "100" or (line[8:12] == "000" and line[20] == "1"):
                        write_described_instruction_32(assembly_description, json_32, line, "11111000100", code, address)
                    elif line[8:12] == "000" and line[20] == "0":
                        write_described_instruction_32(assembly_description, json_32, line, "11111000000", code, address)
                    elif line[8:12] == "101" or (line[8:12] == "001" and line[20] == "1"):
                        write_described_instruction_32(assembly_description, json_32, line, "11111000101", code, address)
                    elif line[8:12] == "001" and line[20] == "0":
                        write_described_instruction_32(assembly_description, json_32, line, "11111000001", code, address)
                    elif line[8:12] == "110" or (line[8:12] == "010" and line[20] == "1"):
                        write_described_instruction_32(assembly_description, json_32, line, "11111000110", code, address)
                    else:
                        assembly_description.write("0x" + address + " : " + line + " : UNDEFINED or UNPREDICTABLE\n")
                # STR et LDR
                elif line[:7] == "1111100":
                    # Load Byte
                    if line[9:12] == "001":
                        if line[7] == "0" and line[12:16] == "1111" and line[16:20] != "1111":
                            write_described_instruction_32(assembly_description, json_32, line, "11111000x0011111", code, address)
                        elif (line[7:9] == "01" and line[12:16] != "1111" and line[16:20] != "1111") or (line[7:9] == "00" and line[20] == "1" and line[23] == "1" and line[12:16] != "1111") or (line[7:9] == "00" and line[20:24] == "1100" and line[12:16] != "1111" and line[16:20] != "1111"):
                            write_described_instruction_32(assembly_description, json_32, line, "111110000001", code, address)
                        elif line[7:9] == "00" and line[20:26] == "000000" and line[12:16] != "1111" and line[16:20] != "1111":
                            write_described_instruction_32(assembly_description, json_32, line, "111110000001xxxxxxxx000000", code, address)
                        elif line[7] == "1" and line[12:16] == "1111" and line[16:20] != "1111":
                            write_described_instruction_32(assembly_description, json_32, line, "11111001x0011111", code, address)
                        elif (line[7:9] == "11" and line[12:16] != "1111" and line[16:20] != "1111") or (line[7:9] == "10" and line[20] == "1" and line[23] == "1" and line[12:16] != "1111") or (line[7:9] == "10" and line[20:24] == "1100" and line[12:16] != "1111" and line[16:20] != "1111"):
                            write_described_instruction_32(assembly_description, json_32, line, "111110011001", code, address)
                        elif line[7:9] == "10" and line[20:26] == "000000" and line[12:16] != "1111" and line[16:20] != "1111":
                            write_described_instruction_32(assembly_description, json_32, line, "111110010001", code, address)
                        elif line[7:9] == "00" and line[20:24] == "1110" and line[12:16] != "1111":
                            write_described_instruction_32(assembly_description, json_32, line, "111110000001xxxxxxxx1110", code, address)
                        elif (line[7:9] == "10" and line[12:16] != "1111" and line[16:20] == "1111") or (line[7:9] == "00" and line[20:24] == "1100"and line[12:16] != "1111" and line[16:20] == "1111") or (line[7] == "0" and line[12:16] == "1111" and line[16:20] == "1111"):
                            write_described_instruction_32(assembly_description, json_32, line, "11111000x00111111111", code, address)
                        elif line[7:9] == "00" and line[20:26] == "000000" and line[12:16] != "1111" and line[16:20] == "1111":
                            write_described_instruction_32(assembly_description, json_32, line, "111110000001xxxx1111000000", code, address)
                        elif (line[7:9] == "11" and line[12:16] != "1111" and line[16:20] == "1111") or (line[7:9] == "10" and line[20:24] == "1100"and line[12:16] != "1111" and line[16:20] == "1111") or (line[7] == "1" and line[12:16] == "1111" and line[16:20] == "1111"):
                            write_described_instruction_32(assembly_description, json_32, line, "111110011001xxxx1111", code, address)
                        elif line[7:9] == "10" and line[20:26] == "000000" and line[12:16] != "1111" and line[16:20] == "1111":
                            write_described_instruction_32(assembly_description, json_32, line, "111110010001xxxx1111000000", code, address)
                        else:
                            assembly_description.write("0x" + address + " : " + line + " : UNDEFINED or UNPREDICTABLE\n")
                    # Load halfword
                    elif line[9:12] == "011":
                        if line[7] == "0" and line[12:16] == "1111" and line[16:20] != "1111":
                            write_described_instruction_32(assembly_description, json_32, line, "11111000x0111111", code, address)
                        elif (line[7:9] == "01" and line[12:16] != "1111" and line[16:20] != "1111") or (line[7:9] == "00" and line[20] == "1" and line[23] == "1" and line[12:16] != "1111" and line[16:20] != "1111") or (line[7:9] == "00" and line[20:24] == "1100" and line[12:16] != "1111" and line[16:20] != "1111"):
                            write_described_instruction_32(assembly_description, json_32, line, "111110001011xxxxxxxx000000", code, address)
                        elif line[7:9] == "00" and line[20:26] == "000000" and line[12:16] != "1111" and line[16:20] != "1111":
                            write_described_instruction_32(assembly_description, json_32, line, "111110000011", code, address)
                        elif (line[7:9] == "11" and line[12:16] != "1111" and line[16:20] != "1111") or (line[7:9] == "10" and line[20] == "1" and line[23] == "1" and line[12:16] != "1111" and line[16:20] != "1111") or (line[7:9] == "10" and line[20:24] == "1100" and line[12:16] != "1111" and line[16:20] != "1111"):
                            write_described_instruction_32(assembly_description, json_32, line, "111110011011", code, address)
                        elif line[7] == "0" and line[12:16] == "1111" and line[16:20] != "1111":
                            write_described_instruction_32(assembly_description, json_32, line, "11111000x011", code, address)
                        elif line[7:9] == "10" and line[20:26] == "000000" and line[12:16] != "1111" and line[16:20] != "1111":
                            write_described_instruction_32(assembly_description, json_32, line, "111110010011", code, address)
                        elif line[7:9] == "00" and line[20:24] == "1110" and line[12:16] != "1111" and line[16:20] != "1111":
                            write_described_instruction_32(assembly_description, json_32, line, "111110000011xxxxxxxx1110", code, address)
                        elif line[7:9] == "00" and line[20:24] == "1110" and line[12:16] != "1111" and line[16:20] != "1111":
                            write_described_instruction_32(assembly_description, json_32, line, "111110010011xxxxxxxx1110", code, address)
                        else:
                            assembly_description.write("0x" + address + " : " + line + " : UNDEFINED or UNPREDICTABLE\n")
                    # Load word
                    elif line[9:12] == "101":
                        if line[7] == "0" and line[12:16] == "1111":
                            write_described_instruction_32(assembly_description, json_32, line, "11111000x1011111", code, address)
                        elif ((line[7:9] == "01") or (line[7:9] == "00" and line[20] == "1" and line[23] == "1") or (line[7:9] == "11" and line[20:24] == "1100")) and line[12:16] != "1111":
                            write_described_instruction_32(assembly_description, json_32, line, "111110001101", code, address)
                        elif line[7:9] == "01" and line[20:26] == "000000" and line[12:16] != "1111":
                            write_described_instruction_32(assembly_description, json_32, line, "111110001101xxxxxxxx000000", code, address)
                        elif line[7:9] == "00" and line[20:24] == "1110" and line[12:16] != "1111":
                            write_described_instruction_32(assembly_description, json_32,line, "111110000101xxxxxxxx1110", code, address)
                        else:
                            assembly_description.write("0x" + address + " : " + line + " : UNDEFINED or UNPREDICTABLE\n")
                    else:
                        assembly_description.write("0x" + address + " : " + line + " : UNDEFINED or UNPREDICTABLE\n")
                # Store single data item
                elif line[:8] == "11111000":
                    if (line[8:11] == "100") or (line[8:11] == "000" and line[20] == "1"):
                        write_described_instruction_32(assembly_description, json_32, line, "11111000100", code, address)
                    elif line[8:11] == "000" and line[20] == "0":
                        write_described_instruction_32(assembly_description, json_32, line, "11111000000", code, address)
                    elif (line[8:11] == "101") or (line[8:11] == "001" and line[20] == "1"):
                        write_described_instruction_32(assembly_description, json_32, line, "11111000101", code, address)
                    elif line[8:11] == "001" and line[20] == "0":
                        write_described_instruction_32(assembly_description, json_32, line, "11111000001", code, address)
                    elif (line[8:11] == "110") or (line[8:11] == "010" and line[20] == "1"):
                        write_described_instruction_32(assembly_description, json_32, line, "11111000110", code, address)
                    elif line[8:11] == "010":
                        write_described_instruction_32(assembly_description, json_32, line, "11111000010", code, address)
                # Data processing (register)
                elif line[:8] == "11111010" and line[16:20] == "1111":
                    if line[24:28] == "0000":
                        match line[8:11]:
                            case "000":
                                write_described_instruction_32(assembly_description, json_32, line, "11111010000", code, address)
                            case "001":
                                write_described_instruction_32(assembly_description, json_32, line, "11111010001", code, address)
                            case "010":
                                write_described_instruction_32(assembly_description, json_32, line, "11111010010", code, address)
                            case "011":
                                write_described_instruction_32(assembly_description, json_32, line, "11111010011", code, address)
                            case _:
                                assembly_description.write("0x" + address + " : " + line + " : UNDEFINED or UNPREDICTABLE\n")
                    elif line[12:16] == "1111" and line[24] == "1":
                        match line[8:12]:
                            case "0000":
                                write_described_instruction_32(assembly_description, json_32, line, "11111010000011111111xxxx1", code, address)
                            case "0001":
                                write_described_instruction_32(assembly_description, json_32, line, "11111010000111111111xxxx1", code, address)
                            case "0100":
                                write_described_instruction_32(assembly_description, json_32, line, "11111010010011111111xxxx1", code, address)
                            case "0101":
                                write_described_instruction_32(assembly_description, json_32, line, "11111010010111111111xxxx1", code, address)
                            case _:
                                assembly_description.write("0x" + address + " : " + line + " : UNDEFINED or UNPREDICTABLE\n")
                    else:
                        assembly_description.write("0x" + address + " : " + line + " : UNDEFINED or UNPREDICTABLE\n")
                # Miscellaneous operations
                elif line[:10] == "1111101010":
                    if line[10:12] == "01":
                        match line[26:28]:
                            case "00":
                                write_described_instruction_32(assembly_description, json_32, line, "111110101001xxxx1111xxxx1000", code, address)
                            case "01":
                                write_described_instruction_32(assembly_description, json_32, line, "111110101001xxxx1111xxxx1001", code, address)
                            case "10":
                                write_described_instruction_32(assembly_description, json_32, line, "111110101001xxxx1111xxxx1010", code, address)
                            case "11":
                                write_described_instruction_32(assembly_description, json_32, line, "111110101001xxxx1111xxxx1011", code, address)
                            case _:
                                assembly_description.write("0x" + address + " : " + line + " : UNDEFINED or UNPREDICTABLE\n")
                    elif line[10:12] == "11" and line[26:28] == "00":
                        write_described_instruction_32(assembly_description, json_32, line, "111110101011", code, address)
                    else:
                        assembly_description.write("0x" + address + " : " + line + " : UNDEFINED or UNPREDICTABLE\n")
                # Multiply, multiply accumulate, and absolute difference
                elif line[:9] == "111110110":
                    if line[9:12] == "000" and line[26:28] == "00" and line[16:20] == "1111":
                        write_described_instruction_32(assembly_description, json_32, line, "111110110000xxxx1111xxxx0000", code, address)
                    elif line[9:12] == "000" and line[26:28] == "00" and line[16:20] != "1111":
                        write_described_instruction_32(assembly_description, json_32, line, "111110110000xxxxxxxxxxxx0000", code, address)
                    elif line[9:12] == "000" and line[26:28] == "01":
                        write_described_instruction_32(assembly_description, json_32, line, "111110110000xxxxxxxxxxxx0001", code, address)
                    else:
                        assembly_description.write("0x" + address + " : " + line + " : UNDEFINED or UNPREDICTABLE\n")
                # Long multiply, long multiply accumulate, and divide
                elif line[:9] == "111110111":
                    if line[9:12] == "000" and line[24:28] == "0000":
                        write_described_instruction_32(assembly_description, json_32, line, "111110111000xxxxxxxxxxxx0000", code, address)
                    elif line[9:12] == "001" and line[24:28] == "1111":
                        write_described_instruction_32(assembly_description, json_32, line, "111110111001xxxxxxxxxxxx1111", code, address)
                    elif line[9:12] == "010" and line[24:28] == "0000":
                        write_described_instruction_32(assembly_description, json_32, line, "111110111010xxxxxxxxxxxx0000", code, address)
                    elif line[9:12] == "011" and line[24:28] == "1111":
                        write_described_instruction_32(assembly_description, json_32, line, "111110111011xxxxxxxxxxxx1111", code, address)
                    elif line[9:12] == "100" and line[24:28] == "0000":
                        write_described_instruction_32(assembly_description, json_32, line, "111110111100xxxxxxxxxxxx0000", code, address)
                    elif line[9:12] == "110" and line[24:28] == "0000":
                        write_described_instruction_32(assembly_description, json_32, line, "111110111110xxxxxxxxxxxx0000", code, address)
                    else:
                        assembly_description.write("0x" + address + " : " + line + " : UNDEFINED or UNPREDICTABLE\n")
                # Coprocessor instructions
                elif line[:3] == "111" and line[4:6] == "11":
                    if line[6] == "0" and line[11] == "0" and line[6:9] != "000" and line[11] != "0":
                        write_described_instruction_32(assembly_description, json_32, line, "111x110xxxx0", code, address)
                    elif line[6] == "0" and line[11] == "1" and line[6:9] != "000" and line[11] != "0":
                        write_described_instruction_32(assembly_description, json_32, line, "111x110xxxx0", code, address)
                    elif line[6:12] == "000100":
                        write_described_instruction_32(assembly_description, json_32, line, "111x11000100", code, address)
                    elif line[6:12] == "000101":
                        write_described_instruction_32(assembly_description, json_32, line, "111x11000101", code, address)
                    elif line[6:8] == "10" and line[27] == "0":
                        write_described_instruction_32(assembly_description, json_32, line, "111x1110xxxxxxxxxxxxxxxxxxx0", code, address)
                    elif line[6:8] == "10" and line[27] == "1":
                        if line[11] == "0":
                            write_described_instruction_32(assembly_description, json_32, line, "111x1110xxx0xxxxxxxxxxxxxxx1", code, address)
                        else:
                            write_described_instruction_32(assembly_description, json_32, line, "111x1110xxx1xxxxxxxxxxxxxxx1", code, address)
                    else:
                        assembly_description.write("0x" + address + " : " + line + " : UNDEFINED or UNPREDICTABLE\n")
                else:
                    assembly_description.write("0x" + address + " : " + line + " : UNDEFINED or UNPREDICTABLE\n")
        else:  # 16-bits
            # Shift (immediate), add, subtract, move, and compare
            if line[:2] == "00":
                if line[2:5] in ["000", "001", "010", "001", "100", "101", "110", "111"]:
                    write_described_instruction_16(assembly_description, json_16, line, 5, code, address)
                elif line[2:7] in ["01100", "01101", "01110", "01111"]:
                    write_described_instruction_16(assembly_description, json_16, line, 7, code, address)
                else:
                    assembly_description.write("0x" + address + " : " + line + " : UNDEFINED\n")
            # Data processing
            elif line[:6] == "010000":
                write_described_instruction_16(assembly_description, json_16, line, 10, code, address)
            # Special data instructions and branch and exchange
            elif line[:6] == "010001":
                if line[6:8] in ["00", "10"]:
                    write_described_instruction_16(assembly_description, json_16, line, 8, code, address)
                elif line[6:9] in ["011", "110", "111"]:
                    write_described_instruction_16(assembly_description, json_16, line, 9, code, address)
                elif line[6:10] == "0101":
                    write_described_instruction_16(assembly_description, json_16, line, 10, code, address)
                else:
                    assembly_description.write("0x" + address + " : " + line + " : UNDEFINED\n")
            # Load / store single data item
            elif line[:4] == "0101":
                write_described_instruction_16(assembly_description, json_16, line, 7, code, address)
            # Load / store single data item
            elif line[:4] in ["0110", "0111", "1000", "1001"]:
                write_described_instruction_16(assembly_description, json_16, line, 5, code, address)
            # Miscellaneous 16-bit instructions
            elif line[:4] == "1011":
                if line[4:11] == "0110011":
                    write_described_instruction_16(assembly_description, json_16, line, 11, code, address)
                elif line[4:10] in ["001000", "001001", "001010", "001011", "101000", "101001", "101011"]:
                    write_described_instruction_16(assembly_description, json_16, line, 10, code, address)
                elif line[4:9] in ["00000", "00001"]:
                    write_described_instruction_16(assembly_description, json_16, line, 9, code, address)
                elif line[4:8] in ["0001", "0011", "1001", "1011", "1110"]:
                    write_described_instruction_16(assembly_description, json_16, line, 8, code, address)
                elif line[4:7] in ["010", "110"]:
                    write_described_instruction_16(assembly_description, json_16, line, 7, code, address)
                elif line[4:8] == "1111":
                    if line[12:16] == "0000":
                        if line[8:12] in ["0000", "0001", "0010", "0011", "0100"]:
                            write_described_instruction_16(assembly_description, json_16, line, 16, code, address)
                        else:
                            assembly_description.write("0x" + address + " : " + line + " : UNDEFINED\n")
                    else:
                        write_described_instruction_16(assembly_description, json_16, line, 8, code, address)
                elif line[:4] == "1100":
                    if line[4:8] == "1111":
                        write_described_instruction_16(assembly_description, json_16, line, 8, code, address)
                    elif line[4:7] not in ["1110", "1110"]:
                        write_described_instruction_16(assembly_description, json_16, line, 7, code, address)
                    else:
                        assembly_description.write("0x" + address + " : " + line + " : UNDEFINED\n")
                else:
                    assembly_description.write("0x" + address + " : " + line + " : UNDEFINED\n")
            elif line[:4] == "1101":
                if line[4:8] == "1111":
                    write_described_instruction_16(assembly_description, json_16, line, 8, code, address)
                elif line[4:7] != "111":
                    write_described_instruction_16(assembly_description, json_16, line, 4, code, address)
                else:
                    assembly_description.write("0x" + address + " : " + line + " : UNDEFINED\n")
            # Unconditional branch, Generate PC-relative address, Generate SP-relative address, Store multiple registers, Load multiple registers, LDR (literal)
            elif line[:5] in ["11100", "10100", "10101", "11000", "11001", "01001"]:
                write_described_instruction_16(assembly_description, json_16, line, 5, code, address)
            else:
                assembly_description.write("0x" + address + " : " + line + " : UNDEFINED\n")

#! /usr/bin/python

import struct
import argparse
from xml.dom.minidom import *


header = '''\
#! /usr/bin/python

import struct
from types import *

class LLRPError(Exception):
    def __str__(self, message = ""):
        return message

class LLRPResponseError(LLRPError):
    def __str__(self, message = ""):
        return message

class LLRPMessage(dict):
    def __repr__(self):
        return llrp_data2xml(self)

def reverse_dict(data):
    atad = {}
    for m in data:
        i = data[m]
        atad[i] = m
    return atad

def decode(data):
    return Parameter_struct[data]['decode']


def encode(data):
    return Parameter_struct[data]['encode']

def llrp_data2xml(msg):
    def __llrp_data2xml(msg, name, level=0):
        tabs = '\\t' * level
        str = tabs + '<%s>\\n' % name
        if Message_struct.has_key(name):
            fields = Message_struct[name]['fields']
        else:
            fields = Parameter_struct[name]['fields']
        for p in fields:
            try:
                sub = msg[p]
            except KeyError:
                continue

            if type(sub) == DictionaryType:
                str += __llrp_data2xml(sub, p, level + 1)
            elif type(sub) == ListType and len(sub) > 0 and\\
                    type(sub[0]) == DictionaryType:
                for e in sub:
                    str += __llrp_data2xml(e, p, level + 1)
            else:
                str += tabs + '\\t<%s>%s</%s>\\n' % (p, sub, p)
                
        str += tabs + '</%s>\\n' % name
        return str
    ans = ''
    for p in msg:
        ans += __llrp_data2xml(msg[p], p)
    return ans[: -1]

def reverse_Message_struct():
    for m in Message_struct:
        i=Message_struct[m]['type']
        Message_Type2Name[i]=m


Message_struct = {}
Parameter_struct = {}
Message_Type2Name = {}


'''



ChoiceDefDict = {}

def GenChoiceDefDict(choiceDefinition):
    for c in choiceDefinition:
        choiceName = c.getAttribute("name")
        ChoiceDefDict[choiceName] = []
        childs = c.getElementsByTagName("parameter")
        for child in childs:
            ChoiceDefDict[choiceName].append(child.getAttribute("type"))


def encodeNomalFieldOfList(elementList):
    typeName = elementList[0].getAttribute("type")
    packStr = typeToPackStr(typeName)
    name = elementList[0].getAttribute("name")
    enumName = elementList[0].getAttribute("enumeration")
    if enumName:
        result = 'data += struct.pack("' + packStr + '", ' + \
            enumName + '_Name2Type[par["' + name + '"]])\n    '
    else:
        result = 'data += struct.pack("' + \
            packStr + '", par["' + name + '"])\n    '
    return result, elementList[1:]


def typeToPackStr(typeName):
    typeList = ['u8', 'u16', 'u32', 'u64', 's8', 's16', 's32', 's64']
    packStrList = ['!B', '!H', '!I', '!Q', '!b', '!h', '!i', '!q']
    return packStrList[typeList.index(typeName)]


def typeToPackLen(typeName):
    typeList = ['u8', 'u16', 'u32', 'u64', 's8', 's16', 's32', 's64']
    packStrList = ['!B', '!H', '!I', '!Q', '!b', '!h', '!i', '!q']
    packStr = packStrList[typeList.index(typeName)]
    return struct.calcsize(packStr)


def decodeParameterDefinition(paraDef):
    elementList = elementOfChildNodes(paraDef.childNodes)
    result = ''
    while True:
        if not elementList:
            break
        data, elementList = decodeElementList(elementList)
        result += data
    return result


def decodeTVEncodingParameterDefinition(paraDef):
    elementList = elementOfChildNodes(paraDef.childNodes)
    paraName = paraDef.getAttribute("name")
    result = ''
    result += "type = ord(data[0])&0x7f\n    "
    result += "if type != Parameter_struct['"  + paraName + "']['type']:\n    "
    result += "    return par, data\n    "
    result += "data = data[1:]\n    "
    for element in elementList:
        if element.tagName == "field":
            name = element.getAttribute("name")
            typeName = element.getAttribute("type")
            if typeName != "u96":                
                packStr = typeToPackStr(typeName)
                packLen = typeToPackLen(typeName) 
                result += "(" + name + ",) = struct.unpack('" + packStr + "'," +  "data[0:" +  str(packLen) + "])\n    "
                result += "par['" + name + "'] = " + name + "\n    "
                result += "data = data[" + str(packLen) + ":]\n    "
            else:
                result += "par['" + name + "'] = data[0:12]\n    "
                result += "data = data[" + str(12) + ":]\n    "
    result += 'return par, data\n\n'
    return result

def decodeElementList(elementList):
    if elementList[0].tagName == "field":
        return decodeFieldOfList(elementList)
    elif elementList[0].tagName == "parameter":
        return decodeParameterOfList(elementList)
    elif elementList[0].tagName == "choice":
        return decodeChoiceOfList(elementList)
    else:
        return '', elementList[1:]


def decodeFieldOfList(elementList):
    typeName = elementList[0].getAttribute("type")
    if typeName in ['u8', 'u16', 'u32', 'u64', 's8', 's16', 's32', 's64']:
        return decodeNomalFieldOfList(elementList)
    elif typeName == 'u1' or typeName == 'u2':
        return decodeBitFieldOfList(elementList)
    else:
        return decodeArrayFieldOfList(elementList)
    return '', elementList[1:]


def decodeNomalFieldOfList(elementList):
    name = elementList[0].getAttribute("name")
    typeName = elementList[0].getAttribute("type")
    packStr = typeToPackStr(typeName)
    packLen = typeToPackLen(typeName)
    result = '(' + name + ',) = struct.unpack("' + packStr + \
        '", body[0:' + str(packLen) + '])\n    '
    if elementList[0].getAttribute("enumeration"):
        result += 'par["' + name + '"] = ' + elementList[0].getAttribute(
            "enumeration") + '_Type2Name[' + name + ']\n    '
    else:
        result += 'par["' + name + '"] = ' + name + '\n    '
    result += 'body = body[' + str(packLen) + ':]\n    '
    return result, elementList[1:]


def decodeBitFieldOfList(elementList):
    result = ''
    numOfBits = 0
    for ele in elementList:
        if ele.getAttribute("type") == "u1":
            numOfBits += 1
        elif ele.getAttribute("type") == "u2":
            numOfBits += 2
        else:
            break
    numOfBytes = numOfBits / 8
    if numOfBits % 8 != 0:
        numOfBytes += 1
    i = 0
    j = 0
    for b in range(numOfBytes):
        if i > numOfBits:
            break
        seg = '(e,) = struct.unpack("!B", body[0:1])\n    '
        x = 0
        while x < 8:
            i = b * 8 + x
            if i >= numOfBits:
                break
            if elementList[j].getAttribute("type") == "u2":
                x += 1
                seg += 'par["' + elementList[j].getAttribute(
                "name") + '"] = (e>>' + str(7 - x) + ")&3\n    "
            else:
                seg += 'par["' + elementList[j].getAttribute(
                "name") + '"] = (e>>' + str(7 - x) + ")&1\n    "
            j += 1
            x += 1
        result += seg + "body = body[1:]\n    "
    return result, elementList[numOfBits:]


def decodeArrayFieldOfList(elementList):
    typeName = elementList[0].getAttribute("type")
    result = ''
    if typeName == 'u1v':
        result,  elementList = decodeBitArrayFieldOfList(elementList)
    else:
        result,  elementList = decodeNormalArrayFieldOfList(elementList)
    return result, elementList


def decodeBitArrayFieldOfList(elementList):
    name = elementList[0].getAttribute("name")
    result = '(bitArrayLen, ) = struct.unpack("!H", body[0:2])\n    '
    result += 'par["' + name + '"] = {}\n    '
    result += 'par["' + name + '"]["BitLen"] = bitArrayLen\n    '
    result += "body = body[2:]\n    "
    result += "if (bitArrayLen%8) == 0:\n        "
    result += "bitArrayLen  = bitArrayLen/8\n    "
    result += "else:\n        "
    result += "bitArrayLen = bitArrayLen/8 + 1\n    "
    result += 'par["' + name + '"]["Data"] = body[0:bitArrayLen' + ']\n    '
    result += 'body = body[bitArrayLen' + ':]\n    '
    return result, elementList[1:]


def decodeNormalArrayFieldOfList(elementList):
    typeList = ['u8v', 's8v', 'u16v', 's16v', 'u32v', 's32v',
                'u64v', 's64v', 'utf8v', 'bytesToEnd', 'u96', 'u2']
    packStrList = ['!B', '!b', '!H', '!h', '!I',
                   '!i', '!Q', '!q', '!s', '!s', '!s', '!s']
    name = elementList[0].getAttribute("name")
    typeName = elementList[0].getAttribute("type")
    packStr = packStrList[typeList.index(typeName)]
    packLen = struct.calcsize(packStr)
    result = '(arrayLen, ) = struct.unpack("!H", body[0:2])\n    '
    result += "body = body[2:]\n    "
    result += 'par["' + name + '"] = body[0:arrayLen*' + \
        str(packLen) + ']\n    '
    result += 'body = body[arrayLen*' + str(packLen) + ':]\n    '
    return result, elementList[1:]


def decodeParameterOfList(elementList):
    name = elementList[0].getAttribute("type")
    repeat = elementList[0].getAttribute("repeat")
    result = ''
    if repeat == "1":
        result += 'ret, body = decode("' + name + '")(body)\n    '
        result += 'if ret:\n        '
        result += 'par["' + name + '"] = ret\n    '
        result += 'else:\n        '
        result += 'raise LLRPError("missing ' + name + ' parameter")\n    '
    elif repeat == "0-1":
        result += 'ret, body = decode("' + name + '")(body)\n    '
        result += 'if ret:\n        '
        result += 'par["' + name + '"] = ret\n    '
    elif repeat == "0-N" or repeat == "1-N":
        result += 'par["' + name + '"] = []\n    '
        result += "while True:\n        "
        result += 'ret, body = decode("' + name + '")(body)\n        '
        result += 'if ret:\n            '
        result += 'par["' + name + '"].append(ret)\n        '
        result += 'else:\n            '
        result += 'break\n    '
    return result, elementList[1:]


def decodeChoiceOfList(elementList):
    choiceName = elementList[0].getAttribute("type")
    repeat = elementList[0].getAttribute("repeat")
    choiceList = ChoiceDefDict[choiceName]
    result = ''
    if repeat == "0-N" or repeat == "1-N":
        for name in choiceList:
            result += 'par["' + name + '"] = []\n    '
        result += "flag = True\n    "
        result += "while flag:\n        "
        result += "flag = False\n        "
    for name in choiceList:
        if repeat == "0-1" or repeat == "1":
            result += 'ret, body = decode("' + name + '")(body)\n    '
            result += 'if ret:\n        '
            result += 'par["' + name + '"] = ret\n    '
        elif repeat == "0-N" or repeat == "1-N":
            result += 'ret, body = decode("' + name + '")(body)\n        '
            result += 'if ret:\n            '
            result += 'par["' + name + '"].append(ret)\n            '
            result += 'flag = True\n        '
    result += "\n    "
    return result, elementList[1:]


def Name2TypeByNode(enumDef):
    s = ""
    s += enumDef.getAttribute("name") + "_Name2Type = {\n"
    for entry in enumDef.getElementsByTagName("entry"):
        s += "\t'" + entry.getAttribute("name") + \
            "' : " + entry.getAttribute("value") + ",\n"
    s += "}\n\n"
    s += enumDef.getAttribute("name")
    s += "_Type2Name = reverse_dict(" + \
        enumDef.getAttribute("name") + "_Name2Type)"
    s += "\n\n"
    return s


def EnumName2TypeDict(enumList):
    dictStr = ""
    for enumDef in enumList:
        dictStr += Name2TypeByNode(enumDef)
    return dictStr


def elementOfChildNodes(childNodesList):
    elementList = []
    for ele in childNodesList:
        if ele.nodeType == 1:
            elementList.append(ele)
    return elementList


def ParameterStructDefs(paraDefList):
    s = ""
    for paraDef in paraDefList:
        s += "Parameter_struct['" + paraDef.getAttribute("name") + "'] = {\n"
        s += "    'type' : " + paraDef.getAttribute("typeNum") + ",\n"
        s += "    'fields':  [ \n        'Type', \n    "
        elementList = elementOfChildNodes(paraDef.childNodes)
        for element in elementList:
            if element.tagName == 'field':
                s += "    '" + element.getAttribute("name") + "',\n     "
            elif element.hasAttribute("type"):
                s += "    '" + element.getAttribute("type") + "',\n     "
            else:
                pass

        s += "],\n"
        s += "    'encode' : encode_" + paraDef.getAttribute("name") + ",\n"
        s += "    'decode' : decode_" + paraDef.getAttribute("name") + ",\n"
        s += "\n}\n\n"
    return s


def MessageStructDefs(messageDefList):
    s = ""
    for msgDef in messageDefList:
        s += "Message_struct['" + msgDef.getAttribute("name") + "'] = {\n"
        s += "    'type' :  " + msgDef.getAttribute("typeNum") + ",\n"
        s += "    'fields':  [ 'Rsvd', 'Ver', 'Type', 'ID',  \n    "
        elementList = elementOfChildNodes(msgDef.childNodes)
        for element in elementList:
            if element.tagName == 'field':
                s += "'" + element.getAttribute("name") + "',\n     "
            elif element.hasAttribute("type"):
                s += "'" + element.getAttribute("type") + "',\n     "
            else:
                pass

        s += "],\n"
        s += "    'encode' : encode_" + msgDef.getAttribute("name") + ",\n"
        s += "    'decode' : decode_" + msgDef.getAttribute("name") + ",\n"
        s += "\n}\n\n"
    return s


def encodeFieldOfList(elementList):
    typeName = elementList[0].getAttribute("type")
    if typeName in ['u8', 'u16', 'u32', 'u64', 's8', 's16', 's32', 's64']:
        return encodeNomalFieldOfList(elementList)
    elif typeName == 'u1' or typeName == 'u2':
        return encodeBitFieldOfList(elementList)
    elif typeName == 'u96':
        return encodeEpc96FieldOfList(elementList)
    else:
        return encodeArrayFieldOfList(elementList)


def encodeBitFieldOfList(elementList):
    result = ''
    numOfBits = 0
    for ele in elementList:
        if ele.getAttribute("type") == "u1":
            numOfBits += 1
        elif ele.getAttribute("type") == "u2":
            numOfBits += 2
        else:
            break
    numOfBytes = numOfBits / 8
    if numOfBits % 8 != 0:
        numOfBytes += 1
    i = 0
    j = 0
    for b in range(numOfBytes):
        if i > numOfBits:
            break
        seg = 'e = '
        x = 0        
        while x < 8:
            i = b * 8 + x
            if i >= numOfBits:
                break
            if elementList[j].getAttribute("type") == "u2":
                x += 1
            if elementList[j].getAttribute("enumeration"):
                seg += elementList[j].getAttribute("enumeration") + '_Name2Type[par["' + elementList[
                    j].getAttribute("name") + '"]]' + '<<' + str(7 - x) + '|'
            else:
                seg += 'par["' + elementList[j].getAttribute(
                    "name") + '"]' + '<<' + str(7 - x) + '|'
            x += 1
            j += 1
        result += seg + "0\n    "
        result += 'data += struct.pack("!B", e)\n    '

    return result, elementList[numOfBits:]

def encodeEpc96FieldOfList(elementList):
    result = ""
    return result





def encodeArrayFieldOfList(elementList):
    typeName = elementList[0].getAttribute("type")
    result = ''
    if typeName == 'u1v':
        result,  elementList = encodeBitArrayFieldOfList(elementList)
    else:
        result,  elementList = encodeNormalArrayFieldOfList(elementList)
    return result, elementList


def encodeNormalArrayFieldOfList(elementList):
    typeList = ['u8v', 's8v', 'u16v', 's16v', 'u32v', 's32v',
                'u64v', 's64v', 'utf8v', 'u96', 'bytesToEnd', 'u2']
    packStrList = ['!B', '!b', '!H', '!h', '!I',
                   '!i', '!Q', '!q', '!s', '!s', '!s', '!s']
    typeName = elementList[0].getAttribute("type")
    packStr = packStrList[typeList.index(typeName)]
    result = elementList[0].getAttribute(
        "name") + ' = par["' + elementList[0].getAttribute("name") + '"]\n    '
    result += "data += struct.pack('!H', len(" + \
        elementList[0].getAttribute("name") + "))\n    "
    result += "for x in " + elementList[0].getAttribute("name") + ":\n        "
    if not elementList[0].getAttribute("enumeration"):
        result += "data += struct.pack('" + packStr + "', x)\n\n    "
    else:
        result += "data += struct.pack('" + packStr + "', " + elementList[0].getAttribute("enumeration") +"_Name2Type[x])\n\n    "
    return result, elementList[1:]


def encodeBitArrayFieldOfList(elementList):
    name = elementList[0].getAttribute("name")
    result = ""
    result += 'data += struct.pack("!H", par["' + name + '"]["BitLen"])\n    '
    result += "data += par['" + name + "']['Data']\n    "
    return result, elementList[1:]


def encodeParameterOfList(elementList):
    name = elementList[0].getAttribute("type")
    repeat = elementList[0].getAttribute("repeat")
    result = ''
    if repeat == "1":
        result += 'data += encode("' + name + '")(par["' + name + '"])\n    '
    elif repeat == "0-1":
        result += 'if par.has_key("' + name + '"):\n        '
        result += 'data += encode("' + name + '")(par["' + name + '"])\n    '
    elif repeat == "0-N":
        result += 'if par.has_key("' + name + '"):\n        '
        result += 'for x in par["' + name + '"]:\n            '
        result += 'data += encode("' + name + '")(x)\n    '
    elif repeat == "1-N":
        result += 'for x in par["' + name + '"]:\n        '
        result += 'data += encode("' + name + '")(x)\n    '
    return result, elementList[1:]


def encodeChoiceOfList(elementList):
    choiceName = elementList[0].getAttribute("type")
    repeat = elementList[0].getAttribute("repeat")
    choiceList = ChoiceDefDict[choiceName]
    result = ''
    for name in choiceList:
        if repeat == "0-1" or repeat == "1":
            result += 'if par.has_key("' + name + '"):\n        '
            result += 'data += encode("' + name + \
                '")(par["' + name + '"])\n    '
        elif repeat == "0-N" or repeat == "1-N":
            result += 'if par.has_key("' + name + '"):\n        '
            result += 'for x in par["' + name + '"]:\n            '
            result += 'data += encode("' + name + '")(x)\n    '
    return result, elementList[1:]


def encodeElementList(elementList):
    if elementList[0].tagName == "field":
        return encodeFieldOfList(elementList)
    elif elementList[0].tagName == "parameter":
        return encodeParameterOfList(elementList)
    elif elementList[0].tagName == "choice":
        return encodeChoiceOfList(elementList)
    else:
        return '', elementList[1:]


def encodeParameterDefinition(paraDef):
    elementList = elementOfChildNodes(paraDef.childNodes)
    result = ''
    while True:
        if not elementList:
            break
        data, elementList = encodeElementList(elementList)
        result += data
    return result

def encodeTvEncodingParameterDefinition(paraDef):
    result = ''
    typeNum = paraDef.getAttribute("typeNum")
    result += "data += " + "chr(" +  str(int(typeNum)|0x80) + ")\n    "
    elementList = elementOfChildNodes(paraDef.childNodes)
    for element in elementList:
        if element.tagName == "field":            
            typeName = element.getAttribute("type")
            if typeName == "u96":
                name = element.getAttribute("name")
                result += "data += par['" + name + "']\n    "
            else:
                packStr = typeToPackStr(typeName)
                name = element.getAttribute("name")
                result += "data += struct.pack('" + packStr + "', par['" + name + "'])\n    "
    result += "return data"
    result += "\n\n"
    return result


def EncodeParameterFuncs(paraDefList):
    s = ""
    for paraDef in paraDefList:
        s += "def encode_" + paraDef.getAttribute("name") + "(par):\n    "
        s += "data = ''\n    "
        typeNum = paraDef.getAttribute("typeNum")
        if int(typeNum) >= 128:
            s += encodeParameterDefinition(paraDef)
            #s += "msgheader = '!HH'\n    "
            #s += "megheaderLen = 4\n    "
            s += "type = Parameter_struct['" + \
                paraDef.getAttribute("name") + "']['type']\n    "
            s += "data = struct.pack('!HH', type, (4+len(data))) + data\n    "
            s += 'return data\n\n'
        else:
            s += encodeTvEncodingParameterDefinition(paraDef)
    return s


def EncodeMessageFuncs(msgDefList):
    s = ""
    for msgDef in msgDefList:
        s += "def encode_" + msgDef.getAttribute("name") + "(par):\n    "
        s += "data = ''\n    "
        s += encodeParameterDefinition(msgDef)
        #s += "type = Parameter_struct['" + paraDef.getAttribute("name") + "']['type']\n    "
        #s += "data = struct.pack('!HH', type, (4+len(data))) + data\n    "
        s += 'return data\n\n'
    return s


def DecodeParameterFuncs(paraDefList):
    s = ""
    for paraDef in paraDefList:
        s += "def decode_" + paraDef.getAttribute("name") + "(data):\n    "
        s += 'par = {}\n\n    '
        s += 'if len(data) == 0:\n        '
        s += 'return None, data\n    '
        typeNum = paraDef.getAttribute("typeNum")
        if int(typeNum) >= 128:
            s += 'type, length = struct.unpack("!HH", data[0:4])\n\n    '
            s += 'if type != Parameter_struct["' + \
                paraDef.getAttribute("name") + '"]["type"]:\n        '
            s += 'return None, data\n\n    '
            s += 'body = data[4:length]\n    '
            s += decodeParameterDefinition(paraDef)
            s += 'return par, data[length:]\n\n'
        else:
            s += decodeTVEncodingParameterDefinition(paraDef)        
    return s


def DecodeMessageFuncs(msgDefList):
    s = ""
    for msgDef in msgDefList:
        s += "def decode_" + msgDef.getAttribute("name") + "(body):\n    "
        s += "par = LLRPMessage()\n\n    "
        s += decodeParameterDefinition(msgDef)
        #s += "type = Parameter_struct['" + paraDef.getAttribute("name") + "']['type']\n    "
        #s += "data = struct.pack('!HH', type, (4+len(data))) + data\n    "
        s += 'return par\n\n'
    return s



def MessageClassDefs(paraDefList):
    s = ""
    for paraDef in paraDefList:
        s += "class " + paraDef.getAttribute("name") + "(LLRPMessage):\n"
        s += "    def __init__(self):\n"
        s += "        self['" + paraDef.getAttribute("name") + "'] = {}\n"
        s += "        self['" + paraDef.getAttribute("name") + "']['Type'] = " + paraDef.getAttribute("typeNum") + "\n"
        s += "        self['" + paraDef.getAttribute("name") + "']['ID'] = 1\n"

        s += "\n\n"
    return s



extra_func = '''

VER_PROTO_V1_1 = 2 

reverse_Message_struct()

def encode_message(msg):
    key = msg.keys()
    if (len(key) != 1):
        raise LLRPError('invalid message format')
    name = key[0]
    
    if name not in Message_struct:
        raise LLRPError('invalid message %s' % name)

    data = Message_struct[name]['encode'](msg[name])
    message_type = (VER_PROTO_V1_1<<10) | msg[name]['Type']
    message_length = len(data) + 10
    message_id = msg[name]['ID']
    message_header = struct.pack("!HII", message_type, message_length, message_id)
    return message_header + data 

def decode_message(msg_data):
    msg_type, msg_length, msg_id = struct.unpack("!HII", msg_data[0:10])
    msg_type = msg_type & 0x03ff
    try:
        msg_name = Message_Type2Name[msg_type]
    except KeyError:
        raise LLRPError('message type %d is not supported' % type)
    parameters = Message_struct[msg_name]['decode'](msg_data[10 : msg_length])
    msg = LLRPMessage()
    msg[msg_name] = parameters
    msg[msg_name]['Ver'] = VER_PROTO_V1_1
    msg[msg_name]['Type'] = msg_type
    msg[msg_name]['ID'] = msg_id
    return msg

'''

def xml2py(XMLName):
    mydom = parse(XMLName)
    root = mydom.documentElement
    messageDefinition = root.getElementsByTagName("messageDefinition")
    enumerationDefinition = root.getElementsByTagName("enumerationDefinition")
    parameterDefinition = root.getElementsByTagName("parameterDefinition")
    choiceDefinition = root.getElementsByTagName("choiceDefinition")
    GenChoiceDefDict(choiceDefinition)
    #header = GenHeader()
    enumeration = EnumName2TypeDict(enumerationDefinition)
    parameter = ParameterStructDefs(parameterDefinition)
    message = MessageStructDefs(messageDefinition)
    parameterEncoderFuncs = EncodeParameterFuncs(parameterDefinition)
    messageEncoderFuncs = EncodeMessageFuncs(messageDefinition)
    parameterDecodeFuncs = DecodeParameterFuncs(parameterDefinition)
    messageDecodeFuncs = DecodeMessageFuncs(messageDefinition)
    message_class_defs = MessageClassDefs(messageDefinition)
    return header + enumeration + parameterEncoderFuncs + messageEncoderFuncs +\
        parameterDecodeFuncs + messageDecodeFuncs + parameter + message + \
        message_class_defs + extra_func


def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument("-f", "--file", required=False,
                        default="llrp-1x0-def.xml", help="ltk def XML file name")
    parser.add_argument("-o", "--output", required=False,
                        default="llrp_codec.py", help="")
    args = parser.parse_args()
    output_str = xml2py(args.file)
    with open(args.output, "w") as f:
        f.write(output_str)


if __name__ == '__main__':
    main()

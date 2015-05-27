# encoding: utf-8
import sys
import codecs
from  xml.dom import  minidom


def get_nodevalue(node, index = 0):
    return node.childNodes[index].nodeValue if node else ''

def get_xmlnode(node,name):
    return node.getElementsByTagName(name) if node else []

def xml_to_string(filename):
    doc = minidom.parse(filename)
    return doc.toxml('UTF-8')

def is_zh(string):
    unicode_string = unicode(string,"utf-8")
    state = False
    for uchar in unicode_string:
        if uchar>= u'\u4e00' and uchar <= u'\u9fa5':
            state = True
    return state

def is_w(string):
    if (len(string) <= 3):
        return True
    else:
        return False

def test_load_xml(filename):
    #user_list = get_xml_data(filename)
    doc = minidom.parse(filename)
    root = doc.documentElement
    user_nodes = get_xmlnode(root,'item')
    user_list=[]
    for node in user_nodes:
        node_name = get_xmlnode(node,'khmc')
        user_name = get_nodevalue(node_name[0]).encode('utf-8','ignore')

        user = {}
        if is_w(user_name):
            new_name = "%s某" % (user_name)
            node_name[0].childNodes[0].nodeValue = new_name.decode('utf-8')
            user['username'] = node_name[0].childNodes[0].nodeValue
            user_list.append(user)
        elif not is_zh(user_name):
            new_name = "%s某某" % (user_name)
            node_name[0].childNodes[0].nodeValue = new_name.decode('utf-8')
            user['username'] = node_name[0].childNodes[0].nodeValue
            user_list.append(user)
            


    #for user in user_list :
            #print '-----------------------------------------------------'
            #user_string = "username %s" % user['username']
            #print user_string
            #print '====================================================='
    outer_file = file(filename, 'w')
    writer = codecs.lookup('utf-8')[3](outer_file)
    doc.writexml(writer, encoding='utf-8')
    outer_file.close()
    #print doc.toxml('UTF-8')

def convertGBK2UTF8(filename):
    fp = open(filename, "r")
    dataString = fp.read()
    fp.close()
    unicodeString = unicode(dataString, 'gbk')
    utf8String = unicodeString.encode('utf-8')
    outer_file = file(filename, 'w')
    outer_file.write(utf8String)
    outer_file.close()

def convertUTF82GBK(filename):
    fp = open(filename, "r")
    dataString = fp.read()
    fp.close()
    unicodeString = unicode(dataString, 'utf-8')
    gbkString = unicodeString.encode('gbk')
    
    outer_file = file(filename, 'w')
    outer_file.write(gbkString)
    outer_file.close()

if __name__ == "__main__":
    ori_filename = sys.argv[1]
    convertGBK2UTF8(ori_filename)
    test_load_xml(ori_filename)
    convertUTF82GBK(ori_filename)


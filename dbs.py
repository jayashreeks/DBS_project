from typing import Tuple
from Levenshtein import distance, hamming, median
import mysql.connector
# -*- coding: utf-8 -*-


class TrieNode(object):
    
    def __init__(self, char: str):
        self.char = char
        self.children = []
        # Is it the last character of the word.`
        self.word_finished = False
        # How many times this character appeared in the addition process
        self.counter = 1
    

def add(root, word: str):
    """
    Adding a word in the trie structure
    """
    node = root
    for char in word:
        found_in_child = False
        # Search for the character in the children of the present `node`
        for child in node.children:
            if child.char == char:
                # We found it, increase the counter by 1 to keep track that another
                # word has it as well
                child.counter += 1
                # And point the node to the child that contains this char
                node = child
                found_in_child = True
                break
        # We did not find it so add a new chlid
        if not found_in_child:
            new_node = TrieNode(char)
            node.children.append(new_node)
            # And then point node to the new child
            node = new_node
    # Everything finished. Mark it as the end of a word.
    node.word_finished = True


def find_prefix(root, prefix: str) -> Tuple[bool, int]:
    
    """
    Check and return 
      1. If the prefix exsists in any of the words we added so far
      2. If yes then how may words actually have the prefix
    """
    node = root
    res=''
    # If the root node has no children, then return False.
    # Because it means we are trying to search in an empty trie
    if not root.children:
        print('Empty trie') 
    for char in prefix:
        char_not_found = True
        # Search through all the children of the present `node`
        for child in node.children:
            if child.char == char:
                # We found the char existing in the child.
                char_not_found = False
                # Assign node as the child containing the char and break
                node = child
                res+=node.char
                if node.word_finished==True:
                    return res
                break
        # Return False anyway when we did not find a char.
    return 'Not found'
    # Well, we are here means we have found the prefix. Return true to indicate that
    # And also the counter of the last node. This indicates how many words have this
    # prefix
def lev_dist(root,word):
    node=root
    query1=word
    dist=0
    query2=''
    one_distance_list=[]
    parent=None
    if not root.children:
        print('Empty trie')
    for char in word:
        char_not_found = True
        # Search through all the children of the present `node`
        for child in node.children:
            if child.char == char:
                # We found the char existing in the child.
                # Assign node as the child containing the char and break
                node = child
                query2=query2+node.char
                dist=distance(query1,query2)
                if(dist==1) and node.word_finished==True:
                    one_distance_list.append(query2)
                parent=node
    for child in parent.children:
        parent= child
        query2=query2+parent.char
        dist=distance(query1,query2)
        if(dist==1):
            one_distance_list.append(query2)
        parent=child
    if len(one_distance_list)==0:
            print('Not found')
    return one_distance_list


if __name__ == "__main__":
    root = TrieNode('*')
    f=open("data.txt", "r", encoding="utf-8")
    contents=f.read()
    words_list=contents.split()
    for word in words_list:
        word=''.join(c for c in word if c not in '.,?!')
        add(root,word)


    mydb = mysql.connector.connect(host="127.0.0.1",user="root",passwd="root",database="DBPROJECT",port=3306)
    mycursor = mydb.cursor()
    sql = "INSERT INTO pronoun VALUES (%s, %s)"
    val = ("ಅವನು", "M")
    mycursor.execute(sql, val)
    val=("ಅವಳು", "F")
    mycursor.execute(sql, val)
    val=("ಆತ", "M")
    mycursor.execute(sql, val)
    val=('ಅದನ್ನು','O')
    mycursor.execute(sql, val)
    val=('ಇದನ್ನು','O')
    mycursor.execute(sql, val)
    val=('ಅವನಿಗೆ','M')
    mycursor.execute(sql, val)
    sql = "INSERT INTO verb VALUES (%s, %s)"
    val = ("ಕೊಯ್ದು", "O")
    mycursor.execute(sql, val)
    val=("ಕೊಡಬೇಕು", "O")
    mycursor.execute(sql, val)
    val=("ಕೊಡುವವನಲ್ಲ", "M")
    mycursor.execute(sql, val)
    val=("ತಂದಿದ್ದೇನೆ", "M")
    mycursor.execute(sql, val)
    val=('ಕೊಟ್ಟೆ','O')
    mycursor.execute(sql, val)
    val=('ಕೇಳಿದ','M')
    mycursor.execute(sql, val)
    val=('ನಿರಾಕರಿಸಿದ','M')
    mycursor.execute(sql, val)
    mycursor.execute("SELECT * FROM pronoun")
    print('pronoun table:')
    myresult = mycursor.fetchall()
    for x in myresult:
      print(x)
    print('verb table:')
    mycursor.execute("SELECT * FROM verb")
    myresult = mycursor.fetchall()
    for x in myresult:
      print(x)

    no_of_correct=0
    no_of_wrong=0
    is_wrong=False

    print(find_prefix(root,'ಕುಳಿತುಕೊಂಡ'))
    print(lev_dist(root,'ಕುಳಿತುಕೊಂ'))
    
    user_input_list=input('Enter text\n')
    text_list=user_input_list.split()
    tokenize_list=[]
    for word in text_list:
        word=''.join(c for c in word if c not in '.,?!')
        tokenize_list.append(word)
        if find_prefix(root,word)=='Not found':
            print(word)
            no_of_wrong+=1
            is_wrong=True
        else:
            no_of_correct+=1
            
        if is_wrong==True:
            print('Pick from the below list')
            print(lev_dist(root,word))
            
    input_text=user_input_list.split('.')
    del input_text[-1]
    print(input_text)
    form1=''
    form2=''
    for l in input_text:
        string=''
        for i in range(len(l)):
            if l[i].isspace():
                break
            else:
                string+=l[i]
            print(string,)
            sql1 = "SELECT value FROM pronoun WHERE word = %s"
            adr1 = (string, )
            mycursor.execute(sql1, adr1)
            myresult = mycursor.fetchall()
            for x in myresult:
                if x!=[]:
                    form1=x
                    print(x)
            sql2 = "SELECT value FROM verb WHERE word = %s"
            adr2 = (string, )
            mycursor.execute(sql2, adr2)
            myresult = mycursor.fetchall()
            for x in myresult:
                if x!=[]:
                    form2=x
                    print(x)
            if form1==form2:
                no_of_correct+=1
            else:
                no_of_wrong+=1
    print('WRONG:',no_of_wrong)
    print('CORRECT:',no_of_correct)


    

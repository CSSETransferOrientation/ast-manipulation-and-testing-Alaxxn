#!/usr/bin/python3
import ast
import os
from os.path import join as osjoin

import unittest
from enum import Enum

# Use these to distinguish node types, note that you might want to further
# distinguish between the addition and multiplication operators
NodeType = Enum('BinOpNodeType', ['number', 'operator', 'variable'])
operators = ['+','-', '*', '/']



class BinOpAst():
    """
    A somewhat quick and dirty structure to represent a binary operator AST.

    Reads input as a list of tokens in prefix notation, converts into internal representation,
    then can convert to prefix, postfix, or infix string output.
    """
    def __init__(self, prefix_list):
        """
        Initialize a binary operator AST from a given list in prefix notation.
        Destroys the list that is passed in.
        """
        if prefix_list:#For empty list
            self.val = prefix_list.pop(0)
            if self.val.isnumeric():
                self.type = NodeType.number
                self.left = False
                self.right = False
            elif (self.val in operators):
                self.type = NodeType.operator
                self.left = BinOpAst(prefix_list)
                self.right = BinOpAst(prefix_list)
            else:
                self.type = NodeType.variable
                self.left = False
                self.right = False
        else:
            self.val = None
            self.type = NodeType.number
            self.left = False
            self.right = False

    def __str__(self, indent=0):
        """
        Convert the binary tree printable string where indentation level indicates
        parent/child relationships
        """
        ilvl = '  '*indent
        left = '\n  ' + ilvl + self.left.__str__(indent+1) if self.left else ''
        right = '\n  ' + ilvl + self.right.__str__(indent+1) if self.right else ''
        return f"{ilvl}{self.val}{left}{right}"

    def __repr__(self):
        """Generate the repr from the string"""
        return str(self)

    def prefix_str(self):
        """
        Convert the BinOpAst to a prefix notation string.
        Make use of new Python 3.10 case!
        """
        if self.val == None:
            return "0"
        match self.type:
            case NodeType.variable:
                return self.val
            case NodeType.number:
                return self.val
            case NodeType.operator:
                return self.val + ' ' + self.left.prefix_str() + ' ' + self.right.prefix_str()

    def infix_str(self):
        """
        Convert the BinOpAst to a prefix notation string.
        Make use of new Python 3.10 case!
        """
        if self.val == None:
            return "0"
        match self.type:
            case NodeType.variable:
                return self.val
            case NodeType.number:
                return self.val
            case NodeType.operator:
                return '(' + self.left.infix_str() + ' ' + self.val + ' ' + self.right.infix_str() + ')'
                
    def postfix_str(self):
        """
        Convert the BinOpAst to a prefix notation string.
        Make use of new Python 3.10 case!
        """
        if self.val == None:
            return "0"
        
        match self.type:
            case NodeType.variable:
                return self.val
            case NodeType.number:
                return self.val
            case NodeType.operator:
                return self.left.postfix_str() + ' ' + self.right.postfix_str() + ' ' + self.val

    def additive_identity(self):
        """
        Reduce additive identities
        x + 0 = x
        """
        # ;;> This likely can't trigger because of the way you've set everything else up
        # ;;> but being more defensive to prevent weird errors is probably not bad
        if self.val == None:
            return
            
        match self.type:
            case NodeType.variable:
                return
            case NodeType.number:
                return
            case NodeType.operator:
                if self.val == "+":
                    if self.left.val == "0" or self.right.val == "0":
                        if self.left.val == "0":
                            temp = self.right
                        else:
                            temp = self.left
                            
                        self.val = temp.val
                        self.type = temp.type
                        self.left = temp.left
                        self.right = temp.right
                # ;;> You want to call these first so that things propogate upwards        
                # ;;> see the 'propogate' test I added
                if self.left: self.left.additive_identity()
                if self.right: self.right.additive_identity()
                
        
                        
    def multiplicative_identity(self):
        """
        Reduce multiplicative identities
        x * 1 = x
        """
        if self.val == None:
            return
        match self.type:
            case NodeType.variable:
                return
            case NodeType.number:
                return
            case NodeType.operator:
                if self.val == "*":
                    if self.left.val == "1" or self.right.val == "1":
                        if self.left.val == "1":
                            temp = self.right
                        else:
                            temp = self.left
                        self.val = temp.val
                        self.type = temp.type
                        self.left = temp.left
                        self.right = temp.right
                if self.left: self.left.additive_identity()
                if self.right: self.right.additive_identity()
    
    
    
    def mult_by_zero(self):
        """ Multiplication by 0, e.g. x * 0 = 0
        """
    
        if self.val == None:
            return
        match self.type:
            case NodeType.variable:
                return
            case NodeType.number:
                return
            case NodeType.operator:
                if self.val == "*":
                    if self.left.val == "0" or self.right.val == "0":
                        self.val = "0"
                        self.type = NodeType.number
                        self.left = False
                        self.right = False
                if self.left: self.left.additive_identity()
                if self.right: self.right.additive_identity()


    def simplify_binops(self):
        self.additive_identity()
        self.multiplicative_identity()
        self.mult_by_zero()

class BinOpTester (unittest.TestCase):


    def test_additive_identity(self):
        print(self.id())
        ins = osjoin("testbench","arith_id","inputs")
        outs = osjoin("testbench","arith_id","outputs")
        for filename in os.listdir(ins):
            in_path = osjoin(ins, filename)
            out_path = osjoin(outs, filename)
            with open (in_path, "r") as file: # Formatting input
                inp = file.read().strip().replace("\n"," ")
                arr = ast.literal_eval(inp)
            with open(out_path,"r") as file: #get expected output
                expected = file.read().strip().replace("\n"," ")
            #Run test
            t = BinOpAst(arr)
            t.additive_identity()
            solution = t.prefix_str()
            self.assertEqual(solution, expected)

    def test_multiplicative_identity(self):
        print(self.id())
        ins = osjoin("testbench","mult_id","inputs")
        outs = osjoin("testbench","mult_id","outputs")
        for filename in os.listdir(ins):
            in_path = osjoin(ins, filename)
            out_path = osjoin(outs, filename)
            with open (in_path, "r") as file: # Formatting input
                inp = file.read().strip().replace("\n"," ")
                arr = ast.literal_eval(inp)
            with open(out_path,"r") as file: #get expected output
                expected = file.read().strip().replace("\n"," ")
            #Run test
            t = BinOpAst(arr)
            t.multiplicative_identity()
            solution = t.prefix_str()
            self.assertEqual(solution, expected)
        
    def test_mult_by_zero(self):
        print(self.id())
        ins = osjoin("testbench","mult_by_zero","inputs")
        outs = osjoin("testbench","mult_by_zero","outputs")
        for filename in os.listdir(ins):
            in_path = osjoin(ins, filename)
            out_path = osjoin(outs, filename)
            with open (in_path, "r") as file: # Formatting input
                inp = file.read().strip().replace("\n"," ")
                arr = ast.literal_eval(inp)
            with open(out_path,"r") as file: #get expected output
                expected = file.read().strip().replace("\n"," ")
            #Run test
            t = BinOpAst(arr)
            t.mult_by_zero()
            solution = t.prefix_str()
            self.assertEqual(solution, expected)
            
    def test_combined(self):
        print(self.id())
        ins = osjoin("testbench","combined","inputs")
        outs = osjoin("testbench","combined","outputs")
        for filename in os.listdir(ins):
            in_path = osjoin(ins, filename)
            out_path = osjoin(outs, filename)
            with open (in_path, "r") as file: # Formatting input
                inp = file.read().strip().replace("\n"," ")
                arr = ast.literal_eval(inp)
            with open(out_path,"r") as file: #get expected output
                expected = file.read().strip().replace("\n"," ")
            #Run test
            t = BinOpAst(arr)
            t.simplify_binops()
            solution = t.prefix_str()
            self.assertEqual(solution, expected)



if __name__ == "__main__":
    unittest.main()

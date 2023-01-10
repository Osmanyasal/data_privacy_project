"""
WHERE PROGRAM BEGINS.
"""
import sys
import helper.parser as cli_parser
from helper.filebase import FileBase 

if __name__ == "__main__":
    dic = cli_parser.parse(sys.argv)
    print(dic)

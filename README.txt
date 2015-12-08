password_search is used to find any potential string which resembles a password for 
specified file types in a given directory. 

It is important to note that a fair number of false positiveswill be found. 
The regular expressions and tests this program uses errs on the side of caution. 
It is best used to find any passwords which may have accidently been left in unencrypted documents.

Example:
    > python password_search.py C:\Users .txt C:\output_results.txt

Output:
    Checking file: C:\Users\username\Documents\meeting_notes.txt
        ['Figuredout!1']
    Checking file: C:\Users\username\Documents\readme.txt
    Checking file: C:\Users\username\Documents\notes.txt
        ['local.datastore1']
        ['WHYamistoringpasswords?123']
        ['WOOPSYcaught101!']
        ['1334focus!']
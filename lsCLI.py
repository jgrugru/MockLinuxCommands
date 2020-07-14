import click
import os
import datetime
from tabulate import tabulate


def printFile(stringToPrint):
    click.secho(stringToPrint, fg='blue')

def printDir(stringToPrint):
    click.secho(stringToPrint, fg='red')

def getLastModifiedTime(abspath):
    return datetime.datetime.fromtimestamp(os.path.getmtime(abspath)).strftime('%Y-%m-%d %H:%M:%S')

# def printDict(lsdict):
#     for x in lsdict:
#         if lsdict[x][0] == 'file':
#             stringToPrint=x+'\t'
#             for args in lsdict[x][1:]:
#                 stringToPrint+=args+'\t'
#             printFile(stringToPrint)
#         elif lsdict[x][0] == 'dir':
#             stringToPrint=x+'\t'
#             for args in lsdict[x][1:]:
#                 if args=='':
#                     stringToPrint+='\t\t'
#                 else:
#                     stringToPrint+=args+'\t'
#             printDir(stringToPrint)

def printList(lslist):
    for x in lslist:
        if x[1][0]=='file':
            stringToPrint=x[0]+'\t'
            stringToPrint=createStringFromList(x[1], stringToPrint)
            printFile(stringToPrint)
        elif x[1][0]=='dir':
            stringToPrint=x[0]+'\t'
            stringToPrint=createStringFromList(x[1], stringToPrint)
            printDir(stringToPrint)

def createStringFromList(mylist, stringToPrint):
    for args in mylist[1:]:
        if args=='':
            stringToPrint+='\t\t'
        else:
            stringToPrint+=args+'\t'
    return stringToPrint

@click.group()
@click.version_option(version='0.0.1', prog_name="LS 2.0 CLI")
def main():
    """LS Mimick CLI"""
    pass
@main.command()
@click.argument('filepath', type=click.Path(exists=True), default='.')
@click.option('--size','-s', is_flag=True, help="Displays size of files in bytes") ##sends True as argument when the option is added.
@click.option('--long','-l', is_flag=True, help="Displays last modified time of file") 
@click.option('--reverse','-r', is_flag=True, help="Displays files in reverse order") 
@click.option('--extension','-x', is_flag=True, help="Displays files by extensiont ype") 
def ls(filepath, size, long, reverse, extension):
    """Print out files in directory"""
    lsdict = {}
    for x in os.listdir(filepath):
        abspath = os.path.join(filepath, x)
        if os.path.isdir(abspath):              #if is dir
            lsdict[x] = ['dir']                 #mark as dir
            if size:                            #if -s flag is set
                lsdict[x].append('')            #don't show file size for directories
        elif os.path.isfile(abspath):           #if is file
            lsdict[x] = ['file']                #mark as file
            if size:                            #if -s flag is set
                lsdict[x].append(str(os.path.getsize(abspath)))
        if long:                                # if -l flag is set
            lsdict[x].append(getLastModifiedTime(abspath))
    lslist = list(lsdict.items())
    if reverse:
        lslist = sorted(lslist, key=lambda x: x[0], reverse=True)
    if extension:
        pass
    printList(lslist)

if __name__=='__main__':
    main()
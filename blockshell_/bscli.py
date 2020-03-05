# -*- coding: utf-8 -*-
# ===================================================
# ==================== META DATA ===================
# ==================================================
__author__ = "Daxeel Soni"
__url__ = "https://daxeel.github.io"
__email__ = "daxeelsoni44@gmail.com"
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daxeel Soni"

# ==================================================
# ================= IMPORT MODULES =================
# ==================================================
import click
import urllib
import json
from blockchain.chain import Block, Blockchain

# ==================================================
# ===== SUPPORTED COMMANDS LIST IN BLOCKSHELL ======
# ==================================================
SUPPORTED_COMMANDS = [
    'dotx',
    'allblocks',
    'getblock',
    'help'
]

# Init blockchain
coin = Blockchain()

# Create group of commands
@click.group()
def cli():
    """
        Create a group of commands for CLI
    """
    pass

# ==================================================
# ============= BLOCKSHELL CLI COMMAND =============
# ==================================================
@cli.command()
@click.option("--difficulty", default=3, help="Define difficulty level of blockchain.")
def init(difficulty):
    """Initialize local blockchain"""
    print """
$$\   $$\ $$\                      $$$$$$\            $$\           
$$$\  $$ |\__|                    $$  __$$\           \__|          
$$$$\ $$ |$$\  $$$$$$$\  $$$$$$\  $$ /  \__| $$$$$$\  $$\ $$$$$$$\  
$$ $$\$$ |$$ |$$  _____|$$  __$$\ $$ |      $$  __$$\ $$ |$$  __$$\ 
$$ \$$$$ |$$ |$$ /      $$$$$$$$ |$$ |      $$ /  $$ |$$ |$$ |  $$ |
$$ |\$$$ |$$ |$$ |      $$   ____|$$ |  $$\ $$ |  $$ |$$ |$$ |  $$ |
$$ | \$$ |$$ |\$$$$$$$\ \$$$$$$$\ \$$$$$$  |\$$$$$$  |$$ |$$ |  $$ |
\__|  \__|\__| \_______| \_______| \______/  \______/ \__|\__|  \__|

 Example: $ dotx {"inputs":[{"addr":${IN},"value":${amount}}],"outputs":[{"addr":${OUT1},"value":${amount1}},{"addr":${OUT2},"value":${amount2}}]}
 > A command line utility for learning Blockchain concepts.
 > Type 'help' to see supported commands.
 > Project by Daxeel Soni - https://daxeel.github.io

    """

    # Set difficulty of blockchain
    coin.difficulty = difficulty

    # Start blockshell shell
    while True:
        cmd = raw_input("[BlockShell@NiceCoin] $ ")
        processInput(cmd)

# Process input from Blockshell shell


def processInput(cmd):
    """
        Method to process user input from Blockshell CLI.
    """
    userCmd = cmd.split(" ")[0]
    if len(cmd) > 0:
        if userCmd in SUPPORTED_COMMANDS:
            globals()[userCmd](cmd)
        else:
            # error
            msg = "Command not found. Try help command for documentation"
            throwError(msg)


# ==================================================
# =========== BLOCKSHELL COMMAND METHODS ===========
# ==================================================
def dotx(cmd):
    """
        Do Transaction - Method to perform new transaction on blockchain.
    """
    txData = cmd.split("dotx ")[-1]
    # try:
    txData = json.loads(txData)
    input0, value = txData["inputs"][0]["addr"], txData["inputs"][0]["value"]
    output1, output2 = txData["outputs"][0]["addr"], txData["outputs"][1]["addr"]
    value1, value2 = txData["outputs"][0]["value"], txData["outputs"][1]["value"]
    if input0 == "" or output1 == "" or output2 == "" or value-value1-value2<0:
        print "Transaction Format Error"
    else:
        print "===========================================================================\n"
        print "INPUT: " + input0 + " Value:" + str(value) + "\nTO===>OUTPUT 1:"+output1 + \
                " Value:" + str(value1) + "\nTO===>OUTPUT 2:"+output2+" Value:" + str(value2) + "\n"
        print "===========================================================================\n"
        print "Doing transaction..."
        coin.addBlock(Block(data=txData))
    # except:
    #     print "Transaction Format Error"


def allblocks(cmd):
    """
        Method to list all mined blocks.
    """
    print ""
    for eachBlock in coin.chain:
        print eachBlock.hash
    print ""


def getblock(cmd):
    """
        Method to fetch the details of block for given hash.
    """
    blockHash = cmd.split(" ")[-1]
    for eachBlock in coin.chain:
        if eachBlock.hash == blockHash:
            print ""
            print eachBlock.__dict__
            print ""


def help(cmd):
    """
        Method to display supported commands in Blockshell
    """
    print "Commands:"
    print "   dotx <transaction data>    Create new transaction"
    print "   allblocks                  Fetch all mined blocks in blockchain"
    print "   getblock <block hash>      Fetch information about particular block"


def throwError(msg):
    """
        Method to throw an error from Blockshell.
    """
    print "Error : " + msg

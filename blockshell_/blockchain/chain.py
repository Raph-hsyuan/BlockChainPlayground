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
import hashlib
import datetime
import json
from colorama import Fore, Back, Style
import time
import sys

# ==================================================
# =================== BLOCK CLASS ==================
# ==================================================
class Block:
    """
        Create a new block in chain with metadata
    """
    def __init__(self, data, index=0):
        self.index = index
        self.previousHash = ""
        self.data = data
        # self.timestamp = str(datetime.datetime.now())
        self.nonce = 0
        self.hash = self.calculateHash()

    def calculateHash(self):
        """
            Method to calculate hash from metadata
        """
        self.nonce = self.nonce + 1
        hashData = str(self.index) + str(self.data) + self.previousHash + str(self.nonce)
        return hashlib.sha256(hashData).hexdigest()

    def mineBlock(self, difficulty):
        """
            Method for Proof of Work
        """
        print Back.RED + "\n[Status] Mining block (" + str(self.index) + ") with PoW ..."
        startTime = time.time()

        while self.hash[:difficulty] != "0"*difficulty:
            self.nonce += 1
            self.hash = self.calculateHash()

        endTime = time.time()
        print Back.BLUE + "[ Info ] Time Elapsed : " + str(endTime - startTime) + " seconds."
        print Back.BLUE + "[ Info ] Mined Hash : " + self.hash
        print Style.RESET_ALL


# ==================================================
# ================ BLOCKCHAIN CLASS ================
# ==================================================

class Blockchain:
    """
        Initialize blockchain
    """
    def __init__(self):
        #Send NiceCoin * 12 to Alice Bob and Peter
        self.chain = [self.createGenesisBlock(),Block(json.loads(
            '''
            {"inputs":[{"addr":"GOD","value":36}],"outputs":[{"addr":"ADDRALICE","value":12},{"addr":"ADDRBOB","value":12},{"addr":"ADDRPETER","value":12}]}
            ''')
        )]
        self.difficulty = 3

    def createGenesisBlock(self):
        """
            Method create genesis block
        """
        return Block("Genesis Block")

    def addBlock(self, newBlock):
        """
            Method to add new block from Block class
        """
        print "Checking All Recorded Block for Transaction ... "
        if self.checkTransation(newBlock.data["inputs"][0]["addr"],newBlock.data["inputs"][0]["value"]):
            print "Transaction Checked [OK]"
        else:
            print "Transaction Checked [ERROR] : The Block Can't be validated due to some problem transaction"
            return
        newBlock.index = len(self.chain)
        newBlock.previousHash = self.chain[-1].hash
        newBlock.mineBlock(self.difficulty)
        self.chain.append(newBlock)
        self.writeBlocks()

    def checkTransation(self,sender,value):
        balance=0
        # Because we have in/out for each transaction, and each time we
        # create a transaction we check that in - out = 0, so we only
        # need to find the last transaction in which the sender is an 
        # OUTPUT
        for eachBlock in self.chain:
            print "checking Block " + str(eachBlock.index)
            trans = eachBlock.data
            if trans == "Genesis Block" :
                continue
            for output in trans["outputs"]:
                if output["addr"] == sender:
                    balance = int(output["value"])
        if value < balance:
            print "Wrong balance[ERROR]"
        if value > balance:
            print "Not enough balance[ERROR]"
        print sender + " HAS " + str(balance) + " NiceCoin"
        return value == balance


    def writeBlocks(self):
        """
            Method to write new mined block to blockchain
        """
        dataFile = file("chain.txt", "w")
        chainData = []
        for eachBlock in self.chain:
            chainData.append(eachBlock.__dict__)
        dataFile.write(json.dumps(chainData, indent=4))
        dataFile.close()

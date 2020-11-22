from hashlib import sha256
from pprint import pprint
import time


class Block(object):
    """
    data -> array of object
    之前区块的哈希值
    自己的哈希值：由存储在区块里的信息算出来的（data + 之前区块的哈希值）
    """
    def __init__(self, transactions, previousHash):
        """
        初始化
        """
        self.transactions = transactions
        self.previousHash = previousHash
        self.timestamp = round(time.time())
        self.nonce = 1 # Number once的缩写，一个只被使用一次的任意或非重复的随机数值
        self.hash = self.computeHash

    @property
    def computeHash(self):
        """
        计算当前区块的哈希值
        """
        return sha256(
            (str(self.transactions)
            + self.previousHash
            + str(self.nonce)
            + str(self.timestamp)).encode("utf-8")
        ).hexdigest()

    def getAnswer(self, difficulty):
        """
        开头前n位为零的hash
        """
        answer = ""
        for _ in range(difficulty):
            answer += '0'
        return answer

    def mine(self, difficulty):
        """
        计算符合区块链难度要求的hash
        """
        while True:
            self.hash = self.computeHash
            if self.hash[:difficulty] != self.getAnswer(difficulty):
                self.nonce += 1
                self.hash = self.computeHash
            else:
                break
        print("挖矿结束", self.hash)

    @property
    def prt(self):
        """
        打印当前区块
        """
        pprint(vars(self))


class Chain(object):
    """
    区块的链
    """
    def __init__(self):
        self.chain = [self.bigBang]
        self.transactionPool = []
        self.minerReward = 50 # 每挖出一个区块奖励50
        self.difficulty = 4 # 工作量证明难度设置

    @property
    def bigBang(self):
        genesisBlock = Block("我是祖先", "")
        return genesisBlock

    def getLatestBlock(self):
        """
        获取最新的区块
        """
        return self.chain[len(self.chain) - 1]

    def addTransaction(self, transaction):
        """
        添加transaction到transactionPool里
        """
        self.transactionPool.append(transaction)

    def addBlockToChain(self, newBlock):
        """
        添加区块到区块链上
        找到最近一个block的hash，这个hash就是最新区块的previousHash
        """
        newBlock.previousHash = self.getLatestBlock().hash
        # newBlock.hash = newBlock.computeHash
        newBlock.mine(self.difficulty)
        self.chain.append(newBlock)

    def mineTransactionPool(self, minerRewardAddress):
        """
        发放矿工奖励、挖矿、添加区块到区块链
        """
        # 发放矿工奖励
        minerRewardTransaction = Transaction("", minerRewardAddress, self.minerReward)
        self.transactionPool.append(minerRewardTransaction)

        # tpStr -> transactionPool序列化
        tpStr = ""
        for item in self.transactionPool:
            tpStr += str(vars(item))

        # 挖矿
        newBlock = Block(tpStr, self.getLatestBlock().hash)
        newBlock.mine(self.difficulty)

        # 添加区块到区块链，清空 transactionPool
        self.chain.append(newBlock)
        self.transactionPool.clear()

    @property
    def prt(self):
        """
        打印区块链
        """
        print("chain:\n[")
        for i in self.chain:
            i.prt
        print("]\ntransactionPool:")
        for j in self.transactionPool:
            print(vars(j))
        print("minerReward: " + str(self.minerReward))
        print("difficulty: " + str(self.difficulty))

    def validateChain(self):
        """
        验证当前的区块链是否合法
        当前的数据有没有被篡改
        要验证区块的previousHash是否等于previous区块的hash
        """
        if len(self.chain) == 1:
            if self.chain[0].computeHash != self.chain[0].hash:
                return False
            return True

        """
        从第二个区块开始验证
        验证到最后一个
        """
        for i in range(1, len(self.chain)):
            blockToValidate = self.chain[i] # blockToValidate: 要送去验证的块
            # 当前的数据是否有被篡改
            if blockToValidate.hash != blockToValidate.computeHash:
                print("数据被篡改！")
                return False
            
            # 我们要验证区块的previousHash是否等于previousBlock区块的hash
            previousBlock = self.chain[i-1]
            if blockToValidate.previousHash != previousBlock.hash:
                print("前后区块链断裂")
                return False

        return True


class Transaction(object):
    """
    交易
    """
    def __init__(self, fromWho, toWho, amount):
        """
        fromWho: 转账人
        toWho: 收款人
        amount: 数额
        """
        self.fromWho = fromWho
        self.toWho = toWho
        self.amount = amount
        # self.timestamp = timestamp


if __name__ == "__main__":
    duanCoin = Chain()

    t1 = Transaction("HUT", "Duan", 2500)
    # pprint(vars(t1))
    t2 = Transaction("HUT", "Duan", 3000)
    # pprint(vars(t2))
    duanCoin.addTransaction(t1)
    duanCoin.addTransaction(t2)
    # duanCoin.prt
    duanCoin.mineTransactionPool("DuanQi")
    duanCoin.prt

from hashlib import sha256
from pprint import pprint


class Block(object):
    """
    data
    之前区块的哈希值
    自己的哈希值：由存储在区块里的信息算出来的（data + 之前区块的哈希值）
    """
    def __init__(self, data, previousHash):
        """
        初始化
        """
        self.data = data
        self.previousHash = previousHash
        self.nonce = 1 # Number once的缩写，一个只被使用一次的任意或非重复的随机数值
        self.hash = self.computeHash

    @property
    def computeHash(self):
        """
        计算当前区块的哈希值
        """
        return sha256((self.data + self.previousHash + str(self.nonce)).encode("utf-8")).hexdigest()

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
        self.difficulty = 5 # 工作量证明难度设置

    @property
    def bigBang(self):
        genesisBlock = Block("我是祖先", "")
        return genesisBlock

    def getLatestBlock(self):
        """
        获取最新的区块
        """
        return self.chain[len(self.chain) - 1]

    def addBlockToChain(self, newBlock):
        """
        添加区块到区块链上
        找到最近一个block的hash，这个hash就是最新区块的previousHash
        """
        newBlock.previousHash = self.getLatestBlock().hash
        # newBlock.hash = newBlock.computeHash
        newBlock.mine(self.difficulty)
        self.chain.append(newBlock)

    @property
    def prt(self):
        """
        打印区块链
        """
        print("chain:\n[")
        for i in self.chain:
            i.prt
        print("]")

    def validateChain(self):
        """
        验证当前的区块链是否合法
        当前的数据有没有被篡改
        要验证区块的previousHash是否等于previous区块的hash
        """
        if len(self.chain) == 1:
            if sha256(self.chain[0].data.encode("utf-8")).hexdigest() != self.chain[0].hash:
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


if __name__ == "__main__":
    duanChain = Chain()
    
    block1 = Block("转账十元", "")
    duanChain.addBlockToChain(block1)
    block2 = Block("转账十个十元", "")
    duanChain.addBlockToChain(block2)

    # 尝试篡改这个区块链
    duanChain.chain[1].data = "转账一百个十元"
    duanChain.chain[1].mine(5)
    duanChain.prt
    print(duanChain.validateChain())

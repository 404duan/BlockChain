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
        self.hash = self.computeHash

    @property
    def computeHash(self):
        """
        计算当前区块的哈希值
        """
        return sha256((self.data + self.previousHash).encode("utf-8")).hexdigest()

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
        newBlock.hash = newBlock.computeHash
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
    print(duanChain.validateChain())
    
    block1 = Block("转账十元", "")
    duanChain.addBlockToChain(block1)
    block2 = Block("转账十个十元", "")
    duanChain.addBlockToChain(block2)
    # block3 = Block("转账2个十元", "")
    # duanChain.addBlockToChain(block3)
    # block4 = Block("转账3十个十元", "")
    # duanChain.addBlockToChain(block4)
    # block5 = Block("转账4十个十元", "")
    # duanChain.addBlockToChain(block5)
    # print(duanChain.validateChain())

    # 尝试篡改这个区块链
    duanChain.chain[1].data = "转账一百个十元"
    duanChain.chain[1].hash = duanChain.chain[1].computeHash
    duanChain.prt
    print(duanChain.validateChain())

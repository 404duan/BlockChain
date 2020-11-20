import hashlib


print(hashlib.sha256("duanqi1".encode("utf-8")).hexdigest())
print(hashlib.sha256("duanqi2".encode("utf-8")).hexdigest())

def proofOfWork():
    """
    需要得到一个开头值为零的哈希值，想知道x是多少
    """
    data = "duanqi"
    x = 0
    while True:
        if hashlib.sha256((data + str(x)).encode("utf-8")).hexdigest()[0] != '0':
            x = x + 1
        else:
            print(hashlib.sha256((data + str(x)).encode("utf-8")).hexdigest())
            print(x)
            break


def proofOfWorkn(n):
    """
    需要得到一个开头值为n的哈希值，想知道x是多少
    """
    data = "duanqi"
    x = 0
    while True:
        if hashlib.sha256((data + str(x)).encode("utf-8")).hexdigest()[0:len(n)] != n:
            x = x + 1
        else:
            print(hashlib.sha256((data + str(x)).encode("utf-8")).hexdigest())
            print(x)
            break


if __name__ == "__main__":
    # proofOfWork()
    proofOfWorkn("000000")
import time
from hashlib import sha256
from storages import Storage, InMemoryStorage

class Block:

    def __init__(self, *args, **kwargs):
        
        if len(args) > 0:
            prev_hash = args[0]
        elif 'prev_hash' in kwargs:
            prev_hash = kwargs.pop('prev_hash')
        else:
            raise ValueError

        if type(prev_hash) != str:
            prev_hash = hex(prev_hash)

        if len(args) > 1:
            difficulty = args[1]
        elif 'difficulty' in kwargs:
            difficulty = kwargs.pop('difficulty')
        else:
            raise ValueError

        self.transactions = []
        self.states = {}

        self.header = {
            'prev_hash': prev_hash,
            'timestamp': int(time.time()),
            'nonce': 0,
            'difficulty': difficulty,
            'data_hash': hash((self.transactions, self.states))
        }

    def __repr__(self):
        return str({
            'header': self.header,
            'body': {
                'transactions': self.transactions,
                'states': self.states
            }
        })

    def __hash__(self):
        return sha256(str(self.header)).hexdigest()

    def find_nonce(self):
        self.header['nonce'] = 0
        difficulty = self.header['difficulty']
        while hash(self)[:difficulty] != '0'*difficulty:
            self.header['nonce'] += 1

    def verify(self):
        difficulty = self.header['difficulty']
        return self.__hash__()[:difficulty] == '0'*difficulty

    def add_transaction(self, txn):
        self.transactions.append(txn)

class Blockchain:

    default_storage_class = InMemoryStorage
    default_genesis = Block(hex(0))

    def __init__(self, *args, **kwargs):
        self._storage_class = kwargs.pop('storage', self.default_storage_class)
        genesis = kwargs.pop('genesis', self.default_genesis)
        self._storage = self._storage_class(*args, **kwargs) 
        self._storage.put_block(genesis)
        self._transaction_pool = []

    def add_block(self, block: Block):
        assert block.header['prev_hash'] in self
        assert block.verify()
        self._storage.put_block(block)

    def create_transaction(self):
        pass

    def __contains__(self, block_hash):
        return block_hash in self._storage



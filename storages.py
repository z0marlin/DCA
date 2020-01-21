from abc import ABC, abstractmethod

class Storage(ABC):

    @abstractmethod
    def has_block(self, block_hash):
        raise NotImplementedError('Need to override this method!')
    
    @abstractmethod
    def get_block(self, block_hash):
        raise NotImplementedError('Need to override this method!')
    
    @abstractmethod
    def put_block(self, block):
        raise NotImplementedError('Need to override this method!')

    @abstractmethod
    def delete_block(self, block_hash):
        raise NotImplementedError('Need to override this method!')

    def __contains__(self, block_hash):
        return self.has_block(block_hash)


class InMemoryStorage(Storage):
    
    def __init__(self):
        super().__init__()
        self.blocks = {}
        self.num_blocks = 0
        self.chain_ends = set()

    def has_block(self, block_hash):
        return block_hash in self.blocks

    def get_block(self, block_hash):
        return self.blocks[block_hash]

    def put_block(self, block):
        block_hash = hash(block)
        prev_block_hash = block.header['prev_hash']
        self.blocks[block_hash] = {
            'block': block,
            'chain_length': self.blocks[prev_block_hash]['chain_length'] + 1
        }
        if prev_block_hash in self.chain_ends:
            self.chain_ends.remove(prev_block_hash)
        self.chain_ends.add(block_hash)
        self.num_blocks += 1

class LevelDBStorage(Storage):
    pass
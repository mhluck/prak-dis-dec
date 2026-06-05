import CoreBlockchain

class UtdiBlockchain:
    def __init__(self):
        self.chain = []
        self.init_genesis_block() # Genesis is the first block in Blockchain

    def init_genesis_block(self):
        # Genesis always has 0 for previous block.
        first_block = CoreBlockchain.CoreBlockchain(0, "Blok Genesis / Awal", "0")
        self.chain.append(first_block)

    def add_block(self, new_data):
        last_block = self.chain[-1]
        new_block = CoreBlockchain.CoreBlockchain(
            idx=len(self.chain),
            data=new_data,
            previous_hash=last_block.hash # Lock new block with hash from previous block
        )
        self.chain.append(new_block)
import functions as f

class Blockchain:
    
    def __init__(self, max_transactions_per_block): #, wallets = {}):
        self.max_transactions_per_block = max_transactions_per_block
        
        #create genesis and first blocks
        block_0 = {}
        block_0["header"] = {}
        block_0["header"]["timestamp"] =  f.current_milli_time()
        block_0["header"]["block_number"] = 0

        block_1 = f.init_block(block_0)

        self.chain = (block_0,block_1)
      
#        self.wallets = wallets

    def add_transaction(self,wallets,transaction):
        #, fee, timestamp_transaction)
        # check if transaction valid:the 2 wallets given exist and there is enough cash in the wallet of the payer.

        number_actual_transactions = len(self.chain[-1]["body"]["transactions"])
        if number_actual_transactions < self.max_transactions_per_block:
            assert wallets[transaction[0]] - transaction[2] >= 0
            wallets[transaction[0]] -= transaction[2]
            wallets[transaction[1]] += transaction[2]
            #add transaction to last block
            self.chain[-1]["body"]["transactions"] += (transaction,)

        elif number_actual_transactions == self.max_transactions_per_block: 
            raise ValueError("the block is full.\nmine it to add a transaction in a new block. ")

    def mine_last_block(self):
        # last block is mined and a new block is created
        # se puede minar si no tiene el múmero max. de transacciones

        # armar merkle tree con todas las transacciones.
        transactions = self.chain[-1]["body"]["transactions"] 
        merkle_tree = f.merkle_tree_from_txs(transactions)
        self.chain[-1]["body"]["merkle_tree"] = merkle_tree
        self.chain[-1]["header"]["merkle_tree_root_hash"] = merkle_tree.root.name

        #timestamp last block
        self.chain[-1]["header"]["timestamp"] =  f.current_milli_time() # time when PoW initiated. its ok?
        #tmb se puede poner el tpo anterior a que se consiga el nonce valido. 
        # si uso la hora como nonce?

        #PoW
        _ , hash = f.mine_block(self.chain[-1],2)

        #create new_block
        new_block = f.init_block(self.chain[-1])
        
        #add it to the chain
        self.chain += (new_block,)

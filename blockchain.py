import functions as f
from anytree import RenderTree

class Blockchain:
    def __init__(self, max_transactions_per_block,pow_difficulty):
        self.wallets = {"miner" : 0}
        
        self.max_transactions_per_block = max_transactions_per_block
        self.pow_difficulty = pow_difficulty
        
        #create genesis and second block
        block_0 = f.init_block(self, prev_block = None)
        self.chain = (block_0,)
        f.reward_miner(self)
        self.mine_last_block()
        
    def add_transaction(self,transaction):
        # check if transaction valid: the 2 wallets given exist and there is enough cash in the wallet of the payer.
        
        payer = transaction[0]
        payee = transaction[1]
        amount = transaction[2]
        fee = transaction[3]
        
        number_actual_transactions = len(self.chain[-1]["body"]["transactions"])
        
        if number_actual_transactions + 2 <= self.max_transactions_per_block:
            assert self.wallets[payer] - amount - fee >= 0
            # add transaction of cash to be sent to the payee
            self.wallets[payer] -= amount
            self.wallets[payee] += amount
            self.chain[-1]["body"]["transactions"] += (transaction[:3],)
            
            # send fee to the miner of the block
            self.wallets[payer] -= fee
            self.wallets["miner"] += fee
            fee_transaction = (payer,"miner",fee)
            self.chain[-1]["body"]["transactions"] += (fee_transaction,)
            
            print("Current block transactions = ", number_actual_transactions + 2,". Max allowed = ", self.max_transactions_per_block)

        else: 
            raise ValueError("The block is full. Mine it to add a transaction in a new block. ")

    def mine_last_block(self):
        # last block is mined and a new block is created
        # se puede minar si no tiene el múmero max. de transacciones

        # armar merkle tree con todas las transacciones.
        transactions = self.chain[-1]["body"]["transactions"] 
        merkle_tree = f.merkle_tree_from_txs(transactions)
        self.chain[-1]["body"]["merkle_tree"] = merkle_tree
        self.chain[-1]["header"]["merkle_tree_root_hash"] = merkle_tree.root.name

        self.chain[-1]["body"]["wallets_after_block_transactions"] = self.wallets.copy()

        #timestamp last block
        self.chain[-1]["header"]["timestamp"] =  f.current_milli_time() # time when PoW initiated.
                
        #PoW
        f.mine_block(self.chain[-1],self.pow_difficulty)

        #create new_block
        new_block = f.init_block(self, prev_block = self.chain[-1])
        #add it to the chain
        self.chain += (new_block,)
        
        # first transaction of the new block:
        f.reward_miner(self)
        
    def add_account(self,name_account):
        # add account with 0 cash.
        assert type(name_account) is str
        if name_account not in self.wallets.keys():
            self.wallets[name_account] = 0
        else:
            raise ValueError("Account name already exists")
    def wallets_taking_only_mined_blocks(self):
        print(self.chain[-2]["body"]["wallets_after_block_transactions"])

    def visualize_merkle_tree(self,number_block):
        merkle_tree = self.chain[number_block]["body"]["merkle_tree"]
        for pre, _, node in RenderTree(merkle_tree):
            print("%s%s" % (pre, node.name))
            
    def show(self):
        for i,b in enumerate(self.chain):
            print("\nblock ",i)
            print("\nheader:")
            for k, v in b["header"].items():
                print(k," : ", v)
            print("\nbody:")
            for k, v in b["body"].items():
                print(k," : ", v)
            print("\n","-"*100)

import time as time
import hashlib
from anytree import Node

def create_roots_and_first_hashes(transactions):
    # create len(nodes) nodes with anytree lib.
    txs_nodes = []
    shallower_nodes = []
    for tx in transactions:
        child_1 = Node(tx)
        hash = string_to_hash(f"{child_1.name}")
        new_node = Node(hash, children = [child_1])
        txs_nodes.append(child_1)
        shallower_nodes.append(new_node)
    return shallower_nodes, txs_nodes

def string_to_hash(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()

def hashes_given_depth(nodes):
    # nodes = [] #lista de nodos EN ORDEN (idx mas grande, txs más nuevas)
    shallower_nodes = []
    len_transactions = len(nodes)
    if len_transactions % 2 == 0:
        for idx in range(0,len_transactions,2):
            #creo nodo padre, le asigno 2 hijos y devuelvo nodo padre con hash
            child_1 = nodes[idx]
            child_2 = nodes[idx+1]
            hash = string_to_hash(f"{child_1.name}{child_2.name}")
            new_node = Node(hash, children = [child_1,child_2])
            shallower_nodes.append(new_node)

    else:
        #si len_transactions es impar, a la primer tx la hasheo sola:
        child_1 = nodes[0]
        hash = string_to_hash(f"{child_1.name}")
        new_node = Node(hash, children = [child_1])
        shallower_nodes.append(new_node)

        for idx in range(1,len_transactions,2):
            child_1 = nodes[idx]
            child_2 = nodes[idx+1]
            hash = string_to_hash(f"{child_1.name}{child_2.name}")
            new_node = Node(hash, children = [child_1,child_2])
            shallower_nodes.append(new_node)

    print("len(shallower_nodes)=",len(shallower_nodes))
    return shallower_nodes

def merkle_tree_from_txs(transactions):
    # returns the entire tree
    if len(transactions)==0:
        raise ValueError("No transactions given!")
    nodes, txs_nodes = create_roots_and_first_hashes(transactions)
    while len(nodes)!=1:
        nodes = hashes_given_depth(nodes)
    root = nodes[0]
    return root

def current_milli_time():
    return round(time.time() * 1000)
  
def mine_block(block,hash_zeros):
    while not string_to_hash(str(block["header"])).startswith("0"*hash_zeros):
        block["header"]["nonce"]+=1
    return block, string_to_hash(str(block["header"]))

def init_block(prev_block):
    new_block = {}
    new_block["header"] = {}
    new_block["header"]["prev_hash"] =  string_to_hash(str(prev_block["header"]))   
    new_block["header"]["block_number"] = prev_block["header"]["block_number"] + 1
    new_block["header"]["nonce"] = 0
    
    new_block["body"] = {}
    new_block["body"]["transactions"] = ()
    return new_block
    
def add_account(wallets,name_account,cash):
    # add account with amount of cash (in a real case, initial cash must be 0)
    assert type(name_account) is str
    if name_account not in wallets.keys():
        wallets[name_account] = cash
    else:
      raise ValueError("Account name already exists")
    return wallets
    
def block_newer_than(block1,block2):
    return block1["header"]["timestamp"] > block2["header"]["timestamp"]




class BTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.values = [] #values are rows in the table
        self.children = []

class BTree:
    def __init__(self, t=2):  # min degree
        self.root = BTreeNode(leaf=True)
        self.t = t

    def insert(self, key, value):
        root = self.root
        if len(self.root.keys) == (2 * self.t - 1):
            new_root = BTreeNode()
            new_root.children.append(root)
            self.split_child(new_root, 0)
            self.root = new_root
            self.insert_non_full(new_root, key, value)
        else:
            # Safe to insert directly into root
            self.insert_non_full(self.root, key, value)
        

    def insert_non_full(self, node, key, value):
        if node.leaf:
            # Simple case, where we can insert the key and value into the leaf node
            i = len(node.keys) - 1
            while i >= 0 and key < node.keys[i]:
                i -= 1
            node.keys.insert(i + 1, key)
            node.values.insert(i + 1, value)
        else:
            i = len(node.keys) - 1
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1

            if len(node.children[i].keys) == (2 * self.t) - 1:
                self.split_child(node, i)
                if key > node.keys[i]:
                    i += 1

            self.insert_non_full(node.children[i], key, value)


    def split_child(self, parent, index):
        t = self.t
        full_child = parent.children[index]

        middle_key = full_child.keys[t - 1]
        middle_value = full_child.values[t - 1]

        # Right Half
        right_node = BTreeNode(leaf=full_child.leaf)       
        right_node.keys = full_child.keys[t:]              
        right_node.values = full_child.values[t:]           

        # Left Half
        full_child.keys = full_child.keys[:t - 1]           
        full_child.values = full_child.values[:t - 1]

        # If not a leaf, move children too
        if not full_child.leaf:
            right_node.children = full_child.children[t:]     # right half
            full_child.children = full_child.children[:t]     # left half

        # move middle key and value to the parent
        parent.keys.insert(index, middle_key)
        parent.values.insert(index, middle_value)

        # insert the new right node into parent's children
        parent.children.insert(index + 1, right_node)

    def search(self, key):
        # Given a key, return the value
        return self.search_node(self.root, key)

    def search_node(self, node, key):
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        if i < len(node.keys) and key == node.keys[i]:
            return node.values[i]
        elif node.leaf:
            return None
        else:
            return self.search_node(node.children[i], key)
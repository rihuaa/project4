"""Lab 8: Hash Tables
Hashtables implementation with separate chaining, linear probing,
and quadratic probing collision handling methods.

Author: Richard Hua
Class: CPE202
Date: 3/2/2020
"""

class Node:
    """Linked List is one of None or Node
    Attributes:
        val (int): an item in the list
        next (Node): a link to the next item in the list (Linked List)
    """
    def __init__(self, key=None, val=None, nxt=None):
        self.key = key
        self.val = val
        self.next = nxt

    def __repr__(self):
        return "Node(key=%s, data=%s, next=%s)"\
        % (self.key, self.val, self.next)

    def __eq__(self, other):
        return (self.val == other.val)\
        and (self.next == other.next)

class HashTableSepchain:
    """Hash table that holds key-value pairs with separate chaining
    collision handling.

    Table is a list of nodes that hold k-v pairs with links to next pair
    from chaining, otherwise None.

    Attributes:
        size (int) : size/capacity of the table
        num_items (int) : number of k-v pairs currently in table
        num_collisions (int) : number of collisions during insertions
        table (list) : a list of nodes holding k-v pairs
    """

    def __init__(self, table_size=11):
        self.table_size = table_size
        self.num_items = 0
        self.num_collisions = 0
        self.table = [None] * self.table_size

    def __eq__(self, other):
        return isinstance(other, HashTableSepchain)\
        and (self.table_size == other.table_size)\
        and (self.num_collisions == other.num_collisions)\
        and (self.num_items == other.num_items)\
        and (self.table == other.table)

    def __repr__(self):
        return 'HashTableSepchain\
        (size=%s, num_items=%s, num_collisions=%s, table=%s)'\
        % (self.table_size, self.num_items, self.num_collisions, self.table)

    def __getitem__(self, key):
        """implementing this method enables getting an item with [] notation
        This function calls your get method.

        Args:
            key (str) : a key which is compareable by <,>,==
        Returns:
            any : the value associated with the key
        Raises:
            KeyError : it raises KeyError because the get function in bst.py raises the error.
        """
        return self.get(key)

    def __setitem__(self, key, val):
        """implementing this method enables setting a key value pair with [] notation
        This function calls your put method.

        Args:
            key (any) : a key which is compareable by <,>,==
            val (any): the value associated with the key
        """
        self.put(key, val)

    def __contains__(self, key):
        """implementing this method enables checking if a key exists with in notaion

        Args:
            key (any) : a key which is compareable by <,>,==
        Returns:
            bool : True is the key exists, otherwise False
        """
        return self.contains(key)


    def put(self, key, data):
        """Takes a key and data, then stores the key-value pair into a hash
        table based on the hash value of the key.

        If k-v pair is duplicate, the old k-v pair will be replaced by new k-v pair.
        If load factor of hash table is greater than following values, hash table
        doubles its size and stores old data in new one.

        Load factors for:

        Separate Chaining: 1.5
        Linear Probing: 0.75
        Quadratic Probing: 0.75

        Note: Key and data are same string for this lab (i.e, stop words like "the")

        Args:
            key (str): string for key to hash and insert to hash table
            data (str): value of the k-v pair, same string as key in this case

        Returns:
            None
        """
        if (self.num_items + 1) / self.table_size >= 1.5:
            enlarge(self)
        # if key == chr(0):
        #     return
        hkey = hash_string(key, self.table_size)
        # Case 1 : Empty slot - insert item
        if self.table[hkey] is None:
            self.table[hkey] = Node(key, data)
        else: # collision
            self.num_collisions += 1
            if self.table[hkey].key == key:
                # self.table[hkey] = Node(key, data)
                self.table[hkey].key = key
                self.table[hkey].val = data
            else:
                temp = self.table[hkey]
                inserted = False
                while temp:
                    if temp.key == key:
                        self.table[hkey].key = key
                        self.table[hkey].val = data
                        inserted = True
                        break
                    if temp.next is None:
                        break
                    temp = temp.next
                if not inserted:
                    temp.next = Node(key, data)
        self.num_items += 1

    def get(self, key):
        """Returns the value (the item of a key-item pair) from the hash table
        associated with given key. Raises keyerror if not found.

        Args:
            key (str) : key to retrieve k-v pair from

        Returns:
            str : value from given key

        Raises:
            KeyError
        """
        hkey = hash_string(key, self.table_size)
        if self.table[hkey] is None:
            raise KeyError
        temp = self.table[hkey]
        while temp is not None:
            if temp.key == key:
                return temp.val
            temp = temp.next
        raise KeyError

    def contains(self, key):
        """Returns true if key is in table, otherwise false.

        Args:
            key (str) : key to check existence in table

        Returns:
            bool : True if key is in table. False if not.
        """
        hkey = hash_string(key, self.table_size)
        temp = self.table[hkey]
        # if key is chr(0):
        #     return False
        if self.table[hkey] is None:
            return False
        while temp is not None:
            if temp.key == key:
                # print('temp key', temp.key)
                # print('key', key)
                return True
            temp = temp.next
        return False

    def remove(self, key):
        """Removes the k-v pair from hash table and returns pair.
        Else raise KeyError if not found.

        Args:
            key (str) : key of k-v pair to be removed

        Returns:
            Node : the k-v pair removed at key's hash location on table

        Raises:
            KeyError: key-item pair not found
        """
        hkey = hash_string(key, self.table_size)
        if self.table[hkey] is None:
            raise KeyError

        curr = self.table[hkey]
        nxt = self.table[hkey].next
        if curr.key == key:
            # print('from remove', self.table[hkey])
            self.num_items -= 1
            curr = curr.next
            return curr
            # print('from remove', self.table[hkey])
        while nxt is not None:
            if nxt.key == key:
                self.num_items -= 1
                curr.next = nxt.next
                return nxt
            nxt = nxt.next
        raise KeyError

    def size(self):
        """Gets the number of key-value pairs in the hash table.

        Args:
            None

        Returns:
            int : the number of k-v pairs in hash table
        """
        return self.num_items

    def load_factor(self):
        """Returns the current load factor of the hash table.

        Args:
            None

        Returns:
            int : the current load factor
        """
        return self.num_items / self.table_size
        # lf = str(self.num_items / self.table_size)
        # lf = lf[:-14:]
        # return lf

    def collisions(self):
        """Returns number of collisions.
        A collision is defined as trying to insert an item into the table at
        a location with an already existing key-item pair. Collisions are not
        incremented when resizing, unless new item insertion is a collision.

        Args:
            None

        Returns:
            int : number of collisions that have occured during insertions
        """
        return self.num_collisions

class HashTableLinear:
    """Hash table that holds key-value pairs with linear probing collision
    handling.

    Attributes:
        size (int) : size/capacity of the table
        num_items (int) : number of k-v pairs currently in table
        num_collisions (int) : number of collisions during insertions
        table (list) : a list of of k-v pairs
    """

    def __init__(self, table_size=11):
        self.table_size = table_size
        self.num_items = 0
        self.num_collisions = 0
        self.table = [None] * self.table_size

    def __eq__(self, other):
        return isinstance(other, HashTableSepchain)\
        and (self.table_size == other.table_size)\
        and (self.num_collisions == other.num_collisions)\
        and (self.num_items == other.num_items)\
        and (self.table == other.table)

    def __repr__(self):
        return 'HashTableLinear\
        (size=%s, num_items=%s, num_collisions=%s, table=%s)'\
        % (self.table_size, self.num_items, self.num_collisions, self.table)

    def __getitem__(self, key):
        """implementing this method enables getting an item with [] notation
        This function calls your get method.

        Args:
            key (str) : a key which is compareable by <,>,==
        Returns:
            any : the value associated with the key
        Raises:
            KeyError : it raises KeyError because the get function in bst.py raises the error.
        """
        return self.get(key)

    def __setitem__(self, key, val):
        """implementing this method enables setting a key value pair with [] notation
        This function calls your put method.

        Args:
            key (any) : a key which is compareable by <,>,==
            val (any): the value associated with the key
        """
        self.put(key, val)

    def __contains__(self, key):
        """implementing this method enables checking if a key exists with in notaion

        Args:
            key (any) : a key which is compareable by <,>,==
        Returns:
            bool : True is the key exists, otherwise False
        """
        return self.contains(key)

    def keys(self):
        """gets all keys in hash table

            Returns:
                list : list of keys in hash table
        """
        keys = []
        for idx, node in enumerate(self.table):
            if node:
                keys.append(node.key)
        return keys

    def put(self, key, data):
        """Takes a key and data, then stores the key-value pair into a hash
        table based on the hash value of the key.

        If k-v pair is duplicate, the old k-v pair will be replaced by new k-v pair.
        If load factor of hash table is greater than following values, hash table
        doubles its size and stores old data in new one.

        Load factors for:

        Separate Chaining: 1.5
        Linear Probing: 0.75
        Quadratic Probing: 0.75

        Note: Key and data are same string for this lab (i.e, stop words like "the")

        Args:
            key (str): string for key to hash and insert to hash table
            data (str): value of the k-v pair, same string as key in this case

        Returns:
            None
        """
        if (self.num_items + 1) / self.table_size >= 0.75:
            enlarge(self)
        # if key == chr(0):
        #     return
        hkey = hash_string(key, self.table_size)
        while True:
            if self.table[hkey] is None:
                self.table[hkey] = Node(key, data)
                break
            if self.table[hkey].key == key:
                self.table[hkey].key = key
                self.table[hkey].val = data
                self.num_collisions += 1
                break
            hkey = (hkey + 1) % self.table_size
            self.num_collisions += 1
        self.num_items += 1

    def get(self, key):
        """Returns the value (the item of a key-item pair) from the hash table
        associated with given key. Raises keyerror if not found.

        Args:
            key (str) : key to retrieve k-v pair from

        Returns:
            str : value from given key

        Raises:
            KeyError
        """
        hkey = hash_string(key, self.table_size)
        count = 0
        if self.table[hkey] is None:
            raise KeyError
        while True:
            count += 1
            if count > self.table_size:
                raise KeyError
            if self.table[hkey] is None:
                hkey = (hkey + 1) % self.table_size
                continue
            if self.table[hkey].key == key:
                return self.table[hkey].val
            hkey = (hkey + 1) % self.table_size

    def contains(self, key):
        """Returns true if key is in table, otherwise false.

        Args:
            key (str) : key to check existence in table

        Returns:
            bool : True if key is in table. False if not.
        """
        hkey = hash_string(key, self.table_size)
        count = 0
        if self.table[hkey] is None:
            return False
        while True:
            count += 1
            # print("key: ", key)
            # print("hkey: ", hkey)
            # print('count:', count)
            # print(self)
            if count > self.table_size:
                return False
            if self.table[hkey] is None:
                hkey = (hkey + 1) % self.table_size
                continue
            if self.table[hkey].key == key:
                return True
            # if count - 1 >= self.table_size:
            #     return False
            hkey = (hkey + 1) % self.table_size

            # hkey = (hkey + 1) % self.table_size

    def remove(self, key):
        """Removes the k-v pair from hash table and returns pair.
        Else raise KeyError if not found.

        Args:
            key (str) : key of k-v pair to be removed

        Returns:
            Node : the k-v pair removed at key's hash location on table

        Raises:
            KeyError: key-item pair not found
        """
        hkey = hash_string(key, self.table_size)
        count = 0
        if self.table[hkey] is None:
            raise KeyError
        while True:
            count += 1
            if count > self.table_size:
                raise KeyError
            if self.table[hkey] is None:
                hkey = (hkey + 1) % self.table_size
                continue
            if self.table[hkey].key == key:
                pair = self.table[hkey]
                self.table[hkey] = None
                self.num_items -= 1
                return pair
            hkey = (hkey + 1) % self.table_size


    def size(self):
        """Gets the number of key-value pairs in the hash table.

        Args:
            None

        Returns:
            int : the number of k-v pairs in hash table
        """
        return self.num_items

    def load_factor(self):
        """Returns the current load factor of the hash table.

        Args:
            None

        Returns:
            int : the current load factor
        """
        return self.num_items / self.table_size
        # lf = str(self.num_items / self.table_size)
        # lf = lf[:-14:]
        # return lf

    def collisions(self):
        """Returns number of collisions.
        A collision is defined as trying to insert an item into the table at
        a location with an already existing key-item pair. Collisions are not
        incremented when resizing, unless new item insertion is a collision.

        Args:
            None

        Returns:
            int : number of collisions that have occured during insertions
        """
        return self.num_collisions

class HashTableQuadratic:
    def __init__(self, table_size=11):
        self.table_size = table_size
        self.num_items = 0
        self.num_collisions = 0
        self.table = [None] * self.table_size

    def __eq__(self, other):
        return isinstance(other, HashTableSepchain)\
        and (self.table_size == other.table_size)\
        and (self.num_collisions == other.num_collisions)\
        and (self.num_items == other.num_items)\
        and (self.table == other.table)

    def __repr__(self):
        return 'HashTableSepchain\
        (size=%s, num_items=%s, num_collisions=%s, table=%s)'\
        % (self.table_size, self.num_items, self.num_collisions, self.table)

    def __getitem__(self, key):
        """implementing this method enables getting an item with [] notation
        This function calls your get method.

        Args:
            key (str) : a key which is compareable by <,>,==
        Returns:
            any : the value associated with the key
        Raises:
            KeyError : it raises KeyError because the get function in bst.py raises the error.
        """
        return self.get(key)

    def __setitem__(self, key, val):
        """implementing this method enables setting a key value pair with [] notation
        This function calls your put method.

        Args:
            key (any) : a key which is compareable by <,>,==
            val (any): the value associated with the key
        """
        self.put(key, val)

    def __contains__(self, key):
        """implementing this method enables checking if a key exists with in notaion

        Args:
            key (any) : a key which is compareable by <,>,==
        Returns:
            bool : True is the key exists, otherwise False
        """
        return self.contains(key)

    # def quad_probing(self, key):


    def put(self, key, data):
        """Takes a key and data, then stores the key-value pair into a hash
        table based on the hash value of the key.

        If k-v pair is duplicate, the old k-v pair will be replaced by new k-v pair.
        If load factor of hash table is greater than following values, hash table
        doubles its size and stores old data in new one.

        Load factors for:

        Separate Chaining: 1.5
        Linear Probing: 0.75
        Quadratic Probing: 0.75

        Note: Key and data are same string for this lab (i.e, stop words like "the")

        Args:
            key (str): string for key to hash and insert to hash table
            data (str): value of the k-v pair, same string as key in this case

        Returns:
            None
        """
        if (self.num_items + 1) / self.table_size >= 0.75:
            enlarge(self)
        # if key == chr(0):
        #     return
        hkey = hash_string(key, self.table_size)
        for i in range(1, self.table_size + 1):
            if self.table[hkey] is None:
                self.table[hkey] = Node(key, data)
                break
            if self.table[hkey].key == key:
                self.table[hkey].key = key
                self.table[hkey].val = data
                self.num_collisions += 1
                break
            hkey = (hkey + i**2) % self.table_size
            self.num_collisions += 1
        self.num_items += 1

    def get(self, key):
        """Returns the value (the item of a key-item pair) from the hash table
        associated with given key. Raises keyerror if not found.

        Args:
            key (str) : key to retrieve k-v pair from

        Returns:
            str : value from given key

        Raises:
            KeyError
        """
        hkey = hash_string(key, self.table_size)
        count = 0
        if self.table[hkey] is None:
            raise KeyError
        while True:
            count += 1
            if count > self.table_size:
                raise KeyError
            if self.table[hkey] is None:
                hkey = (hkey + 1) % self.table_size
                continue
            if self.table[hkey].key == key:
                return self.table[hkey].val
            hkey = (hkey + 1) % self.table_size

    def contains(self, key):
        """Returns true if key is in table, otherwise false.

        Args:
            key (str) : key to check existence in table

        Returns:
            bool : True if key is in table. False if not.
        """
        hkey = hash_string(key, self.table_size)
        count = 0
        if self.table[hkey] is None:
            return False
        while True:
            count += 1
            # print("key: ", key)
            # print("hkey: ", hkey)
            # print('count:', count)
            # print(self)
            if count > self.table_size:
                return False
            if self.table[hkey] is None:
                hkey = (hkey + 1) % self.table_size
                continue
            if self.table[hkey].key == key:
                return True
            hkey = (hkey + 1) % self.table_size

    def remove(self, key):
        """Removes the k-v pair from hash table and returns pair.
        Else raise KeyError if not found.

        Args:
            key (str) : key of k-v pair to be removed

        Returns:
            Node : the k-v pair removed at key's hash location on table

        Raises:
            KeyError: key-item pair not found
        """
        hkey = hash_string(key, self.table_size)
        count = 0
        if self.table[hkey] is None:
            raise KeyError
        while True:
            count += 1
            if count > self.table_size:
                raise KeyError
            if self.table[hkey] is None:
                hkey = (hkey + 1) % self.table_size
                continue
            if self.table[hkey].key == key:
                pair = self.table[hkey]
                self.table[hkey] = None
                self.num_items -= 1
                return pair
            hkey = (hkey + 1) % self.table_size
    def size(self):
        """Gets the number of key-value pairs in the hash table.

        Args:
            None

        Returns:
            int : the number of k-v pairs in hash table
        """
        return self.num_items

    def load_factor(self):
        """Returns the current load factor of the hash table.

        Args:
            None

        Returns:
            int : the current load factor
        """
        return self.num_items / self.table_size
        # lf = str(self.num_items / self.table_size)
        # lf = lf[:-14:]
        # return lf

    def collisions(self):
        """Returns number of collisions.
        A collision is defined as trying to insert an item into the table at
        a location with an already existing key-item pair. Collisions are not
        incremented when resizing, unless new item insertion is a collision.

        Args:
            None

        Returns:
            int : number of collisions that have occured during insertions
        """
        return self.num_collisions

def hash_string(string, size):
    hash = 0
    for char in string:
        # print('char', char, ord(char))
        hash = (hash*31 + ord(char)) % size
    return hash

def import_stopwords(filename, hashtable):
    """Imports a file of stop words and stores it into a hashtable object.
    Hashtable can be one of the different collision handling methods:
    separate chaining, linear probing, or quadratic probing

    Args:
        filename (file) : the file of stop words to be stored
        hashtable (HashTableXXX) : one of the different hash table classes

    Returns:
        hashtable : the hashtable with stop words inserted
    """
    with open(filename) as stopfile:
        for line in stopfile:
            for word in line.split():
                hashtable.put(word, word)
    return hashtable

def enlarge(table):
    table.table_size = 2*table.table_size + 1
    copy = table.table
    table.table = [None] * table.table_size
    table.num_items = 0
    for item in copy:
        while item:
            table.put(item.key, item.val)
            item = item.next
    return table

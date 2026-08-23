"""
RESTAURANT MANAGEMENT SYSTEM - Terminal Project
=================================================
Demonstrates core data structures & algorithms:
    - Stack           -> Order history / Undo last order
    - Queue           -> Kitchen order processing (FIFO)
    - Linked List     -> Customer records
    - Binary Search Tree -> Menu catalog (indexed & searched by price)
    - Graph (BFS/DFS) -> Restaurant table layout & waiter routes
    - Sorting (Merge Sort) -> Bill / order reports
    - Searching (Binary Search) -> Find a bill by exact amount

Run:  python restaurant_management_system.py
"""

import os
from collections import deque

# =====================================================================
#  1. STACK  ->  used for Order History (undo last order)
# =====================================================================
class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return None if self.is_empty() else self.items.pop()

    def peek(self):
        return None if self.is_empty() else self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def display(self):
        return list(reversed(self.items))   # most recent first


# =====================================================================
#  2. QUEUE  ->  used for Kitchen Order Processing (FIFO)
# =====================================================================
class Queue:
    def __init__(self):
        self.items = deque()

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        return None if self.is_empty() else self.items.popleft()

    def is_empty(self):
        return len(self.items) == 0

    def display(self):
        return list(self.items)


# =====================================================================
#  3. LINKED LIST  ->  used for Customer Records
# =====================================================================
class LLNode:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def insert_end(self, data):
        node = LLNode(data)
        self.size += 1
        if not self.head:
            self.head = node
            return
        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = node

    def delete(self, match_fn):
        prev, cur = None, self.head
        while cur:
            if match_fn(cur.data):
                if prev:
                    prev.next = cur.next
                else:
                    self.head = cur.next
                self.size -= 1
                return True
            prev, cur = cur, cur.next
        return False

    def find(self, match_fn):
        cur = self.head
        while cur:
            if match_fn(cur.data):
                return cur.data
            cur = cur.next
        return None

    def to_list(self):
        result, cur = [], self.head
        while cur:
            result.append(cur.data)
            cur = cur.next
        return result


# =====================================================================
#  4. BINARY SEARCH TREE  ->  Menu catalog, keyed by price
# =====================================================================
class BSTNode:
    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, key, data):
        self.root = self._insert(self.root, key, data)

    def _insert(self, node, key, data):
        if node is None:
            return BSTNode(key, data)
        if key < node.key:
            node.left = self._insert(node.left, key, data)
        else:
            node.right = self._insert(node.right, key, data)
        return node

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if node is None:
            return None
        if key == node.key:
            return node.data
        return self._search(node.left, key) if key < node.key else self._search(node.right, key)

    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result   # sorted ascending by price

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.data)
            self._inorder(node.right, result)

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            successor = node.right
            while successor.left:
                successor = successor.left
            node.key, node.data = successor.key, successor.data
            node.right = self._delete(node.right, successor.key)
        return node


# =====================================================================
#  5. GRAPH  ->  Restaurant table layout / waiter routes (BFS & DFS)
# =====================================================================
class Graph:
    def __init__(self):
        self.adj = {}

    def add_node(self, node):
        self.adj.setdefault(node, [])

    def add_edge(self, a, b, weight=1):
        self.add_node(a)
        self.add_node(b)
        self.adj[a].append((b, weight))
        self.adj[b].append((a, weight))

    def bfs_shortest_path(self, start, goal):
        if start not in self.adj or goal not in self.adj:
            return None
        visited = {start}
        queue = deque([[start]])
        while queue:
            path = queue.popleft()
            node = path[-1]
            if node == goal:
                return path
            for neighbor, _ in self.adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(path + [neighbor])
        return None

    def dfs(self, start, visited=None):
        if visited is None:
            visited = []
        if start not in self.adj:
            return visited
        visited.append(start)
        for neighbor, _ in self.adj.get(start, []):
            if neighbor not in visited:
                self.dfs(neighbor, visited)
        return visited


# =====================================================================
#  6. SORTING  ->  Merge Sort (used for bill/order reports)
# =====================================================================
def merge_sort(arr, key=lambda x: x):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key)
    right = merge_sort(arr[mid:], key)
    return _merge(left, right, key)


def _merge(left, right, key):
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# =====================================================================
#  7. SEARCHING  ->  Binary Search (find a bill by exact total amount)
# =====================================================================
def binary_search(sorted_arr, target, key=lambda x: x):
    lo, hi = 0, len(sorted_arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        val = key(sorted_arr[mid])
        if val == target:
            return sorted_arr[mid]
        elif val < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return None


# =====================================================================
#  DOMAIN MODELS
# =====================================================================
class MenuItem:
    _counter = 1

    def __init__(self, name, price, category="General"):
        self.item_id = MenuItem._counter
        MenuItem._counter += 1
        self.name = name
        self.price = price
        self.category = category

    def __repr__(self):
        return f"[#{self.item_id}] {self.name:<20} ${self.price:>7.2f}  ({self.category})"


class Customer:
    _counter = 1

    def __init__(self, name, phone):
        self.customer_id = Customer._counter
        Customer._counter += 1
        self.name = name
        self.phone = phone

    def __repr__(self):
        return f"[#{self.customer_id}] {self.name:<20} {self.phone}"


class Order:
    _counter = 1

    def __init__(self, customer_name, items):
        self.order_id = Order._counter
        Order._counter += 1
        self.customer_name = customer_name
        self.items = items                 # list of MenuItem
        self.total = round(sum(i.price for i in items), 2)

    def __repr__(self):
        item_names = ", ".join(i.name for i in self.items)
        return f"Order#{self.order_id} | {self.customer_name} | [{item_names}] | Total: ${self.total:.2f}"


# =====================================================================
#  RESTAURANT SYSTEM  ->  ties every structure together
# =====================================================================
class RestaurantSystem:
    def __init__(self):
        self.menu_bst = BST()                 # menu catalog by price
        self.menu_lookup = {}                 # item_id -> MenuItem (quick access)
        self.customers = LinkedList()         # customer records
        self.kitchen_queue = Queue()          # pending orders (FIFO)
        self.order_history = Stack()          # completed/placed orders (undo-able)
        self.served_orders = []               # for billing reports
        self.table_graph = Graph()            # table layout

        self._seed_demo_data()

    # ---------------- demo data so the program isn't empty on first run ----------------
    def _seed_demo_data(self):
        for name, price, cat in [
            ("Margherita Pizza", 8.99, "Main"),
            ("Caesar Salad", 6.50, "Starter"),
            ("Grilled Chicken", 12.75, "Main"),
            ("Iced Tea", 2.25, "Beverage"),
            ("Chocolate Cake", 5.00, "Dessert"),
        ]:
            item = MenuItem(name, price, cat)
            self.menu_bst.insert(item.price, item)
            self.menu_lookup[item.item_id] = item

        self.customers.insert_end(Customer("Alice Johnson", "555-0101"))
        self.customers.insert_end(Customer("Bob Smith", "555-0102"))

        # Table layout: T1 - T2 - T3
        #                |         |
        #               T4 ------ T5
        self.table_graph.add_edge("T1", "T2")
        self.table_graph.add_edge("T2", "T3")
        self.table_graph.add_edge("T1", "T4")
        self.table_graph.add_edge("T3", "T5")
        self.table_graph.add_edge("T4", "T5")

    # ------------------------- MENU (BST) -------------------------
    def add_menu_item(self, name, price, category):
        item = MenuItem(name, price, category)
        self.menu_bst.insert(price, item)
        self.menu_lookup[item.item_id] = item
        return item

    def view_menu_sorted(self):
        return self.menu_bst.inorder()

    def search_menu_by_price(self, price):
        return self.menu_bst.search(price)

    def remove_menu_item(self, item_id):
        item = self.menu_lookup.pop(item_id, None)
        if item:
            self.menu_bst.delete(item.price)
        return item

    # ------------------------- CUSTOMERS (Linked List) -------------------------
    def add_customer(self, name, phone):
        c = Customer(name, phone)
        self.customers.insert_end(c)
        return c

    def remove_customer(self, customer_id):
        return self.customers.delete(lambda c: c.customer_id == customer_id)

    def list_customers(self):
        return self.customers.to_list()

    # ------------------------- ORDERS (Queue + Stack) -------------------------
    def place_order(self, customer_name, item_ids):
        items = [self.menu_lookup[i] for i in item_ids if i in self.menu_lookup]
        if not items:
            return None
        order = Order(customer_name, items)
        self.kitchen_queue.enqueue(order)     # goes to kitchen
        self.order_history.push(order)        # tracked for undo
        return order

    def serve_next_order(self):
        order = self.kitchen_queue.dequeue()
        if order:
            self.served_orders.append(order)  # goes to billing history
        return order

    def undo_last_order(self):
        """Cancels the most recently placed order (removes from queue if still pending)."""
        last_order = self.order_history.pop()
        if last_order is None:
            return None
        # remove it from the kitchen queue if it hasn't been served yet
        if last_order in self.kitchen_queue.items:
            self.kitchen_queue.items.remove(last_order)
        return last_order

    def pending_orders(self):
        return self.kitchen_queue.display()

    def order_history_list(self):
        return self.order_history.display()

    # ------------------------- TABLES (Graph) -------------------------
    def add_table(self, name):
        self.table_graph.add_node(name)

    def connect_tables(self, a, b):
        self.table_graph.add_edge(a, b)

    def find_route(self, start, goal):
        return self.table_graph.bfs_shortest_path(start, goal)

    def all_reachable_tables(self, start):
        return self.table_graph.dfs(start)

    # ------------------------- BILLING (Sort + Search) -------------------------
    def sorted_bills(self):
        return merge_sort(self.served_orders, key=lambda o: o.total)

    def find_bill_by_amount(self, amount):
        sorted_list = self.sorted_bills()
        return binary_search(sorted_list, amount, key=lambda o: o.total)


# =====================================================================
#  TERMINAL UI
# =====================================================================
def clear():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("\nPress Enter to continue...")


def read_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")


def read_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid whole number.")


def menu_management(sys_: RestaurantSystem):
    while True:
        clear()
        print("=== MENU MANAGEMENT (Binary Search Tree) ===")
        print("1. Add menu item")
        print("2. View menu (sorted by price)")
        print("3. Search item by exact price")
        print("4. Remove menu item")
        print("0. Back")
        choice = input("Choose: ").strip()

        if choice == "1":
            name = input("Item name: ")
            price = read_float("Price: $")
            category = input("Category: ") or "General"
            item = sys_.add_menu_item(name, price, category)
            print(f"Added: {item}")
        elif choice == "2":
            print("\n--- Menu (ascending price) ---")
            for item in sys_.view_menu_sorted():
                print(item)
        elif choice == "3":
            price = read_float("Search price: $")
            result = sys_.search_menu_by_price(price)
            print(f"Found: {result}" if result else "No item at that exact price.")
        elif choice == "4":
            item_id = read_int("Item ID to remove: ")
            removed = sys_.remove_menu_item(item_id)
            print(f"Removed: {removed}" if removed else "Item not found.")
        elif choice == "0":
            return
        pause()


def customer_management(sys_: RestaurantSystem):
    while True:
        clear()
        print("=== CUSTOMER MANAGEMENT (Linked List) ===")
        print("1. Add customer")
        print("2. View all customers")
        print("3. Remove customer")
        print("0. Back")
        choice = input("Choose: ").strip()

        if choice == "1":
            name = input("Name: ")
            phone = input("Phone: ")
            c = sys_.add_customer(name, phone)
            print(f"Added: {c}")
        elif choice == "2":
            print(f"\n--- Customers ({sys_.customers.size}) ---")
            for c in sys_.list_customers():
                print(c)
        elif choice == "3":
            cid = read_int("Customer ID to remove: ")
            ok = sys_.remove_customer(cid)
            print("Removed." if ok else "Customer not found.")
        elif choice == "0":
            return
        pause()


def order_management(sys_: RestaurantSystem):
    while True:
        clear()
        print("=== ORDER MANAGEMENT (Queue + Stack) ===")
        print("1. Place new order")
        print("2. Serve next order (dequeue kitchen)")
        print("3. Undo last placed order")
        print("4. View pending orders (queue)")
        print("5. View order history (stack, latest first)")
        print("0. Back")
        choice = input("Choose: ").strip()

        if choice == "1":
            print("\nCurrent menu:")
            for item in sys_.view_menu_sorted():
                print(item)
            name = input("Customer name: ")
            ids_raw = input("Enter item IDs separated by commas (e.g. 1,3,4): ")
            try:
                item_ids = [int(x.strip()) for x in ids_raw.split(",") if x.strip()]
            except ValueError:
                item_ids = []
            order = sys_.place_order(name, item_ids)
            print(f"Placed: {order}" if order else "Invalid item selection.")
        elif choice == "2":
            order = sys_.serve_next_order()
            print(f"Served: {order}" if order else "No pending orders.")
        elif choice == "3":
            cancelled = sys_.undo_last_order()
            print(f"Cancelled: {cancelled}" if cancelled else "Nothing to undo.")
        elif choice == "4":
            print("\n--- Pending Kitchen Orders (FIFO) ---")
            for o in sys_.pending_orders():
                print(o)
        elif choice == "5":
            print("\n--- Order History (most recent first) ---")
            for o in sys_.order_history_list():
                print(o)
        elif choice == "0":
            return
        pause()


def table_management(sys_: RestaurantSystem):
    while True:
        clear()
        print("=== TABLE LAYOUT (Graph - BFS / DFS) ===")
        print("1. Add table")
        print("2. Connect two tables (path exists between them)")
        print("3. Find shortest route between two tables (BFS)")
        print("4. List all tables reachable from a table (DFS)")
        print("0. Back")
        choice = input("Choose: ").strip()

        if choice == "1":
            name = input("Table name (e.g. T6): ")
            sys_.add_table(name)
            print(f"Table {name} added.")
        elif choice == "2":
            a = input("Table A: ")
            b = input("Table B: ")
            sys_.connect_tables(a, b)
            print(f"Connected {a} <-> {b}")
        elif choice == "3":
            a = input("Start table: ")
            b = input("Destination table: ")
            path = sys_.find_route(a, b)
            print(f"Shortest route: {' -> '.join(path)}" if path else "No route found.")
        elif choice == "4":
            a = input("Start table: ")
            reachable = sys_.all_reachable_tables(a)
            print(f"Reachable from {a}: {reachable}")
        elif choice == "0":
            return
        pause()


def billing_reports(sys_: RestaurantSystem):
    while True:
        clear()
        print("=== BILLING & REPORTS (Merge Sort + Binary Search) ===")
        print("1. View all served bills (sorted by total, ascending)")
        print("2. Find a bill by exact total amount (binary search)")
        print("0. Back")
        choice = input("Choose: ").strip()

        if choice == "1":
            bills = sys_.sorted_bills()
            if not bills:
                print("No served orders yet. Serve some orders first!")
            for b in bills:
                print(b)
        elif choice == "2":
            amount = read_float("Enter exact bill total to find: $")
            result = sys_.find_bill_by_amount(amount)
            print(f"Found: {result}" if result else "No bill with that exact total.")
        elif choice == "0":
            return
        pause()


def main():
    sys_ = RestaurantSystem()
    while True:
        clear()
        print("############################################")
        print("#   RESTAURANT MANAGEMENT SYSTEM (Terminal) #")
        print("############################################")
        print("1. Menu Management        (Binary Search Tree)")
        print("2. Customer Management    (Linked List)")
        print("3. Order Management       (Queue + Stack)")
        print("4. Table Layout / Routes  (Graph - BFS/DFS)")
        print("5. Billing & Reports      (Merge Sort + Binary Search)")
        print("0. Exit")
        choice = input("Choose: ").strip()

        if choice == "1":
            menu_management(sys_)
        elif choice == "2":
            customer_management(sys_)
        elif choice == "3":
            order_management(sys_)
        elif choice == "4":
            table_management(sys_)
        elif choice == "5":
            billing_reports(sys_)
        elif choice == "0":
            print("Thank you! Goodbye.")
            break
        else:
            print("Invalid choice.")
            pause()


if __name__ == "__main__":
    main()

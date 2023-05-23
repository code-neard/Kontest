class Node:
    def __init__(self, value, parent, left=None, right=None):
        self.value = value
        self.parent = parent
        self.left = left
        self.right = right

    def __str__(self):
        return f"{self.value}"


class Tree:
    def __init__(self, array: [] = None):
        self.root = None
        if array is not None and len(array) > 0:
            self.root = self.form_tree_from_array(array, 0, len(array))

    def form_tree_from_array(self, array: [], left: int, right: int) -> Node:
        if left + 1 > right:
            return None
        if left + 1 == right:
            return Node(array[left], None)
        middle = (left + right - 1) // 2
        node = Node(array[middle], None)
        node.left = self.form_tree_from_array(array, left, middle)
        node.right = self.form_tree_from_array(array, middle + 1, right)
        if node.left is not None:
            node.left.parent = node
        if node.right is not None:
            node.right.parent = node
        return node

    def add_array(self, array: []):
        if array is None or len(array) == 0:
            return
        for i in array:
            self.add(i)

    def add(self, value: int):
        if self.root is None:
            self.root = Node(value, None)
        parent_node = self.root
        node = self.root
        while node is not None:
            parent_node = node
            node = node.left if value < node.value else node.right
        new_node = Node(value, parent_node)
        if value < parent_node.value:
            parent_node.left = new_node
        else:
            parent_node.right = new_node

    def delete(self, node: Node):
        if node is None:
            return

        if node.left is None or node.right is None:
            child_node = node.left if node.left is not None else node.right
            if node == self.root:
                self.root = child_node
                if child_node is not None:
                    child_node.parent = None

            parent_node = node.parent
            if parent_node.left == node:
                parent_node.left = child_node
            else:
                parent_node.right = child_node

            if child_node is not None:
                child_node.parent = parent_node
        else:
            next_node = node.right
            while next_node.left is not None:
                next_node = next_node.left
            node.value = next_node.value
            self.delete(next_node)

    def find(self, value: int) -> Node:
        node = self.root
        while node is not None:
            if node.value == value:
                return node
            node = node.right if value > node.value else node.left
        return None

    def next(self, node: Node) -> Node:
        if node is None:
            return None
        if node.right is not None:
            next_node = node.right
            while next_node.left is not None:
                next_node = next_node.left
            return next_node
        next_node = node
        while next_node.parent is not None and next_node.parent.right == next_node:
            next_node = next_node.parent
        return next_node.parent

    def print(self, node: Node, nesting_level: []):
        if node is None:
            return

        deep_str = ""
        nesting_level_count = len(nesting_level)
        if nesting_level_count > 0:
            for i in range(nesting_level_count - 1):
                deep_str += '│   ' if nesting_level[i] else '    '

            deep_str += "├───" if nesting_level[nesting_level_count - 1] else "└───"

        print(f"{deep_str}{node}")
        self.print(node.left, nesting_level + [node.right is not None])
        self.print(node.right, nesting_level + [False])

    def __str__(self):
        self.print(self.root, [])
        return ""


def main():
    array = list(map(int, input().split()))
    tree = Tree(array)

    while True:
        command, *args = input().split()
        if command.startswith("add"):
            values = list(map(int, args))
            tree.add_array(values)
            print("Ok")
        elif command.startswith("delete"):
            value = int(args[0])
            node = tree.find(value)
            if node is not None:
                tree.delete(node)
            print("Ok")
        elif command.startswith("find"):
            value = int(args[0])
            node = tree.find(value)
            print("Число нашлось" if node is not None else "Число не нашлось")
        elif command.startswith("next"):
            value = int(args[0])
            node = tree.find(value)
            if node is not None:
                node = tree.next(node)
            print(node if node is not None else "Следующего числа нет")
        elif command.startswith("print"):
            print(tree, end="")
        elif command.startswith("exit"):
            break


if __name__ == "__main__":
    main()

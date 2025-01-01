class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def get_height(self, root: Node) -> int:
        if not root:
            return 0
        return root.height

    def get_balance(self, root: Node) -> int:
        if not root:
            return 0
        return self.get_height(root.left) - self.get_height(root.right)

    def rotate_right(self, y: Node) -> Node:

        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        y.height = 1 + max(self.get_height(y.left),
                           self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left),
                           self.get_height(x.right))

        return x

    def rotate_left(self, x: Node) -> Node:
        
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(self.get_height(x.left),
                           self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left),
                           self.get_height(y.right))

        return y

    def insert(self, root: Node, value: int) -> Node:
        if not root:
            return Node(value)
        elif value < root.value:
            root.left = self.insert(root.left, value)
        else:
            root.right = self.insert(root.right, value)

        root.height = 1 + max(self.get_height(root.left),
                              self.get_height(root.right))

        balance = self.get_balance(root)

        if balance > 1 and value < root.left.value:
            return self.rotate_right(root)

        if balance < -1 and value > root.right.value:
            return self.rotate_left(root)


        if balance > 1 and value > root.left.value:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)

        if balance < -1 and value < root.right.value:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)

        return root



if __name__ == "__main__":

    avl_tree = AVLTree()
    root = None

    values_to_insert = [20, 4, 15, 70, 50, 80, 10, 5, 3, 25]
    for val in values_to_insert:
        root = avl_tree.insert(root, val)

    print("Висота кореня:", avl_tree.get_height(root))
    print("Баланс кореня:", avl_tree.get_balance(root))

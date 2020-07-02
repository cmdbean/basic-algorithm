from algorithm import Node, KMeans, KNeighbor


def main():
    nodes = [
        Node(-3, -5, 'negative'),
        Node(-3, -5, 'negative'),
        Node(1, 2, 'positive'),
        Node(1.1, 2.1, 'positive'),
        Node(-3, -22, 'negative'),
    ]

    clf = KNeighbor(nodes=nodes, k=3)
    result = clf.predict(Node(0, 1))
    print(result)


if __name__ == '__main__':
    main()

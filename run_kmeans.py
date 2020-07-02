from algorithm import Node, KNeighbor, KMeans, LinearRegression


def main():
    nodes = [
        Node(-3, -5, 'negative'),
        Node(-3, -5, 'negative'),
        Node(1, 2, 'positive'),
        Node(1.1, 2.1, 'positive'),
        Node(-3, -22, 'negative'),
    ]

    clf = KMeans(nodes=nodes, k=2)
    clf.fit()


if __name__ == '__main__':
    main()

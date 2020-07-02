from algorithm import Node, LinearRegression


def main():
    clf = LinearRegression(nodes=[
        Node(50, 40),
        Node(60, 70),
        Node(70, 90),
        Node(80, 60),
        Node(90, 100),
    ])
    clf.fit()
    clf.show()
    print(clf.predict(70))


if __name__ == '__main__':
    main()

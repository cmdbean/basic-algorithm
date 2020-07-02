from collections import Counter
from dataclasses import dataclass
from typing import Union, List, Optional
from math import pow, sqrt
from random import random
from pprint import pprint


@dataclass
class Node:
    x: Union[float, int]
    y: Union[float, int]
    label: Optional[any] = None

    def get_distance(self, node):
        # 平面上における二点間の距離公式
        return sqrt(pow((node.x - self.x), 2) + pow((node.y - self.y), 2))


@dataclass
class LinearRegression:
    # 参考：https://sci-pursuit.com/math/statistics/least-square-method.html
    nodes: List[Node]
    slope: Optional[Union[float, int]] = None
    intercept: Optional[Union[float, int]] = None

    def fit(self):
        # ステップ 1：平均値を求める 
        x_avg = sum([n.x for n in self.nodes]) / len(self.nodes)
        y_avg = sum([n.y for n in self.nodes]) / len(self.nodes)

        # ステップ 2：偏差を求める
        x_deviations = [n.x - x_avg for n in self.nodes]
        y_deviations = [n.y - y_avg for n in self.nodes]

        # ステップ 3：変数 x の分散を求める
        x_variances = sum([pow(d, 2) for d in x_deviations]) / len(x_deviations)

        # ステップ 4：共分散を求める
        covariance = sum([x * y for x, y in zip(x_deviations, y_deviations)]) / len(x_deviations)

        # ステップ 5：傾きを求める
        self.slope = covariance / x_variances

        # ステップ 6：y 切片を求める
        self.intercept = y_avg - self.slope * x_avg

    def show(self):
        assert self.slope is not None
        print(f'y = {str(self.slope)}x + {str(self.intercept)}')

    def predict(self, x):
        assert self.slope is not None
        return x * self.slope + self.intercept




@dataclass
class KNeighbor:
    nodes: List[Node]
    k: int

    def predict(self, node) -> str:
        distances = {idx: node.get_distance(n) for idx, n in enumerate(self.nodes)}
        distances = sorted(distances.items(), key=lambda x: x[1])
        labels = [self.nodes[idx].label for idx, _ in distances][:self.k]
        c = Counter(labels)

        return c.most_common(1)[0][0]


@dataclass
class KMeans:
    nodes: List[Node]
    k: int
    centers = []

    def update_centers(self):
        if not self.centers:
            max_x = max([n.x for n in self.nodes])
            max_y = max([n.y for n in self.nodes])

            self.centers = [Node(random() * max_x, random() * max_y, label=i) for i in range(self.k)]
        else:
            for idx, center in enumerate(self.centers):
                related_nodes = [n for n in self.nodes if n.label == center.label]
                self.centers[idx].x = sum([n.x for n in related_nodes]) / len(related_nodes)
                self.centers[idx].y = sum([n.y for n in related_nodes]) / len(related_nodes)

    def map_nodes(self):
        total_distance = 0
        for node_idx, node in enumerate(self.nodes):
            distances = {idx: node.get_distance(c) for idx, c in enumerate(self.centers)}
            distances = sorted(distances.items(), key=lambda x: x[1])
            self.nodes[node_idx].label = distances[0][0]
            total_distance += distances[0][1]

        return total_distance

    def fit(self):
        total_distance = 0
        for _ in range(100):
            self.update_centers()

            _total_distance = self.map_nodes()
            if total_distance == _total_distance:
                break
            total_distance = +_total_distance
            print('total distance', total_distance)
        pprint(self.nodes)
















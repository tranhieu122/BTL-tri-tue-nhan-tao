"""
benchmark.py – Đo hiệu năng các thuật toán tìm kiếm trên đồ thị G1.
  - Mỗi thuật toán được chạy 20 lần
  - Tính thời gian trung bình (ms)
  - Xuất kết quả ra màn hình và file result.csv
"""

import time
import csv

from graph      import G1_GRAPH, G1_HEURISTIC, G1_START, G1_GOAL
from bfs        import bfs
from dfs        import dfs
from ids        import ids
from best_first import best_first
from gbfs       import gbfs
from astar      import astar

RUNS = 20

ALGORITHMS = [
    ('DFS',         lambda: dfs(G1_GRAPH, G1_START, G1_GOAL)),
    ('BFS',         lambda: bfs(G1_GRAPH, G1_START, G1_GOAL)),
    ('IDS',         lambda: ids(G1_GRAPH, G1_START, G1_GOAL)),
    ('Best-First',  lambda: best_first(G1_GRAPH, G1_START, G1_GOAL)),
    ('GBFS',        lambda: gbfs(G1_GRAPH, G1_HEURISTIC, G1_START, G1_GOAL)),
    ('A*',          lambda: astar(G1_GRAPH, G1_HEURISTIC, G1_START, G1_GOAL)),
]


def run_benchmark():
    results = []

    for name, algo in ALGORITHMS:
        times = []
        result = None

        for _ in range(RUNS):
            t0 = time.perf_counter()
            result = algo()
            t1 = time.perf_counter()
            times.append(t1 - t0)

        avg_ms = (sum(times) / RUNS) * 1000

        if result:
            path_str  = '→'.join(result['path'])
            cost      = result['cost']
            expanded  = result['expanded']
            generated = result['generated']
        else:
            path_str  = 'Không tìm thấy'
            cost = expanded = generated = '-'

        results.append({
            'algorithm':   name,
            'path':        path_str,
            'cost':        cost,
            'expanded':    expanded,
            'generated':   generated,
            'avg_time_ms': round(avg_ms, 4),
        })

    return results


def print_table(headers, rows):
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))

    def fmt(row):
        return ' | '.join(str(c).ljust(widths[i]) for i, c in enumerate(row))

    sep = '-+-'.join('-' * w for w in widths)
    print(fmt(headers))
    print(sep)
    for row in rows:
        print(fmt(row))


def print_results(results):
    headers = ['Thuật toán', 'Đường đi', 'Chi phí',
               'Node mở', 'Node sinh', 'TG TB (ms)']
    rows = [
        [r['algorithm'], r['path'], r['cost'],
         r['expanded'], r['generated'], r['avg_time_ms']]
        for r in results
    ]

    print()
    print('=' * 75)
    print(f'  BENCHMARK – {RUNS} lần chạy / thuật toán  (đồ thị G1: S → G)')
    print('=' * 75)
    print_table(headers, rows)
    print()


def save_csv(results, filepath='result.csv'):
    with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'algorithm', 'path', 'cost', 'expanded', 'generated', 'avg_time_ms'
        ])
        writer.writeheader()
        writer.writerows(results)
    print(f'Kết quả đã lưu vào: {filepath}')


if __name__ == '__main__':
    results = run_benchmark()
    print_results(results)
    save_csv(results)

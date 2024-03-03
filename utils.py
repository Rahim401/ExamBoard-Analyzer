from tabulate import tabulate


def printTable(resultTable):
    data = [list(row) for row in resultTable]
    print(tabulate(headers=resultTable.keys(), tabular_data=data, tablefmt='outline'))
# 实例1
"""
列出1到20的数字，
若是3的倍数就用apple代替，
若是5的倍数就用orange代替，
若既是3的倍数又是5的倍数就用appleorange代替
"""
import heapq
from collections import namedtuple

print(['apple'[i % 3 * 5::] + 'orange'[i % 5 * 6::] or i for i in range(1, 21)])

# input result
# [1, 2, 'apple', 4, 'orange', 'apple', 7, 8, 'apple', 'orange',
#  11, 'apple', 13, 14, 'appleorange', 16, 17, 'apple', 19, 'orange']
"""
分析:
'apple'[i%3*5::]: 从i(包括)开始切到最后
后面的5主要是取余后要么等于0,要么等于从1~4,乘以5之后,都切不到字符串
最后的or 是那三种情况都不满足情况下,就直接显示当前循环变量i
"""
# 实例2
# 推导列表生成字典
my_list = [(1, 'a'), (2, 'b')]
print({x[0]: x[1] for x in my_list})
# input result
# {1: 'a', 2: 'b'}

print({index: x for index, x in enumerate('abcd')})
# input result
# {0: 'a', 1: 'b', 2: 'c', 3: 'd'}

# 实例3
# 漂亮的zip生成
print(dict(zip('abcd', range(10))))
# input result
# {'a': 0, 'b': 1, 'c': 2, 'd': 3}

chinese = [90, 70, 96]

eng = [80, 78, 90]

math = [96, 84, 80]

total = []
for c, e, m in zip(chinese, eng, math):
    total.append(c + e + m)
print(total)

# input result
[266, 232, 266]

# 实例4
# if val is not None
# if val ,其中的val可以是'',0,None,[],{}

# 实例5----list分组
a = [3, 8, 9, 4, 1, 10, 6, 7, 2]
list(a[i:i + 3] for i in range(0, len(a), 3))
# input result
# [[3, 8, 9], [4, 1, 10], [6, 7, 2]]

# 实例6
"""
比如有一个嵌套的列表，里面嵌套了很多层，
有列表有元组，层层嵌套，
如何把它转换成只有一层的列表，必须要用递归也能解决
"""
cascade = [1, [2], [3, [4, [10, [34, 53]]]], (6, 98)]
stream = []


def flat(seq):
    for each in seq:
        if isinstance(each, list) or isinstance(each, tuple):
            flat(each)
        else:
            stream.append(each)


flat(cascade)
print(stream)
# result
# [1, 2, 3, 4, 10, 34, 53, 6, 98]


# 实例7---查询列表里面的某一个值
landscape = ['bog', 'cave', 'cliff', 'coast', 'desert', 'jungle']
list(filter(lambda x: x.startswith('c'), landscape))
# result
# ['cave', 'cliff', 'coast']

# 实例8 ----namedtuple
# ranks: 数字   suits:花色
Card = namedtuple('Card', ['rank', 'suit'])
c = Card('7', 'diamonds')
print(c)  # Card(rank='7', suit='diamonds')


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)]
    ranks = ranks + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                       for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]


f1 = FrenchDeck()
print(f1._cards)
print(f1.__len__())
print(f1.__getitem__(3))  # 下标从0开始

# result
# [Card(rank='2', suit='spades'), Card(rank='3', suit='spades')...]


# 实例9 ---获取列表,字典中的元素,进行排序
nums = [19, 3, 13, 54, 89]
print(heapq.nlargest(3, nums))
print(heapq.nsmallest(3, nums))
# [89, 54, 19]
# [3, 13, 19]

students = [
    {'weather': 'breeze', 'score': 100, 'height': 190},
    {'weather': 'chilly', 'score': 160, 'height': 130},
    {'weather': 'breeze', 'score': 120, 'height': 167},
    {'weather': 'breeze', 'score': 110, 'height': 128},
]

result = heapq.nsmallest(2, students, key=lambda x: x['height'])
print(result)
# [{'weather': 'breeze', 'score': 110, 'height': 128},
# {'weather': 'chilly', 'score': 160, 'height': 130}]

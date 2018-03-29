"""
给定两个非空链表来代表两个非负数，位数按照逆序方式存储，它们的每个节点只存储单个数字。将这两数相加会返回一个新的链表。

你可以假设除了数字 0 之外，这两个数字都不会以零开头。

示例：

输入：(2 -> 4 -> 3) + (5 -> 6 -> 4)
输出：7 -> 0 -> 8
原因：342 + 465 = 807
"""

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None


class Solution:
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        al = []
        flag = False
        for i in range(len(l1)):
            if flag == True:
                r = l1[i] + l2[i] + 1
                flag = False
            else:
                r = l1[i] + l2[i]
            if r > 10:
                m = r - 10
                flag = True
            else:
                m = r
            al.append(m)
        return al


s = Solution()
a = [9, 6, 9]
b = [3, 9, 5]
c = s.addTwoNumbers(a, b)
print(c)

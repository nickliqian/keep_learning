class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        carry = 0
        root = n = ListNode(0)
        while l1 or l2 or carry:
            v1 = v2 = 0
            if l1:
                v1 = l1.val
                l1 = l1.next
            if l2:
                v2 = l2.val
                l2 = l2.next
            # carry -> 十位->累积到上级节点并相加
            # val   -> 个位->赋值给当前节点相加
            carry, val = divmod(v1+v2+carry, 10)
            # 放到初始链n下个节点
            n.next = ListNode(val)
            # n作指针，每计算一次就移动一次
            n = n.next
        return root.next


l1 = ListNode(2)
l1.next = ListNode(4)
l1.next.next = ListNode(3)

l2 = ListNode(5)
l2.next = ListNode(6)
l2.next.next = ListNode(4)

s = Solution()

c = s.addTwoNumbers(l1, l2)
print(c.val)
print(c.next.val)
print(c.next.next.val)
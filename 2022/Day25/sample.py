class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


def lst2link(lst):
    cur = dummy = ListNode(0)
    for e in lst:
        cur.next = ListNode(e)
        cur = cur.next
    return dummy.next

# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        
        
        int3 = l1.val + l2.val
        result = ListNode(int3%10)   

        while l1.next and l2.next:
          l1, l2 = l1.next, l2.next
          int3 = l1.val + l2.val + int3//10
          result.next = ListNode(int3%10)
          
        while l1.next: 
          l1 = l1.next
          int3 = l1.val + int3//10
          result.next = ListNode(int3%10)
            
        while l2.next:
          l2 = l2.next
          int3 = l2.val + int3//10
          result.next = ListNode(int3%10)
        int3//=10
        if int3:
          result.next = ListNode(int3)

        return result
          
        # while l1.next:
        #   l1 = l1.next
        #   int1 = l1.val*pow(10,count) + int1
        #   count+=1
        # count = 1
        # print(int1)
        # while l2.next:
        #   l2 = l2.next
        #   int2 = int2 + l2.val*pow(10,count)
        #   count+=1
        # print(int2)
        # return int1+int2

l1 = [9,9,9,9,9,9,9] 
l2 = [9,9,9,9]
n1 = lst2link(l1)
n2 = lst2link(l2)
s = Solution()
print(s.addTwoNumbers(n1,n2))
  

ransomNote = "aabb"
magazine = "aab"
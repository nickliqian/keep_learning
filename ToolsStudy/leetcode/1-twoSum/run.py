class Solution:
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        d = dict()

        for i in range(len(nums)):
            if d.get(nums[i]) is not None:
                if d[nums[i]] != i:
                    return [d[nums[i]], i]
            else:
                d[target - nums[i]] = i


s = Solution()
r = s.twoSum([1,5,5,15], 10)
print(r)
def find_lengt(nums,k):
    left = ans = curr = 0
    for right in range(len(nums)):
        curr += nums[right]
        while curr > k:
            curr -= nums[left]
            left += 1
        ans = max(ans, right - left + 1)
        print('\n left-------->',left)
        print('\n right-------->',right)
        print('\n ans-------->',ans)
        print('--------------------------------------------')
    return ans

nums= [3,1,2,7,4,2,1,1,5]
find_lengt(nums,8)
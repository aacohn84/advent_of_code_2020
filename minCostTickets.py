class Solution(object):
    def mincostTickets(self, days, costs):
        """
        :type days: List[int]
        :type costs: List[int]
        :rtype: int
        """
        # Preconditions:
        # 1 <= days.length <= 365
        # 1 <= days[i] <= 365
        # days is strictly in increasing order
        # costs.length == 3
        # 1 <= costs <= 1000
        costPerDay = [
            costs[0] / 1.0, 
            costs[1] / 7.0, 
            costs[2] / 30.0
        ]


        return 0
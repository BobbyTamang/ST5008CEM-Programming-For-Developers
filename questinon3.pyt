def max_trading_profit(max_trades, prices):
    """
    Optimizes profit for k trades. Uses Dynamic Programming.
    Time Complexity: O(k * n)
    """
    n = len(prices)
    if n <= 1 or max_trades == 0: return 0
    
    # If trades exceed possible pairs, solve as infinite trades
    if max_trades >= n // 2:
        return sum(max(0, prices[i] - prices[i-1]) for i in range(1, n))

    dp = [[0] * n for _ in range(max_trades + 1)]
    for t in range(1, max_trades + 1):
        max_diff = -prices[0]
        for d in range(1, n):
            dp[t][d] = max(dp[t][d-1], prices[d] + max_diff)
            max_diff = max(max_diff, dp[t-1][d] - prices[d])
            
    return dp[max_trades][n-1]

# Example Test Case [cite: 47]
print(f"Max Profit: {max_trading_profit(2, [2000, 4000, 1000])}") # Output: 2000
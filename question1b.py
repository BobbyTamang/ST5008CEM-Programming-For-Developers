def word_break(user_query, dictionary):
    """
    Finds all possible sentences that can be formed by segmenting the query 
    using the provided dictionary words.
    """
    memo = {}

    def solve(s):
        if s in memo: return memo[s]
        if not s: return [""]
        
        res = []
        for word in dictionary:
            if s.startswith(word):
                suffixes = solve(s[len(word):])
                for suffix in suffixes:
                    res.append(word + (" " + suffix if suffix else ""))
        
        memo[s] = res
        return res

    return solve(user_query)

# Example Test Case [cite: 26]
query = "nepaltrekkingguide"
dict_words = ["nepal", "trekking", "guide", "nepaltrekking"]
print(f"Segments: {word_break(query, dict_words)}")
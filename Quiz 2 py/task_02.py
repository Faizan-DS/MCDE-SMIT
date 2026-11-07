# Task 02 | Longest Valid Window


def longest_unique_window(text):
    last_seen = {}
    start = 0
    best_start = 0
    best_len = 0
    for i, ch in enumerate(text):
        if ch in last_seen and last_seen[ch] >= start:
            start = last_seen[ch] + 1
        last_seen[ch] = i

        if i - start + 1 > best_len:
            best_len = i - start + 1
            best_start = start

    return (text[best_start:best_start + best_len], best_start, best_len)


print(longest_unique_window("abcabcbb"))   
print(longest_unique_window(""))           
print(longest_unique_window("a b!a b"))    
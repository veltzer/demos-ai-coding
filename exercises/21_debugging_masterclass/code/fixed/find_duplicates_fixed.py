def find_duplicates(items):
    seen = set()
    duplicates = set()  # Use set instead of list!

    for item in items:
        if item in seen:
            duplicates.add(item)  # Add to set (no duplicates)
        seen.add(item)

    return list(duplicates)

# Test
result = find_duplicates([1, 2, 2, 3, 3, 3, 4])
print(result)  # Expected: [2, 3], Got: [2, 3]

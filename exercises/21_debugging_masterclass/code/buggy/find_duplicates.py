def find_duplicates(items):
    seen = set()
    duplicates = []

    for item in items:
        if item in seen:
            duplicates.append(item)
        seen.add(item)

    return duplicates

# Bug: Returns [2, 3, 3] instead of [2, 3]
result = find_duplicates([1, 2, 2, 3, 3, 3, 4])
print(result)  # Expected: [2, 3], Got: [2, 3, 3]

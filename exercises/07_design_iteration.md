# Design iteration

Invent a task and write the code for it (you can use the AI for this one).

Example: given a set of files on the command line, count the number of words in every file and
print the following output:
[file1] [number of words in file1]
[file2] [number of words in file2]
[file3] [number of words in file3]
...

Now add a memory cache using AI
    If I enocunter the same file twice I only count the words the first time.

Now add a persistant cache using AI
    Even between runs if I encounter the same file I just pull the number of words
    from the cache.

What questions do we want to answer at the end?
- how do we know the file did not change? Did the AI handle that case?

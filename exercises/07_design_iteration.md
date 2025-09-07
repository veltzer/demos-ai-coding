# Design iteration

Given a task write the code for it.

Example: given a set of files on the command line, count the number of words in every file and
print the following output:
[file1] [number of works in file1]
[file2] [number of works in file2]
[file3] [number of works in file3]
...

Now add a memory cache using AI
    If I enocunter the same file twice I only count the words the first time.

Now add a persistant cache using AI
    Even between runs if I encounted the same file I just pull the number of words
    from the cache.

What questions do we want to answer at the end?

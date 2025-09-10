# Design Iteration with Copilot: Building a Robust File Word Counter

## Learning Objective
Learn how to iteratively improve code design using GitHub Copilot, implementing caching strategies, error handling, and performance optimizations through progressive enhancements.

## Instructions
1. Create a new Python file called `word_counter.py`
2. Start with a basic implementation
3. Use Copilot to iteratively add features
4. Learn how to guide Copilot through design improvements
5. Test each iteration to understand the improvements

## Your Task

### Part 1: Basic Implementation
Start by implementing a simple word counter with Copilot's help:

```python
#!/usr/bin/env python3
"""
Word counter utility that processes multiple files.
Counts words in each file and displays results.
"""

import sys

def count_words_in_file(filepath):
    """Count the number of words in a file."""
    # Let Copilot implement basic word counting
    
def main():
    """Main function to process command line arguments."""
    if len(sys.argv) < 2:
        print("Usage: word_counter.py <file1> [file2] [file3] ...")
        sys.exit(1)
    
    # Process each file from command line
    # Let Copilot complete the implementation
```

Expected output format:
```
[file1.txt] 1234 words
[file2.txt] 5678 words
[file3.txt] 910 words
Total: 7822 words
```

### Part 2: Add Memory Cache
Now enhance with an in-memory cache. Ask Copilot to help you implement:

```python
# Add at the top of your file
from functools import lru_cache
import os

class WordCounter:
    def __init__(self):
        self.cache = {}  # Simple dictionary cache
        self.cache_hits = 0
        self.cache_misses = 0
    
    def count_words_cached(self, filepath):
        """Count words with in-memory caching."""
        # Check if file is in cache
        # Let Copilot implement caching logic
        # Should only count words once per file
        
    def print_cache_stats(self):
        """Print cache hit/miss statistics."""
        # Let Copilot implement cache statistics
```

### Part 3: Add Persistent Cache
Enhance with persistent caching across program runs:

```python
import json
import hashlib
from datetime import datetime

class PersistentWordCounter(WordCounter):
    CACHE_FILE = ".word_count_cache.json"
    
    def __init__(self):
        super().__init__()
        self.persistent_cache = self.load_cache()
    
    def load_cache(self):
        """Load cache from disk."""
        # Let Copilot implement cache loading
        
    def save_cache(self):
        """Save cache to disk."""
        # Let Copilot implement cache saving
        
    def get_file_signature(self, filepath):
        """Generate a signature for file to detect changes."""
        # IMPORTANT: How do we know if file changed?
        # Consider: modification time, file size, content hash
        # Let Copilot suggest and implement
```

### Part 4: Advanced Features
Ask Copilot to help add these enhancements:

```python
# Features to add:
# 1. Parallel processing for multiple files
# 2. Support for different file encodings
# 3. Exclude patterns (skip certain words)
# 4. Progress bar for large file sets
# 5. Export results to JSON/CSV

from concurrent.futures import ThreadPoolExecutor
import csv
from tqdm import tqdm

class AdvancedWordCounter(PersistentWordCounter):
    def __init__(self, num_threads=4):
        super().__init__()
        self.num_threads = num_threads
        
    def count_words_parallel(self, filepaths):
        """Process multiple files in parallel."""
        # Let Copilot implement parallel processing
        
    def export_results(self, results, format='json'):
        """Export results to different formats."""
        # Let Copilot implement export functionality
```

## Critical Questions to Explore

### Cache Invalidation
Ask Copilot these questions and implement solutions:
1. "How should we detect if a file has changed since it was cached?"
2. "What happens if a file is deleted after being cached?"
3. "Should we use file modification time, size, or content hash?"
4. "How do we handle symbolic links and duplicate files?"

### Performance Considerations
Discuss with Copilot:
1. "What's the optimal cache size limit?"
2. "When should we evict cache entries?"
3. "How do we handle very large files?"
4. "Should we use memory mapping for large files?"

## What You'll Learn
- Iterative design improvement strategies
- Cache implementation patterns (memory and persistent)
- File change detection techniques
- Error handling in file operations
- Performance optimization techniques
- Parallel processing patterns
- Data persistence strategies

## Success Criteria
- [ ] Basic word counter works correctly
- [ ] Memory cache prevents re-counting same file
- [ ] Persistent cache works across program runs
- [ ] File changes are properly detected
- [ ] Cache statistics are accurately tracked
- [ ] Parallel processing improves performance
- [ ] Error handling is robust

## Test Scenarios

### Test Setup
Create test files with known word counts:
```bash
echo "one two three four five" > test1.txt  # 5 words
echo "six seven eight" > test2.txt          # 3 words
echo "nine ten" > test3.txt                 # 2 words
```

### Test Cases
```python
# Test 1: Basic counting
./word_counter.py test1.txt test2.txt test3.txt

# Test 2: Cache effectiveness (run twice)
./word_counter.py test1.txt test1.txt test2.txt

# Test 3: File modification detection
echo "additional words" >> test1.txt
./word_counter.py test1.txt  # Should detect change

# Test 4: Performance with many files
./word_counter.py *.txt

# Test 5: Error handling
./word_counter.py nonexistent.txt test1.txt
```

## Advanced Challenges

### Challenge 1: Smart Cache Strategies
Implement different caching strategies:
```python
class CacheStrategy:
    """Base class for cache strategies."""
    
class LRUCacheStrategy(CacheStrategy):
    """Least Recently Used cache eviction."""
    
class TTLCacheStrategy(CacheStrategy):
    """Time-To-Live based cache expiration."""
    
class SizeLimitedCache(CacheStrategy):
    """Cache with size limits."""
```

### Challenge 2: Configuration Management
Add configuration file support:
```python
# word_counter_config.yaml
cache:
  type: persistent
  max_size: 100MB
  ttl: 3600  # seconds
  
processing:
  parallel: true
  threads: 8
  
output:
  format: json
  verbose: true
```

### Challenge 3: Plugin Architecture
Create a plugin system for word counting algorithms:
```python
class WordCountPlugin:
    """Base class for word counting plugins."""
    
class SimpleWordCount(WordCountPlugin):
    """Count space-separated words."""
    
class NLTKWordCount(WordCountPlugin):
    """Use NLTK for advanced tokenization."""
    
class RegexWordCount(WordCountPlugin):
    """Custom regex-based word counting."""
```

## Code Review Questions
After implementation, ask Copilot to review:
1. "Are there any race conditions in the parallel processing?"
2. "Is the cache thread-safe?"
3. "What security issues might arise with the persistent cache?"
4. "How can we optimize memory usage for large file sets?"

## Real-World Applications
This pattern applies to:
- Build systems (detecting changed source files)
- Static site generators (regenerating only changed pages)
- Data processing pipelines (incremental processing)
- Backup systems (detecting modified files)
- Search indexers (updating only changed documents)

## Reflection Questions
1. How did the AI handle the file change detection problem?
2. What caching strategy did Copilot suggest and why?
3. Were there any edge cases the AI missed?
4. How did iterative improvements affect code complexity?
5. What would you do differently without AI assistance?

## Tips for Better AI Collaboration
1. **Be Specific**: When asking for cache implementation, specify your requirements
2. **Iterate Gradually**: Don't try to add all features at once
3. **Test Each Stage**: Verify each iteration works before adding complexity
4. **Question Assumptions**: Ask Copilot about edge cases and limitations
5. **Compare Approaches**: Ask for alternative implementations

## Expected Learning Outcomes
By completing this exercise, you should understand:
- How to guide AI through iterative design improvements
- Common caching patterns and their trade-offs
- File system operations and change detection
- Performance optimization techniques
- The importance of error handling and edge cases
- How to evaluate AI-generated solutions critically
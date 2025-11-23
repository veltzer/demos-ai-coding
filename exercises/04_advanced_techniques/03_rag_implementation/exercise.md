# RAG (Retrieval-Augmented Generation) Implementation

## Learning Objective
Learn how to implement Retrieval-Augmented Generation (RAG) systems to enhance AI assistants with domain-specific knowledge. Build systems that can search, retrieve, and use relevant context from large document collections to provide accurate, source-backed responses.

## What is RAG?

RAG combines:
- **Retrieval**: Finding relevant documents from a knowledge base
- **Augmentation**: Adding retrieved context to AI prompts
- **Generation**: Producing responses based on retrieved information

Benefits:
- **Accuracy**: Responses grounded in actual documents
- **Citations**: Can reference sources
- **Up-to-date**: Knowledge base can be updated without retraining
- **Domain-specific**: Customize for your specific needs
- **Reduced hallucination**: AI relies on retrieved facts

## Prerequisites
- Node.js 18+ installed
- GitHub Copilot configured
- Basic understanding of vector search
- Sample documents for indexing

---

## Part 1: Simple Document-Based RAG

### Exercise 1.1: Basic Document Indexer

Create `document-indexer.js`:

```javascript
const fs = require('fs').promises;
const path = require('path');
const crypto = require('crypto');

class DocumentIndexer {
  constructor(indexPath = './rag-index') {
    this.indexPath = indexPath;
    this.documents = new Map();
    this.index = new Map(); // term -> document IDs
    this.init();
  }

  async init() {
    await fs.mkdir(this.indexPath, { recursive: true });
    await this.loadIndex();
  }

  // Generate unique document ID
  generateId(content) {
    return crypto.createHash('md5').update(content).digest('hex').slice(0, 12);
  }

  // Simple tokenization
  tokenize(text) {
    return text
      .toLowerCase()
      .replace(/[^\w\s]/g, ' ')
      .split(/\s+/)
      .filter(word => word.length > 2);
  }

  // Index a document
  async indexDocument(filepath, content, metadata = {}) {
    const docId = this.generateId(filepath + content);

    // Split into chunks for better retrieval
    const chunks = this.chunkDocument(content);

    for (let i = 0; i < chunks.length; i++) {
      const chunkId = `${docId}_${i}`;
      const chunk = chunks[i];

      // Store document chunk
      const doc = {
        id: chunkId,
        filepath,
        content: chunk,
        metadata: {
          ...metadata,
          chunkIndex: i,
          totalChunks: chunks.length,
          indexed: new Date().toISOString(),
        },
      };

      this.documents.set(chunkId, doc);

      // Build inverted index
      const tokens = this.tokenize(chunk);
      for (const token of tokens) {
        if (!this.index.has(token)) {
          this.index.set(token, new Set());
        }
        this.index.get(token).add(chunkId);
      }
    }

    await this.saveIndex();
    return docId;
  }

  // Chunk document into smaller pieces
  chunkDocument(content, chunkSize = 500, overlap = 100) {
    const words = content.split(/\s+/);
    const chunks = [];

    for (let i = 0; i < words.length; i += chunkSize - overlap) {
      const chunk = words.slice(i, i + chunkSize).join(' ');
      if (chunk.trim()) {
        chunks.push(chunk);
      }
    }

    return chunks;
  }

  // Search documents using BM25-like scoring
  search(query, topK = 5) {
    const queryTokens = this.tokenize(query);
    const scores = new Map();

    // Calculate TF-IDF scores
    for (const token of queryTokens) {
      if (this.index.has(token)) {
        const docIds = this.index.get(token);
        const idf = Math.log((this.documents.size + 1) / (docIds.size + 1));

        for (const docId of docIds) {
          const doc = this.documents.get(docId);
          const tf = (doc.content.toLowerCase().match(new RegExp(token, 'g')) || []).length;
          const tfidf = tf * idf;

          scores.set(docId, (scores.get(docId) || 0) + tfidf);
        }
      }
    }

    // Sort by score and return top K
    const sorted = Array.from(scores.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, topK);

    return sorted.map(([docId, score]) => ({
      document: this.documents.get(docId),
      score,
    }));
  }

  // Save index to disk
  async saveIndex() {
    const indexData = {
      documents: Array.from(this.documents.entries()),
      index: Array.from(this.index.entries()).map(([term, docs]) => [term, Array.from(docs)]),
    };

    await fs.writeFile(
      path.join(this.indexPath, 'index.json'),
      JSON.stringify(indexData, null, 2)
    );
  }

  // Load index from disk
  async loadIndex() {
    try {
      const data = await fs.readFile(path.join(this.indexPath, 'index.json'), 'utf8');
      const indexData = JSON.parse(data);

      this.documents = new Map(indexData.documents);
      this.index = new Map(indexData.index.map(([term, docs]) => [term, new Set(docs)]));
    } catch (err) {
      // Index doesn't exist yet
    }
  }
}

module.exports = DocumentIndexer;
```

### Exercise 1.2: Create RAG MCP Service for Copilot

Create `rag-mcp-service.js`:

```javascript
#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import DocumentIndexer from "./document-indexer.js";
import fs from "fs/promises";
import path from "path";

const indexer = new DocumentIndexer('./rag-index');

const server = new Server(
  {
    name: "rag-service",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Define RAG tools for Copilot
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "index_file",
        description: "Index a file for RAG retrieval",
        inputSchema: {
          type: "object",
          properties: {
            filepath: {
              type: "string",
              description: "Path to the file to index",
            },
            tags: {
              type: "array",
              items: { type: "string" },
              description: "Optional tags for categorization",
            },
          },
          required: ["filepath"],
        },
      },
      {
        name: "index_directory",
        description: "Index all files in a directory",
        inputSchema: {
          type: "object",
          properties: {
            directory: {
              type: "string",
              description: "Directory path to index",
            },
            extensions: {
              type: "array",
              items: { type: "string" },
              description: "File extensions to include (e.g., ['.md', '.txt'])",
              default: [".md", ".txt", ".js", ".py"],
            },
          },
          required: ["directory"],
        },
      },
      {
        name: "search_knowledge",
        description: "Search the knowledge base for relevant information",
        inputSchema: {
          type: "object",
          properties: {
            query: {
              type: "string",
              description: "Search query",
            },
            maxResults: {
              type: "number",
              description: "Maximum number of results",
              default: 5,
            },
          },
          required: ["query"],
        },
      },
      {
        name: "ask_with_context",
        description: "Ask a question using RAG context",
        inputSchema: {
          type: "object",
          properties: {
            question: {
              type: "string",
              description: "Question to answer",
            },
            maxContext: {
              type: "number",
              description: "Maximum context documents to use",
              default: 3,
            },
          },
          required: ["question"],
        },
      },
      {
        name: "get_index_stats",
        description: "Get statistics about the indexed knowledge base",
        inputSchema: {
          type: "object",
          properties: {},
        },
      },
    ],
  };
});

// Handle tool execution
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case "index_file": {
      try {
        const content = await fs.readFile(args.filepath, 'utf8');
        const docId = await indexer.indexDocument(
          args.filepath,
          content,
          { tags: args.tags || [] }
        );

        return {
          content: [
            {
              type: "text",
              text: `Successfully indexed ${args.filepath} (ID: ${docId})`,
            },
          ],
        };
      } catch (err) {
        return {
          content: [
            {
              type: "text",
              text: `Error indexing file: ${err.message}`,
            },
          ],
        };
      }
    }

    case "index_directory": {
      try {
        const files = await fs.readdir(args.directory, { withFileTypes: true });
        const extensions = args.extensions || ['.md', '.txt', '.js', '.py'];
        let indexed = 0;

        for (const file of files) {
          if (file.isFile()) {
            const ext = path.extname(file.name);
            if (extensions.includes(ext)) {
              const filepath = path.join(args.directory, file.name);
              const content = await fs.readFile(filepath, 'utf8');
              await indexer.indexDocument(filepath, content);
              indexed++;
            }
          }
        }

        return {
          content: [
            {
              type: "text",
              text: `Indexed ${indexed} files from ${args.directory}`,
            },
          ],
        };
      } catch (err) {
        return {
          content: [
            {
              type: "text",
              text: `Error indexing directory: ${err.message}`,
            },
          ],
        };
      }
    }

    case "search_knowledge": {
      const results = indexer.search(args.query, args.maxResults || 5);

      if (results.length === 0) {
        return {
          content: [
            {
              type: "text",
              text: `No results found for "${args.query}"`,
            },
          ],
        };
      }

      const formatted = results
        .map((r, i) => {
          const preview = r.document.content.slice(0, 200) + '...';
          return `${i + 1}. [${r.document.filepath}] (Score: ${r.score.toFixed(2)})\n   ${preview}`;
        })
        .join('\n\n');

      return {
        content: [
          {
            type: "text",
            text: `Search results for "${args.query}":\n\n${formatted}`,
          },
        ],
      };
    }

    case "ask_with_context": {
      // Search for relevant context
      const results = indexer.search(args.question, args.maxContext || 3);

      if (results.length === 0) {
        return {
          content: [
            {
              type: "text",
              text: "No relevant context found. Please index more documents first.",
            },
          ],
        };
      }

      // Format context for response
      const context = results
        .map(r => `[Source: ${r.document.filepath}]\n${r.document.content}`)
        .join('\n\n---\n\n');

      const response = `Based on the following context, here's the answer to your question:\n\nCONTEXT:\n${context}\n\nQUESTION: ${args.question}\n\nPlease provide an answer based solely on the context above.`;

      return {
        content: [
          {
            type: "text",
            text: response,
          },
        ],
      };
    }

    case "get_index_stats": {
      const stats = {
        totalDocuments: indexer.documents.size,
        uniqueTerms: indexer.index.size,
        indexSize: JSON.stringify(Array.from(indexer.documents.values())).length,
      };

      return {
        content: [
          {
            type: "text",
            text: `Index Statistics:\n- Total document chunks: ${stats.totalDocuments}\n- Unique terms indexed: ${stats.uniqueTerms}\n- Approximate index size: ${(stats.indexSize / 1024).toFixed(2)} KB`,
          },
        ],
      };
    }

    default:
      throw new Error(`Unknown tool: ${name}`);
  }
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("RAG MCP service running on stdio");
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
```

---

## Part 2: Vector-Based RAG System

### Exercise 2.1: Implement Embedding-Based RAG

Create `vector-rag.js`:

```javascript
const fs = require('fs').promises;
const path = require('path');

class VectorRAG {
  constructor(indexPath = './vector-rag-index') {
    this.indexPath = indexPath;
    this.documents = [];
    this.embeddings = [];
    this.init();
  }

  async init() {
    await fs.mkdir(this.indexPath, { recursive: true });
    await this.loadIndex();
  }

  // Simple embedding function (in production, use OpenAI or Sentence Transformers)
  async embed(text) {
    // Character frequency-based embedding (simplified)
    const vector = new Array(768).fill(0); // Simulating 768-dim embedding

    for (let i = 0; i < Math.min(text.length, 768); i++) {
      const charCode = text.charCodeAt(i);
      vector[i % 768] += charCode / 128;
    }

    // Add some text statistics
    vector[0] = text.length / 1000;
    vector[1] = (text.match(/\s/g) || []).length / 100;
    vector[2] = (text.match(/[.!?]/g) || []).length / 10;

    // Normalize
    const magnitude = Math.sqrt(vector.reduce((sum, val) => sum + val * val, 0));
    return vector.map(val => val / magnitude);
  }

  // Calculate cosine similarity
  cosineSimilarity(vec1, vec2) {
    let dotProduct = 0;
    for (let i = 0; i < vec1.length; i++) {
      dotProduct += vec1[i] * vec2[i];
    }
    return dotProduct;
  }

  // Add document with embedding
  async addDocument(content, metadata = {}) {
    const chunks = this.chunkText(content);

    for (const chunk of chunks) {
      const embedding = await this.embed(chunk);

      this.documents.push({
        content: chunk,
        metadata,
        timestamp: new Date().toISOString(),
      });

      this.embeddings.push(embedding);
    }

    await this.saveIndex();
  }

  // Chunk text intelligently
  chunkText(text, maxChunkSize = 512) {
    const sentences = text.match(/[^.!?]+[.!?]+/g) || [text];
    const chunks = [];
    let currentChunk = '';

    for (const sentence of sentences) {
      if ((currentChunk + sentence).length > maxChunkSize && currentChunk) {
        chunks.push(currentChunk.trim());
        currentChunk = sentence;
      } else {
        currentChunk += ' ' + sentence;
      }
    }

    if (currentChunk.trim()) {
      chunks.push(currentChunk.trim());
    }

    return chunks;
  }

  // Semantic search
  async search(query, topK = 5) {
    const queryEmbedding = await this.embed(query);
    const scores = [];

    for (let i = 0; i < this.embeddings.length; i++) {
      const similarity = this.cosineSimilarity(queryEmbedding, this.embeddings[i]);
      scores.push({
        document: this.documents[i],
        score: similarity,
        index: i,
      });
    }

    scores.sort((a, b) => b.score - a.score);
    return scores.slice(0, topK);
  }

  // Hybrid search (combining keyword and semantic)
  async hybridSearch(query, topK = 5) {
    // Semantic search
    const semanticResults = await this.search(query, topK * 2);

    // Keyword search
    const keywords = query.toLowerCase().split(/\s+/);
    const keywordScores = this.documents.map((doc, index) => {
      const content = doc.content.toLowerCase();
      let score = 0;

      for (const keyword of keywords) {
        if (content.includes(keyword)) {
          score += (content.match(new RegExp(keyword, 'g')) || []).length;
        }
      }

      return { document: doc, score, index };
    });

    // Combine scores
    const combined = new Map();

    for (const result of semanticResults) {
      combined.set(result.index, {
        document: result.document,
        semanticScore: result.score,
        keywordScore: 0,
        index: result.index,
      });
    }

    for (const result of keywordScores) {
      if (combined.has(result.index)) {
        combined.get(result.index).keywordScore = result.score;
      } else {
        combined.set(result.index, {
          document: result.document,
          semanticScore: 0,
          keywordScore: result.score,
          index: result.index,
        });
      }
    }

    // Calculate combined score
    const finalResults = Array.from(combined.values()).map(item => ({
      document: item.document,
      score: item.semanticScore * 0.7 + Math.min(item.keywordScore / 10, 1) * 0.3,
      semantic: item.semanticScore,
      keyword: item.keywordScore,
    }));

    finalResults.sort((a, b) => b.score - a.score);
    return finalResults.slice(0, topK);
  }

  // Rerank results using cross-encoder pattern
  async rerank(query, results) {
    // Simulate cross-encoder reranking
    const reranked = results.map(result => {
      const doc = result.document.content.toLowerCase();
      const q = query.toLowerCase();

      // Simple relevance features
      let score = result.score;

      // Exact phrase match
      if (doc.includes(q)) {
        score += 0.5;
      }

      // Query terms coverage
      const queryTerms = q.split(/\s+/);
      const coverage = queryTerms.filter(term => doc.includes(term)).length / queryTerms.length;
      score += coverage * 0.3;

      // Position of first match
      const firstMatch = queryTerms.map(term => doc.indexOf(term)).filter(pos => pos !== -1);
      if (firstMatch.length > 0) {
        const earliness = 1 - (Math.min(...firstMatch) / doc.length);
        score += earliness * 0.2;
      }

      return { ...result, rerankScore: score };
    });

    reranked.sort((a, b) => b.rerankScore - a.rerankScore);
    return reranked;
  }

  // Save and load index
  async saveIndex() {
    const data = {
      documents: this.documents,
      embeddings: this.embeddings,
    };

    await fs.writeFile(
      path.join(this.indexPath, 'vector-index.json'),
      JSON.stringify(data)
    );
  }

  async loadIndex() {
    try {
      const data = await fs.readFile(
        path.join(this.indexPath, 'vector-index.json'),
        'utf8'
      );
      const parsed = JSON.parse(data);
      this.documents = parsed.documents || [];
      this.embeddings = parsed.embeddings || [];
    } catch (err) {
      // Index doesn't exist yet
    }
  }
}

module.exports = VectorRAG;
```

---

## Part 3: Advanced RAG Patterns

### Exercise 3.1: Contextual RAG with Source Tracking

Create `contextual-rag.js`:

```javascript
class ContextualRAG {
  constructor(vectorRAG) {
    this.vectorRAG = vectorRAG;
    this.conversationHistory = [];
  }

  // Build context from multiple sources
  async buildContext(query, maxTokens = 2000) {
    // Search for relevant documents
    const results = await this.vectorRAG.hybridSearch(query, 10);

    // Rerank based on query
    const reranked = await this.vectorRAG.rerank(query, results);

    // Build context with source tracking
    let context = '';
    const sources = [];
    let tokenCount = 0;

    for (const result of reranked) {
      const doc = result.document;
      const docTokens = doc.content.split(/\s+/).length;

      if (tokenCount + docTokens > maxTokens) {
        // Truncate if needed
        const remainingTokens = maxTokens - tokenCount;
        const truncated = doc.content.split(/\s+/).slice(0, remainingTokens).join(' ');
        context += `\n\n[Source ${sources.length + 1}]: ${truncated}...`;
        sources.push({
          content: truncated,
          metadata: doc.metadata,
          truncated: true,
        });
        break;
      }

      context += `\n\n[Source ${sources.length + 1}]: ${doc.content}`;
      sources.push({
        content: doc.content,
        metadata: doc.metadata,
        truncated: false,
      });
      tokenCount += docTokens;
    }

    return { context, sources };
  }

  // Generate response with citations
  async answerWithCitations(question) {
    const { context, sources } = await this.buildContext(question);

    // Add conversation history for continuity
    const history = this.conversationHistory.slice(-3).map(h =>
      `Q: ${h.question}\nA: ${h.answer}`
    ).join('\n\n');

    const prompt = `
${history ? `Previous conversation:\n${history}\n\n` : ''}
Based on the following context, answer the question. Include source citations [1], [2], etc.

Context:
${context}

Question: ${question}

Instructions:
1. Answer based ONLY on the provided context
2. Cite sources using [number] format
3. If the context doesn't contain the answer, say so
4. Be concise and accurate
`;

    // Store in history
    this.conversationHistory.push({
      question,
      context,
      sources,
      timestamp: new Date().toISOString(),
    });

    return {
      prompt,
      sources,
      context,
    };
  }

  // Multi-hop reasoning
  async multiHopReasoning(question, maxHops = 3) {
    const hops = [];
    let currentQuestion = question;

    for (let i = 0; i < maxHops; i++) {
      // Get context for current question
      const { context, sources } = await this.buildContext(currentQuestion);

      hops.push({
        hop: i + 1,
        question: currentQuestion,
        context,
        sources,
      });

      // Generate follow-up question based on context
      const followUp = this.generateFollowUpQuestion(currentQuestion, context);

      if (!followUp) break;

      currentQuestion = followUp;
    }

    return {
      originalQuestion: question,
      hops,
      finalContext: hops.map(h => h.context).join('\n\n'),
    };
  }

  // Generate follow-up questions for deeper understanding
  generateFollowUpQuestion(question, context) {
    // Simple heuristic for follow-up questions
    const mentioned = context.toLowerCase();

    if (mentioned.includes('because') && !question.includes('why')) {
      return `Why ${question.toLowerCase()}?`;
    }

    if (mentioned.includes('several') || mentioned.includes('multiple')) {
      return `What are the specific examples related to ${question}?`;
    }

    if (mentioned.includes('process') || mentioned.includes('steps')) {
      return `What are the detailed steps for ${question}?`;
    }

    return null;
  }
}

module.exports = ContextualRAG;
```

### Exercise 3.2: Document Processing Pipeline

Create `document-processor.js`:

```javascript
class DocumentProcessor {
  constructor() {
    this.processors = new Map();
    this.registerDefaultProcessors();
  }

  registerDefaultProcessors() {
    // Markdown processor
    this.registerProcessor('.md', (content) => {
      // Remove markdown formatting for better indexing
      return content
        .replace(/^#+\s+/gm, '') // Headers
        .replace(/\*\*([^*]+)\*\*/g, '$1') // Bold
        .replace(/\*([^*]+)\*/g, '$1') // Italic
        .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1') // Links
        .replace(/```[^`]*```/gs, '') // Code blocks
        .replace(/`([^`]+)`/g, '$1'); // Inline code
    });

    // Code processor
    this.registerProcessor('.js', (content) => {
      // Extract comments and function names
      const comments = content.match(/\/\*[\s\S]*?\*\/|\/\/.*/g) || [];
      const functions = content.match(/function\s+(\w+)|(\w+)\s*:\s*function|(\w+)\s*=\s*\([^)]*\)\s*=>/g) || [];

      return [
        ...comments.map(c => c.replace(/^\/\*|\*\/$|^\/\//g, '').trim()),
        ...functions.map(f => `Function: ${f}`),
        content, // Include full content too
      ].join('\n\n');
    });

    // JSON processor
    this.registerProcessor('.json', (content) => {
      try {
        const obj = JSON.parse(content);
        return this.flattenObject(obj);
      } catch {
        return content;
      }
    });

    // CSV processor
    this.registerProcessor('.csv', (content) => {
      const lines = content.split('\n');
      const headers = lines[0]?.split(',') || [];

      // Convert to readable format
      const records = lines.slice(1).map(line => {
        const values = line.split(',');
        return headers.map((h, i) => `${h}: ${values[i] || ''}`).join(', ');
      });

      return records.join('\n');
    });
  }

  registerProcessor(extension, processor) {
    this.processors.set(extension, processor);
  }

  process(filepath, content) {
    const ext = path.extname(filepath).toLowerCase();
    const processor = this.processors.get(ext);

    if (processor) {
      return processor(content);
    }

    return content;
  }

  flattenObject(obj, prefix = '') {
    let result = [];

    for (const [key, value] of Object.entries(obj)) {
      const fullKey = prefix ? `${prefix}.${key}` : key;

      if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
        result.push(...this.flattenObject(value, fullKey));
      } else if (Array.isArray(value)) {
        result.push(`${fullKey}: [${value.join(', ')}]`);
      } else {
        result.push(`${fullKey}: ${value}`);
      }
    }

    return result;
  }

  // Extract metadata from documents
  extractMetadata(filepath, content) {
    const metadata = {
      filepath,
      extension: path.extname(filepath),
      size: content.length,
      lines: content.split('\n').length,
      created: new Date().toISOString(),
    };

    // Extract frontmatter from markdown
    if (filepath.endsWith('.md')) {
      const frontmatter = content.match(/^---\n([\s\S]*?)\n---/);
      if (frontmatter) {
        try {
          // Simple YAML parsing
          const lines = frontmatter[1].split('\n');
          for (const line of lines) {
            const [key, value] = line.split(':').map(s => s.trim());
            if (key && value) {
              metadata[key] = value.replace(/^["']|["']$/g, '');
            }
          }
        } catch {}
      }
    }

    // Extract package info from package.json
    if (filepath.endsWith('package.json')) {
      try {
        const pkg = JSON.parse(content);
        metadata.name = pkg.name;
        metadata.version = pkg.version;
        metadata.description = pkg.description;
      } catch {}
    }

    return metadata;
  }
}

module.exports = DocumentProcessor;
```

---

## Part 4: Practical RAG Implementation

### Exercise 4.1: Code Documentation RAG

Create a RAG system for code documentation:

```javascript
class CodeDocRAG {
  constructor(vectorRAG, processor) {
    this.vectorRAG = vectorRAG;
    this.processor = processor;
    this.codePatterns = this.initializePatterns();
  }

  initializePatterns() {
    return {
      functions: /function\s+(\w+)|const\s+(\w+)\s*=\s*(?:async\s*)?\([^)]*\)\s*=>/g,
      classes: /class\s+(\w+)/g,
      imports: /import\s+.*?from\s+['"]([^'"]+)['"]/g,
      exports: /export\s+(?:default\s+)?(?:class|function|const|let|var)\s+(\w+)/g,
    };
  }

  async indexCodebase(directory) {
    const files = await this.walkDirectory(directory);
    const indexed = [];

    for (const file of files) {
      if (this.isCodeFile(file)) {
        const content = await fs.readFile(file, 'utf8');
        const processed = this.processor.process(file, content);
        const metadata = this.extractCodeMetadata(file, content);

        await this.vectorRAG.addDocument(processed, metadata);
        indexed.push(file);
      }
    }

    return indexed;
  }

  extractCodeMetadata(filepath, content) {
    const metadata = {
      filepath,
      type: 'code',
      language: this.detectLanguage(filepath),
    };

    // Extract code elements
    const functions = [...content.matchAll(this.codePatterns.functions)];
    const classes = [...content.matchAll(this.codePatterns.classes)];
    const imports = [...content.matchAll(this.codePatterns.imports)];
    const exports = [...content.matchAll(this.codePatterns.exports)];

    metadata.functions = functions.map(m => m[1] || m[2]).filter(Boolean);
    metadata.classes = classes.map(m => m[1]).filter(Boolean);
    metadata.dependencies = [...new Set(imports.map(m => m[1]))];
    metadata.exports = exports.map(m => m[1]).filter(Boolean);

    return metadata;
  }

  detectLanguage(filepath) {
    const ext = path.extname(filepath);
    const langMap = {
      '.js': 'javascript',
      '.ts': 'typescript',
      '.py': 'python',
      '.java': 'java',
      '.cpp': 'cpp',
      '.go': 'go',
      '.rs': 'rust',
    };
    return langMap[ext] || 'unknown';
  }

  isCodeFile(filepath) {
    const codeExtensions = ['.js', '.ts', '.py', '.java', '.cpp', '.go', '.rs', '.jsx', '.tsx'];
    return codeExtensions.includes(path.extname(filepath));
  }

  async walkDirectory(dir) {
    const files = [];
    const entries = await fs.readdir(dir, { withFileTypes: true });

    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);

      if (entry.isDirectory() && !entry.name.startsWith('.') && entry.name !== 'node_modules') {
        files.push(...await this.walkDirectory(fullPath));
      } else if (entry.isFile()) {
        files.push(fullPath);
      }
    }

    return files;
  }

  // Specialized search for code
  async searchCode(query, type = 'all') {
    let searchQuery = query;

    // Enhance query based on type
    if (type === 'function') {
      searchQuery = `function ${query} implementation code`;
    } else if (type === 'class') {
      searchQuery = `class ${query} definition structure`;
    } else if (type === 'error') {
      searchQuery = `error ${query} solution fix`;
    }

    const results = await this.vectorRAG.hybridSearch(searchQuery, 5);

    // Filter by type if specified
    if (type !== 'all') {
      return results.filter(r => {
        const meta = r.document.metadata;
        if (type === 'function') return meta.functions?.length > 0;
        if (type === 'class') return meta.classes?.length > 0;
        return true;
      });
    }

    return results;
  }

  // Generate documentation from code
  async generateDocs(query) {
    const results = await this.searchCode(query);

    if (results.length === 0) {
      return "No relevant code found.";
    }

    const docs = [];
    for (const result of results.slice(0, 3)) {
      const meta = result.document.metadata;
      docs.push({
        file: meta.filepath,
        language: meta.language,
        functions: meta.functions || [],
        classes: meta.classes || [],
        snippet: result.document.content.slice(0, 500),
      });
    }

    return docs;
  }
}
```

---

## Part 5: Configure for GitHub Copilot

### Exercise 5.1: VS Code Configuration

Add to your VS Code settings (`~/.config/mcp/settings.json` or `.vscode/settings.json`):

```json
{
  "github.copilot.chat.mcp.servers": {
    "rag-service": {
      "command": "node",
      "args": ["/full/path/to/rag-mcp-service.js"]
    }
  }
}
```

### Exercise 5.2: Test with Copilot

After configuring, test these scenarios:

1. **Index your project:**

```txt
"Use the RAG service to index all files in the current directory"
```

1. **Search for information:**

```txt
"Search the knowledge base for information about authentication"
```

1. **Ask questions with context:**

```txt
"Using the indexed documentation, explain how the user service works"
```

1. **Get code examples:**

```txt
"Find examples of error handling in the codebase"
```

---

## Part 6: Production RAG Optimizations

### Exercise 6.1: Query Expansion

```javascript
class QueryExpander {
  expand(query) {
    const expansions = [];

    // Synonym expansion
    const synonyms = {
      'bug': ['error', 'issue', 'problem', 'defect'],
      'function': ['method', 'procedure', 'routine'],
      'create': ['make', 'build', 'construct', 'generate'],
      'delete': ['remove', 'destroy', 'erase'],
    };

    let expanded = query;
    for (const [word, syns] of Object.entries(synonyms)) {
      if (query.toLowerCase().includes(word)) {
        expansions.push(...syns.map(syn => query.replace(new RegExp(word, 'gi'), syn)));
      }
    }

    // Acronym expansion
    const acronyms = {
      'API': 'Application Programming Interface',
      'REST': 'Representational State Transfer',
      'DB': 'Database',
      'UI': 'User Interface',
    };

    for (const [acronym, full] of Object.entries(acronyms)) {
      if (query.includes(acronym)) {
        expansions.push(query.replace(acronym, full));
      }
    }

    return [query, ...expansions];
  }
}
```

### Exercise 6.2: Result Caching

```javascript
class RAGCache {
  constructor(maxSize = 100, ttl = 3600000) {
    this.cache = new Map();
    this.maxSize = maxSize;
    this.ttl = ttl; // 1 hour default
  }

  getCacheKey(query, params = {}) {
    return JSON.stringify({ query, ...params });
  }

  get(query, params) {
    const key = this.getCacheKey(query, params);
    const cached = this.cache.get(key);

    if (cached) {
      if (Date.now() - cached.timestamp < this.ttl) {
        cached.hits++;
        return cached.data;
      }
      this.cache.delete(key);
    }

    return null;
  }

  set(query, params, data) {
    const key = this.getCacheKey(query, params);

    // LRU eviction
    if (this.cache.size >= this.maxSize) {
      const lru = Array.from(this.cache.entries())
        .sort((a, b) => a[1].hits - b[1].hits)[0];
      this.cache.delete(lru[0]);
    }

    this.cache.set(key, {
      data,
      timestamp: Date.now(),
      hits: 0,
    });
  }

  clear() {
    this.cache.clear();
  }

  stats() {
    const entries = Array.from(this.cache.values());
    return {
      size: this.cache.size,
      totalHits: entries.reduce((sum, e) => sum + e.hits, 0),
      avgAge: entries.reduce((sum, e) => sum + (Date.now() - e.timestamp), 0) / entries.length,
    };
  }
}
```

---

## Part 7: Testing Your RAG System

Create `test-rag.js`:

```javascript
const VectorRAG = require('./vector-rag');
const DocumentProcessor = require('./document-processor');
const ContextualRAG = require('./contextual-rag');

async function testRAGSystem() {
  console.log('Testing RAG System...\n');

  // Initialize components
  const vectorRAG = new VectorRAG();
  const processor = new DocumentProcessor();
  const contextualRAG = new ContextualRAG(vectorRAG);

  // Test 1: Index sample documents
  console.log('1. Indexing sample documents...');

  await vectorRAG.addDocument(
    "RAG systems combine retrieval and generation for better AI responses.",
    { source: 'intro.md', type: 'documentation' }
  );

  await vectorRAG.addDocument(
    "Vector databases store embeddings for semantic search capabilities.",
    { source: 'vectors.md', type: 'technical' }
  );

  await vectorRAG.addDocument(
    "GitHub Copilot can use MCP services to access external knowledge bases.",
    { source: 'copilot.md', type: 'integration' }
  );

  // Test 2: Basic search
  console.log('\n2. Testing search...');
  const results = await vectorRAG.search('semantic search', 2);
  console.log(`Found ${results.length} results:`);
  results.forEach(r => {
    console.log(`  - Score: ${r.score.toFixed(3)} | ${r.document.content.slice(0, 50)}...`);
  });

  // Test 3: Hybrid search
  console.log('\n3. Testing hybrid search...');
  const hybrid = await vectorRAG.hybridSearch('RAG generation', 2);
  console.log(`Found ${hybrid.length} results with hybrid scoring`);

  // Test 4: Contextual answering
  console.log('\n4. Testing contextual answering...');
  const answer = await contextualRAG.answerWithCitations('How does RAG work?');
  console.log('Generated prompt with context and sources');
  console.log(`Sources: ${answer.sources.length} documents`);

  // Test 5: Multi-hop reasoning
  console.log('\n5. Testing multi-hop reasoning...');
  const multiHop = await contextualRAG.multiHopReasoning('What is semantic search used for?', 2);
  console.log(`Performed ${multiHop.hops.length} reasoning hops`);

  console.log('\nAll RAG tests completed!');
}

testRAGSystem().catch(console.error);
```

---

## Part 8: Real-World RAG Applications

### Application 1: Documentation QA System

```javascript
// Use with Copilot for answering documentation questions
const docQA = {
  async setup() {
    // Index all documentation
    await indexer.indexDirectory('./docs', ['.md', '.txt']);
    await indexer.indexDirectory('./README.md');
  },

  async answer(question) {
    const context = await rag.buildContext(question);
    return `Based on documentation:\n${context}`;
  }
};
```

### Application 2: Code Understanding Assistant

```javascript
// Help understand large codebases
const codeAssistant = {
  async explainFunction(functionName) {
    const results = await rag.searchCode(functionName, 'function');
    return this.explainCode(results);
  },

  async findUsages(identifier) {
    const results = await rag.search(`usage ${identifier} called`);
    return this.formatUsages(results);
  }
};
```

### Application 3: Error Resolution System

```javascript
// Find solutions to errors
const errorResolver = {
  async findSolution(errorMessage) {
    // Search internal docs
    const internal = await rag.search(errorMessage);

    // Search past fixes
    const history = await rag.search(`fixed error ${errorMessage}`);

    return this.combineSolutions(internal, history);
  }
};
```

---

## Success Criteria

After completing this exercise, you should be able to:

- [ ] Build a document indexing system
- [ ] Implement text chunking strategies
- [ ] Create vector-based semantic search
- [ ] Build hybrid search combining keywords and semantics
- [ ] Implement RAG with source tracking
- [ ] Configure MCP services for GitHub Copilot
- [ ] Process different document types
- [ ] Implement query expansion and reranking
- [ ] Build contextual question answering
- [ ] Cache and optimize RAG queries

## Best Practices

1. **Chunking Strategy**: Balance chunk size with context preservation
1. **Embedding Quality**: Use appropriate embedding models for your domain
1. **Hybrid Search**: Combine multiple retrieval methods
1. **Source Attribution**: Always track and cite sources
1. **Context Limits**: Respect token limits when building context
1. **Caching**: Cache embeddings and frequent queries
1. **Incremental Indexing**: Update index incrementally, not from scratch
1. **Metadata**: Store rich metadata for filtering
1. **Evaluation**: Regularly evaluate retrieval quality
1. **User Feedback**: Incorporate feedback to improve ranking

## Next Steps

- Integrate with production vector databases (Pinecone, Weaviate, Qdrant)
- Implement real embedding models (OpenAI, Cohere, Sentence Transformers)
- Add streaming responses for large contexts
- Build evaluation metrics for RAG quality
- Implement fine-tuning based on user feedback
- Create specialized RAG for different domains

Remember: RAG systems bridge the gap between static AI knowledge and dynamic, domain-specific information!</content>

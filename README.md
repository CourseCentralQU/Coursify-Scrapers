### ✅ **Feature Implementation Order (Suggested Flow)**

1. **UI Updates (Quick Wins)**

   - Hero section headline + subheading
   - Replace hero visual with a [Cursorful demo](https://www.cursor.sh)
   - Footer + remove Schools page
   - Add yourself to Team page

2. **Student Reviews Module**

   - Structure your review system like [UWFlow](https://uwflow.com/course/cs115)
     - Fields: course rating, difficulty, workload, recommended prof, comments
     - Optional: thumbs up/down for helpful reviews
   - Store in your backend (MongoDB, Supabase, etc.)

3. **Web Scraping for Reddit Reviews**

   - Use [PRAW](https://praw.readthedocs.io/) (Python Reddit API Wrapper)
     - Filter subreddits like r/queensuniversity with keywords like "course", "PSYC100", "BIOL102"
     - Clean and tag content by course code
   - Optional: Display most recent Reddit mentions for a course

4. **RAG-Based Course Chatbot**
   - Scrape + store text content from course calendars/syllabi
   - Convert to chunks and embed using OpenAI embeddings or SentenceTransformers
   - Store embeddings in FAISS or Pinecone
   - Build a simple frontend chatbot with puter.js (or LangChain JS if you want a JS-first stack)
   - On query: use semantic search → context → LLM prompt → return answer with context

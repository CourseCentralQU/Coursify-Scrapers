### ✅ **Feature Implementation Order (Suggested Flow)**

1. **UI Updates (Quick Wins)**

   - Hero section headline + subheading
   - Replace hero visual with a [Cursorful demo](https://www.cursor.sh)
   - Footer + remove Schools page
   - Add yourself to Team page
   - A feature that says "is this not up to date, update this". This will fetch the up to date course info and update it in the database.

2. **Web Scraping for Reddit Reviews**

   - Use [PRAW](https://praw.readthedocs.io/) (Python Reddit API Wrapper)
     - Filter subreddits like r/queensuniversity with keywords like "course", "PSYC100", "BIOL102"
     - Clean and tag content by course code
   - Optional: Display most recent Reddit mentions for a course

3. **RAG-Based Course Chatbot**
   - Scrape + store text content from course calendars/syllabi
   - Convert to chunks and embed using OpenAI embeddings or SentenceTransformers
   - Store embeddings in FAISS or Pinecone
   - Build a simple frontend chatbot with puter.js (or LangChain JS if you want a JS-first stack)
   - On query: use semantic search → context → LLM prompt → return answer with context

You're absolutely right to clarify this upfront — 🔑 **the quality of a RAG system depends entirely on the quality and relevance of the data it retrieves**. So designing your scraper around the kinds of questions students will **actually ask** is a strategic move.

Let’s map this out clearly:

---

## 🎯 Purpose of the Scraper (Restated)

> ✅ To collect high-signal Reddit comments (and later user-submitted reviews) **per course** that can be embedded and used by a RAG system to answer common student questions.

---

## 🤖 What Can RAG Actually Answer Well?

A RAG system is best at:

- **Context-based opinion summarization**
- **Extracting insights from scattered sources**
- **Providing “vibe checks” or soft info**

It struggles with:

- Hard facts not present in the data (e.g., "When is the PSYC100 exam?")
- Logic/multistep reasoning unless the LLM is very strong

---

## 💬 Categories of High-Value Student Questions for RAG

Here’s a structured set of **question types** that your scraper should support by finding Reddit comments about them.

---

### 📘 **Course Difficulty + Workload**

- “Is PSYC100 a bird course?”
- “How hard is BIOL102?”
- “Is CISC124 very math-heavy?”
- “What’s the weekly workload like?”

**→ Your scraper should target**: “easy”, “hard”, “bird course”, “time-consuming”, “light workload”

---

### 🧑‍🏫 **Professor Experience**

- “Is Dr. Smith a good prof for PSYC100?”
- “Should I take CISC124 with Dr. Jones or Dr. Patel?”
- “Is the TA support any good?”

**→ Target keywords**: professor names, “boring”, “amazing prof”, “TA support”, “clear lectures”

---

### 📝 **Exam and Assignment Structure**

- “How are the tests in COGS100?”
- “Are the exams MCQ or short answer?”
- “Is there a final or just assignments?”

**→ Target keywords**: “exam”, “midterm”, “final”, “assignment heavy”, “weekly quizzes”

---

### 🧠 **Comparisons Between Courses**

- “Is PSYC100 easier than SOCY122?”
- “Which elective is better for a GPA boost?”

**→ Target keywords**: course codes mentioned together, “better than”, “easier than”, “compare”

---

### 🧪 **Advice From Past Students**

- “Any tips for surviving BIOL103?”
- “Is it worth taking this course for a minor?”

**→ Target keywords**: “tip”, “advice”, “recommend”, “worth it”

---

### ✅ RAG-friendly Question Examples:

| Question                               | Can RAG Answer It? | Why                                       |
| -------------------------------------- | ------------------ | ----------------------------------------- |
| “Is PSYC100 a bird course?”            | ✅                 | It can retrieve opinions about difficulty |
| “How’s Dr. Smith for CISC124?”         | ✅                 | It can surface subjective prof reviews    |
| “What’s the workload like in BIOL102?” | ✅                 | Many Reddit posts mention this            |
| “When are lectures scheduled?”         | ❌                 | Not in Reddit, structured data needed     |
| “Is there a midterm?”                  | ✅ if mentioned    | Depends on comment coverage               |
| “How does this compare to SOCY122?”    | ✅                 | If both courses are mentioned together    |
| “What textbook is used?”               | ❌ (usually)       | Needs scraping of syllabi or calendars    |

---

## 📈 Goal for Scraper:

Your scraper should aim to collect **comments** that are:

- Linked to **course codes**
- (Optionally) contain **professor names**
- Mention things like:
  - “easy”, “hard”, “bird course”
  - “professor was good/bad”
  - “midterm/final”
  - “lots of readings/homework”
  - “group project”
  - “better than [other course]”
  - “tips for success”

---

## 🧠 Suggested Tag Categories (You Can Preprocess These Later)

| Tag                | Detected By                                     |
| ------------------ | ----------------------------------------------- |
| `easy`             | "easy", "light", "bird course"                  |
| `hard`             | "hard", "tough", "difficult"                    |
| `professor_review` | Prof names, “professor”, “lecturer”, “teaching” |
| `exam_info`        | “exam”, “midterm”, “final”                      |
| `workload`         | “homework”, “assignments”, “reading”            |
| `tips`             | “recommend”, “tip”, “advice”                    |
| `comparison`       | Mentions 2+ course codes in one comment         |

You’ll later embed only the `text`, but keep these `tags` in metadata for filtering or highlighting.

---

## ✅ TL;DR

### 🎯 Your scraper’s mission:

> Get comments that answer common **course selection questions** — especially subjective ones Reddit is best at.

### 🤖 Your RAG will be great at:

- "Is this course hard?"
- "Which prof is better?"
- "What’s the exam format?"
- "Tips from students?"

And for that, you need comments that mention:

- Course codes
- Difficulty
- Professors
- Exam/assignment info
- Comparisons

---

Would you like:

- A checklist for designing the scraper filter logic around these categories?
- A JSON structure for storing these questions/tags?
- Pre-built tag-detection logic to run after scraping?

You're setting this up with perfect foresight 🔥

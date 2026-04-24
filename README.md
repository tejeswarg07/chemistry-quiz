# 🧪 Chemistry Quiz — NEET / JEE / CBSE

A Python-based command-line quiz application for Chemistry exam preparation.  
Built by **Tejeswara Rao Guttavalli** — M.Sc. Organic Chemistry | STEM Subject Matter Expert | AI Data Operations

---

## 🚀 Features

- 12 curated Chemistry MCQs across Organic, Inorganic, and Physical Chemistry
- Covers NEET, JEE Foundation, and CBSE syllabus
- Filter questions by **topic**, **difficulty**, or **subject**
- Detailed **explanation** shown after every answer
- **Performance report** with topic-wise score breakdown
- Auto-saves quiz result to a `.txt` log file
- Supports random question sampling

---

## 📦 Installation

```bash
# No external libraries needed — uses Python standard library only
git clone https://github.com/tejeswarg07/chemistry-quiz.git
cd chemistry-quiz
python quiz.py
```

---

## 💻 Usage

```bash
# Full quiz (all questions, shuffled)
python quiz.py

# Only Organic Chemistry questions
python quiz.py --subject "Organic Chemistry"

# Only Hard questions
python quiz.py --difficulty Hard

# Filter by topic keyword
python quiz.py --topic Stereochemistry

# Pick 5 random questions
python quiz.py --random 5

# Combine filters
python quiz.py --subject "Physical Chemistry" --difficulty Medium
```

---

## 📊 Sample Output

```
  Question 3/12  [Organic Chemistry]  [Hard]
  Topic: Stereochemistry
  ─────────────────────────────────────────
  How many stereoisomers are possible for 2,3-dichlorobutane?

    A)  2
    B)  3
    C)  4
    D)  5

  Your answer: B

  ✅ CORRECT!  Answer: B
  📖 Explanation:
  2,3-dichlorobutane has 2 chiral centres but one combination gives a
  meso compound, so total stereoisomers = 3 (2 enantiomers + 1 meso).
```

---

## 📁 Project Structure

```
chemistry-quiz/
├── quiz.py           # Main application
├── questions.json    # Question bank (easily extendable)
└── README.md         # Documentation
```

---

## ➕ Adding More Questions

Simply add entries to `questions.json` following this format:

```json
{
  "id": 13,
  "subject": "Organic Chemistry",
  "topic": "Reaction Mechanisms",
  "difficulty": "Medium",
  "question": "Your question here?",
  "options": {
    "A": "Option A",
    "B": "Option B",
    "C": "Option C",
    "D": "Option D"
  },
  "answer": "B",
  "explanation": "Reason why B is correct..."
}
```

---

## 🛠 Tech Stack

- **Language**: Python 3.x
- **Libraries**: `json`, `random`, `argparse`, `time`, `os`, `datetime` (all standard library)
- **Data Format**: JSON question bank

---

## 👤 Author

**Tejeswara Rao Guttavalli**  
M.Sc. Organic Chemistry | Senior Associate – AI Data Operations (Innodata)  
📧 tejeswarg07@gmail.com  
📍 Andhra Pradesh, India

---

## 📄 License

MIT License — free to use and extend for educational purposes.

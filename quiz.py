"""
Chemistry Quiz Application
Author: Tejeswara Rao Guttavalli
GitHub: github.com/tejeswarg07/chemistry-quiz

A command-line quiz tool for NEET/JEE/CBSE Chemistry preparation.
Loads questions from a JSON file, tracks scores, shows explanations,
and generates a performance report by topic.

Usage:
    python quiz.py                  # Full quiz (all questions)
    python quiz.py --topic organic  # Filter by topic keyword
    python quiz.py --difficulty easy
    python quiz.py --subject "Physical Chemistry"
    python quiz.py --random 5       # Pick 5 random questions
"""

import json
import random
import argparse
import time
import os
from datetime import datetime


# ─── Load Questions ───────────────────────────────────────────
def load_questions(filepath="questions.json"):
    """Load question bank from JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


# ─── Filter Questions ─────────────────────────────────────────
def filter_questions(questions, topic=None, difficulty=None, subject=None):
    """Filter questions by topic, difficulty, or subject."""
    filtered = questions
    if topic:
        filtered = [q for q in filtered if topic.lower() in q["topic"].lower()]
    if difficulty:
        filtered = [q for q in filtered if q["difficulty"].lower() == difficulty.lower()]
    if subject:
        filtered = [q for q in filtered if subject.lower() in q["subject"].lower()]
    return filtered


# ─── Display Helpers ──────────────────────────────────────────
def clear():
    os.system("cls" if os.name == "nt" else "clear")


def print_separator(char="═", width=65):
    print(char * width)


def print_header():
    clear()
    print_separator("═")
    print("  🧪  CHEMISTRY QUIZ  |  NEET / JEE / CBSE")
    print("  By: Tejeswara Rao Guttavalli  |  M.Sc. Organic Chemistry")
    print_separator("═")
    print()


def print_question(q, number, total):
    """Display a single question with options."""
    print(f"\n  Question {number}/{total}  [{q['subject']}]  [{q['difficulty']}]")
    print(f"  Topic: {q['topic']}")
    print_separator("─", 65)
    print(f"\n  {q['question']}\n")
    for key, val in q["options"].items():
        print(f"    {key})  {val}")
    print()


# ─── Quiz Engine ──────────────────────────────────────────────
def run_quiz(questions):
    """
    Core quiz loop.
    Returns a results dict with score, time taken, and per-question breakdown.
    """
    results = {
        "total": len(questions),
        "correct": 0,
        "wrong": 0,
        "skipped": 0,
        "score_percent": 0,
        "time_seconds": 0,
        "breakdown": []
    }

    start_time = time.time()

    for i, q in enumerate(questions, start=1):
        print_header()
        print_question(q, i, len(questions))

        # Get user input
        while True:
            raw = input("  Your answer (A/B/C/D) or S to skip: ").strip().upper()
            if raw in ["A", "B", "C", "D", "S"]:
                break
            print("  ⚠  Please enter A, B, C, D or S.")

        correct = q["answer"]
        is_correct = (raw == correct)
        skipped = (raw == "S")

        # Update counters
        if skipped:
            results["skipped"] += 1
            status = "SKIPPED"
        elif is_correct:
            results["correct"] += 1
            status = "CORRECT ✓"
        else:
            results["wrong"] += 1
            status = "WRONG ✗"

        # Show feedback
        print()
        print_separator("─", 65)
        if skipped:
            print(f"  ⏭  Skipped.  Correct answer: {correct}")
        elif is_correct:
            print(f"  ✅  CORRECT!  Answer: {correct}")
        else:
            print(f"  ❌  WRONG.   Your answer: {raw}  |  Correct: {correct}")

        print(f"\n  📖  Explanation:\n  {q['explanation']}")
        print_separator("─", 65)

        results["breakdown"].append({
            "id": q["id"],
            "topic": q["topic"],
            "subject": q["subject"],
            "difficulty": q["difficulty"],
            "your_answer": raw,
            "correct_answer": correct,
            "status": status
        })

        input("\n  Press Enter for next question...")

    results["time_seconds"] = round(time.time() - start_time)
    total_answered = results["correct"] + results["wrong"]
    results["score_percent"] = (
        round((results["correct"] / total_answered) * 100, 1)
        if total_answered > 0 else 0
    )
    return results


# ─── Performance Report ───────────────────────────────────────
def print_report(results):
    """Print a detailed performance report grouped by topic."""
    clear()
    print_header()
    print("  📊  PERFORMANCE REPORT")
    print_separator("═")

    mins, secs = divmod(results["time_seconds"], 60)
    print(f"\n  Total Questions : {results['total']}")
    print(f"  Correct         : {results['correct']}  ✅")
    print(f"  Wrong           : {results['wrong']}   ❌")
    print(f"  Skipped         : {results['skipped']}  ⏭")
    print(f"  Score           : {results['score_percent']}%")
    print(f"  Time Taken      : {mins}m {secs}s")

    # Grade
    score = results["score_percent"]
    if score >= 90:
        grade = "🏆 EXCELLENT — NEET/JEE Ready!"
    elif score >= 75:
        grade = "👍 GOOD — Keep practising!"
    elif score >= 50:
        grade = "📚 AVERAGE — Review weak topics"
    else:
        grade = "⚠  NEEDS WORK — Revise fundamentals"

    print(f"\n  Grade : {grade}")
    print_separator("─", 65)

    # Per-topic breakdown
    topic_stats = {}
    for item in results["breakdown"]:
        t = item["topic"]
        if t not in topic_stats:
            topic_stats[t] = {"correct": 0, "total": 0, "subject": item["subject"]}
        topic_stats[t]["total"] += 1
        if item["status"].startswith("CORRECT"):
            topic_stats[t]["correct"] += 1

    print("\n  TOPIC-WISE BREAKDOWN:\n")
    print(f"  {'Topic':<30} {'Subject':<22} {'Score'}")
    print(f"  {'─'*30} {'─'*22} {'─'*10}")
    for topic, stat in topic_stats.items():
        pct = round((stat["correct"] / stat["total"]) * 100)
        bar = "█" * (pct // 10) + "░" * (10 - pct // 10)
        print(f"  {topic:<30} {stat['subject']:<22} {pct}%  {bar}")

    print_separator("═")

    # Save report to file
    save_report(results)


def save_report(results):
    """Save quiz results to a text log file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"quiz_report_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("CHEMISTRY QUIZ — PERFORMANCE REPORT\n")
        f.write(f"Date     : {datetime.now().strftime('%d %b %Y, %H:%M')}\n")
        f.write(f"Score    : {results['score_percent']}%\n")
        f.write(f"Correct  : {results['correct']} / {results['total']}\n\n")
        f.write("QUESTION-WISE RESULTS:\n")
        f.write(f"{'Q#':<5} {'Topic':<30} {'Difficulty':<10} {'Result'}\n")
        f.write("-" * 65 + "\n")
        for item in results["breakdown"]:
            f.write(
                f"  {item['id']:<4} {item['topic']:<30} "
                f"{item['difficulty']:<10} {item['status']}\n"
            )
    print(f"\n  💾  Report saved to: {filename}")


# ─── Main Entry Point ─────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Chemistry Quiz — NEET / JEE / CBSE"
    )
    parser.add_argument("--topic", type=str, help="Filter by topic keyword")
    parser.add_argument("--difficulty", type=str,
                        choices=["Easy", "Medium", "Hard"],
                        help="Filter by difficulty")
    parser.add_argument("--subject", type=str,
                        help="Filter by subject (e.g. 'Organic Chemistry')")
    parser.add_argument("--random", type=int, metavar="N",
                        help="Pick N random questions")
    parser.add_argument("--file", type=str, default="questions.json",
                        help="Path to questions JSON file")
    args = parser.parse_args()

    # Load and filter
    all_questions = load_questions(args.file)
    questions = filter_questions(
        all_questions,
        topic=args.topic,
        difficulty=args.difficulty,
        subject=args.subject
    )

    if not questions:
        print("⚠  No questions found for those filters. Try different options.")
        return

    if args.random:
        n = min(args.random, len(questions))
        questions = random.sample(questions, n)
    else:
        random.shuffle(questions)

    # Welcome screen
    print_header()
    print(f"  Loaded : {len(questions)} questions")
    if args.topic:
        print(f"  Topic  : {args.topic}")
    if args.difficulty:
        print(f"  Level  : {args.difficulty}")
    if args.subject:
        print(f"  Subject: {args.subject}")
    print()
    input("  Press Enter to start the quiz...")

    # Run quiz and show report
    results = run_quiz(questions)
    print_report(results)
    print()


if __name__ == "__main__":
    main()

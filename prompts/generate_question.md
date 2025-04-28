Generate a quick assessment question that tests the following skills together:
Skills: {skill_names}
Skill Descriptions:
{skill_descriptions}

Requirements:
1. Question should take less than 1 minute to answer
2. Question must test understanding of ALL listed skills
3. Question must be one of these formats:
   - Numerical answer (e.g., "What is 2+2?")
   - Multiple choice (labeled A, B, C, D, etc.)

Format your response as a JSON object:

```json
{{
    "question": "your question text here",
    "type": "numerical | choice",
    "answer": "exact number or letter",
    "options": ["option1", "option2", "option3", "option4"]
}}
```

Example numerical:

```json
{{
    "question": "If a function f(x) = 2x + 3, what is f(2)?",
    "type": "numerical",
    "answer": "7"
}}
```

Example multiple choice:

```json
{{
    "question": "Which data structure provides O(1) access to elements by index?",
    "type": "multiple_choice",
    "answer": "A",
    "options": [
        "Array",
        "Linked List",
        "Binary Tree",
        "Hash Table"
    ]
}}
```


Given the skill '{name}' with description '{description}', list the direct prerequisites needed to learn this skill.

For each prerequisite, provide:
    1. A name (short and clear)
    2. A description (1-2 sentences)

Format your response as a list of JSON objects:

```json
[
[
  {{
    "name_1": "prerequisite 1 name",
    "description_1": "prerequisite 1 description"
  }},
  ...
  {{
    "name_n": "prerequisite n name",
    "description_n": "prerequisite n description"
  }}
]
]
```

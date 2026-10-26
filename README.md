# Softnear social assets

Public images used by PostDesk posts (Instagram and Facebook fetch them from here when publishing).

- `YYYY-MM/week-MM-DD/` – one folder per week: `plan.md`, `copy/`, `week.json`, rendered media per post, `manifest.json`
- `_system/` – brand and voice (`brand.md`), the weekly procedure (`PLAYBOOK.md`), the renderer (`render.py`) and the history (`log.md`)

A weekly scheduled task plans next week's Instagram, Facebook and LinkedIn posts with
[instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill) and
[linkedin-skills](https://github.com/sergebulaev/linkedin-skills), renders the media, pushes it here,
and drafts every post into PostDesk for review. Nothing is published without approval.

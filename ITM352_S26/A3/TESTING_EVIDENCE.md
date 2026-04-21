# Testing Evidence Documentation

## Purpose
This quiz app now records **runtime testing evidence** whenever users interact with it.

## Evidence File
- File name: `testing_evidence.jsonl`
- Location: same folder as `quiz_webapp.py`
- Format: one JSON object per line (JSONL)

## What gets logged
The app logs events such as:
- Home page viewed
- User registration
- Quiz restart/start
- Question answered (including correctness)
- Hint usage
- Quiz completion (final score)
- Logout

Each event stores:
- timestamp
- event name
- path and HTTP method
- user id and user name (if available)
- client IP
- details object

## In-app evidence page
Use this route in the browser:
- `/testing_evidence`

This page shows:
1. Event count summary by event type
2. Recent log table for quick review and grading evidence

## Suggested testing workflow
1. Start app and use normal quiz flow.
2. Complete at least one full quiz.
3. Use hint in one question.
4. View `/testing_evidence`.
5. Confirm records exist for all expected steps.

## Notes
- Evidence grows over time as the app is used.
- Logs are append-only unless the file is manually deleted.

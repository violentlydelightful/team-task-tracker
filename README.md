# Team Task Tracker

An internal dashboard for managing team workload and tracking project tasks. Built for team leads and project managers who need visibility into what everyone is working on.

## The Problem

Managing a team's workload is challenging when tasks are scattered across emails, spreadsheets, and chat. Managers need to:
- See at a glance who's overloaded and who has capacity
- Track task progress across multiple projects
- Identify bottlenecks and overdue items
- Balance workload across the team

## The Solution

A clean, focused task tracker that shows:
- **Team workload at a glance** - Visual workload indicators per team member
- **Kanban board** - Drag-and-drop task management
- **Dashboard metrics** - Key stats on task status and priorities
- **Team view** - Per-member task assignments and capacity

## Features

### Dashboard
- Stats cards: total, in progress, review, complete, overdue, high priority
- Team workload visualization
- Recent task activity feed

### Kanban Board
- Four columns: To Do, In Progress, Review, Done
- Drag-and-drop task movement
- Priority and due date indicators
- Assignee avatars

### Team Management
- Add team members with roles
- Per-member task list and workload score
- Capacity planning support

### Task Management
- Create, edit, delete tasks
- Assign to team members
- Set priority (high/medium/low)
- Due dates with overdue highlighting
- Project categorization

## Tech Stack

- **Backend**: Python, Flask, SQLAlchemy
- **Database**: SQLite
- **Frontend**: Vanilla JavaScript, CSS Grid/Flexbox
- **No external JS libraries** - lightweight and fast

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

# Open in browser
open http://localhost:5002

# Load demo data
# Click "Load Demo Data" in the sidebar
```

## Project Structure

```
team-task-tracker/
├── app.py              # Main application (routes + models)
├── templates/
│   ├── base.html       # Layout template
│   ├── dashboard.html  # Dashboard view
│   ├── board.html      # Kanban board view
│   └── team.html       # Team management view
├── static/
│   ├── style.css       # All styles
│   └── app.js          # Client-side interactions
├── requirements.txt    # Dependencies
└── README.md
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Dashboard view |
| `/board` | GET | Kanban board view |
| `/team` | GET | Team management view |
| `/api/task` | POST | Create new task |
| `/api/task/<id>` | PUT | Update task |
| `/api/task/<id>` | DELETE | Delete task |
| `/api/member` | POST | Add team member |
| `/api/stats` | GET | Get dashboard statistics |
| `/seed` | GET | Load demo data |

## Workload Scoring

The workload score helps identify over-assigned team members:
- High priority task: +3 points
- Medium priority task: +2 points
- Low priority task: +1 point

The visual bar fills based on score, making it easy to spot imbalances.

## Future Enhancements

- Task comments and activity log
- Time tracking
- Sprint/milestone support
- Email notifications
- Export to CSV
- User authentication

---

*Built as a portfolio project demonstrating practical internal tool development.*

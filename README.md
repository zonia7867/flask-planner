# Planora – Personal Web Planner

Planora is a **web-based planner app** built with **Flask + MongoDB**, designed to help organize tasks, reminders, notes, and schedules.  
It includes **To-Do lists, a Kanban board, a calendar view, space-based notes, and an inbox for reminders**.

---

## 🚀 Features
- 📝 **To-Do List** – Add, edit, mark done, and delete tasks.
- 📌 **Kanban Board** – Organize tasks into "To Do", "In Progress", and "Done".
- 📅 **Calendar View** – See tasks with due dates in a monthly calendar.
- 📂 **Spaces** – Create multiple spaces with notes inside each.
- 🔔 **Inbox** – Manage reminders with due dates.
- 🎨 **Modern UI** – Sidebar navigation, beige theme for content, dark blue sidebar.

---

## 📁 Folder Structure
Planner/
│
├── app/
│ ├── init.py # Flask app factory
│ ├── routes.py # All routes and backend logic
│ ├── templates/ # HTML templates (Jinja2)
│ │ ├── base.html
│ │ ├── home.html
│ │ ├── list.html
│ │ ├── board.html
│ │ ├── calendar.html
│ │ ├── inbox.html
│ │ ├── space.html
│ │ └── edit_task.html
│ └── static/ # CSS, images, JS files
│
├── requirements.txt # Python dependencies
├── run.py # Entry point

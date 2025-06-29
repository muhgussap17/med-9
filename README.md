# med-9

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Electronic Medical Record using Django

Live Demo: [https://muhgussap.pythonanywhere.com](https://muhgussap.pythonanywhere.com)

---

## Table of Contents

- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [License](#license)
- [Author](#author)

---

## About

**med-9** is an Electronic Medical Record (EMR) management system built with Django. It provides a robust platform for managing patient records, integrating with APIs such as WHO ICD, and offers a modern Argon Dashboard-based interface for users.

---

## Features

- User authentication and registration (Django)
- Patient record management
- Integration with WHO ICD API for medical coding
- Dashboard UI based on Argon Dashboard PRO (Bootstrap 4)
- Responsive design with HTML, CSS, and custom SCSS
- Google OAuth2 authentication support
- Interactive charts and Google Maps integration
- Notification and calendar features

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/muhgussap17/med-9.git
   cd med-9
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables as needed.

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Run the server:
   ```bash
   python manage.py runserver
   ```

6. Visit `http://localhost:8000` or the hosted link above.

---

## Usage

- Register or login as a user.
- Add, view, or edit patient records.
- Use dashboard features to view statistics, maps, and charts.
- Search for ICD codes using the integrated WHO API.

---

## Technologies Used

- Django (Python)
- Bootstrap 4 (Argon Dashboard PRO)
- HTML5, CSS3, SCSS, JavaScript
- PostgreSQL
- Google OAuth2
- WHO ICD API

---

## Folder Structure

```
med-9/
├── core/               # Main Django app with models, views, templates, etc.
├── myproject/          # Django project settings and configuration
├── static/             # Static files (CSS, JS, images, SCSS)
├── .gitignore          # Git ignore file
├── LICENSE             # Project license
├── manage.py           # Django management script
├── requirements.txt    # Python dependencies
```
---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Author

- [muhgussap17](https://github.com/muhgussap17)
- Instagram: [@muhgussap](https://www.instagram.com/muhgussap?igsh=ZjE4Zjdvc3A4OHY1&utm_source=qr)

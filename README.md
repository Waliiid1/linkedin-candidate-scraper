LinkedIn Candidate Scraper 🔎

A Python tool that finds a LinkedIn profile from a person's name, retrieves publicly available profile information using Apify, and organizes the candidate's professional background into a structured format.

The project combines Serper API, Apify, Python, and OpenAI to create an automated candidate research workflow.

🚀 What It Does

Enter a person's full name and the application will:

🔎 Search Google for the person's LinkedIn profile using Serper.

🔗 Identify the most relevant LinkedIn profile.

🕷️ Send the LinkedIn URL to Apify's LinkedIn Profile Scraper.

📄 Retrieve the available profile information.

💼 Extract the candidate's work experience.

🎓 Extract education and academic background.

🧠 Extract skills, certifications, courses, and projects.

📋 Organize the information into a readable candidate profile.

🤖 Use OpenAI for further candidate analysis.

✨ Information Collected

Depending on what is publicly available, the scraper can retrieve:

💼 Professional Information

Current job title

Current company

Previous companies

Job descriptions

Employment dates

Job locations

Workplace type

Skills associated with positions

Total number of experiences

🎓 Education

University

Degree

Field of study

Education dates

Education descriptions

Academic projects

🧠 Skills & Certifications

Technical skills

Data analysis skills

Data science skills

Certifications

Certification providers

Certification dates

Courses

🚀 Projects

Project names

Project descriptions

Technologies used

Project results and metrics

👤 Profile Information

Full name

LinkedIn username

Profile headline

About / summary section

Location

Followers

Connections

Profile URL

🛠️ Technologies Used
Technology	Purpose
🐍 Python	Main application
🔎 Serper API	Finding LinkedIn profiles through Google search
🕷️ Apify	Retrieving LinkedIn profile data
🤖 OpenAI API	Candidate analysis
🔐 python-dotenv	Managing API keys through .env
🏗️ How It Works
                 Candidate Name
                       │
                       ▼
              ┌─────────────────┐
              │   Serper API    │
              │  Google Search  │
              └────────┬────────┘
                       │
                       ▼
                LinkedIn URL
                       │
                       ▼
              ┌─────────────────┐
              │     Apify       │
              │ LinkedIn Scraper│
              └────────┬────────┘
                       │
                       ▼
              Structured Profile
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
      Experience    Education     Skills
          │            │            │
          └────────────┼────────────┘
                       ▼
                Candidate Data
                       │
                       ▼
                ┌─────────────┐
                │   OpenAI    │
                │  Analysis   │
                └─────────────┘
                       │
                       ▼
              Candidate Assessment

📁 Project Structure
linkedin-candidate-scraper/
│
├── main.py
├── README.md
├── requirements.txt
└── .env.example
└──Screenshot

🔑 API Keys

This project uses environment variables so API keys are not written directly into the Python source code.

Create a .env file in the project folder:

OPENAI_API_KEY=your_openai_api_key
SERPER_API_KEY=your_serper_api_key
APIFY_API_TOKEN=your_apify_api_token


The application loads these values using os.getenv().


⚙️ Installation
1. Clone the repository
git clone https://github.com/Waliiid1/linkedin-candidate-scraper.git

2. Create a virtual environment
Windows
python -m venv venv
venv\Scripts\activate

Mac / Linux
python3 -m venv venv
source venv/bin/activate

3. Install the dependencies
pip install -r requirements.txt

4. Create your .env file

Add your API keys:

OPENAI_API_KEY=your_key_here
SERPER_API_KEY=your_key_here
APIFY_API_TOKEN=your_key_here

5. Run the application
python main.py


Then enter the candidate's full name when prompted.

💻 Example
Enter the person's full name: Walid Ahmed Hassan


The application searches Google using:

site:linkedin.com/in/ "Walid Ahmed Hassan"


It identifies the LinkedIn profile and sends the profile URL to Apify.

The resulting data can include (My experience btw):

Name:
Walid Ahmed Hassan

Current Position:
Business Intelligence Analyst at Microsoft

Previous Experience:
- Technical Support Engineer — Dell Technologies
- Information Technology Administrator — Engineeius
- IT Manager — Engineeius
- Sales Advisor — Bluerock For Real Estate
- Sales Specialist — Blue rock Real-Estate

Education:
- The German University in Cairo
- Computer Engineering
- Electrical Engineering and Computer Science

Skills:
- Data Analysis
- Data Science
- Database Queries
- Microsoft Business Intelligence
- Business Intelligence

Certifications:
- AWS Certified Cloud Practitioner
- Associate - PowerEdge Version 2.0

Projects:
- Battery Failure Prediction
- Face Mask Detection (YOLOv8)

🧠 Why I Built This

I built this project to explore how multiple APIs can be combined into a practical candidate research workflow.

The goal was to create a pipeline that could:

Find → Scrape → Structure → Analyze

Instead of manually searching through a candidate's profile, the application automates the process of finding the profile and organizing the available information.

📚 What I Learned

Through this project, I worked with:

Python

REST APIs

API authentication

Environment variables

.env configuration

JSON data

Nested JSON structures

Python dictionaries and lists

API error handling

Google search APIs

Apify actors

LinkedIn profile data

OpenAI API integration

Data extraction and transformation

Structuring unorganized information into useful candidate profiles

⚠️ Limitations

The amount of information returned can vary depending on:

LinkedIn profile visibility

Publicly available information

The Apify actor being used

Apify limitations

Serper limitations

API availability

Changes to LinkedIn

The application does not guarantee that every LinkedIn profile will return the same fields or amount of information.

🔐 Privacy & Responsible Use

This project is intended for educational and research purposes.

Users should respect LinkedIn's terms, applicable laws, privacy expectations, and the terms of the APIs and services being used.

Do not use this project to collect sensitive personal information or conduct unauthorized surveillance.

🔮 Future Improvements

 Add a web interface

 Export candidates to CSV

 Export candidates to JSON

 Generate candidate reports as PDF

 Add candidate scoring

 Add job-description matching

 Compare candidates against a job description

 Add structured skill extraction

 Add automated tests

 Improve API error handling

 Support multiple candidates

 Add logging

 Add configurable scraping options

📌 Project Status

Working Prototype

The core workflow is functional:

Name → Google Search → LinkedIn Profile → Apify → Structured Candidate Data

Future versions will focus on improving reliability, candidate analysis, user interface, and data export.

📄 License

This project is currently intended for educational purposes.

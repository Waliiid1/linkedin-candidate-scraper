LinkedIn Candidate Research & Profile Enrichment Tool

A Python-based candidate research tool that combines Google search, LinkedIn profile extraction through Apify, and structured profile analysis.

The tool accepts a person's full name, identifies a relevant LinkedIn profile, retrieves publicly available profile information through an Apify actor, and organizes the results into a structured candidate profile.

Features

Search for LinkedIn profiles using Google/Serper (An attempt to automate the process instead of getting the actual links)

Automatically identify a relevant LinkedIn profile

Retrieve profile information using Apify

Extract the full available About/Summary section

Extract complete work experience history

Extract education

Extract skills

Extract certifications

Extract projects

Extract courses

Extract follower and connection counts

Display structured candidate information

Load API credentials securely using environment variables

Architecture

The workflow is:

Candidate Name
      |
      v
Google / Serper
      |
      v
LinkedIn Profile URL
      |
      v
Apify LinkedIn Profile Scraper
      |
      v
Structured JSON Profile
      |
      v
Candidate Analysis / Output

Technologies

Python

Serper API

Apify API

OpenAI API

REST APIs

JSON

python-dotenv

Setup
1. Clone the repository
git clone https://github.com/Waliiid1/linkedin-candidate-scraper


2. Create a virtual environment
python -m venv venv


Activate it.

Windows:

venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Configure environment variables

Create a .env file:

OPENAI_API_KEY=your_openai_key
SERPER_API_KEY=your_serper_key
APIFY_API_TOKEN=your_apify_token


Do not commit .env to GitHub.

A .env.example file is included to show the required variables.

5. Run
python main.py


Enter the candidate's full name when prompted.

Example Workflow

Example:

Enter the person's full name: Walid Ahmed Hassan


The program searches for the candidate's LinkedIn profile, sends the profile URL to Apify, retrieves the available profile data, and organizes information such as:

About / Summary

Current position

Previous positions

Companies

Education

Skills

Certifications

Projects

Courses

Example Output
Candidate: Walid Ahmed Hassan

Current Position:
Business Intelligence Analyst

Current Company:
Microsoft

Location:
Cairo, Egypt

Experience:
Microsoft
Dell Technologies
Engineeius
Bluerock For Real Estate

Education:
The German University in Cairo

Skills:
Data Analysis
Data Science
Database Queries
Microsoft Business Intelligence
Business Intelligence

Certifications:
AWS Certified Cloud Practitioner
Associate - PowerEdge Version 2.0

Why I Built This

This project was built to explore practical API integration and automated candidate profile research.

It combines multiple external services into a single Python workflow and demonstrates how unstructured web/profile information can be collected and transformed into useful structured data and later on be used by agents to collect relevant data.

Important Notes

This project relies on third-party APIs and the availability/permissions of the selected Apify actor.

Results may vary depending on the information publicly available on a profile and the actor's capabilities.

Users are responsible for complying with the terms of service, privacy requirements, and applicable laws governing the services and data they use.

Future Improvements

Potential improvements include:

Candidate scoring

Job-description matching

Experience/skill gap analysis

Structured candidate summaries using an LLM

Export to CSV/JSON

Batch candidate processing

Duplicate profile detection

Improved search-result validation

Web interface

Database storage

Recruiter dashboard

Disclaimer

This project is intended for educational and research purposes. It does not bypass authentication or access private LinkedIn information.
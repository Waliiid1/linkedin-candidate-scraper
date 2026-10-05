import os
import sys
import json
import requests
from dotenv import load_dotenv
from apify_client import ApifyClient


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")


# ============================================================
# CONFIGURATION
# ============================================================

APIFY_ACTOR_ID = "data-slayer/linkedin-profile-scraper"

SERPER_URL = "https://google.serper.dev/search"


# ============================================================
# HELPERS
# ============================================================

def section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def clean(value):
    if value is None:
        return ""

    if isinstance(value, str):
        return value.strip()

    return str(value).strip()


def show(label, value):
    value = clean(value)

    if value:
        print(f"{label}: {value}")
    else:
        print(f"{label}: N/A")


# ============================================================
# CHECK API KEYS
# ============================================================

def check_api_keys():

    section("CHECKING API KEYS")

    print("OpenAI API key loaded:", bool(OPENAI_API_KEY))
    print("Serper API key loaded:", bool(SERPER_API_KEY))
    print("Apify API token loaded:", bool(APIFY_API_TOKEN))

    missing = []

    if not OPENAI_API_KEY:
        missing.append("OPENAI_API_KEY")

    if not SERPER_API_KEY:
        missing.append("SERPER_API_KEY")

    if not APIFY_API_TOKEN:
        missing.append("APIFY_API_TOKEN")

    if missing:

        print("\nMissing keys:")

        for key in missing:
            print("-", key)

        print("\nYour .env should contain:")
        print("OPENAI_API_KEY=...")
        print("SERPER_API_KEY=...")
        print("APIFY_API_TOKEN=...")

        sys.exit(1)


# ============================================================
# STEP 1 — GOOGLE / SERPER
# ============================================================

def find_linkedin_profile(name):

    section("STEP 1: SEARCHING GOOGLE")

    query = f'site:linkedin.com/in/ "{name}"'

    print("Search query:")
    print(query)

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "q": query,
        "num": 10
    }

    try:

        response = requests.post(
            SERPER_URL,
            headers=headers,
            json=payload,
            timeout=30
        )

        print(
            "Serper status code:",
            response.status_code
        )

        response.raise_for_status()

        data = response.json()

    except Exception as e:

        print("\nSerper request failed:")
        print(e)

        return None

    results = data.get("organic", [])

    print(
        "Number of Google results:",
        len(results)
    )

    for result in results:

        title = result.get("title", "")
        url = result.get("link", "")
        snippet = result.get("snippet", "")

        print("\n-------------------------")

        print("Title:")
        print(title)

        print("\nURL:")
        print(url)

        print("\nSnippet:")
        print(snippet)

        if "linkedin.com/in/" in url:

            # Normalize the URL
            linkedin_url = url.split("?")[0].strip()

            # Make sure we send a normal LinkedIn URL
            # to Apify rather than the regional domain.
            username = linkedin_url.split("/in/")[-1].strip("/")

            linkedin_url = (
                "https://www.linkedin.com/in/"
                + username
            )

            print("\nLinkedIn profile found!")
            print(linkedin_url)

            return linkedin_url

    print("\nNo LinkedIn profile found.")

    return None


# ============================================================
# STEP 2 — APIFY
# ============================================================

def scrape_linkedin(linkedin_url):

    section("STEP 2: SCRAPING LINKEDIN WITH APIFY")

    print("LinkedIn URL:")
    print(linkedin_url)

    print("\nStarting Apify Actor...")
    print("Actor:", APIFY_ACTOR_ID)

    # --------------------------------------------------------
    # THIS IS THE IMPORTANT FIX
    #
    # The UI displays:
    #
    # LinkedIn profile URL(s)
    #
    # But the API field is:
    #
    # linkedin_urls
    # --------------------------------------------------------

    run_input = {
        "linkedin_urls": [
            linkedin_url
        ]
    }

    print("\nApify input:")
    print(
        json.dumps(
            run_input,
            indent=2
        )
    )

    try:

        client = ApifyClient(
            APIFY_API_TOKEN
        )

        # Start actor and wait until it finishes
        run = client.actor(
            APIFY_ACTOR_ID
        ).call(
            run_input=run_input
        )

        # ----------------------------------------------------
        # Apify returns a Run object.
        #
        # DO NOT use:
        #
        # run.get(...)
        #
        # ----------------------------------------------------

        run_id = getattr(
            run,
            "id",
            None
        )

        dataset_id = getattr(
            run,
            "default_dataset_id",
            None
        )

        print("\nApify Actor finished.")

        print("\nRun ID:")
        print(run_id)

        print("\nDataset ID:")
        print(dataset_id)

        if not dataset_id:

            print(
                "\nERROR: Apify did not return a dataset ID."
            )

            return None

        # ----------------------------------------------------
        # READ DATASET
        # ----------------------------------------------------

        print("\nReading Apify dataset...")

        dataset = client.dataset(
            dataset_id
        )

        profiles = list(
            dataset.iterate_items()
        )

        print(
            "\nNumber of profiles returned:",
            len(profiles)
        )

        if not profiles:

            print("\nNo profile data was returned.")

            return None

        # We requested one profile
        profile = profiles[0]

        return profile

    except Exception as e:

        print("\nApify request failed:")
        print(type(e).__name__)
        print(e)

        return None


# ============================================================
# ABOUT
# ============================================================

def print_about(profile):

    section("ABOUT")

    about = profile.get(
        "description",
        ""
    )

    if not about:

        print("No About section returned.")

        return

    print(about)

    print(
        "\nAbout character count:",
        len(about)
    )


# ============================================================
# BASIC PROFILE
# ============================================================

def print_profile(profile):

    section("PROFILE")

    show(
        "Name",
        profile.get("full_name")
    )

    show(
        "First Name",
        profile.get("first_name")
    )

    show(
        "Last Name",
        profile.get("last_name")
    )

    show(
        "LinkedIn URL",
        profile.get("profile_link")
    )

    show(
        "Headline",
        profile.get("profile_headline")
    )

    show(
        "Current Job",
        profile.get("job_title")
    )

    show(
        "Current Company",
        profile.get("current_company_name")
    )

    show(
        "Location",
        profile.get("location")
    )

    show(
        "Country",
        profile.get("country")
    )

    show(
        "Connections",
        profile.get("connections")
    )

    show(
        "Followers",
        profile.get("followers")
    )

    show(
        "Total Experiences",
        profile.get("total_experiences")
    )


# ============================================================
# ALL EXPERIENCE
# ============================================================

def print_experience(profile):

    section("WORK EXPERIENCE")

    experiences = profile.get(
        "experience",
        []
    )

    if not isinstance(
        experiences,
        list
    ):

        print(
            "Experience data is not a list."
        )

        return

    print(
        "Number of experiences returned:",
        len(experiences)
    )

    print(
        "Profile total_experiences:",
        profile.get(
            "total_experiences",
            "N/A"
        )
    )

    for index, experience in enumerate(
        experiences,
        start=1
    ):

        print("\n" + "-" * 60)

        print(
            f"EXPERIENCE #{index}"
        )

        print("-" * 60)

        show(
            "Company",
            experience.get("company_name")
        )

        show(
            "Job Title",
            experience.get("job_title")
        )

        show(
            "Employment Type",
            experience.get("employment_type")
        )

        show(
            "Start Date",
            experience.get("job_started_on")
        )

        show(
            "End Date",
            experience.get("job_ended_on")
        )

        show(
            "Still Working",
            experience.get("job_still_working")
        )

        show(
            "Location",
            experience.get("job_location")
        )

        show(
            "Workplace Type",
            experience.get("workplace_type")
        )

        show(
            "Company Industry",
            experience.get("company_industry")
        )

        show(
            "Company Website",
            experience.get("company_website")
        )

        show(
            "Company LinkedIn",
            experience.get("company_url")
        )

        # ----------------------------------------------------
        # JOB DESCRIPTION
        # ----------------------------------------------------

        print("\nJob Description:")

        descriptions = experience.get(
            "job_description",
            []
        )

        if isinstance(
            descriptions,
            list
        ):

            if descriptions:

                for description in descriptions:

                    print(
                        clean(description)
                    )

            else:

                print("N/A")

        else:

            print(
                clean(descriptions)
                or "N/A"
            )

        # ----------------------------------------------------
        # EXPERIENCE SKILLS
        # ----------------------------------------------------

        print(
            "\nSkills associated with this experience:"
        )

        skills = experience.get(
            "skills",
            []
        )

        if isinstance(
            skills,
            list
        ) and skills:

            for skill in skills:

                print(
                    f"- {skill}"
                )

        else:

            print("N/A")


# ============================================================
# EDUCATION
# ============================================================

def print_education(profile):

    section("EDUCATION")

    education = profile.get(
        "education",
        []
    )

    if not isinstance(
        education,
        list
    ):

        print(
            "Education data is not a list."
        )

        return

    print(
        "Number of education entries:",
        len(education)
    )

    for index, item in enumerate(
        education,
        start=1
    ):

        print("\n" + "-" * 60)

        print(
            f"EDUCATION #{index}"
        )

        print("-" * 60)

        university = (
            item.get("university_name")
            or
            item.get("raw_university_name")
        )

        show(
            "University",
            university
        )

        show(
            "Degree",
            item.get("degree")
        )

        fields = item.get(
            "fields_of_study",
            []
        )

        print("\nFields of Study:")

        if isinstance(
            fields,
            list
        ) and fields:

            for field in fields:

                print(
                    f"- {field}"
                )

        else:

            print("N/A")

        started = item.get(
            "started_on",
            {}
        )

        ended = item.get(
            "ended_on",
            {}
        )

        if isinstance(
            started,
            dict
        ):

            show(
                "Start Year",
                started.get("year")
            )

        if isinstance(
            ended,
            dict
        ):

            show(
                "End Year",
                ended.get("year")
            )

        show(
            "Description",
            item.get("description")
        )

        show(
            "University Website",
            item.get("university_website")
        )


# ============================================================
# SKILLS
# ============================================================

def print_skills(profile):

    section("SKILLS")

    skills = profile.get(
        "skills",
        []
    )

    if not isinstance(
        skills,
        list
    ):

        print(
            "Skills data is not a list."
        )

        return

    print(
        "Number of skills:",
        len(skills)
    )

    if not skills:

        print(
            "No skills returned."
        )

        return

    for skill in skills:

        print(
            f"- {skill}"
        )


# ============================================================
# CERTIFICATIONS
# ============================================================

def print_certifications(profile):

    section("CERTIFICATIONS")

    certifications = profile.get(
        "certification",
        []
    )

    if not isinstance(
        certifications,
        list
    ):

        print(
            "Certification data is not a list."
        )

        return

    print(
        "Number of certifications:",
        len(certifications)
    )

    for index, cert in enumerate(
        certifications,
        start=1
    ):

        print("\n" + "-" * 60)

        print(
            f"CERTIFICATION #{index}"
        )

        print("-" * 60)

        show(
            "Name",
            cert.get("name")
        )

        show(
            "Issuer",
            cert.get("issuer")
        )

        show(
            "Issued",
            cert.get("issued_on")
        )

        show(
            "Expires",
            cert.get("expires_on")
        )

        show(
            "Credential ID",
            cert.get("credential_id")
        )

        show(
            "Credential URL",
            cert.get("credential_url")
        )


# ============================================================
# COURSES
# ============================================================

def print_courses(profile):

    section("COURSES")

    courses = profile.get(
        "courses",
        []
    )

    if not isinstance(
        courses,
        list
    ):

        print(
            "Courses data is not a list."
        )

        return

    print(
        "Number of courses:",
        len(courses)
    )

    for course in courses:

        show(
            "Course",
            course.get("name")
        )


# ============================================================
# PROJECTS
# ============================================================

def print_projects(profile):

    section("PROJECTS")

    projects = profile.get(
        "project",
        []
    )

    if not isinstance(
        projects,
        list
    ):

        print(
            "Project data is not a list."
        )

        return

    print(
        "Number of projects:",
        len(projects)
    )

    for index, project in enumerate(
        projects,
        start=1
    ):

        print("\n" + "-" * 60)

        print(
            f"PROJECT #{index}"
        )

        print("-" * 60)

        show(
            "Title",
            project.get("title")
        )

        show(
            "Date",
            project.get("date")
        )

        print("\nDescription:")

        description = project.get(
            "description",
            ""
        )

        print(
            clean(description)
            or "N/A"
        )


# ============================================================
# LANGUAGES
# ============================================================

def print_languages(profile):

    section("LANGUAGES")

    languages = profile.get(
        "language",
        []
    )

    if not isinstance(
        languages,
        list
    ):

        print(
            "Language data is not a list."
        )

        return

    print(
        "Number of languages:",
        len(languages)
    )

    if not languages:

        print("No languages returned.")

        return

    for language in languages:

        if isinstance(
            language,
            dict
        ):

            print(
                json.dumps(
                    language,
                    ensure_ascii=False
                )
            )

        else:

            print(
                f"- {language}"
            )


# ============================================================
# SAVE COMPLETE JSON
# ============================================================

def save_profile(profile):

    filename = (
        "linkedin_profile_raw.json"
    )

    try:

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                profile,
                file,
                indent=2,
                ensure_ascii=False
            )

        print(
            "\nComplete profile saved to:"
        )

        print(
            os.path.abspath(filename)
        )

    except Exception as e:

        print(
            "\nCould not save JSON:"
        )

        print(e)


# ============================================================
# MAIN
# ============================================================

def main():

    section(
        "LINKEDIN CANDIDATE SCRAPER"
    )

    check_api_keys()

    print()

    name = input(
        "Enter the person's full name: "
    ).strip()

    if not name:

        print(
            "Name cannot be empty."
        )

        return

    # --------------------------------------------------------
    # GOOGLE
    # --------------------------------------------------------

    linkedin_url = find_linkedin_profile(
        name
    )

    if not linkedin_url:

        section("FINAL RESULT")

        print(
            "Could not find LinkedIn profile."
        )

        return

    # --------------------------------------------------------
    # APIFY
    # --------------------------------------------------------

    profile = scrape_linkedin(
        linkedin_url
    )

    if not profile:

        section("FINAL RESULT")

        print(
            "No profile data returned."
        )

        return

    # --------------------------------------------------------
    # OUTPUT EVERYTHING
    # --------------------------------------------------------

    print_profile(
        profile
    )

    print_about(
        profile
    )

    print_experience(
        profile
    )

    print_education(
        profile
    )

    print_skills(
        profile
    )

    print_certifications(
        profile
    )

    print_courses(
        profile
    )

    print_projects(
        profile
    )

    print_languages(
        profile
    )

    # --------------------------------------------------------
    # SAVE EVERYTHING
    # --------------------------------------------------------

    save_profile(
        profile
    )

    # --------------------------------------------------------
    # FINAL
    # --------------------------------------------------------

    section("FINAL RESULT")

    print(
        "Profile successfully retrieved."
    )

    print(
        "\nName:",
        profile.get(
            "full_name",
            "N/A"
        )
    )

    print(
        "Headline:",
        profile.get(
            "profile_headline",
            "N/A"
        )
    )

    print(
        "Current Company:",
        profile.get(
            "current_company_name",
            "N/A"
        )
    )

    print(
        "Experiences:",
        len(
            profile.get(
                "experience",
                []
            )
        )
    )

    print(
        "Education entries:",
        len(
            profile.get(
                "education",
                []
            )
        )
    )

    print(
        "Skills:",
        len(
            profile.get(
                "skills",
                []
            )
        )
    )

    print(
        "Certifications:",
        len(
            profile.get(
                "certification",
                []
            )
        )
    )

    print(
        "Projects:",
        len(
            profile.get(
                "project",
                []
            )
        )
    )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    main()

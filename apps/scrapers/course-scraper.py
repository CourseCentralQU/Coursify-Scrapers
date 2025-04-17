import os
from supabase import create_client, Client
import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

def create_supabase_client():
    """
    Create a Supabase client using environment variables for URL and key.
    """
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return supabase



def scrape_course_data():
    """
    Scrape course data from Queen's University website and store it in Supabase."""
    headers = { "Accept-Language": "en-US,en;q=0.9,en-GB;q=0.8,en-CA;q=0.7" }
    art_sci_url = "https://www.queensu.ca/academic-calendar/arts-science/course-descriptions/"
    education_url = "https://www.queensu.ca/academic-calendar/education/course-descriptions/"
    health_sci_url = "https://www.queensu.ca/academic-calendar/health-sciences/bhsc/courses-instruction/"
    nursing_url = "https://www.queensu.ca/academic-calendar/nursing/bachelor-nursing-science-course-descriptions/"
    engineering_urls = [
        "https://www.queensu.ca/academic-calendar/engineering-applied-sciences/courses-instruction/apsc/",
        "https://www.queensu.ca/academic-calendar/engineering-applied-sciences/courses-instruction/chee/",
        "https://www.queensu.ca/academic-calendar/engineering-applied-sciences/courses-instruction/civl/",
        "https://www.queensu.ca/academic-calendar/engineering-applied-sciences/courses-instruction/cmpe/",
        "https://www.queensu.ca/academic-calendar/engineering-applied-sciences/courses-instruction/elec/",
        "https://www.queensu.ca/academic-calendar/engineering-applied-sciences/courses-instruction/ench/",
        "https://www.queensu.ca/academic-calendar/engineering-applied-sciences/courses-instruction/enph/",
        "https://www.queensu.ca/academic-calendar/engineering-applied-sciences/courses-instruction/geoe/",
        "https://www.queensu.ca/academic-calendar/engineering-applied-sciences/courses-instruction/mthe/",
        "https://www.queensu.ca/academic-calendar/engineering-applied-sciences/courses-instruction/mech/",
        "https://www.queensu.ca/academic-calendar/engineering-applied-sciences/courses-instruction/mren/",
        "https://www.queensu.ca/academic-calendar/engineering-applied-sciences/courses-instruction/mine/",
        "https://www.queensu.ca/academic-calendar/engineering-applied-sciences/courses-instruction/mntc/",
        "https://www.queensu.ca/academic-calendar/engineering-applied-sciences/courses-instruction/soft/",
    ]

    commerce_url = "https://www.queensu.ca/academic-calendar/business/bachelor-commerce/courses-of-instruction/by20number/#onezerozeroleveltext"
    
    # Create a pandas DataFrame to store the scraped data
    columns = [
        "course_code",
        "course_name",
        "course_description",
        "offering_faculty",
        "learning_hours",
        "course_learning_outcomes",
        "course_requirements",
        "course_equivalencies"
    ]
    course_data = pd.DataFrame(columns=columns)
    
    # Faculty 1: Arts & Science
    print("Scraping Arts & Science courses...")
    
    # Step 1: Get the main URL content
    results = requests.get(art_sci_url, headers=headers)
    art_sci_main_url_content = BeautifulSoup(results.content, "html.parser")

    # Step 2: Find the embedded links for the course offerings page for each department within the faculty
    art_sci_main_url_content_container = art_sci_main_url_content.find("div", class_="sitemap") # get the container element
    art_sci_dept_course_pages = art_sci_main_url_content_container.find_all("a") # get all the links in the container

    # Step 3: For each department, go through the courses offered and scrape the data
    for dept_course_page in art_sci_dept_course_pages:
                
        # Get the URL and name of the department course page
        dept_course_page_url = dept_course_page.get("href")
        dept_course_page_name = dept_course_page.get_text(strip=True)
        print(f"Scraping {dept_course_page_name} courses...")
        
        # Make a request to the department course page
        dept_course_page_results = requests.get("https://www.queensu.ca" + dept_course_page_url, headers=headers)
        dept_course_page_content = BeautifulSoup(dept_course_page_results.content, "html.parser")
        
        # Get each course from the department course page
        courses = dept_course_page_content.find_all("div", class_="courseblock")
        for course in courses:
            course_code = course.find("span", class_="detail-code").get_text(strip=True)
            course_name = course.find("span", class_="detail-title").get_text(strip=True)
            course_units = course.find("span", class_="detail-hours_html").get_text(strip=True).replace("Units: ", "")
            course_description = course.find("div", class_="courseblockextra").get_text(strip=True) if course.find("div", class_="courseblockextra") else None
            course_requirements = course.find("span", class_="detail-requirements").get_text(strip=True).replace("Requirements: ", "") if course.find("span", class_="detail-requirements") else None
            course_learning_hours = course.find("span", class_="detail-learning_hours").get_text(strip=True).replace("Learning Hours: ", "") if course.find("span", class_="detail-learning_hours") else None
            course_equivalencies = course.find("span", class_="detail-course_equivalencies").get_text(strip=True).replace("Course Equivalencies: ", "") if course.find("span", class_="detail-course_equivalencies") else None
            offering_faculty = course.find("span", class_="detail-offering_faculty").get_text(strip=True).replace("Offering Faculty: ", "") if course.find("span", class_="detail-offering_faculty") else None

            learning_outcomes = []
            outcomes_section = course.find("span", class_="detail-cim_los")
            if outcomes_section:
                outcomes_list = outcomes_section.find_all("li")
                for outcome in outcomes_list:
                    learning_outcomes.append(outcome.get_text(strip=True))

            # Append the course data to the DataFrame
            course_data = pd.concat([
            course_data,
            pd.DataFrame([{
                "course_code": course_code,
                "course_name": course_name,
                "course_description": course_description,
                "offering_faculty": offering_faculty,
                "learning_hours": course_learning_hours,
                "course_learning_outcomes": learning_outcomes,
                "course_requirements": course_requirements,
                "course_equivalencies": course_equivalencies,
                "course_units": course_units
            }])
            ], ignore_index=True)

    # Print success message
    print("✔ Successfully scraped Arts & Science courses!")

    # Step 4: Repeat the process for other faculties
    
    # Faculty 2: Education
    print("Scraping Education courses...")
    results = requests.get(education_url, headers=headers)
    education_main_url_content = BeautifulSoup(results.content, "html.parser")

    # Step 1: Get the main URL content
    results = requests.get(education_url, headers=headers)
    education_main_url_content = BeautifulSoup(results.content, "html.parser")

    # Step 2: Find all course blocks
    course_blocks = education_main_url_content.find_all("div", class_="courseblock")

    # Step 3: Extract course details
    for course in course_blocks:
        course_code = course.find("span", class_="detail-code").get_text(strip=True)
        course_name = course.find("span", class_="detail-title").get_text(strip=True)
        course_units = course.find("span", class_="detail-hours_html").get_text(strip=True).replace("Units: ", "")
        course_description = course.find("div", class_="courseblockextra").get_text(strip=True) if course.find("div", class_="courseblockextra") else None
        course_requirements = course.find("span", class_="detail-requirements").get_text(strip=True).replace("Requirements: ", "") if course.find("span", class_="detail-requirements") else None
        course_learning_hours = course.find("span", class_="detail-learning_hours").get_text(strip=True).replace("Learning Hours: ", "") if course.find("span", class_="detail-learning_hours") else None
        course_equivalencies = course.find("span", class_="detail-course_equivalencies").get_text(strip=True).replace("Course Equivalencies: ", "") if course.find("span", class_="detail-course_equivalencies") else None
        offering_faculty = course.find("span", class_="detail-offering_faculty").get_text(strip=True).replace("Offering Faculty: ", "") if course.find("span", class_="detail-offering_faculty") else None

        learning_outcomes = []
        outcomes_section = course.find("span", class_="detail-cim_los")
        if outcomes_section:
            outcomes_list = outcomes_section.find_all("li")
            for outcome in outcomes_list:
                learning_outcomes.append(outcome.get_text(strip=True))

        # Append the course data to the DataFrame
        course_data = pd.concat([
            course_data,
            pd.DataFrame([{
                "course_code": course_code,
                "course_name": course_name,
                "course_description": course_description,
                "offering_faculty": offering_faculty,
                "learning_hours": course_learning_hours,
                "course_learning_outcomes": learning_outcomes,
                "course_requirements": course_requirements,
                "course_equivalencies": course_equivalencies,
                "course_units": course_units
            }])
        ], ignore_index=True)

    # Print success message
    print("✔ Successfully scraped Education courses!")

    # Faculty 3: Health Sciences
    print("Scraping Health Sciences courses...")
    results = requests.get(health_sci_url, headers=headers)
    health_sci_main_url_content = BeautifulSoup(results.content, "html.parser")

    # Step 1: Find all course blocks
    course_blocks = health_sci_main_url_content.find_all("div", class_="courseblock")

    # Step 2: Extract course details
    for course in course_blocks:
        course_code = course.find("span", class_="detail-code").get_text(strip=True)
        course_name = course.find("span", class_="detail-title").get_text(strip=True)
        course_units = course.find("span", class_="detail-hours_html").get_text(strip=True).replace("Units: ", "")
        course_description = course.find("div", class_="courseblockextra").get_text(strip=True) if course.find("div", class_="courseblockextra") else None
        course_requirements = course.find("span", class_="detail-requirements").get_text(strip=True).replace("Requirements: ", "") if course.find("span", class_="detail-requirements") else None
        course_learning_hours = course.find("span", class_="detail-learning_hours").get_text(strip=True).replace("Learning Hours: ", "") if course.find("span", class_="detail-learning_hours") else None
        course_equivalencies = course.find("span", class_="detail-course_equivalencies").get_text(strip=True).replace("Course Equivalencies: ", "") if course.find("span", class_="detail-course_equivalencies") else None
        offering_faculty = course.find("span", class_="detail-offering_faculty").get_text(strip=True).replace("Offering Faculty: ", "") if course.find("span", class_="detail-offering_faculty") else None

        learning_outcomes = []
        outcomes_section = course.find("span", class_="detail-cim_los")
        if outcomes_section:
            outcomes_list = outcomes_section.find_all("li")
            for outcome in outcomes_list:
                learning_outcomes.append(outcome.get_text(strip=True))

        # Append the course data to the DataFrame
        course_data = pd.concat([
            course_data,
            pd.DataFrame([{
                "course_code": course_code,
                "course_name": course_name,
                "course_description": course_description,
                "offering_faculty": offering_faculty,
                "learning_hours": course_learning_hours,
                "course_learning_outcomes": learning_outcomes,
                "course_requirements": course_requirements,
                "course_equivalencies": course_equivalencies,
                "course_units": course_units
            }])
        ], ignore_index=True)

    # Print success message
    print("✔ Successfully scraped Health Sciences courses!")

    # Faculty 4: Nursing
    print("Scraping Nursing courses...")
    results = requests.get(nursing_url, headers=headers)
    nursing_main_url_content = BeautifulSoup(results.content, "html.parser")

    # Step 1: Find all course blocks
    course_blocks = nursing_main_url_content.find_all("div", class_="courseblock")

    # Step 2: Extract course details
    for course in course_blocks:
        course_code = course.find("span", class_="detail-code").get_text(strip=True)
        course_name = course.find("span", class_="detail-title").get_text(strip=True)
        course_units = course.find("span", class_="detail-hours_html").get_text(strip=True).replace("Units: ", "")
        course_description = course.find("div", class_="courseblockextra").get_text(strip=True) if course.find("div", class_="courseblockextra") else None
        course_requirements = course.find("span", class_="detail-requirements").get_text(strip=True).replace("Requirements: ", "") if course.find("span", class_="detail-requirements") else None
        course_learning_hours = None  # Not available in the provided structure
        course_equivalencies = course.find("span", class_="detail-course_equivalencies").get_text(strip=True).replace("Course Equivalencies: ", "") if course.find("span", class_="detail-course_equivalencies") else None
        offering_faculty = course.find("span", class_="detail-offering_faculty").get_text(strip=True).replace("Offering Faculty: ", "") if course.find("span", class_="detail-offering_faculty") else None

        learning_outcomes = []
        outcomes_section = course.find("span", class_="detail-cim_los")
        if outcomes_section:
            outcomes_list = outcomes_section.find_all("li")
            for outcome in outcomes_list:
                learning_outcomes.append(outcome.get_text(strip=True))

        # Append the course data to the DataFrame
        course_data = pd.concat([
            course_data,
            pd.DataFrame([{
                "course_code": course_code,
                "course_name": course_name,
                "course_description": course_description,
                "offering_faculty": offering_faculty,
                "learning_hours": course_learning_hours,
                "course_learning_outcomes": learning_outcomes,
                "course_requirements": course_requirements,
                "course_equivalencies": course_equivalencies,
                "course_units": course_units
            }])
        ], ignore_index=True)

    # Print success message
    print("✔ Successfully scraped Nursing courses!")

    # Faculty 5: Engineering
    print("Scraping Engineering courses...")

    for engineering_url in engineering_urls:
        # Make a request to the engineering URL
        results = requests.get(engineering_url, headers=headers)
        engineering_main_url_content = BeautifulSoup(results.content, "html.parser")

        # Find all course blocks
        course_blocks = engineering_main_url_content.find_all("div", class_="courseblock")

        # Extract course details
        for course in course_blocks:
            course_code = course.find("span", class_="detail-code").get_text(strip=True)
            course_name = course.find("span", class_="detail-title").get_text(strip=True)
            course_units = course.find("span", class_="detail-hours_html").get_text(strip=True).replace("Units: ", "")
            course_description = course.find("div", class_="courseblockextra").get_text(strip=True) if course.find("div", class_="courseblockextra") else None
            course_requirements = course.find("span", class_="detail-requirements").get_text(strip=True).replace("Requirements: ", "") if course.find("span", class_="detail-requirements") else None
            course_learning_hours = None  # Not available in the provided structure
            course_equivalencies = course.find("span", class_="detail-course_equivalencies").get_text(strip=True).replace("Course Equivalencies: ", "") if course.find("span", class_="detail-course_equivalencies") else None
            offering_faculty = course.find("span", class_="detail-offering_faculty").get_text(strip=True).replace("Offering Faculty: ", "") if course.find("span", class_="detail-offering_faculty") else None

            learning_outcomes = []
            outcomes_section = course.find("span", class_="detail-cim_los")
            if outcomes_section:
                outcomes_list = outcomes_section.find_all("li")
                for outcome in outcomes_list:
                    learning_outcomes.append(outcome.get_text(strip=True))

            # Append the course data to the DataFrame
            course_data = pd.concat([
                course_data,
                pd.DataFrame([{
                    "course_code": course_code,
                    "course_name": course_name,
                    "course_description": course_description,
                    "offering_faculty": offering_faculty,
                    "learning_hours": course_learning_hours,
                    "course_learning_outcomes": learning_outcomes,
                    "course_requirements": course_requirements,
                    "course_equivalencies": course_equivalencies,
                    "course_units": course_units
                }])
            ], ignore_index=True)

        print(f"✔ Successfully scraped courses from {engineering_url}")

    # Faculty 6: Commerce
    print("Scraping Commerce courses...")

    # Make a request to the Commerce URL
    response = requests.get(commerce_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all course blocks
    course_blocks = soup.find_all("div", class_="courseblock")

    # Extract course details
    for course in course_blocks:
        course_code = course.find("span", class_="detail-code").get_text(strip=True)
        course_name = course.find("span", class_="detail-title").get_text(strip=True)
        course_units = course.find("span", class_="detail-hours_html").get_text(strip=True).replace("Units: ", "")
        course_description = course.find("div", class_="courseblockextra").get_text(strip=True) if course.find("div", class_="courseblockextra") else None
        course_requirements = course.find("span", class_="detail-requirements").get_text(strip=True).replace("Requirements: ", "") if course.find("span", class_="detail-requirements") else None
        course_equivalencies = course.find("span", class_="detail-course_equivalencies").get_text(strip=True).replace("Course Equivalencies: ", "") if course.find("span", class_="detail-course_equivalencies") else None
        offering_faculty = course.find("span", class_="detail-offering_faculty").get_text(strip=True).replace("Offering Faculty: ", "") if course.find("span", class_="detail-offering_faculty") else None

        learning_outcomes = []
        outcomes_section = course.find("span", class_="detail-cim_los")
        if outcomes_section:
            outcomes_list = outcomes_section.find_all("li")
            for outcome in outcomes_list:
                learning_outcomes.append(outcome.get_text(strip=True))

        # Append the course data to the DataFrame
        course_data = pd.concat([
            course_data,
            pd.DataFrame([{
                "course_code": course_code,
                "course_name": course_name,
                "course_description": course_description,
                "offering_faculty": offering_faculty,
                "learning_hours": None,  # Not available in this structure
                "course_learning_outcomes": learning_outcomes,
                "course_requirements": course_requirements,
                "course_equivalencies": course_equivalencies,
                "course_units": course_units
            }])
        ], ignore_index=True)

    # Print success message
    print("✔ Successfully scraped Commerce courses!")
    
    course_data.to_csv("course_data.csv", index=False)
    print("✔ Successfully saved course data to CSV!")

    # Drop duplicates
    course_data.drop_duplicates(subset=["course_code"], inplace=True)

    # Clean the dataframe
    course_data.replace({np.nan: None, float("inf"): None, float("-inf"): None}, inplace=True)
    
    # Print hte number of rows in the DataFrame
    print(f"Total number of courses scraped: {len(course_data)}")

    return course_data

def insert_course_data_to_supabase(supabase, course_data):
    """
    Insert the scraped course data into Supabase.
    """    
    # Insert the course data into Supabase
    for index, row in course_data.iterrows():
        supabase.table("courses").insert({
            "course_code": row["course_code"],
            "course_name": row["course_name"],
            "course_description": row["course_description"],
            "offering_faculty": row["offering_faculty"],
            "learning_hours": row["learning_hours"],
            "course_learning_outcomes": row["course_learning_outcomes"],
            "course_requirements": row["course_requirements"],
            "course_equivalencies": row["course_equivalencies"],
            "course_units": row["course_units"],
            "average_gpa": None,  # Placeholder for average GPA
            "average_enrollment": None  # Placeholder for average enrollment
        }).execute()
        print(f"Inserted course: {row['course_code']} - {row['course_name']}")

    print("✔ Successfully inserted course data into Supabase!")


if __name__ == "__main__":
    # Create Supabase client
    supabase = create_supabase_client()
    
    # Scrape course data
    course_data = scrape_course_data()
    
    # Insert course data into Supabase
    insert_course_data_to_supabase(supabase, course_data)

    # Print success message
    print("✔ Course data scraping and insertion completed successfully!")

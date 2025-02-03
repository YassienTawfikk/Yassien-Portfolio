import json


def main():
    # 1. Load the personal data
    with open('../data/db_data.json', 'r', encoding='utf-8') as f:
        db_data = json.load(f)

    # 2. Load the aboutMe data
    with open('../data/_02_about.json', 'r', encoding='utf-8') as f:
        about_data = json.load(f)

    # 3. Load the education data
    with open('../data/_04_education.json', 'r', encoding='utf-8') as f:
        education_data = json.load(f)

    # 3. Extract name and age
    name = db_data['personal_information']['name']
    age = db_data['personal_information']['age']
    profession = db_data['personal_information']['profession']
    university = db_data['education']['university']
    faculty = db_data['education']['faculty']
    degree = db_data['education']['degree']
    expected_graduation = db_data['education']['expected_graduation']
    biomedical_courses = db_data['education']['key_courses']['biomedical']
    technical_courses = db_data['education']['key_courses']['technical']
    mathematics_courses = db_data['education']['key_courses']['mathematics']

    # 4. Construct a fresh description based on current data
    updated_description = (
        f"Hi, I’m {name}, a {age}-year-old {profession} from {university}, "
        f"{faculty}. My journey is guided by a deep interest in how "
        "technology can address healthcare challenges and make life easier. I enjoy "
        "finding practical solutions and designing tools that improve accessibility "
        "and efficiency in healthcare. With a calm and precise approach, I focus on "
        "creating meaningful impact through innovation. Outside of my work, I’m "
        "constantly seeking opportunities to learn, grow, and contribute to shaping "
        "a better future for healthcare."
    )

    # 5. Update the 'description' field in the aboutMe data
    about_data['description'] = updated_description
    education_data['university'] = university
    education_data['faculty'] = faculty
    education_data['degree'] = degree
    education_data['expected_graduation'] = expected_graduation
    education_data['key_courses']['biomedical'] = biomedical_courses
    education_data['key_courses']['technical'] = technical_courses
    education_data['key_courses']['mathematics'] = mathematics_courses

    # 6. Write the updated data back to aboutMe.json
    with open('../data/_02_about.json', 'w', encoding='utf-8') as f:
        json.dump(about_data, f, ensure_ascii=False, indent=4)

    with open('../data/_04_education.json', 'w', encoding='utf-8') as f:
        json.dump(education_data, f, ensure_ascii=False, indent=4)

    print("aboutMe.json has been updated successfully!")


if __name__ == "__main__":
    main()

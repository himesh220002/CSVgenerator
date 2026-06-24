# pyrefly: ignore [missing-import]
import streamlit as st
import csv
import random
import os
import pandas as pd
import uuid
# pyrefly: ignore [missing-import]
import rstr
import datetime
# pyrefly: ignore [missing-import]
from faker import Faker

fake = Faker()

st.set_page_config(page_title="CSV Data Generators", layout="wide")

# 80 Unique First Names
FIRST_NAMES = [
    "Rahul", "Priya", "Arjun", "Sneha", "Karan", "Ananya", "Rohan", "Meera", "Aditya", "Neha", 
    "Aman", "Riya", "Dev", "Tanya", "Aarav", "Ishita", "Manav", "Pooja", "Amit", "Kriti",
    "Vikram", "Kavya", "Rohan", "Divya", "Siddharth", "Anjali", "Yash", "Ridhi", "Kabir", "Shreya",
    "Rudra", "Isha", "Gaurav", "Tanvi", "Varun", "Mehak", "Kunwar", "Prisha", "Hrithik", "Nisha",
    "Abhishek", "Aanchal", "Mayank", "Swati", "Rishabh", "Ritu", "Deepak", "Payal", "Sanjay", "Jyoti",
    "Rajesh", "Kiran", "Vijay", "Lata", "Anil", "Suman", "Arun", "Aarti", "Manoj", "Komal",
    "Sameer", "Nupur", "Pranav", "Alka", "Tushar", "Priti", "Vivek", "Sonia", "Alok", "Barkha",
    "Akash", "Kajal", "Sandeep", "Monika", "Pankaj", "Richa", "Saurabh", "Poonam", "Manish", "Sakshi"
]

# 80 Unique Last Names
LAST_NAMES = [
    "Sharma", "Das", "Mehta", "Roy", "Gupta", "Singh", "Verma", "Iqbal", "Kumar", "Patel", 
    "Joshi", "Sen", "Malhotra", "Kapoor", "Jain", "Bose", "Khanna", "Nair", "Reddy", "Choudhury",
    "Mishra", "Pandey", "Yadav", "Trivedi", "Dwivedi", "Bajpai", "Agrawal", "Bansal", "Goel", "Garg",
    "Saxena", "Srivastava", "Sinha", "Prasad", "Ranjan", "Kashyap", "Thakur", "Chauhan", "Rathore", "Rajput",
    "Chatterjee", "Mukherjee", "Banerjee", "Chakraborty", "Ganguly", "Ghosh", "Sen", "Dutta", "Mitra", "Pal",
    "Kulkarni", "Deshmukh", "Joshi", "Patil", "Pawar", "Gaekwad", "Shinde", "Mahajan", "Nair", "Menon",
    "Pillai", "Iyer", "Iyengar", "Rao", "Murthy", "Naidu", "Chetty", "Balakrishnan", "Acharya", "Bhatt",
    "Gill", "Dhillon", "Sidhu", "Grewal", "Sandhu", "Johal", "Chawla", "Malik", "Bhasin", "Suri"
]

st.title("🗂️ Synthetic Data Generators")
st.markdown("Generate robust, diverse datasets for testing and analytics pipelines.")

tab1, tab2 = st.tabs(["🎓 Student Performance Dataset", "🔜 Future Generators"])

with tab1:
    st.header("Student Intelligence Synthetic Data")
    st.markdown("Generates a comprehensive school-wide dataset containing randomized student profiles, grades, and engagement metrics.")
    
    st.markdown("### ⚙️ Dynamic Configuration")
    col1, col2 = st.columns(2)
    with col1:
        max_students = st.number_input("Max Students per Section", min_value=1, max_value=500, value=40)
        classes_input = st.text_input("Classes (comma-separated)", value="8, 9, 10, 11, 12")
        junior_sub_input = st.text_input("Junior Subjects (Class <= 10)", value="Maths, Science, Social, English, Hindi, Arts")
    with col2:
        output_filename = st.text_input("Output Filename", value="complete_school_dataset.csv")
        sections_input = st.text_input("Sections (comma-separated)", value="A, B, C")
        senior_sub_input = st.text_input("Senior Subjects (Class > 10)", value="Maths, Physics, Chemistry, Biology, English, Social, Painting")
        
    if st.button("🚀 Generate Student Dataset", type="primary"):
        with st.spinner("Generating complex school hierarchy..."):
            # 1. School Structure Setup (Parsed dynamically from user input)
            classes = [int(c.strip()) for c in classes_input.split(',') if c.strip().isdigit()]
            sections = [s.strip() for s in sections_input.split(',') if s.strip()]
            
            # Subject Pools
            class_10_subjects = [s.strip() for s in junior_sub_input.split(',') if s.strip()]
            high_school_subjects = [s.strip() for s in senior_sub_input.split(',') if s.strip()]
            
            # Names list to pull from randomly (combining first and last names)
            first_names = FIRST_NAMES
            last_names = LAST_NAMES
            
            # CSV Columns Matching Your Dashboard Schema
            headers = [
                "Class", "Section", "Subject", "Name", "ID", "Roll Number", "Attendance (%)", 
                "Unit Test 1", "Unit Test 2", "Unit Test 3", "Home Tuition (Y/N)", 
                "Focus (0-10)", "Homework (0-10)", "Q&A (0-10)", "Doubt Asking Rate", 
                "Exam Prep (0-10)", "Special Problems Completion (%)"
            ]
            
            all_rows = []
            
            # 2. Loop through the school hierarchy
            for cls in classes:
                for sec in sections:
                    # Loop through student numbers 1 to max_students for this specific section
                    for student_num in range(1, max_students + 1):
                        
                        # Formulate the Name and keep it identical for all this student's subjects
                        student_name = f"{random.choice(first_names)} {random.choice(last_names)}"
                        
                        # ID format: Class_Section_Integer (e.g., 8_A_10)
                        student_id = f"{cls}_{sec}_{student_num}"
                        
                        # Roll Number format based on formula (e.g., 80110 for class 8, section 1, student 10)
                        sec_digit = "01" if sec == 'A' else "02" if sec == 'B' else "03"
                        student_num_padded = f"{student_num:02d}"
                        roll_number = f"{cls}{sec_digit}{student_num_padded}"
                        
                        # Select the correct subject list based on the Class level (<= 10 gets Junior subjects)
                        subjects = class_10_subjects if cls <= 10 else high_school_subjects
                        
                        # Create a row for EACH subject for this unique student
                        for sub in subjects:
                            row = {
                                "Class": cls,
                                "Section": sec,
                                "Subject": sub,
                                "Name": student_name,         # Stays exactly the same
                                "ID": student_id,             # Stays exactly the same
                                "Roll Number": roll_number,   # Stays exactly the same
                                "Attendance (%)": random.randint(65, 100),
                                "Unit Test 1": random.randint(40, 100),
                                "Unit Test 2": random.randint(40, 100),
                                "Unit Test 3": random.randint(40, 100),
                                "Home Tuition (Y/N)": random.choice(['Y', 'N']),
                                "Focus (0-10)": random.randint(3, 10),
                                "Homework (0-10)": random.randint(3, 10),
                                "Q&A (0-10)": random.randint(2, 10),
                                "Doubt Asking Rate": round(random.uniform(0.1, 1.0), 1),
                                "Exam Prep (0-10)": random.randint(3, 10),
                                "Special Problems Completion (%)": random.randint(30, 100)
                            }
                            all_rows.append(row)
            
            # Ensure raw data dir exists
            raw_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', 'raw'))
            os.makedirs(raw_dir, exist_ok=True)
            
            output_path = os.path.join(raw_dir, output_filename)
            
            # 3. Write all generated data rows to a CSV file
            with open(output_path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(all_rows)
                
            st.success(f"🎉 Successfully generated {len(all_rows)} row entries for the entire school!")
            st.info(f"📁 Saved file directly to your system at: `data/raw/{output_filename}`")
            
            # Display sample and provide download
            df = pd.DataFrame(all_rows)
            st.write("### Data Preview")
            st.dataframe(df.head(15), width="stretch")
            
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Generated CSV manually",
                data=csv_data,
                file_name=output_filename,
                mime="text/csv",
            )

with tab2:
    st.header("🛠️ Custom CSV Generator")
    st.markdown("Build your own raw CSV data template from scratch.")
    
    if "custom_fields" not in st.session_state:
        st.session_state.custom_fields = [
            {"id": 0, "name": "id", "type": "Index", "settings": {"start": 100}},
            {"id": 1, "name": "firstname", "type": "First name", "settings": {}},
            {"id": 2, "name": "lastname", "type": "Last name", "settings": {}},
            {"id": 3, "name": "email", "type": "Expression", "settings": {"expr": "{firstname}.{lastname}@yopmail.com"}},
            {"id": 4, "name": "email2", "type": "Custom", "settings": {"code": "f\"{row.get('firstname', '')}.{row.get('lastname', '')}@gmail.com\""}},
            {"id": 5, "name": "profession", "type": "Choice", "settings": {"choices": "doctor\npolice officer\nfirefighter"}},
        ]
        st.session_state.field_counter = 6

    def add_field():
        st.session_state.custom_fields.append({
            "id": st.session_state.field_counter,
            "name": f"field_{st.session_state.field_counter}",
            "type": "First name",
            "settings": {}
        })
        st.session_state.field_counter += 1

    def remove_field(field_id):
        st.session_state.custom_fields = [f for f in st.session_state.custom_fields if f["id"] != field_id]

    # Render Fields
    st.markdown("### Fields Definition")
    
    # Headers
    col_del, col_name, col_type, col_set = st.columns([0.5, 2, 2, 4])
    col_name.write("**Field name**")
    col_type.write("**Data type**")
    col_set.write("**Setting**")
    st.markdown("---")
    
    for i, field in enumerate(st.session_state.custom_fields):
        col1, col2, col3, col4 = st.columns([0.5, 2, 2, 4])
        with col1:
            if st.button("❌", key=f"del_{field['id']}"):
                remove_field(field["id"])
                st.rerun()
        with col2:
            field["name"] = st.text_input("Field name", value=field["name"], key=f"name_{field['id']}", label_visibility="collapsed")
        with col3:
            data_types = [
                "Index", "GUID", "Random (integer)", "Random (Float)", 
                "Random (Date)", "Regular expression", "Expression", 
                "First name", "Last name", "City", "Country", 
                "Country code", "Choice", "Lorem Ipsum", "Custom"
            ]
            current_type = field.get("type", "First name")
            if current_type == "Custom Python": current_type = "Custom"
            field["type"] = st.selectbox("Data type", data_types, index=data_types.index(current_type) if current_type in data_types else 7, key=f"type_{field['id']}", label_visibility="collapsed")
        with col4:
            t = field["type"]
            if t == "Index":
                field["settings"]["start"] = st.number_input("From", value=field["settings"].get("start", 100), key=f"settings_{field['id']}", label_visibility="collapsed")
            elif t == "Random (integer)":
                scol1, scol2 = st.columns(2)
                with scol1: field["settings"]["min"] = st.number_input("Min", value=field["settings"].get("min", 0), key=f"settings_min_{field['id']}", label_visibility="collapsed")
                with scol2: field["settings"]["max"] = st.number_input("Max", value=field["settings"].get("max", 100), key=f"settings_max_{field['id']}", label_visibility="collapsed")
            elif t == "Random (Float)":
                scol1, scol2 = st.columns(2)
                with scol1: field["settings"]["min_f"] = st.number_input("Min", value=field["settings"].get("min_f", 0.0), step=0.1, format="%.2f", key=f"settings_minf_{field['id']}", label_visibility="collapsed")
                with scol2: field["settings"]["max_f"] = st.number_input("Max", value=field["settings"].get("max_f", 100.0), step=0.1, format="%.2f", key=f"settings_maxf_{field['id']}", label_visibility="collapsed")
            elif t == "Random (Date)":
                scol1, scol2 = st.columns(2)
                default_start = datetime.date(2000, 1, 1)
                default_end = datetime.date.today()
                with scol1: field["settings"]["start_date"] = st.date_input("Start", value=field["settings"].get("start_date", default_start), key=f"settings_startd_{field['id']}", label_visibility="collapsed")
                with scol2: field["settings"]["end_date"] = st.date_input("End", value=field["settings"].get("end_date", default_end), key=f"settings_endd_{field['id']}", label_visibility="collapsed")
            elif t == "Regular expression":
                field["settings"]["regex"] = st.text_input("Regex", value=field["settings"].get("regex", "^[A-Z0-9]{8}$"), key=f"settings_{field['id']}", label_visibility="collapsed")
            elif t == "Expression":
                field["settings"]["expr"] = st.text_input("Expression", value=field["settings"].get("expr", ""), placeholder="{firstname}-{lastname}@domain.com", key=f"settings_{field['id']}", label_visibility="collapsed")
            elif t == "Custom":
                field["settings"]["code"] = st.text_area("Python Expression (use 'row' dict)", value=field["settings"].get("code", ""), key=f"settings_{field['id']}", label_visibility="collapsed", height=68)
                with st.expander("💡 View 15 Pre-built Code & Function Templates"):
                    st.markdown("""
**1. Combine Existing Columns**
```python
f"{row.get('firstname', '')} {row.get('lastname', '')}"
```
**2. Email Generator**
```python
f"{row.get('firstname', '').lower()}.{row.get('lastname', '').lower()}@company.com"
```
**3. Conditional Logic (Pass/Fail)**
```python
"Pass" if int(row.get("score", 0)) >= 50 else "Fail"
```
**4. Math Calculation (e.g. Add 15% Tax)**
```python
round(float(row.get("price", 0)) * 1.15, 2)
```
**5. Weighted Random Choice**
```python
random.choices(["Low", "Medium", "High"], weights=[70, 20, 10], k=1)[0]
```
**6. Formatted Date from Faker**
```python
fake.date_time_this_year().strftime("%d-%b-%Y")
```
**7. JSON Payload Structure**
```python
str({"id": str(uuid.uuid4())[:8], "status": "active"})
```
**8. Data Masking (e.g. Phone Number)**
```python
row.get("phone", "")[:3] + "****" + row.get("phone", "")[-2:]
```
**9. MD5 Hashing (e.g. for Emails)**
```python
__import__("hashlib").md5(str(row.get("email", "")).encode()).hexdigest()
```
**10. Advanced Faker Data (Job & Company)**
```python
f"{fake.job()} at {fake.company()}"
```
**11. Function: Assign to 'result'**
```python
if int(row.get('age', 0)) >= 18:
    result = "Adult"
else:
    result = "Minor"
```
**12. Function: Define 'process(row)'**
```python
def process(row):
    score = int(row.get('score', 0))
    if score >= 90: return 'A'
    if score >= 80: return 'B'
    return 'C'
```
**13. Function: Complex Validation**
```python
def process(row):
    email = row.get('email', '')
    if '@' in email and '.' in email:
        return email.lower()
    return 'invalid_email@domain.com'
```
**14. Function: List Aggregation**
```python
def process(row):
    hobbies = []
    if random.random() > 0.5: hobbies.append("Reading")
    if random.random() > 0.5: hobbies.append("Sports")
    return ", ".join(hobbies) if hobbies else "None"
```
**15. Function: External Library API Call (Mocked)**
```python
def process(row):
    import base64
    combined = f"{row.get('id')}:{row.get('email')}"
    return base64.b64encode(combined.encode()).decode()
```
                    """)
            elif t == "Choice":
                field["settings"]["choices"] = st.text_area("Word list (one per line)", value=field["settings"].get("choices", ""), key=f"settings_{field['id']}", label_visibility="collapsed", height=68)
            else:
                st.markdown("<br>", unsafe_allow_html=True) # Spacer
                
    st.button("➕ Add field", on_click=add_field)
    
    st.markdown("---")
    
    # Export Settings
    st.markdown("### Export Settings")
    col_fmt1, col_fmt2, col_fmt3, col_fmt4, col_fmt5 = st.columns(5)
    with col_fmt1:
        file_format = st.selectbox("Format", ["CSV"])
    with col_fmt2:
        num_rows = st.number_input("# Rows", min_value=1, value=1000)
    with col_fmt3:
        num_files = st.number_input("# Files", min_value=1, value=1)
    with col_fmt4:
        output_filename_custom = st.text_input("Filename", value="myFile.csv")
    with col_fmt5:
        delimiter = st.selectbox("Delimiter", [",", ";", "\\t", "|"], format_func=lambda x: "Comma" if x == "," else "Semicolon" if x == ";" else "Tab" if x == "\\t" else "Pipe")
        
    col_ext1, col_ext2, col_ext3, col_ext4 = st.columns(4)
    with col_ext1:
        quote_char = st.selectbox("Quote", ['"', "'"], format_func=lambda x: "Double quote" if x == '"' else "Single quote")
    with col_ext2:
        escape_char = st.selectbox("Escape", ['"', "'", "\\"], format_func=lambda x: "Double quote" if x == '"' else "Single quote" if x == "'" else "Backslash")
    with col_ext3:
        end_line = st.selectbox("End line", ["\\n", "\\r\\n"])
    with col_ext4:
        include_header = st.selectbox("Include header", ["Yes", "No"]) == "Yes"

    if st.button("🚀 Generate Custom Data", type="primary"):
        with st.spinner("Generating custom dataset..."):
            all_generated_rows = []
            
            for row_idx in range(num_rows):
                row = {}
                for field in st.session_state.custom_fields:
                    f_name = field["name"]
                    f_type = field["type"]
                    f_settings = field.get("settings", {})
                    
                    val = ""
                    if f_type == "Index":
                        val = f_settings.get("start", 100) + row_idx
                    elif f_type == "GUID":
                        val = str(uuid.uuid4())
                    elif f_type == "Random (integer)":
                        val = random.randint(int(f_settings.get("min", 0)), int(f_settings.get("max", 100)))
                    elif f_type == "Random (Float)":
                        val = round(random.uniform(float(f_settings.get("min_f", 0.0)), float(f_settings.get("max_f", 100.0))), 2)
                    elif f_type == "Random (Date)":
                        sd = f_settings.get("start_date", datetime.date(2000, 1, 1))
                        ed = f_settings.get("end_date", datetime.date.today())
                        if sd and ed and ed >= sd:
                            delta = ed - sd
                            random_days = random.randint(0, delta.days)
                            val = (sd + datetime.timedelta(days=random_days)).isoformat()
                        else:
                            val = sd.isoformat() if sd else ""
                    elif f_type == "Regular expression":
                        pattern = f_settings.get("regex", "^[A-Z0-9]{8}$")
                        try:
                            val = rstr.xeger(pattern)
                        except Exception:
                            val = "Regex Error"
                    elif f_type == "First name":
                        val = fake.first_name()
                    elif f_type == "Last name":
                        val = fake.last_name()
                    elif f_type == "City":
                        val = fake.city()
                    elif f_type == "Country":
                        val = fake.country()
                    elif f_type == "Country code":
                        val = fake.country_code()
                    elif f_type == "Lorem Ipsum":
                        val = fake.sentence()
                    elif f_type == "Choice":
                        choices = [c.strip() for c in f_settings.get("choices", "").split('\n') if c.strip()]
                        if choices:
                            val = random.choice(choices)
                    elif f_type == "Expression":
                        expr = f_settings.get("expr", "")
                        try:
                            val = expr.format(**row)
                        except Exception as e:
                            val = f"Error: {e}"
                    elif f_type == "Custom":
                        code = f_settings.get("code", "")
                        local_scope = {"row": row, "random": random, "fake": fake, "uuid": uuid}
                        try:
                            val = eval(code, local_scope)
                        except SyntaxError:
                            try:
                                exec(code, local_scope)
                                if 'result' in local_scope:
                                    val = local_scope['result']
                                elif 'process' in local_scope:
                                    val = local_scope['process'](row)
                                else:
                                    val = "Error: Assign 'result' or define 'process(row)'"
                            except Exception as e:
                                val = f"Error: {e}"
                        except Exception as e:
                            val = f"Error: {e}"
                    
                    row[f_name] = val
                
                all_generated_rows.append(row)
            
            raw_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', 'raw'))
            os.makedirs(raw_dir, exist_ok=True)
            output_path = os.path.join(raw_dir, output_filename_custom)
            
            actual_delimiter = '\t' if delimiter == '\\t' else delimiter
            actual_end_line = '\r\n' if end_line == '\\r\\n' else '\n'
            
            with open(output_path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f, 
                    fieldnames=[f["name"] for f in st.session_state.custom_fields],
                    delimiter=actual_delimiter,
                    quotechar=quote_char,
                    escapechar=escape_char if escape_char != '"' else None,
                    doublequote=(escape_char == quote_char),
                    lineterminator=actual_end_line,
                    quoting=csv.QUOTE_MINIMAL
                )
                if include_header:
                    writer.writeheader()
                writer.writerows(all_generated_rows)
                
            st.success(f"🎉 Successfully generated {num_rows} rows!")
            st.info(f"📁 Saved file directly to your system at: `data/raw/{output_filename_custom}`")
            
            df_custom = pd.DataFrame(all_generated_rows)
            st.write("### Data Preview")
            st.dataframe(df_custom.head(15), width="stretch")
            
            csv_data_custom = df_custom.to_csv(
                index=False, 
                sep=actual_delimiter, 
                quotechar=quote_char, 
                lineterminator=actual_end_line,
                header=include_header
            ).encode('utf-8')
            
            st.download_button(
                label="📥 Download Generated CSV manually",
                data=csv_data_custom,
                file_name=output_filename_custom,
                mime="text/csv",
            )

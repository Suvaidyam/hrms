import frappe
import csv
from frappe.utils.file_manager import get_file
from frappe.utils.xlsxutils import read_xlsx_file_from_attached_file
import os
from frappe.utils import get_site_path
# from frappe.utils.pdf import merge_pdfs
from frappe.utils.file_manager import save_file
from frappe.utils.pdf import get_pdf


@frappe.whitelist()
def start_import():
    # ✅ Correct way to load document
    doc = frappe.get_doc("Data Entry  -  Batch-wise Semester Scores")

    if not doc.import_file:
        frappe.throw("Please upload a file first (.xlsx or .csv).")

    file_name, file_content = get_file(doc.import_file)

    # Handle Excel or CSV depending on extension
    if file_name.endswith(('.xlsx', '.xlsm')):
        rows = read_xlsx_file_from_attached_file(doc.import_file)
    elif file_name.endswith('.csv'):
        content = file_content.decode('utf-8').splitlines()
        reader = csv.reader(content)
        rows = list(reader)
    else:
        frappe.throw("Unsupported file format. Please upload .xlsx or .csv file.")

    if not rows:
        frappe.throw("The uploaded file is empty or unreadable.")

    headers = [h.strip() for h in rows[0]]
    data_rows = rows[1:]
    inserted_count = 0

    for row in data_rows:
        row_dict = dict(zip(headers, row))
        new_doc = frappe.new_doc("Assessment Score Data")
        new_doc.batch = doc.batch
        new_doc.semester = doc.semester
        new_doc.district = row_dict.get("District")
        new_doc.name1 = row_dict.get("Name")
        new_doc.mobile_number = row_dict.get("Mobile number")
        new_doc.frappe_id = row_dict.get("Frappe ID")
        new_doc.semester_maximum_marks = row_dict.get("Semester Maximum Marks")
        new_doc.semester_obtaind_marks = row_dict.get("Semester Obtained Marks")
        new_doc.semester_ = row_dict.get("Semester %")
        new_doc.semester_gpa =  row_dict.get("Semester GPA")
        new_doc.semester_passfail =row_dict.get("Semester Pass/Fail")
        new_doc.no_of_modules_pass =row_dict.get("No of modules Passed")
        
        
        own_row = {
            "own_field__continue_assessment_70": row_dict.get("Own field - Continue Assessment (70)"),
            "own_field__continue_assessment_pf": row_dict.get("Own field - Continue Assessment (P/F)"),
            "own_field__end_assessment_30": row_dict.get("Own field - End Assessment (30)"),
            "own_field__end_assessment_pf": row_dict.get("Own field - End Assessment (P/F)"),
            "own_field_total_marks": row_dict.get("Own field (Total Marks)"),
            "own_field__continuous__end": row_dict.get("Own field (Continuous + End)"),
            "own_field_final_result": row_dict.get("Own field - Final Result"),
            "own_field_maximum_marks": row_dict.get("Own field Maximum Marks"),
            "own_field_obtained_marks":  row_dict.get("Own field Obtained Marks"),
            "own_field_weighted_marks" : row_dict.get("Own field Weighted Marks"),
            "own_field_total_pf" :  row_dict.get("Own field (Total) (P/F)"),
            "own_field_":row_dict.get("Own field %"),
        }
        
        Lms_row ={
            "lms__continuous_assessment_70": row_dict.get("LMS - Continuous Assessment (70)"),
            "lms__continuous_assessment_pf": row_dict.get("LMS - Continuous Assessment (P/F)"),
            "lms__end_assessment_30": row_dict.get("LMS - End Assessment (30)"),
            "lms__end_assessment_pf": row_dict.get("LMS - End Assessment (P/F)"),
            "lms_total_marks": row_dict.get("LMS (Total Marks)"),
            "lms__continuous__end": row_dict.get("LMS (Continuous + End)"),
            "lms__final_result": row_dict.get("LMS - Final Result"),
            "lms_total_pf" : row_dict.get("LMS (Total) (P/F)"),
            "lms_maximum_marks": row_dict.get("LMS Maximum Marks"),
            "lms_obtained_marks": row_dict.get("LMS Obtained Marks"),
            "lms_weighted_marks" : row_dict.get("LMS Weighted Marks"),
            "lms_":row_dict.get("LMS %"),
        }
        
        Nf_row ={
            "nf__continue_assessment_70": row_dict.get("NF - Continue Assessment (70)"),
            "nf__continue_assessment_pf": row_dict.get("NF - Continue Assessment (P/F)"),
            "nf__end_assessment_30": row_dict.get("NF - End Assessment (30)"),
            "nf__end_assessment_pf": row_dict.get("NF - End Assessment (P/F)"),
            "nf_total_marks": row_dict.get("NF (Total Marks)"),
            "lms__continuous__end": row_dict.get("NF (Continuous + End)"),
            "nf__final_result": row_dict.get("NF - Final Result"),
            "nf_total_pf" : row_dict.get("NF (Total) (P/F)"),
            "nf_maximum_marks": row_dict.get("NF Maximum Marks"),
            "nf_obtained_marks": row_dict.get("NF Obtained marks"),
            "nf_weighted_marks" : row_dict.get("NF Weighted Marks"),
            "nf_":row_dict.get("NF %"),
        }
        
        managing_farms_row = {
            "managing_farms__continue_assessment_70": row_dict.get("Managing Farms - Continue Assessment (70)"),
            "managing_farms__continue_assessment_pf": row_dict.get("Managing Farms - Continue Assessment (P/F)"),
            "managing_farms__end_assessment_30": row_dict.get("Managing Farms - End Assessment (30)"),
            "managing_farms__end_assessment_pf": row_dict.get("Managing Farms - End Assessment (P/F)"),
            "managing_farms_total_marks": row_dict.get("Managing Farms (Total Marks)"),
            "managing_farms_continuous_end": row_dict.get("Managing Farms (Continuous + End)"),
            "managing_farms__final_result": row_dict.get("Managing Farms - Final Result"),
            "managing_farms_total_pf": row_dict.get("Managing Farms (Total) (P/F)"),
            "managing_farms_maximum_marks": row_dict.get("Managing Farms Maximum Marks"),
            "managing_farms_obtained_marks": row_dict.get("Managing Farms Obtained Marks"),
            "managing_farms_weighted_marks": row_dict.get("Managing Farms Weighted Marks"),
            "managing_farms_": row_dict.get("Managing Farms %"),
        }
        
        research_methods_row = {
            "research_methods__continue_assessment_70": row_dict.get("Research Methods - Continue Assessment (70)"),
            "research_methods__continue_assessment_pf": row_dict.get("Research Methods - Continue Assessment (P/F)"),
            "research_methods__end_assessment_30": row_dict.get("Research Methods - End Assessment (30)"),
            "research_methods__end_assessment_pf": row_dict.get("Research Methods - End Assessment (P/F)"),
            "research_methods_total_marks": row_dict.get("Research Methods (Total Marks)"),
            "research_methods_continuous_end": row_dict.get("Research Methods (Continuous + End)"),
            "research_methods__final_result": row_dict.get("Research Methods - Final Result"),
            "research_methods_total_pf": row_dict.get("Research Methods (Total) (P/F)"),
            "research_methods_maximum_marks": row_dict.get("Research Methods Maximum Marks"),
            "research_methods_obtained_marks": row_dict.get("Research Methods Obtained Marks"),
            "research_methods_weighted_marks": row_dict.get("Research Methods Weighted Marks"),
            "research_methods_": row_dict.get("Research Methods %"),
        }

        food_systems_row = {
            "food_systems__continue_assessment_70": row_dict.get("Food Systems - Continue Assessment (70)"),
            "food_systems__continue_assessment_pf": row_dict.get("Food Systems - Continue Assessment (P/F)"),
            "food_systems__end_assessment_30": row_dict.get("Food Systems - End Assessment (30)"),
            "food_systems__end_assessment_pf": row_dict.get("Food Systems - End Assessment (P/F)"),
            "food_systems_total_marks": row_dict.get("Food Systems (Total Marks)"),
            "food_systems_continuous_end": row_dict.get("Food Systems (Continuous + End)"),
            "food_systems_final_result": row_dict.get("Food Systems - Final Result"),
            "food_systems_total_pf": row_dict.get("Food Systems (Total) (P/F)"),
            "food_systems_maximum_marks": row_dict.get("Food Systems Maximum Marks"),
            "food_systems_obtained_marks": row_dict.get("Food Systems Obtained Marks"),
            "food_systems_weighted_marks": row_dict.get("Food Systems Weighted Marks"),
            "food_systems_": row_dict.get("Food Systems %"),
        }
        
        ofe_fields_row = {
            "ofe__continue_assessment_70": row_dict.get("OFE - Continue Assessment (70)"),
            "ofe__continue_assessment_pf": row_dict.get("OFE - Continue Assessment (P/F)"),
            "ofe__end_assessment_30": row_dict.get("OFE - End Assessment (30)"),
            "ofe__end_assessment_pf": row_dict.get("OFE - End Assessment (P/F)"),
            "ofe__total_marks": row_dict.get("OFE (Total Marks)"),
            "ofe_continuous_end": row_dict.get("OFE (Continuous + End)"),
            "ofe_final_result_pf": row_dict.get("OFE - Final Result (P/F)"),
            "ofe_total_pf": row_dict.get("OFE (Total) (P/F)"),
            "ofe_maximum_marks": row_dict.get("OFE Maximum Marks"),
            "ofe_obtained_marks": row_dict.get("OFE Obtained Marks"),
            "ofe_weighted_marks": row_dict.get("OFE Weighted Marks"),
            "ofe_": row_dict.get("OFE %"),
        }
        
        or_fields_row = {
            "or__continue_assessment_70": row_dict.get("OR - Continue Assessment (70)"),
            "or__continue_assessment_pf": row_dict.get("OR - Continue Assessment (P/F)"),
            "or__end_assessment_30": row_dict.get("OR - End Assessment (30)"),
            "or__end_assessment_pf": row_dict.get("OR - End Assessment (P/F)"),
            "or_total_marks": row_dict.get("OR (Total Marks)"),
            "or_continuous_end": row_dict.get("OR (Continuous + End)"),
            "or_final_result_pf": row_dict.get("OR - Final Result (P/F)"),
            "or_total_pf": row_dict.get("OR (Total) (P/F)"),
            "or_maximum_marks": row_dict.get("OR Maximum Marks"),
            "or_obtained_marks": row_dict.get("OR Obtained Marks"),
            "or_weighted_marks": row_dict.get("OR Weighted Marks"),
            "or_": row_dict.get("OR %"),
        }
        ct_fields_row = {
            "ct__continue_assessment_70": row_dict.get("CT - Continue Assessment (70)"),
            "ct__continue_assessment_pf": row_dict.get("CT - Continue Assessment (P/F)"),
            "ct_end_assessment_30": row_dict.get("CT - End Assessment (30)"),
            "ct__end_assessment_pf": row_dict.get("CT - End Assessment (P/F)"),
            "ct__total_marks": row_dict.get("CT (Total Marks)"),
            "ct_continuous_end": row_dict.get("CT (Continuous + End)"),
            "ct_final_result_pf": row_dict.get("CT - Final Result (P/F)"),
            "ct_total_pf": row_dict.get("CT (Total) (P/F)"),
            "ct_maximum_marks": row_dict.get("CT Maximum Marks"),
            "ct_obtained_marks": row_dict.get("CT Obtained Marks"),
            "ct_weighted_marks": row_dict.get("CT Weighted Marks"),
            "ct_": row_dict.get("CT %"),
        }
        
        crv_fields_row = {
            "crv__continue_assessment_70": row_dict.get("CRV - Continue Assessment (70)"),
            "crv__continue_assessment_pf": row_dict.get("CRV - Continue Assessment (P/F)"),
            "crv__end_assessment_30": row_dict.get("CRV - End Assessment (30)"),
            "crv__end_assessment_pf": row_dict.get("CRV - End Assessment (P/F)"),
            "crv_total_marks": row_dict.get("CRV (Total Marks)"),
            "crv_continuous_end": row_dict.get("CRV (Continuous + End)"),
            "crv_final_result_pf": row_dict.get("CRV - Final Result (P/F)"),
            "crv_total_pf": row_dict.get("CRV (Total) (P/F)"),
            "crv_maximum_marks": row_dict.get("CRV Maximum Marks"),
            "crv_obtained_marks": row_dict.get("CRV Obtained Marks"),
            "crv_weighted_marks": row_dict.get("CRV Weighted Marks"),
            "crv_": row_dict.get("CRV %"),
        }
        
        dnf_fields_row = {
            "dnf__continuous_assessment_70": row_dict.get("DNF - Continuous Assessment (70)"),
            "dnf__continuous_assessment_pf": row_dict.get("DNF - Continuous Assessment (P/F)"),
            "dnf__end_assessment_30": row_dict.get("DNF - End Assessment (30)"),
            "dnf__end_assessment_pf": row_dict.get("DNF - End Assessment (P/F)"),
            "dnf_total_marks": row_dict.get("DNF (Total Marks)"),
            "dnf_continuous_end": row_dict.get("DNF (Continuous + End)"),
            "dnf__final_result": row_dict.get("DNF - Final Result"),
            "dnf_total_pf": row_dict.get("DNF (Total) (P/F)"),
            "dnf_maximum_marks": row_dict.get("DNF Maximum Marks"),
            "dnf_obtained_marks": row_dict.get("DNF Obtained Marks"),
            "dnf_weighted_marks": row_dict.get("DNF Weighted Marks"),
            "dnf_": row_dict.get("DNF %"),
        }
        
        rm_fields_row = {
            "rm__continuous_assessment_70": row_dict.get("RM - Continuous Assessment (70)"),
            "rm__continuous_assessment_pf": row_dict.get("RM - Continuous Assessment (P/F)"),
            "rm__end_assessment_30": row_dict.get("RM - End Assessment (30)"),
            "rm__end_assessment_pf": row_dict.get("RM - End Assessment (P/F)"),
            "rm_total_marks": row_dict.get("RM (Total Marks)"),
            "rm_continuous_end": row_dict.get("RM (Continuous + End)"),
            "rm__final_result": row_dict.get("RM - Final Result"),
            "rm_total_pf": row_dict.get("RM (Total) (P/F)"),
            "rm_maximum_marks": row_dict.get("RM Maximum Marks"),
            "rm_obtained_marks": row_dict.get("RM Obtained Marks"),
            "rm_weighted_marks": row_dict.get("RM Weighted Marks"),
            "rm_": row_dict.get("RM %"),
        }
        if has_data(own_row):
            new_doc.append("own_fields", own_row)
        if has_data(Lms_row):
            new_doc.append("lms_fields", Lms_row)
        if has_data(Nf_row):
            new_doc.append("nf_fields", Nf_row)
        if has_data(managing_farms_row):
            new_doc.append("managing_farms", managing_farms_row)
        if has_data(research_methods_row):
            new_doc.append("research_methods", research_methods_row)
        if has_data(food_systems_row):
            new_doc.append("food_systems", food_systems_row)
        if has_data(ofe_fields_row):
            new_doc.append("ofe_fields", ofe_fields_row)
        if has_data(or_fields_row):
            new_doc.append("or_fields", or_fields_row)
        if has_data(ct_fields_row):
            new_doc.append("ct_fields", ct_fields_row)
        if has_data(crv_fields_row):
            new_doc.append("crv_fields", crv_fields_row)
        if has_data(dnf_fields_row):
            new_doc.append("dnf_fields", dnf_fields_row)
        if has_data(rm_fields_row):
            new_doc.append("rm_fields", rm_fields_row)

        new_doc.insert(ignore_permissions=True)
        inserted_count += 1

    frappe.db.commit()
    return f"{inserted_count} records inserted successfully."

def has_data(d):
    """Return True if at least one non-empty value exists."""
    return any(v not in (None, "", " ") for v in d.values())

import frappe
import os
from frappe.utils import get_site_path
from frappe.utils.file_manager import save_file

@frappe.whitelist()
def generate_bulk_score_card(semester=None, batch=None):
    if not semester or not batch:
        frappe.throw("Please provide both semester and batch.")

    frappe.enqueue(
        background_generate_score_cards,
        semester=semester,
        batch=batch,
        queue="long",
        timeout=600,
        job_id=f"Generate Score Cards {semester}-{batch}"
    )
    # return {
    #     "success": True,
    #     "message": "Score card generation started in background. Check after a few minutes."
    # }


@frappe.whitelist()
def background_generate_score_cards(semester=None, batch=None):
    """
    Background job: Generate individual PDF score cards for all Assessment Score Data
    filtered by semester and batch, and attach them to each record.
    """

    frappe.log_error(
        f"Starting bulk score card generation | Semester: {semester}, Batch: {batch}",
        "Bulk Score Card Generation"
    )

    try:
        # 🔹 Validation
        if not semester or not batch:
            frappe.throw("Please provide both semester and batch.")

        # 🔹 1️⃣ Fetch all Assessment Score Data records
        records = frappe.get_all(
            "Assessment Score Data",
            filters={"semester": semester, "batch": batch},
            fields=["name"],
            limit =1
        )

        if not records:
            return {"success": False, "message": "No Assessment Score Data found."}

        uploaded_files = []

        # 🔹 2️⃣ Generate & attach PDF for each record
        for rec in records:
            doc = frappe.get_doc("Assessment Score Data", rec.name)
            frappe.log_error(f"Generating PDF for {doc.name}", "Bulk Score Card Generation")

            # Load Print Format template HTML
            pdf_template = frappe.get_doc("Print Format", "Assessment Score Data").html

            # Render HTML using Jinja
            html_content = frappe.render_template(pdf_template, {"doc": doc})

            # Convert rendered HTML → PDF bytes
            pdf_bytes = get_pdf(html_content)

            # Save PDF temporarily
            filename = f"{doc.name}.pdf"
            filepath = os.path.join(get_site_path("private", "files"), filename)

            with open(filepath, "wb") as f:
                f.write(pdf_bytes)

            # Attach PDF to same document
            uploaded_file = save_file(
                filename,
                open(filepath, "rb").read(),
                "Assessment Score Data",
                doc.name,
                is_private=True
            )

            # Save URL in 'score_card' field (if exists)
            doc.score_card = uploaded_file.file_url
            doc.save(ignore_permissions=True)
            frappe.db.commit()

            uploaded_files.append({
                "docname": doc.name,
                "file_url": uploaded_file.file_url
            })

            frappe.log_error(f"✅ PDF generated & attached for {doc.name}", "Bulk Score Card Generation")

        # 🔹 3️⃣ Done
        frappe.log_error(f"Completed PDF generation for {len(uploaded_files)} records", "Bulk Score Card Generation")

        return {
            "success": True,
            "message": f"Generated and uploaded {len(uploaded_files)} PDFs.",
            "files": uploaded_files
        }

    except Exception:
        frappe.log_error(
            message=frappe.get_traceback(),
            title="Bulk Score Card Generation Error"
        )
        return {
            "success": False,
            "error": "An unexpected error occurred. Check error logs for details."
        }

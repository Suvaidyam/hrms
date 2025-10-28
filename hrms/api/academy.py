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

    # headers = [h.strip() for h in rows[0]]
    headers = [(h or "").strip() for h in rows[0]]
    data_rows = rows[1:]
    inserted_count = 0
    updated_count = 0

    for row in data_rows:
        row_dict = dict(zip(headers, row))
        existing_doc = frappe.db.get_value("Assessment Score Data", {"semester": doc.semester, "batch": doc.batch, "district": row_dict.get("District"), "name1": row_dict.get("Name")},"name")
        if existing_doc:
            new_doc = frappe.get_doc("Assessment Score Data", existing_doc)
            updated_count += 1
        else:
            new_doc = frappe.new_doc("Assessment Score Data")
            inserted_count += 1
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
        new_doc.assessment_year = row_dict.get("Assessment Year")  
        
        
        
        own_row = {
            "own_field__continue_assessment_70": row_dict.get("Own field - Continue Assessment (70)"),
            # "own_field__continue_assessment_pf": row_dict.get("Own field - Continue Assessment (P/F)"),
            "own_field__end_assessment_30": row_dict.get("Own field - End Assessment (30)"),
            # "own_field__end_assessment_pf": row_dict.get("Own field - End Assessment (P/F)"),
            # "own_field_total_marks": row_dict.get("Own field (Total Marks)"),
            # "own_field__continuous__end": row_dict.get("Own field (Continuous + End)"),
            # "own_field_final_result": row_dict.get("Own field - Final Result"),
            # "own_field_maximum_marks": row_dict.get("Own field Maximum Marks"),
            # "own_field_obtained_marks":  row_dict.get("Own field Obtained Marks"),
            # "own_field_weighted_marks" : row_dict.get("Own field Weighted Marks"),
            # "own_field_total_pf" :  row_dict.get("Own field (Total) (P/F)"),
            # "own_field_":row_dict.get("Own field %"),
            "credits":row_dict.get("Own field - Credits"),
            
        }
        
        Lms_row ={
            "lms__continuous_assessment_70": row_dict.get("LMS - Continuous Assessment (70)"),
            # "lms__continuous_assessment_pf": row_dict.get("LMS - Continuous Assessment (P/F)"),
            "lms__end_assessment_30": row_dict.get("LMS - End Assessment (30)"),
            # "lms__end_assessment_pf": row_dict.get("LMS - End Assessment (P/F)"),
            # "lms_total_marks": row_dict.get("LMS (Total Marks)"),
            # "lms__continuous__end": row_dict.get("LMS (Continuous + End)"),
            # "lms__final_result": row_dict.get("LMS - Final Result"),
            # "lms_total_pf" : row_dict.get("LMS (Total) (P/F)"),
            # "lms_maximum_marks": row_dict.get("LMS Maximum Marks"),
            # "lms_obtained_marks": row_dict.get("LMS Obtained Marks"),
            # "lms_weighted_marks" : row_dict.get("LMS Weighted Marks"),
            # "lms_":row_dict.get("LMS %"),
            "credits":row_dict.get("LMS - Credits"),
        }
        
        Nf_row ={
            "nf__continue_assessment_70": row_dict.get("NF - Continue Assessment (70)"),
            # "nf__continue_assessment_pf": row_dict.get("NF - Continue Assessment (P/F)"),
            "nf__end_assessment_30": row_dict.get("NF - End Assessment (30)"),
            # "nf__end_assessment_pf": row_dict.get("NF - End Assessment (P/F)"),
            # "nf_total_marks": row_dict.get("NF (Total Marks)"),
            # "lms__continuous__end": row_dict.get("NF (Continuous + End)"),
            # "nf__final_result": row_dict.get("NF - Final Result"),
            # "nf_total_pf" : row_dict.get("NF (Total) (P/F)"),
            # "nf_maximum_marks": row_dict.get("NF Maximum Marks"),
            # "nf_obtained_marks": row_dict.get("NF Obtained marks"),
            # "nf_weighted_marks" : row_dict.get("NF Weighted Marks"),
            # "nf_":row_dict.get("NF %"),
            "credits":row_dict.get("NF - Credits"),
        }
        
        managing_farms_row = {
            "managing_farms__continue_assessment_70": row_dict.get("Managing Farms - Continue Assessment (70)"),
            # "managing_farms__continue_assessment_pf": row_dict.get("Managing Farms - Continue Assessment (P/F)"),
            "managing_farms__end_assessment_30": row_dict.get("Managing Farms - End Assessment (30)"),
            # "managing_farms__end_assessment_pf": row_dict.get("Managing Farms - End Assessment (P/F)"),
            # "managing_farms_total_marks": row_dict.get("Managing Farms (Total Marks)"),
            # "managing_farms_continuous_end": row_dict.get("Managing Farms (Continuous + End)"),
            # "managing_farms__final_result": row_dict.get("Managing Farms - Final Result"),
            # "managing_farms_total_pf": row_dict.get("Managing Farms (Total) (P/F)"),
            # "managing_farms_maximum_marks": row_dict.get("Managing Farms Maximum Marks"),
            # "managing_farms_obtained_marks": row_dict.get("Managing Farms Obtained Marks"),
            # "managing_farms_weighted_marks": row_dict.get("Managing Farms Weighted Marks"),
            # "managing_farms_": row_dict.get("Managing Farms %"),
            "credits":row_dict.get("Managing Farms - Credits"),
        }
        
        research_methods_row = {                                                                   
            "research_methods__continue_assessment_70": row_dict.get("Research Methods - Continue Assessment (70)"),
            # "research_methods__continue_assessment_pf": row_dict.get("Research Methods - Continue Assessment (P/F)"),
            "research_methods__end_assessment_30": row_dict.get("Research Methods - End Assessment (30)"),
            # "research_methods__end_assessment_pf": row_dict.get("Research Methods - End Assessment (P/F)"),
            # "research_methods_total_marks": row_dict.get("Research Methods (Total Marks)"),
            # "research_methods_continuous_end": row_dict.get("Research Methods (Continuous + End)"),
            # "research_methods__final_result": row_dict.get("Research Methods - Final Result"),
            # "research_methods_total_pf": row_dict.get("Research Methods (Total) (P/F)"),
            # "research_methods_maximum_marks": row_dict.get("Research Methods Maximum Marks"),
            # "research_methods_obtained_marks": row_dict.get("Research Methods Obtained Marks"),
            # "research_methods_weighted_marks": row_dict.get("Research Methods Weighted Marks"),
            # "research_methods_": row_dict.get("Research Methods %"),
            "credits":row_dict.get("Research Methods - Credits"),
            
        }

        food_systems_row = {
            "food_systems__continue_assessment_70": row_dict.get("Food Systems - Continue Assessment (70)"),
            # "food_systems__continue_assessment_pf": row_dict.get("Food Systems - Continue Assessment (P/F)"),
            "food_systems__end_assessment_30": row_dict.get("Food Systems - End Assessment (30)"),
            # "food_systems__end_assessment_pf": row_dict.get("Food Systems - End Assessment (P/F)"),
            # "food_systems_total_marks": row_dict.get("Food Systems (Total Marks)"),
            # "food_systems_continuous_end": row_dict.get("Food Systems (Continuous + End)"),
            # "food_systems_final_result": row_dict.get("Food Systems - Final Result"),
            # "food_systems_total_pf": row_dict.get("Food Systems (Total) (P/F)"),
            # "food_systems_maximum_marks": row_dict.get("Food Systems Maximum Marks"),
            # "food_systems_obtained_marks": row_dict.get("Food Systems Obtained Marks"),
            # "food_systems_weighted_marks": row_dict.get("Food Systems Weighted Marks"),
            # "food_systems_": row_dict.get("Food Systems %"),
            "credits":row_dict.get("Food Systems - Credits"),
            
        }
        
        ofe_fields_row = {
            "ofe__continue_assessment_70": row_dict.get("OFE - Continue Assessment (70)"),
            # "ofe__continue_assessment_pf": row_dict.get("OFE - Continue Assessment (P/F)"),
            "ofe__end_assessment_30": row_dict.get("OFE - End Assessment (30)"),
            # "ofe__end_assessment_pf": row_dict.get("OFE - End Assessment (P/F)"),
            # "ofe__total_marks": row_dict.get("OFE (Total Marks)"),
            # "ofe_continuous_end": row_dict.get("OFE (Continuous + End)"),
            # "ofe_final_result_pf": row_dict.get("OFE - Final Result (P/F)"),
            # "ofe_total_pf": row_dict.get("OFE (Total) (P/F)"),
            # "ofe_maximum_marks": row_dict.get("OFE Maximum Marks"),
            # "ofe_obtained_marks": row_dict.get("OFE Obtained Marks"),
            # "ofe_weighted_marks": row_dict.get("OFE Weighted Marks"),
            # "ofe_": row_dict.get("OFE %"),
            "credits":row_dict.get("OFE - Credits"),
            
        }
        
        or_fields_row = {
            "or__continue_assessment_70": row_dict.get("OR - Continue Assessment (70)"),
            # "or__continue_assessment_pf": row_dict.get("OR - Continue Assessment (P/F)"),
            "or__end_assessment_30": row_dict.get("OR - End Assessment (30)"),
            # "or__end_assessment_pf": row_dict.get("OR - End Assessment (P/F)"),
            # "or_total_marks": row_dict.get("OR (Total Marks)"),
            # "or_continuous_end": row_dict.get("OR (Continuous + End)"),
            # "or_final_result_pf": row_dict.get("OR - Final Result (P/F)"),
            # "or_total_pf": row_dict.get("OR (Total) (P/F)"),
            # "or_maximum_marks": row_dict.get("OR Maximum Marks"),
            # "or_obtained_marks": row_dict.get("OR Obtained Marks"),
            # "or_weighted_marks": row_dict.get("OR Weighted Marks"),
            # "or_": row_dict.get("OR %"),
            "credits":row_dict.get("OR - Credits"),
            
        }
        ct_fields_row = {
            "ct__continue_assessment_70": row_dict.get("CT - Continue Assessment (70)"),
            # "ct__continue_assessment_pf": row_dict.get("CT - Continue Assessment (P/F)"),
            "ct_end_assessment_30": row_dict.get("CT - End Assessment (30)"),
            # "ct__end_assessment_pf": row_dict.get("CT - End Assessment (P/F)"),
            # "ct__total_marks": row_dict.get("CT (Total Marks)"),
            # "ct_continuous_end": row_dict.get("CT (Continuous + End)"),
            # "ct_final_result_pf": row_dict.get("CT - Final Result (P/F)"),
            # "ct_total_pf": row_dict.get("CT (Total) (P/F)"),
            # "ct_maximum_marks": row_dict.get("CT Maximum Marks"),
            # "ct_obtained_marks": row_dict.get("CT Obtained Marks"),
            # "ct_weighted_marks": row_dict.get("CT Weighted Marks"),
            # "ct_": row_dict.get("CT %"),
            "credits":row_dict.get("CT - Credits"),
            
        }
        
        crv_fields_row = {
            "crv__continue_assessment_70": row_dict.get("CRV - Continue Assessment (70)"),
            # "crv__continue_assessment_pf": row_dict.get("CRV - Continue Assessment (P/F)"),
            "crv__end_assessment_30": row_dict.get("CRV - End Assessment (30)"),
            # "crv__end_assessment_pf": row_dict.get("CRV - End Assessment (P/F)"),
            # "crv_total_marks": row_dict.get("CRV (Total Marks)"),
            # "crv_continuous_end": row_dict.get("CRV (Continuous + End)"),
            # "crv_final_result_pf": row_dict.get("CRV - Final Result (P/F)"),
            # "crv_total_pf": row_dict.get("CRV (Total) (P/F)"),
            # "crv_maximum_marks": row_dict.get("CRV Maximum Marks"),
            # "crv_obtained_marks": row_dict.get("CRV Obtained Marks"),
            # "crv_weighted_marks": row_dict.get("CRV Weighted Marks"),
            # "crv_": row_dict.get("CRV %"),
            "credits":row_dict.get("CRV - Credits"),
            
        }
        
        dnf_fields_row = {
            "dnf__continuous_assessment_70": row_dict.get("DNF - Continuous Assessment (70)"),
            # "dnf__continuous_assessment_pf": row_dict.get("DNF - Continuous Assessment (P/F)"),
            "dnf__end_assessment_30": row_dict.get("DNF - End Assessment (30)"),
            # "dnf__end_assessment_pf": row_dict.get("DNF - End Assessment (P/F)"),
            # "dnf_total_marks": row_dict.get("DNF (Total Marks)"),
            # "dnf_continuous_end": row_dict.get("DNF (Continuous + End)"),
            # "dnf__final_result": row_dict.get("DNF - Final Result"),
            # "dnf_total_pf": row_dict.get("DNF (Total) (P/F)"),
            # "dnf_maximum_marks": row_dict.get("DNF Maximum Marks"),
            # "dnf_obtained_marks": row_dict.get("DNF Obtained Marks"),
            # "dnf_weighted_marks": row_dict.get("DNF Weighted Marks"),
            # "dnf_": row_dict.get("DNF %"),
            "credits":row_dict.get("DNF - Credits"),
            
        }
        
        rm_fields_row = {
            "rm__continuous_assessment_70": row_dict.get("RM - Continuous Assessment (70)"),
            # "rm__continuous_assessment_pf": row_dict.get("RM - Continuous Assessment (P/F)"),
            "rm__end_assessment_30": row_dict.get("RM - End Assessment (30)"),
            # "rm__end_assessment_pf": row_dict.get("RM - End Assessment (P/F)"),
            # "rm_total_marks": row_dict.get("RM (Total Marks)"),
            # "rm_continuous_end": row_dict.get("RM (Continuous + End)"),
            # "rm__final_result": row_dict.get("RM - Final Result"),
            # "rm_total_pf": row_dict.get("RM (Total) (P/F)"),
            # "rm_maximum_marks": row_dict.get("RM Maximum Marks"),
            # "rm_obtained_marks": row_dict.get("RM Obtained Marks"),
            # "rm_weighted_marks": row_dict.get("RM Weighted Marks"),
            # "rm_": row_dict.get("RM %"),
            "credits":row_dict.get("RM - Credits"),
            
        }
        # if has_data(own_row):
        #     new_doc.append("own_fields", own_row)
        # if has_data(Lms_row):
        #     new_doc.append("lms_fields", Lms_row)
        # if has_data(Nf_row):
        #     new_doc.append("nf_fields", Nf_row)
        # if has_data(managing_farms_row):
        #     new_doc.append("managing_farms", managing_farms_row)
        # if has_data(research_methods_row):
        #     new_doc.append("research_methods", research_methods_row)
        # if has_data(food_systems_row):
        #     new_doc.append("food_systems", food_systems_row)
        # if has_data(ofe_fields_row):
        #     new_doc.append("ofe_fields", ofe_fields_row)
        # if has_data(or_fields_row):
        #     new_doc.append("or_fields", or_fields_row)
        # if has_data(ct_fields_row):
        #     new_doc.append("ct_fields", ct_fields_row)
        # if has_data(crv_fields_row):
        #     new_doc.append("crv_fields", crv_fields_row)
        # if has_data(dnf_fields_row):
        #     new_doc.append("dnf_fields", dnf_fields_row)
        # if has_data(rm_fields_row):
        #     new_doc.append("rm_fields", rm_fields_row)
        
        # helper function to insert at 0th index
   
        # use helper for all rows
        append_at_top(new_doc, "own_fields", own_row)
        append_at_top(new_doc, "lms_fields", Lms_row)
        append_at_top(new_doc, "nf_fields", Nf_row)
        append_at_top(new_doc, "managing_farms", managing_farms_row)
        append_at_top(new_doc, "research_methods", research_methods_row)
        append_at_top(new_doc, "food_systems", food_systems_row)
        append_at_top(new_doc, "ofe_fields", ofe_fields_row)
        append_at_top(new_doc, "or_fields", or_fields_row)
        append_at_top(new_doc, "ct_fields", ct_fields_row)
        append_at_top(new_doc, "crv_fields", crv_fields_row)
        append_at_top(new_doc, "dnf_fields", dnf_fields_row)
        append_at_top(new_doc, "rm_fields", rm_fields_row)

        
        if existing_doc:
            new_doc.save(ignore_permissions=True)
        else:    
            new_doc.insert(ignore_permissions=True)

    frappe.db.commit()
    return f"{inserted_count} record(s) inserted and {updated_count} record(s) updated successfully."

def has_data(d):
    """Return True if at least one non-empty value exists."""
    return any(v not in (None, "", " ") for v in d.values())
def append_at_top(doc, table_field, data):
    if has_data(data):
        doc.set(table_field, [])
        doc.append(table_field, data)
        getattr(doc, table_field).insert(0, getattr(doc, table_field).pop())





import frappe
import os
import zipfile
from frappe.utils import get_site_path
from frappe.utils.file_manager import save_file
from frappe.utils.pdf import get_pdf


@frappe.whitelist()
def generate_bulk_score_card(semester=None, batch=None, district=None):
    # if not semester or not batch:
    #     frappe.throw("Please provide both semester and batch.")
    # frappe.msgprint(f'Bulk score card generation started in background for {district}.')
    district_name = frappe.db.get_value("District", district, "district_name")
   
    print("me"*100, semester, batch, district,district_name)
    filters = {
        "semester": semester,
        "batch": batch,
        **({"district": district_name} if district_name else {})
    }
    score_data_exists = frappe.db.exists(
        "Assessment Score Data", filters
    )
    
    msg=f"No Assessment Score Data found for the given Semester and Batch."
    if district_name:
        msg=f"No Assessment Score Data found for the given Semester, Batch and District: {district_name}."  
    if not score_data_exists:
        frappe.throw(msg)

    doc = frappe.get_doc({
            "doctype": "Bulk Assessment Score Card",
            "user": frappe.session.user,
            "request_date": frappe.utils.now_datetime(),
            "semester": semester,
            'district': district_name,
            "batch": batch,
            "status": "Pending",
        })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()    

    frappe.enqueue(
        background_generate_score_cards,
        semester=semester,
        batch=batch,
        record_name= doc.name,
        district_name=district_name,
        queue="long",
        timeout=3600,
        job_id=f"Generate Score Cards {semester}-{batch}"
    )
    return {
            "success": True,
            "message": "Bulk score card generation started in background.",
            "record": doc.name,
        }



@frappe.whitelist()
def background_generate_score_cards(record_name, semester=None, batch=None,district_name=None):
    """
    Background job:
    Generate individual PDF score cards for all Assessment Score Data filtered
    by semester and batch, attach them to each record, and create a ZIP file
    attached to a new 'Bulk Assessment Score Card' record.
    """
    import zipfile, os
    from frappe.utils.file_manager import save_file
    from frappe.utils import get_site_path
    from frappe.utils.pdf import get_pdf

    frappe.log_error(f"🚀 Starting bulk score card generation | Semester: {semester}, Batch: {batch}", "Bulk Score Card Generation")

    try:
        if not semester or not batch:
            frappe.throw("Please provide both semester and batch.")

        # 🔹 1️⃣ Fetch Assessment Score Data
        filters = {
            "semester": semester,
            "batch": batch,
            **({"district": district_name} if district_name else {})
        }
        records = frappe.get_all(
            "Assessment Score Data",
            filters=filters,
            fields=["name"],
            # limit=2  # optional for testing
        )

        if not records:
            _update_bulk_record(record_name, "Failed", None)
            return {"success": False, "message": "No Assessment Score Data found."}
        
        _update_bulk_record(record_name, "Processing")

        uploaded_files = []
        pdf_filepaths = []
        total_records = len(records)
        generated_count = 0
        failed_count = 0

        # 🔹 2️⃣ Generate PDFs and track progress
        for rec in records:
            try:
                doc = frappe.get_doc("Assessment Score Data", rec.name)
                frappe.log_error(f"Generating PDF for {doc.name}", "Bulk Score Card Generation")

                pdf_template = frappe.get_doc("Print Format", "Assessment Score Data").html
                html_content = frappe.render_template(pdf_template, {"doc": doc})
                pdf_bytes = get_pdf(html_content)

                filename = f"{doc.name1 or doc.name}.pdf"
                filepath = os.path.join(get_site_path("private", "files"), filename)

                with open(filepath, "wb") as f:
                    f.write(pdf_bytes)

                pdf_filepaths.append(filepath)

                # Save PDF in File Manager
                uploaded_file = save_file(
                    filename,
                    open(filepath, "rb").read(),
                    "Assessment Score Data",
                    doc.name,
                    is_private=True
                )

                doc.score_card = uploaded_file.file_url
                doc.save(ignore_permissions=True)
                frappe.db.commit()

                uploaded_files.append({
                    "docname": doc.name,
                    "file_url": uploaded_file.file_url
                })

                generated_count += 1

            except Exception as e:
                failed_count += 1
                frappe.log_error(f"❌ Failed for {rec.name}: {str(e)}", "PDF Generation Error")

            # 🔹 Update progress after each record
            progress_text = f"{generated_count + failed_count} of {total_records} processed ({generated_count} succeeded, {failed_count} failed)"
            
            frappe.db.set_value("Bulk Assessment Score Card", record_name, "track_records", progress_text)
            frappe.db.commit()

            frappe.publish_realtime(
                event='score_card_progress',
                message={
                    'record_name': record_name,
                    'progress': progress_text,
                    'generated': generated_count,
                    'failed': failed_count,
                    'total': total_records
                },
                user=frappe.session.user
            )

        # 🔹 3️⃣ Create ZIP
        zip_filename = f"ScoreCards_{batch}_{semester}.zip"
        zip_path = os.path.join(get_site_path("private", "files"), zip_filename)

        with zipfile.ZipFile(zip_path, "w") as zipf:
            for filepath in pdf_filepaths:
                zipf.write(filepath, os.path.basename(filepath))

        frappe.log_error(f"📦 ZIP created at {zip_path}", "Bulk Score Card Generation")

        # 🔹 4️⃣ Create Bulk Record and Attach ZIP
        bulk_doc = frappe.get_doc("Bulk Assessment Score Card", record_name)
        
        

        if not os.path.exists(zip_path):
            frappe.throw(f"ZIP file not found at {zip_path}")

        with open(zip_path, "rb") as zf:
            uploaded_zip = save_file(
                zip_filename,
                zf.read(),
                "Bulk Assessment Score Card",
                bulk_doc.name,
                is_private=True
            )

        bulk_doc.bulk_score_card = uploaded_zip.file_url
        bulk_doc.save(ignore_permissions=True)
        frappe.db.commit()

        frappe.log_error(f"✅ ZIP attached to Bulk Assessment Score Card: {bulk_doc.name}", "Bulk Score Card Generation")
        _update_bulk_record(record_name, "Complete", uploaded_zip.file_url)

        frappe.publish_realtime(
            event='score_card_progress',
            message={
                'record_name': record_name,
                'progress': "All completed",
                'generated': generated_count,
                'failed': failed_count,
                'total': total_records
            },
            user=frappe.session.user
        )

        return {
            "success": True,
            "message": f"Generated {generated_count}/{total_records} PDFs. ZIP uploaded successfully.",
            "zip_url": uploaded_zip.file_url,
            "files": uploaded_files
        }

    except Exception:
        frappe.log_error(
            message=frappe.get_traceback(),
            title="Bulk Score Card Generation Error"
        )
        _update_bulk_record(record_name, "Failed", None)
        return {
            "success": False,
            "error": "An unexpected error occurred. Check logs for details."
        }


def _update_bulk_record(record_name, status, file_url=None):
    try:
        if not record_name:
            return

        doc = frappe.get_doc("Bulk Assessment Score Card", record_name)
        doc.status = status
        if file_url:
            doc.bulk_score_card = file_url
        doc.save(ignore_permissions=True)
        frappe.db.commit()

    except Exception as e:
        frappe.log_error(
            f"Failed to update Bulk Assessment Score Card record {record_name}: {str(e)}",
            "Bulk Assessment Score Card Update"
        )

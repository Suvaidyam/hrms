import frappe
import os
import zipfile
from frappe.utils import get_site_path
from frappe.utils.file_manager import save_file
from frappe.utils.pdf import get_pdf

@frappe.whitelist()
def generate_bulk_score_card(semester=None, batch=None):
    if not semester or not batch:
        frappe.throw("Please provide both semester and batch.")

    frappe.enqueue(
        background_generate_score_cards,
        semester=semester,
        batch=batch,
        queue="long",
        timeout=3600,
        job_id=f"Generate Score Cards {semester}-{batch}"
    )
    return {
        "success": True,
        "message": "Score card generation started in background. Check after a few minutes."
    }


@frappe.whitelist()
def background_generate_score_cards(semester=None, batch=None):
    """
    Background job: Generate individual PDF score cards for all Assessment Score Data
    filtered by semester and batch, attach them to each record, and create a ZIP file.
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
            fields=["name"]
        )

        if not records:
            return {"success": False, "message": "No Assessment Score Data found."}

        # 🔹 Setup temp directory
        temp_dir = frappe.get_site_path('private', 'files')
        os.makedirs(temp_dir, exist_ok=True)
        
        # 🔹 Cleanup old files
        for f in os.listdir(temp_dir):
            if f.startswith("Assessment_Score_Card") and (f.endswith(".pdf") or f.endswith(".zip")):
                try:
                    os.remove(os.path.join(temp_dir, f))
                except Exception as e:
                    frappe.log_error(f"Failed to delete old file {f}: {str(e)}", "Score Card Cleanup")

        pdf_files = []
        uploaded_files = []

        # 🔹 2️⃣ Generate & attach PDF for each record
        for rec in records:
            doc = frappe.get_doc("Assessment Score Data", rec.name)
            frappe.log_error(f"Generating PDF for {doc.name}", "Bulk Score Card Generation")

            try:
                # Load Print Format template HTML
                print_format = frappe.get_doc("Print Format", "Assessment Score Data")
                pdf_template = print_format.html
                css = print_format.css or ""

                # Render HTML using Jinja
                html_content = frappe.render_template(pdf_template, {"doc": doc})
                full_html = f"<style>{css}</style>{html_content}"

                # Convert rendered HTML → PDF bytes
                pdf_bytes = get_pdf(full_html)

                # Save PDF temporarily for ZIP
                filename = f"{doc.name}.pdf"
                filepath = os.path.join(temp_dir, filename)

                with open(filepath, "wb") as f:
                    f.write(pdf_bytes)

                pdf_files.append(filepath)

                # ✅ FIX: Use save_file to properly attach as private
                uploaded_file = save_file(
                    filename,
                    pdf_bytes,
                    "Assessment Score Data",
                    doc.name,
                    is_private=1
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

            except Exception as e:
                frappe.log_error(
                    f"Error generating PDF for {doc.name}: {str(e)}", 
                    "Bulk Score Card Generation"
                )

        # 🔹 3️⃣ Create ZIP file from all PDFs
        zip_filename = f"Assessment_Score_Cards_{semester}_{batch}.zip"
        zip_file_path = os.path.join(temp_dir, zip_filename)
        
        with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for pdf_file in pdf_files:
                if os.path.exists(pdf_file):
                    zipf.write(pdf_file, os.path.basename(pdf_file))
                    os.remove(pdf_file)  # cleanup individual PDFs

        # 🔹 4️⃣ Read ZIP file content and attach using save_file
        with open(zip_file_path, 'rb') as f:
            zip_content = f.read()
        
        # ✅ FIX: Use save_file for ZIP to make it private
        file_doc = save_file(
            zip_filename,
            zip_content,
            dt=None,  # Not attached to any doctype
            dn=None,
            is_private=1
        )

        # 🔹 5️⃣ Cleanup ZIP from disk (optional)
        os.remove(zip_file_path)

        frappe.log_error(
            f"Completed PDF generation for {len(uploaded_files)} records. ZIP created: {file_doc.file_url}", 
            "Bulk Score Card Generation"
        )

        return {
            "success": True,
            "message": f"Generated and uploaded {len(uploaded_files)} PDFs and created ZIP file.",
            "files": uploaded_files,
            "zip_file": file_doc.file_url
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
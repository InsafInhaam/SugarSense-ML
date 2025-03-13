from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf(user_id, health_data):
    file_path = f"reports/{user_id}_health_report.pdf"
    c = canvas.Canvas(file_path, pagesize=letter)
    
    c.drawString(100, 750, "Health Report")
    c.drawString(100, 730, f"User ID: {user_id}")
    
    y_position = 710
    for key, value in health_data.items():
        c.drawString(100, y_position, f"{key}: {value}")
        y_position -= 20
        
    c.save()
    return file_path
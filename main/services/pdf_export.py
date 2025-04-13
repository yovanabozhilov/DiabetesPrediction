from reportlab.lib.pagesizes import letter, inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from main.models import UserResult
from django.http import HttpResponse
from .health_advice import get_health_advice  # Import your health advice function
from django.utils import timezone  # Import timezone utilities

def generate_pdf(user):
    # Fetch the user's prediction results
    user_results = UserResult.objects.filter(user=user)

    # Create the PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="diabetes_predictions.pdf"'

    # Create a PDF document
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []  # List to hold document elements

    # Title style for a professional look
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        fontName='Helvetica-Bold',
        fontSize=18,
        alignment=1,
        spaceAfter=12,
        textColor=colors.black
    )
    title = Paragraph("Diabetes Prediction Results", title_style)
    elements.append(title)

    elements.append(Spacer(1, 20))

    # Check if there are any results
    if not user_results:
        elements.append(Paragraph("No predictions available.", styles['BodyText']))
    else:
        for result in user_results:
            # Convert result date to the user's local time
            local_result_date = timezone.localtime(result.result_date)

            # Table headers and structure with proper padding
            data = [
                # Row 1: Headers for Date, Prediction, Accuracy (%)
                ["Date", "Prediction", "Accuracy (%)"],
                
                # Row 2: Actual prediction results
                [local_result_date.strftime("%Y-%m-%d %H:%M"), result.prediction, f"{result.accuracy}%"],
                
                # Row 3: "Inputs" row with one column (this row will have only one column)
                ["", "Inputs", ""],
                
                # Row 4: The input data in one column
                [f"Pregnancies: {result.pregnancies}\nGlucose: {result.glucose}\nBlood Pressure: {result.blood_pressure}\nSkin Thickness: {result.skin_thickness}\nInsulin: {result.insulin}\nBMI: {result.bmi}\nDiabetes Pedigree Function: {result.diabetes_pedigree}\nAge: {result.age}"],
                
                # Row 5: "Health Summary" row with one column
                ["", "Health Summary", ""],
                
                # Row 6: The health advice in one column
                [ "\n".join(get_health_advice([ 
                        result.pregnancies, result.glucose, result.blood_pressure, 
                        result.skin_thickness, result.insulin, result.bmi, 
                        result.diabetes_pedigree, result.age
                    ])) ]
            ]

            # Define Table Style
            table = Table(data, colWidths=[1.5 * inch, 4.5 * inch, 1.5 * inch])  # Adjusted the width of the center column

            # Apply styles to the table, and set the alignment of the second column to center
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.green),  # Title row background color
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Title row text color
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center alignment for all cells
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold font for title row
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),  # Padding for title row
                ('BACKGROUND', (0, 1), (-1, 1), colors.beige),  # Data rows background color
                ('BACKGROUND', (0, 2), (-1, 2), colors.darkgrey),  # Inputs header background color (darker grey)
                ('TEXTCOLOR', (0, 2), (-1, 2), colors.black),  # Inputs header text color (white)
                ('BACKGROUND', (0, 4), (-1, 4), colors.lightgreen),  # Health Summary header background color
                ('TEXTCOLOR', (0, 4), (-1, 4), colors.black),  # Health Summary header text color
                # Removed the grid lines
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),  # Use Helvetica for content rows
                ('FONTSIZE', (0, 0), (-1, -1), 10),  # Font size for content rows
                ('TOPPADDING', (0, 0), (-1, -1), 10),  # Padding for top of cells
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),  # Padding for bottom of cells
                ('LEFTPADDING', (0, 0), (-1, -1), 12),  # Padding for left of cells
                ('RIGHTPADDING', (0, 0), (-1, -1), 12),  # Padding for right of cells
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Align text to the left within cells for better readability
                
                # Center align the second column
                ('ALIGN', (1, 0), (1, -1), 'CENTER'),  # Align the second column to the center
            ]))

            # Add the table to the document
            elements.append(table)

            # Add spacing between sections for clarity (optional)
            elements.append(Spacer(1, 40))

    # Build the PDF
    doc.build(elements)

    return response

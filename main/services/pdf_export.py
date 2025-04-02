from reportlab.lib.pagesizes import letter, inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from main.models import UserResult
from django.http import HttpResponse

def generate_pdf(user):
    # Fetch the user's prediction results
    user_results = UserResult.objects.filter(user=user)

    # Create the PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="diabetes_predictions.pdf"'

    # Create a PDF document
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []  # List to hold document elements

    # Title
    styles = getSampleStyleSheet()
    title = Paragraph("Diabetes Prediction Results", styles['Title'])
    elements.append(title)

    # Check if there are any results
    if not user_results:
        elements.append(Paragraph("No predictions available.", styles['BodyText']))
    else:
        # Table Headers
        data = [["Date", "Prediction", "Accuracy (%)"]]

        # Table Data
        for result in user_results:
            data.append([
                result.result_date.strftime("%Y-%m-%d %H:%M"),
                result.prediction,
                f"{result.accuracy}%"  # Ensure accuracy is formatted properly
            ])

        # Define Table Style
        table = Table(data, colWidths=[2.5 * inch, 3 * inch, 1.5 * inch])  # Set column widths
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.green),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        elements.append(table)

    # Build the PDF
    doc.build(elements)

    return response

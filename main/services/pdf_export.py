from reportlab.lib.pagesizes import letter, inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from main.models import UserResult
from django.http import HttpResponse
from .health_advice import get_health_advice  
from django.utils import timezone  

def generate_pdf(user):
    user_results = UserResult.objects.filter(user=user)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="diabetes_predictions.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []  

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

    if not user_results:
        elements.append(Paragraph("No predictions available.", styles['BodyText']))
    else:
        for result in user_results:
            # Convert result date to the user's local time
            local_result_date = timezone.localtime(result.result_date)

            # Table headers and structure with proper padding
            data = [
                ["Date", "Prediction", "Accuracy (%)"],
                
                [local_result_date.strftime("%Y-%m-%d %H:%M"), result.prediction, f"{result.accuracy}%"],
                
                ["", "Inputs", ""],
                
                [f"Pregnancies: {result.pregnancies}\nGlucose: {result.glucose}\nBlood Pressure: {result.blood_pressure}\nSkin Thickness: {result.skin_thickness}\nInsulin: {result.insulin}\nBMI: {result.bmi}\nDiabetes Pedigree Function: {result.diabetes_pedigree}\nAge: {result.age}"],
                
                ["", "Health Summary", ""],
                
                [ "\n".join(get_health_advice([ 
                        result.pregnancies, result.glucose, result.blood_pressure, 
                        result.skin_thickness, result.insulin, result.bmi, 
                        result.diabetes_pedigree, result.age
                    ])) ]
            ]

            table = Table(data, colWidths=[1.5 * inch, 4.5 * inch, 1.5 * inch])  

            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.green),  
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),  
                ('BACKGROUND', (0, 1), (-1, 1), colors.beige),  
                ('BACKGROUND', (0, 2), (-1, 2), colors.darkgrey), 
                ('TEXTCOLOR', (0, 2), (-1, 2), colors.black), 
                ('BACKGROUND', (0, 4), (-1, 4), colors.lightgreen),  
                ('TEXTCOLOR', (0, 4), (-1, 4), colors.black), 
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'), 
                ('FONTSIZE', (0, 0), (-1, -1), 10),  
                ('TOPPADDING', (0, 0), (-1, -1), 10),  
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),  
                ('LEFTPADDING', (0, 0), (-1, -1), 12),  
                ('RIGHTPADDING', (0, 0), (-1, -1), 12), 
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'), 
                ('ALIGN', (1, 0), (1, -1), 'CENTER'),  
            ]))

            elements.append(table)

            elements.append(Spacer(1, 40))

    doc.build(elements)

    return response

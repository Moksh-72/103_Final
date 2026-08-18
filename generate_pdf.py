import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT

def create_submission_pdf(filename="Module_8_Capstone_Submission.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=40, leftMargin=40,
        topMargin=40, bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0F172A'),
        alignment=TA_LEFT,
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#475569'),
        spaceAfter=12
    )
    
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=12,
        spaceAfter=6
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#2563EB'),
        spaceBefore=6,
        spaceAfter=4
    )
    
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )
    
    link_style = ParagraphStyle(
        'LinkText',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#2563EB'),
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=4
    )

    box_style = ParagraphStyle(
        'BoxText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#1E293B')
    )

    story = []

    # Title & Subtitle
    story.append(Paragraph("Final Capstone Project: Customer Churn Model Deployment", title_style))
    story.append(Paragraph("Module 8 Assignment Submission & Project Overview", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563EB'), spaceAfter=12))

    # Key Information Box Table
    repo_url = "https://github.com/Moksh-72/103_Final.git"
    info_data = [
        [Paragraph("<b>GitHub Repository URL:</b>", body_style), Paragraph(f'<font color="#2563EB"><u><a href="{repo_url}">{repo_url}</a></u></font>', link_style)],
        [Paragraph("<b>Project Folder:</b>", body_style), Paragraph("<code>customer-churn-api/</code>", code_style)],
        [Paragraph("<b>Framework / Server:</b>", body_style), Paragraph("Flask WSGI Server (Python 3.x)", body_style)],
        [Paragraph("<b>Model Architecture:</b>", body_style), Paragraph("Logistic Regression (ROC-AUC: 0.8481, Accuracy: 80.72%)", body_style)],
        [Paragraph("<b>Batch Scoring Input:</b>", body_style), Paragraph("<code>test_data/all_customers.csv</code> (7,043 records)", code_style)],
        [Paragraph("<b>Batch Outputs:</b>", body_style), Paragraph("<code>scored_customers.csv</code> & <code>logs/batch_log.txt</code>", code_style)]
    ]
    info_table = Table(info_data, colWidths=[150, 380])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#E2E8F0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#F1F5F9')),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 10))

    # Executive Summary
    story.append(Paragraph("1. Executive Summary", h1_style))
    story.append(Paragraph(
        "This project completes the end-to-end deployment of a Machine Learning customer churn prediction model. "
        "The model has been packaged into a production-grade HTTP REST API using Flask and integrated into an automated nightly batch "
        "scoring pipeline. All outputs, prediction probabilities, and runtime exceptions are tracked using Python's standard logging framework. "
        "The repository includes a complete maintenance strategy outlining retraining triggers, feature drift detection, and semantic versioning.",
        body_style
    ))

    # Architecture Overview
    story.append(Paragraph("2. System Architecture & Implementation", h1_style))
    
    story.append(Paragraph("A. Real-Time Inference API (app/main.py)", h2_style))
    story.append(Paragraph(
        "The model is hosted as a Flask web application on port <code>8000</code>. It exposes a <code>POST /predict</code> endpoint that accepts customer attribute JSON "
        "payloads, passes them through a pre-fitted <code>ColumnTransformer</code> (<code>transformer.pkl</code>), and computes churn predictions using the trained model "
        "(<code>model.pkl</code>). It returns probability and binary predictions in JSON format:",
        body_style
    ))
    
    sample_json = "<b>Sample Request Payload:</b><br/><code>{\"customer\": {\"gender\": \"Female\", \"SeniorCitizen\": 0, \"Partner\": \"Yes\", \"tenure\": 1, \"MonthlyCharges\": 29.85, \"TotalCharges\": 29.85, ...}}</code><br/><br/>" \
                  "<b>API JSON Response:</b><br/><code>{\"churn_prediction\": \"Yes\", \"churn_probability\": 0.6373}</code>"
    
    box_table = Table([[Paragraph(sample_json, box_style)]], colWidths=[530])
    box_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(box_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("B. Automated Batch Scoring Pipeline (batch.py)", h2_style))
    story.append(Paragraph(
        "The batch scoring pipeline accepts <code>--input test_data/all_customers.csv</code>, sends each customer row as JSON to the API endpoint over HTTP, "
        "and compiles all results into <code>scored_customers.csv</code>. High-throughput multithreading allows scoring all 7,043 customers "
        "in seconds while generating structured logs in <code>logs/batch_log.txt</code>.",
        body_style
    ))

    # Execution & Monitoring Metrics
    story.append(Paragraph("3. Batch Execution & Monitoring Metrics", h1_style))
    
    metrics_data = [
        [Paragraph("<b>Metric Name</b>", h2_style), Paragraph("<b>Execution Result</b>", h2_style)],
        [Paragraph("Total Customer Records Processed", body_style), Paragraph("7,043", body_style)],
        [Paragraph("Successful Predictions", body_style), Paragraph("7,042 (99.986%)", body_style)],
        [Paragraph("Failed Requests / Exceptions", body_style), Paragraph("1 (Tracked in <code>logs/batch_log.txt</code>)", body_style)],
        [Paragraph("Average Churn Probability", body_style), Paragraph("<b>0.2654 (26.54%)</b>", body_style)],
        [Paragraph("Primary Log File Path", body_style), Paragraph("<code>customer-churn-api/logs/batch_log.txt</code>", code_style)]
    ]
    metrics_table = Table(metrics_data, colWidths=[230, 300])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 10))

    # Maintenance Plan Summary
    story.append(Paragraph("4. Model Maintenance Plan Overview", h1_style))
    
    retrain_text = "<b>Retraining Strategy:</b> Models undergo monthly scheduled retraining on fresh 30-day active data. " \
                   "Event-driven retraining is triggered if ROC-AUC drops below 0.75 or accuracy falls below 78%. Automated evaluation gates " \
                   "require candidate models to surpass baseline performance by 1.5% ROC-AUC before blue-green deployment."
    
    drift_text = "<b>Drift Detection:</b> Numerical features (<code>tenure</code>, <code>MonthlyCharges</code>, <code>TotalCharges</code>) are monitored nightly " \
                 "using Population Stability Index (PSI) and KS-tests. PSI > 0.25 flags data drift; rolling 7-day average churn probability shifts > 15% trigger alerts."
    
    version_text = "<b>Versioning & Documentation:</b> Semantic Versioning (<code>vMAJOR.MINOR.PATCH</code>) governs releases. Model artifacts " \
                   "are tracked in MLflow alongside Model Cards detailing dataset checksums, hyperparameters, and ROC-AUC baselines."

    m_table = Table([
        [Paragraph(retrain_text, body_style)],
        [Paragraph(drift_text, body_style)],
        [Paragraph(version_text, body_style)]
    ], colWidths=[530])
    m_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FAF5FF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#E9D5FF')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#F3E8FF')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(m_table)
    story.append(Spacer(1, 10))

    # Submission Repository Structure
    story.append(Paragraph("5. Repository Directory Layout", h1_style))
    repo_tree = "customer-churn-api/\n" \
                "├── app/\n" \
                "│   ├── __init__.py          # Package initializer\n" \
                "│   ├── main.py              # Flask API server (python -m app.main)\n" \
                "│   ├── model.pkl            # Trained Logistic Regression model\n" \
                "│   ├── transformer.pkl      # Scikit-learn ColumnTransformer\n" \
                "│   └── utils.py             # Inference helper functions\n" \
                "├── test_data/\n" \
                "│   ├── sample_input.json    # Test JSON payload for /predict\n" \
                "│   └── all_customers.csv    # Customer dataset for batch scoring\n" \
                "├── logs/\n" \
                "│   └── batch_log.txt        # Detailed execution & monitoring logs\n" \
                "├── batch.py                 # Batch scoring pipeline script\n" \
                "├── requirements.txt         # Python dependency manifest\n" \
                "├── README.md                # Project README & Maintenance Plan\n" \
                "└── .gitignore               # Git ignore directives"
    
    tree_table = Table([[Paragraph(f'<font fontName="Courier" size="8">{repo_tree.replace("\n", "<br/>").replace(" ", "&nbsp;")}</font>', body_style)]], colWidths=[530])
    tree_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#E2E8F0')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(tree_table)

    doc.build(story)
    print(f"PDF successfully created: {filename}")

if __name__ == "__main__":
    create_submission_pdf("Module_8_Capstone_Submission.pdf")
    create_submission_pdf("customer-churn-api/Module_8_Capstone_Submission.pdf")

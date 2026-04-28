import os
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from reportlab.lib import colors
except ImportError:
    pass

def build_report(audit_results, ppnl_output, evidence_hash):
    """Generates a simple PDF report for the DPIA."""
    report_path = "samfair_audit_report.pdf"
    
    try:
        c = canvas.Canvas(report_path, pagesize=letter)
        width, height = letter
        
        c.setFont("Helvetica-Bold", 20)
        c.drawString(50, height - 50, "SamFair Bias Audit Report (DPIA)")
        
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 80, f"Evidence Hash: {evidence_hash}")
        
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 120, "Audit Results (Flagged Groups)")
        
        y = height - 150
        c.setFont("Helvetica", 10)
        flagged = audit_results[audit_results['flagged'] == True]
        if flagged.empty:
            c.drawString(50, y, "No adverse impact detected.")
            y -= 20
        else:
            for _, row in flagged.iterrows():
                c.drawString(50, y, f"Attribute: {row['attribute']} | Group: {row['group']} | Impact Ratio: {row['impact_ratio']}")
                y -= 20
                
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, y - 30, "Post-Prediction Neural Linker (PPNL) Analysis")
        y -= 60
        
        if ppnl_output:
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "Extracted Logic Rule:")
            y -= 20
            c.setFont("Courier", 10)
            c.drawString(70, y, ppnl_output['rule'])
            y -= 30
            
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "Top Feature Contributions:")
            y -= 20
            c.setFont("Helvetica", 10)
            for feat, imp in ppnl_output['feature_contributions'].items():
                c.drawString(70, y, f"- {feat}: {imp}")
                y -= 20
        
        c.save()
        return report_path
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return None

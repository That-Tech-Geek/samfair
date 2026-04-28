import os
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
except ImportError:
    pass

def generate_report(audit_df, ppnl_output, log_entry_hash, filename="samfair_audit_report.pdf"):
    try:
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter
        
        c.setFont("Helvetica-Bold", 18)
        c.drawString(50, height - 50, "SamFair Bias Audit Report (DPDP & AI Bill 2025)")
        
        c.setFont("Helvetica", 10)
        c.drawString(50, height - 70, f"Audit Log Hash: {log_entry_hash}")
        
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 100, "Flagged Intersectional Groups (Ratio < 0.80)")
        
        y = height - 120
        c.setFont("Helvetica", 10)
        flagged = audit_df[audit_df['flagged'] == True]
        
        if flagged.empty:
            c.drawString(50, y, "No adverse impact detected.")
            y -= 20
        else:
            for _, row in flagged.iterrows():
                c.drawString(50, y, f"- {row['attribute']}: {row['group']} (Ratio: {row['impact_ratio']:.2f}, Rate: {row['selection_rate']:.2%})")
                y -= 20
                
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y - 20, "PPNL Plain-English Explanation")
        y -= 45
        
        if ppnl_output:
            c.setFont("Courier", 10)
            c.drawString(70, y, ppnl_output['rule'])
            y -= 30
            c.setFont("Helvetica", 10)
            c.drawString(50, y, f"Surrogate Accuracy: {ppnl_output['surrogate_accuracy']:.1%}")
            
        c.save()
        return filename
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return None

# run this as generate_test_pdf.py
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_fake_statement():
    c = canvas.Canvas("data/uploads/test.pdf", pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 750, "Bank Statement - March 2024")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, 700, "Account Holder: John Doe")
    c.drawString(50, 680, "Account Number: XXXX-XXXX-1234")
    c.drawString(50, 660, "Period: March 1 - March 31, 2024")

    transactions = [
        ("Mar 1",  "Opening Balance",       "",        "5000.00"),
        ("Mar 3",  "Grocery Store",         "120.50",  "4879.50"),
        ("Mar 5",  "Netflix Subscription",  "15.99",   "4863.51"),
        ("Mar 7",  "Salary Credit",         "",        "7363.51"),
        ("Mar 10", "Electricity Bill",      "85.00",   "7278.51"),
        ("Mar 12", "Amazon Purchase",       "230.00",  "7048.51"),
        ("Mar 15", "Restaurant",            "45.00",   "7003.51"),
        ("Mar 18", "Gym Membership",        "50.00",   "6953.51"),
        ("Mar 20", "Uber",                  "22.00",   "6931.51"),
        ("Mar 25", "Rent Payment",          "1500.00", "5431.51"),
        ("Mar 28", "Spotify",               "9.99",    "5421.52"),
        ("Mar 31", "Closing Balance",       "",        "5421.52"),
    ]

    y = 620
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50,  y, "Date")
    c.drawString(150, y, "Description")
    c.drawString(350, y, "Debit")
    c.drawString(450, y, "Balance")
    
    c.setFont("Helvetica", 11)
    for row in transactions:
        y -= 25
        c.drawString(50,  y, row[0])
        c.drawString(150, y, row[1])
        c.drawString(350, y, row[2])
        c.drawString(450, y, row[3])

    c.save()
    print("Test PDF created at data/uploads/test.pdf")

create_fake_statement()
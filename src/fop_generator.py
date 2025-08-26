#!/usr/bin/env python3




def ensure_file(path: Path, content: str) -> Path:
if not path.exists():
if path.suffix.lower() == ".pdf":
path.write_bytes(content.encode("utf-8"))
else:
path.write_text(content, encoding="utf-8")
return path




def build_email(subject: str, body: str, from_addr: str, to_addr: str, attachments: list[Path]) -> EmailMessage:
msg = EmailMessage()
msg["Subject"] = subject
msg["From"] = from_addr
msg["To"] = to_addr
msg.set_content(body)
for p in attachments:
ctype, encoding = mimetypes.guess_type(str(p))
if ctype is None or encoding is not None:
ctype = "application/octet-stream"
maintype, subtype = ctype.split("/", 1)
with open(p, "rb") as f:
msg.add_attachment(f.read(), maintype=maintype, subtype=subtype, filename=p.name)
return msg




def main():
parser = argparse.ArgumentParser(description="UK FOP (Foreign Carrier Permit) generator")
parser.add_argument("--mode", choices=["pdf", "mock"], default="pdf", help="pdf=fill real CPG3200, mock=JSON only")
parser.add_argument("--send", action="store_true", help="Send email via SMTP (env: SMTP_HOST/PORT/USER/PASS)")
parser.add_argument("--attach-template", action="store_true", help="Bundle assets/CPG3200.pdf as attachment if present")


args = parser.parse_args()


# 1) Fill form
if args.mode == "pdf":
filled = fill_cpg3200_pdf(CPG3200_PDF_TEMPLATE, CPG3200_PDF_OUT, TEST_DATA)
else:
filled = fill_cpg3200_mock(CPG3200_JSON_OUT, TEST_DATA)


# 2) Attachments
atts = [
filled,
ensure_file(Path("uk_tco_certificate.pdf"), "Placeholder: UK TCO certificate"),
ensure_file(Path("insurance_certificate.pdf"), "Placeholder: EC 785/2004 insurance"),
ensure_file(Path("flight_schedule.pdf"), "Placeholder: Schedule/itinerary"),
ensure_file(Path("FOP-receipt.pdf"), "Placeholder: FOP receipt"),
]
if args.attach_template and CPG3200_PDF_TEMPLATE.exists():
atts.append(CPG3200_PDF_TEMPLATE)


# 3) Email
subject = "Application: Foreign Registered Aircraft Permit – Ad-hoc (CPG3200)"
body = (
f"Dear CAA Foreign Carrier Permits,\n\n"
f"Please find attached our completed CPG3200 form for {OPERATOR_NAME} (ICAO {ICAO_CALLSIGN}) submitted by {APPLICANT_NAME}. "
f"Our AOC is {AOC_NUMBER}.\n\n"
f"Kind regards,\n{OPERATOR_NAME} – Permits\n"
)
msg = build_email(subject, body, CONTACT_EMAIL, "foreigncarrierpermits@caa.co.uk", atts)


# 4) Send (optional)
if args.send:
import smtplib
host = os.getenv("SMTP_HOST", "smtp.example.com")
port = int(os.getenv("SMTP_PORT", "587"))
user = os.getenv("SMTP_USER")
pwd = os.getenv("SMTP_PASS")
s = smtplib.SMTP(host, port)
s.starttls()
if user and pwd:
s.login(user, pwd)
s.send_message(msg)
s.quit()


# Summary
print(json.dumps({
"mode": args.mode,
"send": args.send,
"attachments": [p.name for p in atts],
"filled": str(filled),
}, indent=2))




if __name__ == "__main__":
sys.exit(main())  

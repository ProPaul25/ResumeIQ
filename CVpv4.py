import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import PyPDF2
import io
import re
import os
from docx import Document

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token
BOT_TOKEN = "7449244249:AAEW-7u-YPWKPDtX8UVX0sKLvYzhB0rZdfM"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "👋 Welcome to the CV Parser Bot!\n\n"
        "Send me a PDF or DOCX CV to parse. I can extract and organize information about:\n"
        "📚 Academic Background\n"
        "💼 Work Experience\n"
        "🏆 Achievements\n"
        "🛠️ Technical Skills\n"
        "📱 Contact Information\n"
        "🎯 Projects\n"
        "🌟 Certifications\n"
        "And more!"
    )
    await update.message.reply_text(welcome_message)

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        file_name = update.message.document.file_name.lower()
        if not (file_name.endswith('.pdf') or file_name.endswith('.docx')):
            await update.message.reply_text("Please send a PDF or DOCX file.")
            return

        await update.message.reply_text("Processing your CV... Please wait.")

        file = await update.message.document.get_file()
        
        if file_name.endswith('.pdf'):
            pdf_data = await file.download_as_bytearray()
            pdf_file = io.BytesIO(pdf_data)
            text = extract_text_from_pdf(pdf_file)
        else:  # DOCX
            docx_data = await file.download_as_bytearray()
            text = extract_text_from_docx(io.BytesIO(docx_data))

        if text:
            formatted_text = format_cv_text(text)
            chunks = [formatted_text[i:i+4096] for i in range(0, len(formatted_text), 4096)]
            for chunk in chunks:
                await update.message.reply_text(chunk, parse_mode='HTML')
        else:
            await update.message.reply_text("Could not extract text from the document.")

    except Exception as e:
        logger.error(f"Error processing document: {e}")
        await update.message.reply_text(f"An error occurred while processing the document: {str(e)}")

def extract_text_from_pdf(pdf_file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(docx_file):
    doc = Document(docx_file)
    return '\n'.join([paragraph.text for paragraph in doc.paragraphs])

def format_cv_text(text):
    """Formats extracted CV text for better readability in Telegram."""
    
    # First, add line breaks around common section indicators
    text = text.replace("Education", "\n\nEducation")
    text = text.replace("EDUCATION", "\n\nEDUCATION")
    text = text.replace("Experience", "\n\nExperience")
    text = text.replace("EXPERIENCE", "\n\nEXPERIENCE")
    text = text.replace("Skills", "\n\nSkills")
    text = text.replace("SKILLS", "\n\nSKILLS")
    text = text.replace("Projects", "\n\nProjects")
    text = text.replace("PROJECTS", "\n\nPROJECTS")
    text = text.replace("Certifications", "\n\nCertifications")
    text = text.replace("CERTIFICATIONS", "\n\nCERTIFICATIONS")
    
    # Remove excessive whitespace but preserve intentional line breaks
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Define section patterns with explicit multiple line breaks
    sections = {
        'personal_info': r'(Personal Information|Contact Details|Contact Information|PERSONAL INFORMATION|CONTACT DETAILS)',
        'education': r'(Education|Academic Background|Academic Qualifications|Educational Qualifications|EDUCATION|ACADEMIC BACKGROUND)',
        'experience': r'(Experience|Work Experience|Professional Experience|Employment History|EXPERIENCE|WORK EXPERIENCE)',
        'skills': r'(Skills|Technical Skills|Core Competencies|Expertise|SKILLS|TECHNICAL SKILLS)',
        'projects': r'(Projects|Academic Projects|Professional Projects|Key Projects|PROJECTS)',
        'extra_curricular': r'(Extra-Curricular Activities|Extra-Curricular Roles|EXTRA-CURRICULAR|EXTRA-CURRICULAR ROLES)',
        'achievements': r'(Achievements|Awards|Honors|Accomplishments|Recognition|ACHIEVEMENTS|AWARDS)',
        'certifications': r'(Certifications|Professional Certifications|Courses|CERTIFICATIONS)',
        'languages': r'(Languages|Language Proficiency|LANGUAGES)',
        'interests': r'(Interests|Hobbies|INTERESTS|HOBBIES)',
        'publications': r'(Publications|Research Papers|Articles|PUBLICATIONS)',
        'references': r'(References|Referees|REFERENCES)'
    }
    
    # Format each section with multiple line breaks
    for section_type, pattern in sections.items():
        text = re.sub(f"({pattern}):?", r'\n\n\n🔸 <b>\1</b>\n\n', text, flags=re.IGNORECASE)
    
    # Enhanced formatting for educational qualifications
    education_patterns = [
        r'(B\.?Tech|Bachelor of Technology|Bachelor of Engineering|B\.?E\.?)',
        r'(M\.?Tech|Master of Technology|Master of Engineering|M\.?E\.?)',
        r'(B\.?Sc|Bachelor of Science)',
        r'(M\.?Sc|Master of Science)',
        r'(Ph\.?D|Doctor of Philosophy)',
        r'(HSC|Higher Secondary|12th)',
        r'(SSC|10th|Matriculation)',
        r'(Diploma)',
    ]
    
    for pattern in education_patterns:
        text = re.sub(f"({pattern}[^\n]+)", r'<b>\1</b>\n', text, flags=re.IGNORECASE)
    
    # Format company/organization names
    text = re.sub(r'(?<=\n)([A-Z][A-Za-z\s&]+)(?=\s*[-–—]\s*|\s*\()', r' <b>\1</b>', text)
    
    # Format projects
    text = re.sub(r'(?i)project[s]?\s*[:]-?\s*([^\n]+)', r'\n🎯 <b>Project: \1</b>\n', text)
    
    # Format achievements
    text = re.sub(r'(?i)(\b(?:won|awarded|achieved|secured|ranked)(?:[^\n.]+))', r'\n🏆 \1', text)
    
    # Format bullet points
    text = re.sub(r'\n[•●○◦⦿⭐]\s*([^\n]+)', r'\n  • \1', text)
    text = re.sub(r'\n(?<=\n)(\d+\.)\s*([^\n]+)', r'\n  \1 \2', text)
    
    # Format contact information
    text = re.sub(r"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})", r'\n📧 <a href="mailto:\1">\1</a>', text)
    text = re.sub(r"(\+\d{1,}\s?)?(\(?\d{3}\)?[\s.-]?)?[\d]{3}[\s.-]?[\d]{4}", r"\n📱 <code>\g<0></code>", text)
    
    # Format social links
    text = re.sub(r'(?:https?://)?(?:www\.)?linkedin\.com/[^\s]+', r'\n🔗 <a href="https://\g<0>">\g<0></a>', text)
    text = re.sub(r'(?:https?://)?(?:www\.)?github\.com/[^\s]+', r'\n💻 <a href="https://\g<0>">\g<0></a>', text)
    
    # Format dates
    text = re.sub(r'\b(19|20)\d{2}\b', r'📅 \g<0>', text)
    
    # Clean up line breaks
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    text = re.sub(r' +', ' ', text)
    
    # Add header
    text = "<b>📄 PARSED CV DETAILS</b>\n\n" + text
    
    # Add footer
    text += "\n\n<i>Note: Some formatting and special characters may have been modified for better readability.</i>"
    
    # Ensure sections are well-separated
    text = re.sub(r'(🔸 <b>[^<]+</b>)', r'\n\n\1\n\n', text)
    
    return text
    
def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    # Start the bot
    print("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
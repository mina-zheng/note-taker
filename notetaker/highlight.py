import fitz  


doc = fitz.open(r"C:\Users\minaz\OneDrive\Desktop\personal\note_taker\media\RESUME_MINA_ZHENG_1.pdf")

# Keyword to search
keyword = "the"

# Loop through each page
for page in doc:
    # Search for all instances of the keyword
    text_instances = page.search_for(keyword)

    # Highlight each instance
    for inst in text_instances:
        page.add_highlight_annot(inst)

# Save the new PDF with highlights
doc.save("highlighted.pdf")
import fitz
import pymupdf
import sys

#pdf = sys.argv[1]

pdf = fitz.open('sample1.pdf')



# out = open("output.txt", "wb") # create a text output
# for page in pdf: # iterate the document pages
#     text = page.get_text().encode("utf8") # get plain text (is in UTF-8)
#     out.write(text) # write text of page
#     out.write(bytes((12,))) # write page delimiter (form feed 0x0C)
#
# out.close()

# open document, extract text into variable
with pymupdf.open(pdf) as doc:  # open document
    text = chr(12).join([page.get_text() for page in doc])

print(text)

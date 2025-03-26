import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


# Function to create a PDF file of the specified size
def create_pdf_file(filename, size_in_bytes):
    #with open(filename, 'w') as file:
        c = canvas.Canvas(filename, pagesize=letter)
        while os.path.getsize(filename) < size_in_bytes:
            c.showPage()
        c.save()


# Function to create a TXT file of the specified size
def create_txt_file(filename, size_in_bytes):
    with open(filename, 'w') as file:
        while os.path.getsize(filename) < size_in_bytes:
            file.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 100)


def create_file_if_not_exists(file_type, size_in_mb):
    size_in_bytes = size_in_mb * 1024 * 1024
    directory = os.path.join(os.getcwd(), "uploadFiles")  # Create a directory named "uploadfiles"
    filename = os.path.join(directory, f"output_{size_in_mb}MB.{file_type}")

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    if not os.path.exists(filename):
        if file_type == "pdf":
            create_pdf_file(filename, size_in_bytes)
        elif file_type == "txt":
            create_txt_file(filename, size_in_bytes)
        else:
            print("Invalid file type. Supported types are 'pdf' and 'txt'.")
    else:
        print(f"{filename} already exists.")


if __name__ == "__main__":
    file_type = input("Enter file type (pdf/txt): ").lower()
    size_in_mb = int(input("Enter file size in MB: "))

    create_file_if_not_exists(file_type, size_in_mb)
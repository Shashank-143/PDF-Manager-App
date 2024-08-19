import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, scrolledtext
import PyPDF2
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os

class PDFManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Manager")

        # Same variables as the original code
        self.pdf_reader = None
        self.num_pages = 0
        self.pdf_file = None

        # Create the GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Create a frame to center align the content
        content_frame = tk.Frame(self.root)
        content_frame.pack(expand=True, fill='both')

        # Open PDF Button
        open_pdf_btn = tk.Button(content_frame, text="Open PDF", command=self.open_pdf_file)
        open_pdf_btn.pack(pady=10)

        # Operations Description
        operations = [
            "1. Print all pages",
            "2. Print specific range of pages",
            "3. Print a specific page",
            "4. Rotate and save a page",
            "5. Merge two PDFs",
            "6. Split PDF",
            "7. Add Watermark",
            "8. Encrypt PDF",
            "9. Decrypt PDF"
        ]

        # Display the operations in a centered label
        for operation in operations:
            lbl = tk.Label(content_frame, text=operation)
            lbl.pack(anchor="center")  # Center align the text in the window

        # Entry for operation selection
        self.operation_entry = tk.Entry(content_frame)
        self.operation_entry.pack(pady=5)

        # Execute Button
        execute_btn = tk.Button(content_frame, text="Execute", command=self.execute_operation)
        execute_btn.pack(pady=10)

        # Exit Button
        exit_btn = tk.Button(content_frame, text="Exit", command=self.root.quit)
        exit_btn.pack(pady=10)

    def open_pdf_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        
        if file_path and os.path.isfile(file_path):
            try:
                self.pdf_file = open(file_path, 'rb')
                self.pdf_reader = PdfReader(self.pdf_file)
                self.num_pages = len(self.pdf_reader.pages)
                messagebox.showinfo("Success", f"PDF loaded successfully. Total pages: {self.num_pages}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open PDF: {str(e)}")
        else:
            messagebox.showwarning("Invalid File", "Please select a valid PDF file.")

    def execute_operation(self):
        try:
            func_no = int(self.operation_entry.get())
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter a valid operation number.")
            return
        
        if self.pdf_reader is None:
            messagebox.showwarning("No PDF Loaded", "Please load a PDF first.")
            return

        # Match the function number with the corresponding operation
        match func_no:
            case 1:
                self.print_all_pages()
            case 2:
                self.print_specific_pages()
            case 3:
                self.print_specific_page()
            case 4:
                self.rotate_page()
            case 5:
                self.merge_pdfs()
            case 6:
                self.split_pdf()
            case 7:
                self.add_watermark()
            case 8:
                self.encrypt_pdf()
            case 9:
                self.decrypt_pdf()
            case _:
                messagebox.showwarning("Invalid Operation", "Please select a valid operation.")

    def print_all_pages(self):
        self.create_output_window("Print All Pages", 
                                  "\n".join(f"Page No: {page_num}\n\n{page.extract_text()}\n\n"
                                            for page_num, page in enumerate(self.pdf_reader.pages, start=1)))

    def print_specific_pages(self):
        start_page = simpledialog.askinteger("Input", "Enter the start page:")
        end_page = simpledialog.askinteger("Input", "Enter the end page:")
        
        if start_page and end_page and 1 <= start_page <= end_page <= self.num_pages:
            content = "\n".join(f"Page No: {page_num}\n\n{self.pdf_reader.pages[page_num - 1].extract_text()}\n\n"
                                for page_num in range(start_page, end_page + 1))
            self.create_output_window("Print Specific Range of Pages", content)
        else:
            messagebox.showerror("Invalid Range", "Please enter a valid page range.")

    def print_specific_page(self):
        page_no = simpledialog.askinteger("Input", "Enter the page number:")
        
        if page_no and 1 <= page_no <= self.num_pages:
            content = f"Page No: {page_no}\n\n{self.pdf_reader.pages[page_no - 1].extract_text()}\n\n"
            self.create_output_window("Print Specific Page", content)
        else:
            messagebox.showerror("Invalid Page", "Please enter a valid page number.")

    def rotate_page(self):
        page_no = simpledialog.askinteger("Input", "Enter the page number:")
        
        if page_no and 1 <= page_no <= self.num_pages:
            self.pdf_reader.pages[page_no - 1].rotate(90)
            pdf_writer = PdfWriter()
            pdf_writer.add_page(self.pdf_reader.pages[page_no - 1])
            with open("Rotated_page.pdf", "wb") as f:
                pdf_writer.write(f)
            messagebox.showinfo("Success", "Page rotated and saved as Rotated_page.pdf")
        else:
            messagebox.showerror("Invalid Page", "Please enter a valid page number.")

    def merge_pdfs(self):
        pdf_merger = PdfMerger()

        second_pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        
        if second_pdf_path and os.path.isfile(second_pdf_path):
            with open(second_pdf_path, 'rb') as pdf_file2:
                pdf_reader2 = PdfReader(pdf_file2)
                pdf_merger.append(self.pdf_reader)
                pdf_merger.append(pdf_reader2)

                with open("Merged_file.pdf", "wb") as output:
                    pdf_merger.write(output)

                messagebox.showinfo("Success", "PDFs merged and saved as Merged_file.pdf")
        else:
            messagebox.showerror("File Error", "Failed to open the second PDF for merging.")

    def split_pdf(self):
        split_page = simpledialog.askinteger("Input", f"Enter the page number to split the PDF (1-{self.num_pages}):")
        
        if split_page and 1 <= split_page < self.num_pages:
            pdf_writer1 = PdfWriter()
            pdf_writer2 = PdfWriter()
            
            for page_num in range(split_page):
                pdf_writer1.add_page(self.pdf_reader.pages[page_num])
            for page_num in range(split_page, self.num_pages):
                pdf_writer2.add_page(self.pdf_reader.pages[page_num])
            
            with open("Split_file1.pdf", "wb") as output1, open("Split_file2.pdf", "wb") as output2:
                pdf_writer1.write(output1)
                pdf_writer2.write(output2)
            
            messagebox.showinfo("Success", "PDF split into Split_file1.pdf and Split_file2.pdf")
        else:
            messagebox.showerror("Invalid Split", "Please enter a valid page number to split the PDF.")

    def add_watermark(self):
        watermark_text = simpledialog.askstring("Input", "Enter watermark text (default: Confidential):") or "Confidential"
        watermark_pdf_path = "watermark_preview.pdf"
        self.create_watermark_pdf(watermark_text, watermark_pdf_path)
        self.apply_watermark_pdf(watermark_pdf_path)
        messagebox.showinfo("Success", "Watermark added and saved as watermarked_output.pdf")

    def create_watermark_pdf(self, watermark_text, watermark_pdf_path):
        c = canvas.Canvas(watermark_pdf_path, pagesize=A4)
        width, height = A4
        font_size = 100
        c.setFont("Helvetica", font_size)
        c.setFillColorRGB(0.6, 0.6, 0.6, alpha= 0.6)
        c.saveState()
        c.translate(width / 2, height / 2)
        c.rotate(45)
        c.drawCentredString(0, 0, watermark_text)
        c.restoreState()
        c.save()

    def apply_watermark_pdf(self, watermark_pdf_path):
        watermark_reader = PdfReader(watermark_pdf_path)
        watermark_page = watermark_reader.pages[0]
        pdf_writer = PdfWriter()

        for page in self.pdf_reader.pages:
            page.merge_page(watermark_page)
            pdf_writer.add_page(page)

        with open("watermarked_output.pdf", "wb") as output_file:
            pdf_writer.write(output_file)

    def encrypt_pdf(self):
        password = simpledialog.askstring("Input", "Enter password to encrypt PDF:")
        
        if password:
            pdf_writer = PdfWriter()
            for page in self.pdf_reader.pages:
                pdf_writer.add_page(page)
            pdf_writer.encrypt(password)
            
            with open("encrypted_pdf.pdf", "wb") as output:
                pdf_writer.write(output)

            messagebox.showinfo("Success", "PDF encrypted and saved as encrypted_pdf.pdf")
        else:
            messagebox.showerror("Password Error", "Please provide a password.")

    def decrypt_pdf(self):
        password = simpledialog.askstring("Input", "Enter password to decrypt PDF:")
        
        if password and self.pdf_reader.is_encrypted:
            self.pdf_reader.decrypt(password)
            pdf_writer = PdfWriter()
            for page in self.pdf_reader.pages:
                pdf_writer.add_page(page)

            with open("decrypted_pdf.pdf", "wb") as output:
                pdf_writer.write(output)

            messagebox.showinfo("Success", "PDF decrypted and saved as decrypted_pdf.pdf")
        else:
            messagebox.showerror("Decryption Error", "Failed to decrypt PDF. Check the password and try again.")

    def create_output_window(self, title, content):
        # Create a new window
        output_window = tk.Toplevel(self.root)
        output_window.title(title)
        
        # Create a scrolled text widget
        text_widget = scrolledtext.ScrolledText(output_window, wrap=tk.WORD, width=80, height=20)
        text_widget.pack(expand=True, fill='both')
        
        # Insert the content into the text widget
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)  # Make the text widget read-only

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFManagerApp(root)
    root.mainloop()

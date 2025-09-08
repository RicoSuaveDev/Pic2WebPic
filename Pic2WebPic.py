import tkinter as tk
from tkinter import messagebox, filedialog
import customtkinter as ctk
from PIL import Image
import os
import sys
import time

# Set appearance mode and default color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Define color scheme
DARK_BG = '#2E2E2E'
DARKER_BG = '#252525'
ACCENT = '#5170ff'
TEXT_COLOR = '#FFFFFF'
BUTTON_BG = '#5A6B7B'  # Blue-gray color
BORDER_COLOR = '#3C4B5B'  # Darker blue-gray for borders

class Pic2WebPic(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Pic2WebPic")
        self.geometry("600x500")
        
        # Initialize variables
        self.output_dir = None
        self.selected_files = []
        
        # New instance variables to track conversion progress
        self.converted_count = 0
        self.error_count = 0
        self.total_files = 0
        
        # Configure the main window
        self.configure(fg_color=DARK_BG)
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self, fg_color=DARK_BG)
        self.main_frame.pack(expand=True, fill='both', padx=30, pady=30)
        
        # Title label
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Convert your images to WebP format",
            text_color=TEXT_COLOR,
            font=('Arial', 18, 'bold')
        )
        self.title_label.pack(pady=(0, 30))
        
        # Frame for output directory display with rounded corners
        self.output_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=DARK_BG,
            border_color=BORDER_COLOR,
            border_width=2,
            corner_radius=15
        )
        self.output_frame.pack(fill='x', pady=(0, 10))
        
        # Output directory label
        self.output_label = ctk.CTkLabel(
            self.output_frame,
            text="Output folder: Not selected",
            text_color=TEXT_COLOR,
            font=('Arial', 10),
            wraplength=400,
            justify='left'
        )
        self.output_label.pack(padx=15, pady=15)
        
        # Output directory selection button
        self.output_button = ctk.CTkButton(
            self.main_frame,
            text="Select Output Folder",
            command=self.select_output_dir,
            fg_color=BUTTON_BG,
            hover_color=BORDER_COLOR,
            height=35,
            width=200
        )
        self.output_button.pack(pady=(10, 20))
        
        # Files container with rounded corners
        self.files_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=DARK_BG,
            border_color=BORDER_COLOR,
            border_width=2,
            corner_radius=15
        )
        self.files_frame.pack(fill='x', pady=(0, 20))
        
        # Selected files label
        self.files_label = ctk.CTkLabel(
            self.files_frame,
            text="No files selected",
            text_color=TEXT_COLOR,
            font=('Arial', 10)
        )
        self.files_label.pack(padx=15, pady=15)
        
        # Buttons frame
        self.buttons_frame = ctk.CTkFrame(self.main_frame, fg_color=DARK_BG)
        self.buttons_frame.pack(pady=20)
        
        # Add button to select files
        self.select_button = ctk.CTkButton(
            self.buttons_frame,
            text="Select Images",
            command=self.select_files,
            fg_color=BUTTON_BG,
            hover_color=BORDER_COLOR,
            height=35,
            width=150
        )
        self.select_button.pack(side='left', padx=10)
        
        # Add convert button
        self.convert_button = ctk.CTkButton(
            self.buttons_frame,
            text="Convert",
            command=self.convert_files,
            fg_color=ACCENT,
            hover_color=BORDER_COLOR,
            height=35,
            width=150,
            state='disabled'
        )
        self.convert_button.pack(side='left', padx=10)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ctk.CTkProgressBar(
            self.main_frame,
            variable=self.progress_var,
            progress_color=ACCENT,
            height=10,
            width=400
        )
        self.progress_bar.pack(pady=(20, 10))
        self.progress_bar.set(0)
        
        # Status label (initially hidden)
        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            text_color=TEXT_COLOR,
            font=('Arial', 10)
        )
        self.status_label.pack(pady=(10, 0))

    def select_output_dir(self):
        dir_path = filedialog.askdirectory(
            title="Select Output Folder"
        )
        if dir_path:
            self.output_dir = dir_path
            # Show truncated path if it's too long
            display_path = dir_path
            if len(dir_path) > 40:
                display_path = "..." + dir_path[-37:]
            self.output_label.configure(text=f"Output folder: {display_path}")

    def select_files(self):
        if not self.output_dir:
            messagebox.showwarning(
                "No Output Folder",
                "Please select an output folder first!"
            )
            return
            
        files = filedialog.askopenfilenames(
            title="Select files to convert",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.gif"),
                ("All files", "*.*")
            ]
        )
        
        if not files:
            return
            
        # Filter valid image files
        self.selected_files = [
            f for f in files
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))
        ]
        
        # Update UI
        if self.selected_files:
            self.convert_button.configure(state='normal')
            self.files_label.configure(
                text=f"{len(self.selected_files)} file{'s' if len(self.selected_files) != 1 else ''} selected"
            )
            self.status_label.configure(text="")
        else:
            self.convert_button.configure(state='disabled')
            self.files_label.configure(text="No valid image files selected")
            self.status_label.configure(text="Please select valid image files")
            
        # Reset progress bar
        self.progress_var.set(0)
        
    def convert_files(self):
        """Initializes the conversion process and starts the first file conversion."""
        if not self.selected_files:
            return
            
        # Reset counters
        self.converted_count = 0
        self.error_count = 0
        self.total_files = len(self.selected_files)
        
        # Reset progress bar
        self.progress_var.set(0)
        
        # Disable buttons during conversion
        self.convert_button.configure(state='disabled')
        self.select_button.configure(state='disabled')
        self.output_button.configure(state='disabled')
        
        # Start the conversion process after a slight delay
        self.status_label.configure(text=f"Converting...")
        self.after(10, self.process_next_file)

    def process_next_file(self):
        """Converts one file and schedules the next, allowing the GUI to update."""
        # Check if all files have been processed
        if self.converted_count + self.error_count >= self.total_files:
            self.convert_complete()
            return
            
        # Get the current file to process
        file_path = self.selected_files[self.converted_count + self.error_count]
        
        try:
            # Open the image and save as WebP
            with Image.open(file_path) as img:
                output_name = os.path.basename(os.path.splitext(file_path)[0]) + '.webp'
                output_path = os.path.join(self.output_dir, output_name)
                img.save(output_path, 'WEBP')
                self.converted_count += 1
                
        except Exception as e:
            self.error_count += 1
            messagebox.showerror(
                "Error",
                f"Error converting {os.path.basename(file_path)}:\n{str(e)}"
            )
        
        # Update the progress bar and status label
        progress = (self.converted_count / self.total_files)
        self.progress_var.set(progress)
        self.status_label.configure(
            text=f"Converting: {self.converted_count}/{self.total_files} completed"
        )
        
        # Schedule the next file to be processed with a slight delay
        self.after(20, self.process_next_file)
        
    def convert_complete(self):
        """Handles finalization after all files are processed."""
        # Re-enable buttons
        self.convert_button.configure(state='normal')
        self.select_button.configure(state='normal')
        self.output_button.configure(state='normal')
        
        # Show final status
        if self.converted_count > 0:
            self.status_label.configure(
                text=f"Converted {self.converted_count} file{'s' if self.converted_count != 1 else ''}" +
                     (f" ({self.error_count} error{'s' if self.error_count != 1 else ''})" if self.error_count > 0 else "")
            )
            messagebox.showinfo(
                "Conversion Complete",
                f"Successfully converted {self.converted_count} file{'s' if self.converted_count != 1 else ''}\n" +
                f"to {self.output_dir}" +
                (f"\n\n{self.error_count} file{'s' if self.error_count != 1 else ''} failed to convert." if self.error_count > 0 else "")
            )
        else:
            self.status_label.configure(text="No files converted")

def main():
    app = Pic2WebPic()
    app.mainloop()

if __name__ == '__main__':
    # Add a check to prevent the code from running as a script within an IDE
    # when being imported for testing or other purposes.
    if getattr(sys, 'frozen', False):
        main()
    else:
        main()

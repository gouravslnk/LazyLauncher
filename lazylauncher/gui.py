"""
GUI Module for LazyLauncher using Tkinter.

This Module contains the main GUI Interface for creating, updating, and deleting Custom KRunner Shortcuts
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional

from .creator import DesktopFileCreator
from .config import Config
from .utils import validate_browser_command

class LazyLauncherGUI:
    """Main GUI Class for LazyLauncher"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("LazyLauncher - Custom KRunner Shortcuts")
        self.root.geometry("650x500")
        self.root.resizable(False, False)

        # Configure style for ttk widgets - only buttons get colors
        self.style = ttk.Style()
        
        # Configure button styles - keep colors only for buttons
        self.style.configure('Create.TButton', 
                           background='#4CAF50', 
                           foreground='white',
                           font=('Arial', 9, 'bold'))
        self.style.map('Create.TButton',
                      background=[('active', '#45a049')])
        
        self.style.configure('Delete.TButton', 
                           background='#f44336', 
                           foreground='white',
                           font=('Arial', 9, 'bold'))
        self.style.map('Delete.TButton',
                      background=[('active', '#da190b')])
        
        self.style.configure('Update.TButton', 
                           background='#2196F3', 
                           foreground='white',
                           font=('Arial', 9, 'bold'))
        self.style.map('Update.TButton',
                      background=[('active', '#1976D2')])
        
        self.style.configure('Secondary.TButton', 
                           background='#6c757d', 
                           foreground='white',
                           font=('Arial', 9))
        self.style.map('Secondary.TButton',
                      background=[('active', '#545b62')])

        self.config = Config()
        self.creator = DesktopFileCreator()

        self.setup_gui()

    def setup_gui(self):
        """Set-Up the GUI Elements"""
        # Main Frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Title 
        title_label = ttk.Label(main_frame, text="LazyLauncher - KRunner Shortcuts Manager", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(0, 10))
        
        # Create tabs
        self.create_tab = ttk.Frame(self.notebook)
        self.manage_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.create_tab, text="Create Shortcut")
        self.notebook.add(self.manage_tab, text="Manage Shortcuts")
        
        # Setup individual tabs
        self.setup_create_tab()
        self.setup_manage_tab()
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

    def setup_create_tab(self):
        """Setup the Create Shortcut tab"""
        create_frame = ttk.Frame(self.create_tab, padding="20")
        create_frame.grid(row=0, column=0, sticky="nsew")
        
        # Shortcut Name
        ttk.Label(create_frame, text="Shortcut Name:").grid(row=0, column=0, sticky="w", pady=5)
        self.name_entry = ttk.Entry(create_frame, width=40)
        self.name_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Description
        ttk.Label(create_frame, text="Description:").grid(row=1, column=0, sticky="w", pady=5)
        self.description_entry = ttk.Entry(create_frame, width=40)
        self.description_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # URL or Path
        ttk.Label(create_frame, text="URL or Path:").grid(row=2, column=0, sticky="w", pady=5)
        self.url_entry = ttk.Entry(create_frame, width=40)
        self.url_entry.grid(row=2, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Browser selection
        ttk.Label(create_frame, text="Browser:").grid(row=3, column=0, sticky="w", pady=5)
        browser_frame = ttk.Frame(create_frame)
        browser_frame.grid(row=3, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        self.browser_var = tk.StringVar(value="default")
        self.default_radio = ttk.Radiobutton(browser_frame, text="Default Browser", 
                                           variable=self.browser_var, value="default")
        self.default_radio.grid(row=0, column=0, sticky="w")
        
        self.custom_radio = ttk.Radiobutton(browser_frame, text="Custom Browser", 
                                          variable=self.browser_var, value="custom")
        self.custom_radio.grid(row=1, column=0, sticky="w")
        
        self.browser_path_entry = ttk.Entry(browser_frame, width=25, state="disabled")
        self.browser_path_entry.grid(row=1, column=1, sticky="ew", padx=(10, 0))
        
        self.browse_button = ttk.Button(browser_frame, text="Browse...", 
                                       command=self.browse_browser, state="disabled")
        self.browse_button.grid(row=1, column=2, padx=(5, 0))
        
        # Bind radio button events
        self.browser_var.trace("w", self.on_browser_selection_change)
        
        # Installation mode
        ttk.Label(create_frame, text="Installation Mode:").grid(row=4, column=0, sticky="w", pady=5)
        mode_frame = ttk.Frame(create_frame)
        mode_frame.grid(row=4, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        self.mode_var = tk.StringVar(value="user")
        ttk.Radiobutton(mode_frame, text="User Mode (~/.local/share/applications)", 
                       variable=self.mode_var, value="user").grid(row=0, column=0, sticky="w")
        ttk.Radiobutton(mode_frame, text="System Mode (/usr/share/applications)", 
                       variable=self.mode_var, value="system").grid(row=1, column=0, sticky="w")
        
        # Buttons
        button_frame = ttk.Frame(create_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(button_frame, text="Create Shortcut", 
                  command=self.create_shortcut, style='Create.TButton').grid(row=0, column=0, padx=(0, 10))
        ttk.Button(button_frame, text="Clear Form", 
                  command=self.clear_form, style='Secondary.TButton').grid(row=0, column=1, padx=(10, 0))
        
        # Configure grid weights
        create_frame.columnconfigure(1, weight=1)
        browser_frame.columnconfigure(1, weight=1)
        self.create_tab.columnconfigure(0, weight=1)
        self.create_tab.rowconfigure(0, weight=1)

    def setup_manage_tab(self):
        """Setup the Manage Shortcuts tab"""
        manage_frame = ttk.Frame(self.manage_tab, padding="20")
        manage_frame.grid(row=0, column=0, sticky="nsew")
        
        # Mode selection for listing
        mode_frame = ttk.Frame(manage_frame)
        mode_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        ttk.Label(mode_frame, text="Mode:").grid(row=0, column=0, sticky="w")
        self.manage_mode_var = tk.StringVar(value="user")
        ttk.Radiobutton(mode_frame, text="User", variable=self.manage_mode_var, 
                       value="user", command=self.refresh_shortcuts).grid(row=0, column=1, padx=(10, 0))
        ttk.Radiobutton(mode_frame, text="System", variable=self.manage_mode_var, 
                       value="system", command=self.refresh_shortcuts).grid(row=0, column=2, padx=(10, 0))
        
        # Search functionality
        search_frame = ttk.Frame(manage_frame)
        search_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        ttk.Label(search_frame, text="Search:").grid(row=0, column=0, sticky="w")
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.on_search_change)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.grid(row=0, column=1, sticky="ew", padx=(10, 0))
        
        # Shortcuts list
        list_frame = ttk.Frame(manage_frame)
        list_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(0, 10))
        
        ttk.Label(list_frame, text="Existing Shortcuts:").grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        # Listbox with scrollbar
        listbox_frame = ttk.Frame(list_frame)
        listbox_frame.grid(row=1, column=0, sticky="nsew")
        
        self.shortcuts_listbox = tk.Listbox(listbox_frame, height=10, width=50)
        scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical", command=self.shortcuts_listbox.yview)
        self.shortcuts_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.shortcuts_listbox.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        listbox_frame.columnconfigure(0, weight=1)
        listbox_frame.rowconfigure(0, weight=1)
        
        # Buttons for manage tab
        manage_button_frame = ttk.Frame(manage_frame)
        manage_button_frame.grid(row=3, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(manage_button_frame, text="Refresh", 
                  command=self.refresh_shortcuts, style='Secondary.TButton').grid(row=0, column=0, padx=(0, 10))
        ttk.Button(manage_button_frame, text="Update Selected", 
                  command=self.update_shortcut, style='Update.TButton').grid(row=0, column=1, padx=(0, 10))
        ttk.Button(manage_button_frame, text="Delete Selected", 
                  command=self.delete_shortcut, style='Delete.TButton').grid(row=0, column=2, padx=(0, 10))
        
        # Configure grid weights
        manage_frame.columnconfigure(0, weight=1)
        manage_frame.rowconfigure(2, weight=1)
        search_frame.columnconfigure(1, weight=1)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(1, weight=1)
        self.manage_tab.columnconfigure(0, weight=1)
        self.manage_tab.rowconfigure(0, weight=1)
        
        # Load shortcuts initially
        self.all_shortcuts = []
        self.refresh_shortcuts()

    def refresh_shortcuts(self):
        """Refresh the shortcuts list"""
        self.shortcuts_listbox.delete(0, tk.END)
        self.all_shortcuts = self.creator.list_shortcuts(self.manage_mode_var.get())
        self.filter_shortcuts()

    def filter_shortcuts(self):
        """Filter shortcuts based on search term"""
        self.shortcuts_listbox.delete(0, tk.END)
        search_term = self.search_var.get().lower()
        
        for shortcut in self.all_shortcuts:
            if search_term == "" or search_term in shortcut.lower():
                self.shortcuts_listbox.insert(tk.END, shortcut)

    def on_search_change(self, *args):
        """Handle search text changes"""
        self.filter_shortcuts()

    def update_shortcut(self):
        """Update the selected shortcut"""
        selection = self.shortcuts_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a shortcut to update.")
            return
        
        shortcut_name = self.shortcuts_listbox.get(selection[0])
        details = self.creator.get_shortcut_details(shortcut_name, self.manage_mode_var.get())
        
        if not details:
            messagebox.showerror("Error", "Could not load shortcut details.")
            return
        
        # Switch to create tab and populate with current values
        self.notebook.select(self.create_tab)
        
        # Clear and populate form
        self.clear_form()
        self.name_entry.insert(0, details.get('name', ''))
        self.description_entry.insert(0, details.get('description', ''))
        self.url_entry.insert(0, details.get('url', ''))
        
        if details.get('browser_command') == 'xdg-open':
            self.browser_var.set('default')
        else:
            self.browser_var.set('custom')
            self.browser_path_entry.delete(0, tk.END)
            self.browser_path_entry.insert(0, details.get('browser_command', ''))
        
        self.mode_var.set(self.manage_mode_var.get())
        
        messagebox.showinfo("Update Mode", 
                           f"Shortcut '{shortcut_name}' loaded for editing.\n\n"
                           "Make your changes and click 'Create Shortcut' to update.")

    def delete_shortcut(self):
        """Delete the selected shortcut"""
        selection = self.shortcuts_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a shortcut to delete.")
            return
        
        shortcut_name = self.shortcuts_listbox.get(selection[0])
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Deletion", 
                              f"Are you sure you want to delete the shortcut '{shortcut_name}'?\n\n"
                              "This action cannot be undone."):
            success = self.creator.remove_shortcut(shortcut_name, self.manage_mode_var.get())
            
            if success:
                messagebox.showinfo("Success", f"Shortcut '{shortcut_name}' deleted successfully!")
                self.refresh_shortcuts()
            else:
                messagebox.showerror("Error", f"Failed to delete shortcut '{shortcut_name}'.")

    def on_browser_selection_change(self, *args):
        """Handle browser selection change."""
        if self.browser_var.get() == "custom":
            self.browser_path_entry.config(state="normal")
            self.browse_button.config(state="normal")
        else:
            self.browser_path_entry.config(state="disabled")
            self.browse_button.config(state="disabled")
    
    def browse_browser(self):
        """Open file dialog to select custom browser."""
        filename = filedialog.askopenfilename(
            title="Select Browser Executable",
            filetypes=[
                ("Executable files", "*.AppImage"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.browser_path_entry.delete(0, tk.END)
            self.browser_path_entry.insert(0, filename)
    
    def create_shortcut(self):
        """Create the desktop shortcut."""
        # Validate inputs
        name = self.name_entry.get().strip()
        description = self.description_entry.get().strip()
        url = self.url_entry.get().strip()
        
        if not name:
            messagebox.showerror("Error", "Shortcut name is required!")
            return
        
        if not url:
            messagebox.showerror("Error", "URL or path is required!")
            return
        
        # Get browser command
        browser_command = "xdg-open"
        if self.browser_var.get() == "custom":
            browser_path = self.browser_path_entry.get().strip()
            if not browser_path:
                messagebox.showerror("Error", "Custom browser path is required!")
                return
            if not validate_browser_command(browser_path):
                messagebox.showerror("Error", "Browser executable not found or not valid!")
                return
            browser_command = browser_path
        
        # Create shortcut
        try:
            success = self.creator.create_shortcut(
                name=name,
                description=description,
                url=url,
                browser_command=browser_command,
                mode=self.mode_var.get()
            )
            
            if success:
                messagebox.showinfo("Success", 
                                  f"Shortcut '{name}' created successfully!\n\n"
                                  f"You can now use 'Alt+SPACE' and type '{name}' to launch it.")
                self.clear_form()
                # Refresh the manage tab if it's the same mode
                if hasattr(self, 'manage_mode_var') and self.manage_mode_var.get() == self.mode_var.get():
                    self.refresh_shortcuts()
            else:
                messagebox.showerror("Error", "Failed to create shortcut!")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def clear_form(self):
        """Clear all form fields."""
        self.name_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.url_entry.delete(0, tk.END)
        self.browser_path_entry.delete(0, tk.END)
        self.browser_var.set("default")
        self.mode_var.set("user")
    
    def run(self):
        """Start the GUI application."""
        self.root.mainloop()


def main():
    """Main entry point for the GUI."""
    app = LazyLauncherGUI()
    app.run()


if __name__ == "__main__":
    main()

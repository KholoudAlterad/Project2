# """GUI entry point for the Mythic Python Project."""

# import base64
# import io
# import re
# import threading
# import tkinter as tk
# from contextlib import redirect_stdout
# from tkinter import messagebox, ttk

# import requests

# from Scraper import scrape_wiki_creatures
# from Serper import serper_search
# from Scenario import scenario_txt2img

# try:  # Pillow is optional but provides better image support
#     from PIL import Image, ImageTk

#     PIL_AVAILABLE = True
# except ModuleNotFoundError:  # pragma: no cover - optional dependency
#     PIL_AVAILABLE = False


# MAX_CREATURE_LIMIT = 50


# def main() -> None:
#     """Launch the Tkinter GUI that replaces the CLI menu."""

#     root = tk.Tk()
#     root.title("Mythic Python Explorer")
#     root.geometry("900x650")
#     root.minsize(760, 520)

#     style = ttk.Style(root)
#     if "clam" in style.theme_names():
#         style.theme_use("clam")

#     limit_var = tk.StringVar(value="5")
#     query_var = tk.StringVar()
#     prompt_var = tk.StringVar()
#     status_var = tk.StringVar(value="Ready")

#     action_buttons: list[ttk.Button] = []

#     def set_running(running: bool) -> None:
#         state = "disabled" if running else "normal"
#         for button in action_buttons:
#             button.configure(state=state)
#         status_var.set("Working..." if running else "Ready")

#     output_frame = ttk.Frame(root, padding=20)
#     output_frame.pack(fill="both", expand=True)

#     heading = ttk.Label(
#         output_frame,
#         text="✨ Mythic Python Project ✨",
#         font=("Segoe UI", 20, "bold"),
#     )
#     heading.pack(pady=(0, 10))

#     controls = ttk.Frame(output_frame)
#     controls.pack(fill="x", pady=(0, 15))

#     creatures_frame = ttk.LabelFrame(controls, text="Legendary Creatures")
#     creatures_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

#     ttk.Label(
#         creatures_frame,
#         text="How many names? (1-50)",
#     ).grid(row=0, column=0, padx=10, pady=10, sticky="w")

#     limit_entry = ttk.Entry(creatures_frame, textvariable=limit_var, width=8)
#     limit_entry.grid(row=0, column=1, padx=(0, 10), pady=10)

#     def build_creature_output(limit: int) -> str:
#         names = scrape_wiki_creatures()
#         if not names:
#             return "❌ No creature names found."

#         bounded_limit = max(1, min(limit, min(len(names), MAX_CREATURE_LIMIT)))
#         lines = [
#             f"✅ Random sample of {bounded_limit} creatures (from {len(names)} total):",
#             "",
#         ]
#         for index, name in enumerate(names[:bounded_limit], start=1):
#             lines.append(f"- {index} · {name}")
#         return "\n".join(lines)

#     def append_output(text: str) -> None:
#         message = text.rstrip() if text.strip() else "✅ Done."
#         output_text.configure(state="normal")
#         output_text.insert("end", message + "\n")
#         output_text.insert("end", "-" * 60 + "\n")
#         output_text.see("end")
#         output_text.configure(state="disabled")

#     image_frame = ttk.LabelFrame(output_frame, text="Image Preview")
#     image_frame.pack(fill="x", pady=(0, 15))

#     image_label = ttk.Label(
#         image_frame,
#         text="No image loaded",
#         anchor="center",
#         width=60,
#         padding=10,
#     )
#     image_label.pack(padx=10, pady=10)

#     displayed_image: dict[str, tk.PhotoImage | "ImageTk.PhotoImage" | None] = {"image": None}

#     def clear_image() -> None:
#         displayed_image["image"] = None
#         image_label.configure(image="", text="No image loaded")

#     def show_image_from_url(url: str) -> None:
#         try:
#             response = requests.get(url, timeout=30)
#             response.raise_for_status()
#         except Exception as exc:  # noqa: BLE001 - present download issues to user
#             messagebox.showerror("Image download failed", f"Could not download image.\n{exc}")
#             return

#         data = response.content

#         if PIL_AVAILABLE:
#             try:
#                 image = Image.open(io.BytesIO(data))
#                 image.thumbnail((600, 600))
#                 photo = ImageTk.PhotoImage(image)
#             except Exception as exc:  # noqa: BLE001 - any PIL issue
#                 messagebox.showerror("Image display failed", f"Could not process image.\n{exc}")
#                 return
#         else:
#             try:
#                 encoded = base64.b64encode(data).decode()
#                 photo = tk.PhotoImage(data=encoded)
#             except tk.TclError as exc:
#                 messagebox.showerror(
#                     "Image display failed",
#                     "Install Pillow (pip install pillow) for broader image support.\n"
#                     f"Underlying error: {exc}",
#                 )
#                 return

#         displayed_image["image"] = photo
#         image_label.configure(image=photo, text="")

#     def extract_urls(text: str) -> list[str]:
#         pattern = r"https?://\S+"
#         return [match.rstrip(".,)") for match in re.findall(pattern, text)]

#     def handle_image_output(text: str) -> None:
#         urls = extract_urls(text)
#         image_url = None
#         for candidate in reversed(urls):
#             if any(candidate.lower().endswith(ext) for ext in (".png", ".jpg", ".jpeg", ".webp")):
#                 image_url = candidate
#                 break
#         if image_url is None and urls:
#             image_url = urls[-1]

#         if image_url:
#             show_image_from_url(image_url)
#         else:
#             messagebox.showinfo("Scenario output", "No image URL detected in the Scenario response.")

#     def on_task_complete(result_text: str, post_process=None) -> None:
#         append_output(result_text)
#         if post_process:
#             post_process(result_text)
#         set_running(False)

#     def run_async(func, *args, capture_stdout: bool = False, post_process=None) -> None:
#         set_running(True)

#         def worker() -> None:
#             try:
#                 if capture_stdout:
#                     buffer = io.StringIO()
#                     with redirect_stdout(buffer):
#                         func(*args)
#                     result = buffer.getvalue()
#                 else:
#                     returned = func(*args)
#                     result = returned if isinstance(returned, str) else ""
#             except Exception as exc:  # noqa: BLE001 - surface all exceptions to the UI
#                 result = f"❌ {type(exc).__name__}: {exc}"
#             finally:
#                 root.after(0, lambda: on_task_complete(result, post_process))

#         threading.Thread(target=worker, daemon=True).start()

#     def fetch_creatures() -> None:
#         raw = limit_var.get().strip()
#         if not raw:
#             limit = 5
#         else:
#             try:
#                 limit = int(raw)
#             except ValueError:
#                 messagebox.showerror("Invalid number", "Please enter a whole number between 1 and 50.")
#                 return
#             if limit < 1:
#                 messagebox.showerror("Invalid number", "Limit must be at least 1.")
#                 return

#         run_async(build_creature_output, limit)

#     summon_button = ttk.Button(creatures_frame, text="Summon Creatures", command=fetch_creatures)
#     summon_button.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")
#     action_buttons.append(summon_button)

#     search_frame = ttk.LabelFrame(controls, text="Serper Web Search")
#     search_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 10))

#     ttk.Label(search_frame, text="Search query").grid(row=0, column=0, padx=10, pady=10, sticky="w")
#     query_entry = ttk.Entry(search_frame, textvariable=query_var, width=35)
#     query_entry.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="ew")

#     def run_search() -> None:
#         query = query_var.get().strip() or "coffee"
#         run_async(serper_search, query, capture_stdout=True)

#     search_button = ttk.Button(search_frame, text="Search", command=run_search)
#     search_button.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")
#     action_buttons.append(search_button)

#     scenario_frame = ttk.LabelFrame(controls, text="Scenario Image Generation")
#     scenario_frame.grid(row=0, column=2, sticky="nsew")

#     ttk.Label(scenario_frame, text="Image prompt").grid(row=0, column=0, padx=10, pady=10, sticky="w")
#     prompt_entry = ttk.Entry(scenario_frame, textvariable=prompt_var, width=35)
#     prompt_entry.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="ew")

#     def run_generation() -> None:
#         prompt = prompt_var.get().strip()
#         if not prompt:
#             messagebox.showerror("Missing prompt", "Please enter a prompt to generate an image.")
#             return
#         clear_image()
#         run_async(scenario_txt2img, prompt, capture_stdout=True, post_process=handle_image_output)

#     generate_button = ttk.Button(scenario_frame, text="Generate Image", command=run_generation)
#     generate_button.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")
#     action_buttons.append(generate_button)

#     for frame in (creatures_frame, search_frame, scenario_frame):
#         frame.columnconfigure(1, weight=1)

#     controls.columnconfigure(0, weight=1)
#     controls.columnconfigure(1, weight=1)
#     controls.columnconfigure(2, weight=1)

#     output_container = ttk.LabelFrame(output_frame, text="Output")
#     output_container.pack(fill="both", expand=True)

#     output_text = tk.Text(output_container, wrap="word", state="disabled", font=("Consolas", 10))
#     output_text.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)

#     scrollbar = ttk.Scrollbar(output_container, orient="vertical", command=output_text.yview)
#     scrollbar.pack(side="right", fill="y", pady=10, padx=(0, 10))
#     output_text.configure(yscrollcommand=scrollbar.set)

#     def clear_output() -> None:
#         output_text.configure(state="normal")
#         output_text.delete("1.0", "end")
#         output_text.configure(state="disabled")
#         clear_image()

#     clear_button = ttk.Button(output_frame, text="Clear Output", command=clear_output)
#     clear_button.pack(pady=(10, 0))

#     status_bar = ttk.Label(root, textvariable=status_var, anchor="w", padding=10)
#     status_bar.pack(fill="x")

#     root.mainloop()


# if __name__ == "__main__":
#     main()



"""
GUI entry point for the Mythic Python Project — Purple & Gold Edition
--------------------------------------------------------------------
Visual-only upgrade requested by user:
- Launch in full-screen (best-effort across platforms)
- Purple (royal) primary + Gold accent theme
- Dismissable image preview (close/X button)
- Refreshed layout: compact header bar, two-row content (controls on top, output below)
- No new app features or behaviors beyond UI polish and image dismiss
"""
from __future__ import annotations

import base64
import io
import re
import threading
import tkinter as tk
from contextlib import redirect_stdout
from tkinter import messagebox, ttk

import requests

from Scraper import scrape_wiki_creatures
from Serper import serper_search
from Scenario import scenario_txt2img

try:  # Pillow is optional but provides better image support
    from PIL import Image, ImageTk

    PIL_AVAILABLE = True
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    PIL_AVAILABLE = False


MAX_CREATURE_LIMIT = 50

# ----------------------- Theming ----------------------- #
PRIMARY = "#6D28D9"      # Royal Purple 700
PRIMARY_DARK = "#5B21B6"  # Purple 800
PRIMARY_LIGHT = "#8B5CF6" # Purple 500
GOLD = "#D4AF37"         # Metallic Gold
GOLD_DARK = "#B5952F"
INK = "#0F172A"          # Slate-900 (text)
INK_MUTED = "#64748B"     # Slate-500
PAPER = "#F8F7FB"        # Soft purple-tinted paper
WHITE = "#FFFFFF"
BORDER = "#E5E7EB"


def _apply_theme(root: tk.Tk) -> ttk.Style:
    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")

    # Global fonts
    base_font = ("Segoe UI", 10)
    title_font = ("Segoe UI", 20, "bold")
    sub_font = ("Segoe UI", 11)

    # Frame backgrounds
    style.configure("TFrame", background=PAPER)
    style.configure("TLabel", background=PAPER, foreground=INK, font=base_font)

    # Header bar
    style.configure("AppBar.TFrame", background=PRIMARY)
    style.configure("AppTitle.TLabel", background=PRIMARY, foreground=WHITE, font=title_font)
    style.configure("AppSub.TLabel", background=PRIMARY, foreground=WHITE, font=sub_font)

    # Cards
    style.configure("Card.TLabelframe", background=WHITE, bordercolor=BORDER, relief="solid")
    style.configure("Card.TLabelframe.Label", background=WHITE, foreground=INK, font=("Segoe UI", 11, "bold"))

    # Buttons
    style.configure(
        "Accent.TButton",
        font=("Segoe UI", 10, "bold"),
        padding=(14, 8),
        background=PRIMARY,
        foreground=WHITE,
        borderwidth=0,
    )
    style.map(
        "Accent.TButton",
        background=[("!disabled", PRIMARY), ("active", PRIMARY_DARK), ("pressed", PRIMARY_DARK)],
        foreground=[("disabled", "#C7C7C7")],
    )

    style.configure(
        "Gold.TButton",
        font=("Segoe UI", 10, "bold"),
        padding=(12, 6),
        background=GOLD,
        foreground=INK,
        borderwidth=0,
    )
    style.map(
        "Gold.TButton",
        background=[("!disabled", GOLD), ("active", GOLD_DARK), ("pressed", GOLD_DARK)],
    )

    # Entries
    style.configure("TEntry", padding=6, fieldbackground=WHITE, bordercolor=BORDER, borderwidth=1)
    style.map("TEntry", bordercolor=[("focus", PRIMARY_LIGHT)])

    # Status bar
    style.configure("Status.TLabel", background=WHITE, foreground=INK_MUTED, padding=10)

    root.option_add("*Font", base_font)
    return style


# ----------------------- App ----------------------- #

def main() -> None:
    """Launch the Tkinter GUI that replaces the CLI menu."""

    root = tk.Tk()
    root.title("Mythic Python Explorer")

    # Try full-screen across platforms
    try:
        # Windows (zoomed)
        root.state("zoomed")
    except Exception:
        pass
    try:
        # X11
        root.attributes("-zoomed", True)
    except Exception:
        pass
    # macOS / general fallback
    root.geometry("1200x760")
    root.minsize(960, 600)

    _apply_theme(root)

    # --- State ---
    limit_var = tk.StringVar(value="5")
    query_var = tk.StringVar()
    prompt_var = tk.StringVar()
    status_var = tk.StringVar(value="Ready")

    action_buttons: list[ttk.Button] = []

    def set_running(running: bool) -> None:
        state = "disabled" if running else "normal"
        for button in action_buttons:
            button.configure(state=state)
        status_var.set("Working..." if running else "Ready")

    # ---------------- Header Bar ---------------- #
    appbar = ttk.Frame(root, style="AppBar.TFrame")
    appbar.pack(fill="x")

    header = ttk.Frame(appbar, style="AppBar.TFrame", padding=(20, 14))
    header.pack(fill="x")

    title = ttk.Label(header, text="✨ Mythic Python Project", style="AppTitle.TLabel")
    title.pack(side="left")

    subtitle = ttk.Label(header, text="Serper • Scraper • Scenario", style="AppSub.TLabel")
    subtitle.pack(side="left", padx=(10, 0))

    # ---------------- Main Body ---------------- #
    outer = ttk.Frame(root, padding=18)
    outer.pack(fill="both", expand=True)

    # Grid: three cards in a row (controls), then output row below
    # Row 0: control cards
    controls = ttk.Frame(outer)
    controls.grid(row=0, column=0, sticky="ew")
    controls.grid_columnconfigure(0, weight=1, uniform="cols")
    controls.grid_columnconfigure(1, weight=1, uniform="cols")
    controls.grid_columnconfigure(2, weight=1, uniform="cols")

    # --- Creatures Card ---
    creatures_frame = ttk.Labelframe(controls, text="Legendary Creatures", style="Card.TLabelframe", padding=12)
    creatures_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

    ttk.Label(creatures_frame, text="How many names? (1-50)").grid(row=0, column=0, padx=(2, 8), pady=(2, 8), sticky="w")
    limit_entry = ttk.Entry(creatures_frame, textvariable=limit_var, width=10)
    limit_entry.grid(row=0, column=1, padx=(0, 2), pady=(2, 8), sticky="ew")

    # --- Search Card ---
    search_frame = ttk.Labelframe(controls, text="Serper Web Search", style="Card.TLabelframe", padding=12)
    search_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 12))

    ttk.Label(search_frame, text="Search query").grid(row=0, column=0, padx=(2, 8), pady=(2, 8), sticky="w")
    query_entry = ttk.Entry(search_frame, textvariable=query_var, width=35)
    query_entry.grid(row=0, column=1, padx=(0, 2), pady=(2, 8), sticky="ew")

    # --- Scenario Card ---
    scenario_frame = ttk.Labelframe(controls, text="Scenario Image Generation", style="Card.TLabelframe", padding=12)
    scenario_frame.grid(row=0, column=2, sticky="nsew")

    ttk.Label(scenario_frame, text="Image prompt").grid(row=0, column=0, padx=(2, 8), pady=(2, 8), sticky="w")
    prompt_entry = ttk.Entry(scenario_frame, textvariable=prompt_var, width=35)
    prompt_entry.grid(row=0, column=1, padx=(0, 2), pady=(2, 8), sticky="ew")

    # ---------------- Output Row ---------------- #
    output_row = ttk.Frame(outer)
    output_row.grid(row=1, column=0, sticky="nsew", pady=(16, 0))
    outer.grid_rowconfigure(1, weight=1)
    output_row.grid_columnconfigure(0, weight=1)
    output_row.grid_columnconfigure(1, weight=1)

    # Left: Output console
    output_container = ttk.Labelframe(output_row, text="Output", style="Card.TLabelframe", padding=10)
    output_container.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

    text_holder = ttk.Frame(output_container)
    text_holder.pack(fill="both", expand=True)

    output_text = tk.Text(
        text_holder,
        wrap="word",
        state="disabled",
        font=("Consolas", 10),
        relief="flat",
        height=14,
        background=WHITE,
        foreground=INK,
        padx=8,
        pady=8,
    )
    output_text.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(text_holder, orient="vertical", command=output_text.yview)
    scrollbar.pack(side="right", fill="y")
    output_text.configure(yscrollcommand=scrollbar.set)

    # Right: Image preview (dismissable)
    image_frame = ttk.Labelframe(output_row, text="Image Preview", style="Card.TLabelframe", padding=10)
    image_frame.grid(row=0, column=1, sticky="nsew")
    image_frame.grid_columnconfigure(0, weight=1)

    # Top bar with dismiss button
    img_top = ttk.Frame(image_frame)
    img_top.grid(row=0, column=0, sticky="ew")
    img_top.grid_columnconfigure(0, weight=1)
    ttk.Label(img_top, text="Preview").grid(row=0, column=0, sticky="w")
    dismiss_btn = ttk.Button(img_top, text="✕ Dismiss", style="Gold.TButton")
    dismiss_btn.grid(row=0, column=1, sticky="e")

    image_label = ttk.Label(image_frame, text="No image loaded", anchor="center")
    image_label.grid(row=1, column=0, sticky="nsew", padx=6, pady=6)
    image_frame.grid_rowconfigure(1, weight=1)

    displayed_image: dict[str, tk.PhotoImage | "ImageTk.PhotoImage" | None] = {"image": None}

    # ---------------- Logic (unchanged behaviors) ---------------- #
    def append_output(text: str) -> None:
        message = text.rstrip() if text.strip() else "✅ Done."
        output_text.configure(state="normal")
        output_text.insert("end", message + "\n")
        output_text.insert("end", "-" * 60 + "\n")
        output_text.see("end")
        output_text.configure(state="disabled")

    def clear_image() -> None:
        displayed_image["image"] = None
        image_label.configure(image="", text="No image loaded")

    dismiss_btn.configure(command=clear_image)

    def show_image_from_url(url: str) -> None:
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
        except Exception as exc:  # noqa: BLE001 - present download issues to user
            messagebox.showerror("Image download failed", f"Could not download image.\n{exc}")
            return

        data = response.content

        if PIL_AVAILABLE:
            try:
                image = Image.open(io.BytesIO(data))
                image.thumbnail((900, 900))
                photo = ImageTk.PhotoImage(image)
            except Exception as exc:  # noqa: BLE001 - any PIL issue
                messagebox.showerror("Image display failed", f"Could not process image.\n{exc}")
                return
        else:
            try:
                encoded = base64.b64encode(data).decode()
                photo = tk.PhotoImage(data=encoded)
            except tk.TclError as exc:
                messagebox.showerror(
                    "Image display failed",
                    "Install Pillow (pip install pillow) for broader image support.\n"
                    f"Underlying error: {exc}",
                )
                return

        displayed_image["image"] = photo
        image_label.configure(image=photo, text="")

    def extract_urls(text: str) -> list[str]:
        pattern = r"https?://\S+"
        return [match.rstrip(".,)") for match in re.findall(pattern, text)]

    def handle_image_output(text: str) -> None:
        urls = extract_urls(text)
        image_url = None
        for candidate in reversed(urls):
            if any(candidate.lower().endswith(ext) for ext in (".png", ".jpg", ".jpeg", ".webp")):
                image_url = candidate
                break
        if image_url is None and urls:
            image_url = urls[-1]

        if image_url:
            show_image_from_url(image_url)
        else:
            messagebox.showinfo("Scenario output", "No image URL detected in the Scenario response.")

    def on_task_complete(result_text: str, post_process=None) -> None:
        append_output(result_text)
        if post_process:
            post_process(result_text)
        set_running(False)

    def run_async(func, *args, capture_stdout: bool = False, post_process=None) -> None:
        set_running(True)

        def worker() -> None:
            try:
                if capture_stdout:
                    buffer = io.StringIO()
                    with redirect_stdout(buffer):
                        func(*args)
                    result = buffer.getvalue()
                else:
                    returned = func(*args)
                    result = returned if isinstance(returned, str) else ""
            except Exception as exc:  # noqa: BLE001 - surface all exceptions to the UI
                result = f"❌ {type(exc).__name__}: {exc}"
            finally:
                root.after(0, lambda: on_task_complete(result, post_process))

        threading.Thread(target=worker, daemon=True).start()

    def build_creature_output(limit: int) -> str:
        names = scrape_wiki_creatures()
        if not names:
            return "❌ No creature names found."

        bounded_limit = max(1, min(limit, min(len(names), MAX_CREATURE_LIMIT)))
        lines = [
            f"✅ Random sample of {bounded_limit} creatures (from {len(names)} total):",
            "",
        ]
        for index, name in enumerate(names[:bounded_limit], start=1):
            lines.append(f"- {index} · {name}")
        return "\n".join(lines)

    def fetch_creatures() -> None:
        raw = limit_var.get().strip()
        if not raw:
            limit = 5
        else:
            try:
                limit = int(raw)
            except ValueError:
                messagebox.showerror("Invalid number", "Please enter a whole number between 1 and 50.")
                return
            if limit < 1:
                messagebox.showerror("Invalid number", "Limit must be at least 1.")
                return

        run_async(build_creature_output, limit)

    summon_button = ttk.Button(creatures_frame, text="Summon Creatures", style="Accent.TButton", command=fetch_creatures)
    summon_button.grid(row=1, column=0, columnspan=2, padx=2, pady=(6, 2), sticky="ew")
    action_buttons.append(summon_button)

    def run_search() -> None:
        query = query_var.get().strip() or "coffee"
        run_async(serper_search, query, capture_stdout=True)

    search_button = ttk.Button(search_frame, text="Search", style="Accent.TButton", command=run_search)
    search_button.grid(row=1, column=0, columnspan=2, padx=2, pady=(6, 2), sticky="ew")
    action_buttons.append(search_button)

    def run_generation() -> None:
        prompt = prompt_var.get().strip()
        if not prompt:
            messagebox.showerror("Missing prompt", "Please enter a prompt to generate an image.")
            return
        clear_image()
        run_async(scenario_txt2img, prompt, capture_stdout=True, post_process=handle_image_output)

    generate_button = ttk.Button(scenario_frame, text="Generate Image", style="Accent.TButton", command=run_generation)
    generate_button.grid(row=1, column=0, columnspan=2, padx=2, pady=(6, 2), sticky="ew")
    action_buttons.append(generate_button)

    # Clear output button below rows
    def clear_output() -> None:
        output_text.configure(state="normal")
        output_text.delete("1.0", "end")
        output_text.configure(state="disabled")
        clear_image()

    clear_button = ttk.Button(outer, text="Clear Output", style="Gold.TButton", command=clear_output)
    clear_button.grid(row=2, column=0, sticky="e", pady=(12, 0))
    action_buttons.append(clear_button)

    # Status bar
    status_bar = ttk.Label(root, textvariable=status_var, anchor="w", style="Status.TLabel")
    status_bar.pack(fill="x", side="bottom")

    root.mainloop()


if __name__ == "__main__":
    main()

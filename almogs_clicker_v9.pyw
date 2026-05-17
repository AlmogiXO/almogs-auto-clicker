"""
Almog's Clicker  v9.0  –  Python 3.13
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Save as .pyw → zero console window, ever.
• Always-On-Top toggle in titlebar  (📌)
• Gaming / eSports UI
• 18 built-in presets  •  Custom HSV/RGB color picker
• Custom rebindable hotkey  •  Glass mode
Dependencies: pip install pynput
"""

import colorsys, json, math, os, subprocess, sys
import threading, time
import tkinter as tk
from tkinter import ttk, messagebox
from pynput.mouse import Button, Controller
from pynput import keyboard as kb

# ── suppress console window on Windows ─────────────────
if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.user32.ShowWindow(
            ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except Exception:
        pass

# ═══════════════════════════════════════════════════════
#  PATHS
# ═══════════════════════════════════════════════════════
_DATA_DIR   = os.path.join(os.path.expanduser("~"), "Documents", "Almog's Clicker")
os.makedirs(_DATA_DIR, exist_ok=True)
THEMES_FILE = os.path.join(_DATA_DIR, "themes.json")
STATS_FILE  = os.path.join(_DATA_DIR, "stats.json")
PREFS_FILE  = os.path.join(_DATA_DIR, "prefs.json")

def open_data_folder():
    if sys.platform == "win32":    os.startfile(_DATA_DIR)
    elif sys.platform == "darwin": subprocess.Popen(["open", _DATA_DIR])
    else:                          subprocess.Popen(["xdg-open", _DATA_DIR])

# ═══════════════════════════════════════════════════════
#  COLOR PALETTE
# ═══════════════════════════════════════════════════════
DEFAULT_KEYS = [
    "bg","panel","accent","highlight",
    "text","muted","header_fg","btn_fg",
    "entry_fg","stat_num","stat_lbl","logo",
]
COLOR_LABELS = {
    "bg":"Background","panel":"Panel / Header","accent":"Accent / Fields",
    "highlight":"Highlight / Buttons","text":"Text","muted":"Muted Labels",
    "header_fg":"Header Title","btn_fg":"Button Text",
    "entry_fg":"Entry Text","stat_num":"Stat Numbers",
    "stat_lbl":"Stat Labels","logo":"Logo Color",
}

PRESETS: dict = {
    "Almog Red":{
        "bg":"#0a0a0a","panel":"#141414","accent":"#2a0000",
        "highlight":"#cc0000","text":"#f5f5f5","muted":"#666666",
        "header_fg":"#ff4444","btn_fg":"#ffffff",
        "entry_fg":"#f5f5f5","stat_num":"#ff4444","stat_lbl":"#666666","logo":"#cc0000",
    },
    "Dark Plum":{
        "bg":"#1a0a2e","panel":"#2a1040","accent":"#4a2070",
        "highlight":"#c084fc","text":"#f3e8ff","muted":"#9d7ab8",
        "header_fg":"#e8d5ff","btn_fg":"#ffffff",
        "entry_fg":"#f3e8ff","stat_num":"#c084fc","stat_lbl":"#9d7ab8","logo":"#c084fc",
    },
    "Dark Navy":{
        "bg":"#1a1a2e","panel":"#16213e","accent":"#0f3460",
        "highlight":"#e94560","text":"#eaeaea","muted":"#8892a4",
        "header_fg":"#ffffff","btn_fg":"#ffffff",
        "entry_fg":"#eaeaea","stat_num":"#e94560","stat_lbl":"#8892a4","logo":"#e94560",
    },
    "Cyberpunk":{
        "bg":"#0d0d0d","panel":"#1a0033","accent":"#2d0060",
        "highlight":"#ff00cc","text":"#f0e6ff","muted":"#9966cc",
        "header_fg":"#ff88ee","btn_fg":"#ffffff",
        "entry_fg":"#f0e6ff","stat_num":"#ff00cc","stat_lbl":"#9966cc","logo":"#ff00cc",
    },
    "Midnight Green":{
        "bg":"#0d1f1a","panel":"#122b24","accent":"#1a4a3a",
        "highlight":"#39d98a","text":"#e0f5ec","muted":"#6aaf8a",
        "header_fg":"#b7f5d8","btn_fg":"#0d1f1a",
        "entry_fg":"#e0f5ec","stat_num":"#39d98a","stat_lbl":"#6aaf8a","logo":"#39d98a",
    },
    "Arctic Blue":{
        "bg":"#0a1628","panel":"#0f2040","accent":"#1a3a6e",
        "highlight":"#4fc3f7","text":"#e8f4fd","muted":"#7ab3d4",
        "header_fg":"#b3e5fc","btn_fg":"#0a1628",
        "entry_fg":"#e8f4fd","stat_num":"#4fc3f7","stat_lbl":"#7ab3d4","logo":"#4fc3f7",
    },
    "Dracula":{
        "bg":"#282a36","panel":"#1e2029","accent":"#44475a",
        "highlight":"#ff79c6","text":"#f8f8f2","muted":"#6272a4",
        "header_fg":"#f8f8f2","btn_fg":"#282a36",
        "entry_fg":"#f8f8f2","stat_num":"#ff79c6","stat_lbl":"#6272a4","logo":"#ff79c6",
    },
    "Monochrome":{
        "bg":"#111111","panel":"#1e1e1e","accent":"#333333",
        "highlight":"#ffffff","text":"#dddddd","muted":"#777777",
        "header_fg":"#ffffff","btn_fg":"#111111",
        "entry_fg":"#dddddd","stat_num":"#ffffff","stat_lbl":"#777777","logo":"#ffffff",
    },
    "Blood Orange":{
        "bg":"#0f0800","panel":"#1c1000","accent":"#3d2000",
        "highlight":"#ff6600","text":"#fff3e0","muted":"#886644",
        "header_fg":"#ffaa55","btn_fg":"#0f0800",
        "entry_fg":"#fff3e0","stat_num":"#ff6600","stat_lbl":"#886644","logo":"#ff6600",
    },
    "Neon Tokyo":{
        "bg":"#04001a","panel":"#0a0030","accent":"#1a0050",
        "highlight":"#00ffff","text":"#e0ffff","muted":"#4488aa",
        "header_fg":"#00ffff","btn_fg":"#04001a",
        "entry_fg":"#e0ffff","stat_num":"#00ffff","stat_lbl":"#4488aa","logo":"#00ffff",
    },
    "Rust & Ash":{
        "bg":"#1a1210","panel":"#251a16","accent":"#3d2820",
        "highlight":"#c0603a","text":"#e8ddd8","muted":"#7a6055",
        "header_fg":"#d4907a","btn_fg":"#1a1210",
        "entry_fg":"#e8ddd8","stat_num":"#c0603a","stat_lbl":"#7a6055","logo":"#c0603a",
    },
    "Forest Hacker":{
        "bg":"#001200","panel":"#001a00","accent":"#003300",
        "highlight":"#00ff41","text":"#ccffcc","muted":"#336633",
        "header_fg":"#00ff41","btn_fg":"#001200",
        "entry_fg":"#ccffcc","stat_num":"#00ff41","stat_lbl":"#336633","logo":"#00ff41",
    },
    "Rose Gold":{
        "bg":"#1a0e0e","panel":"#271515","accent":"#3d2020",
        "highlight":"#e8a0a0","text":"#ffeaea","muted":"#886666",
        "header_fg":"#f5c0c0","btn_fg":"#1a0e0e",
        "entry_fg":"#ffeaea","stat_num":"#e8a0a0","stat_lbl":"#886666","logo":"#e8a0a0",
    },
    "Void Purple":{
        "bg":"#050008","panel":"#0d000f","accent":"#200020",
        "highlight":"#9b30ff","text":"#eedeff","muted":"#5a3a7a",
        "header_fg":"#c880ff","btn_fg":"#050008",
        "entry_fg":"#eedeff","stat_num":"#9b30ff","stat_lbl":"#5a3a7a","logo":"#9b30ff",
    },
    "Ice Storm":{
        "bg":"#f0f4f8","panel":"#e2eaf0","accent":"#c8d8e8",
        "highlight":"#2266cc","text":"#111828","muted":"#6688aa",
        "header_fg":"#1144aa","btn_fg":"#ffffff",
        "entry_fg":"#111828","stat_num":"#2266cc","stat_lbl":"#6688aa","logo":"#2266cc",
    },
    "Sunset Vibe":{
        "bg":"#0d0510","panel":"#180a20","accent":"#2a1040",
        "highlight":"#ff6b6b","text":"#ffe8f0","muted":"#884466",
        "header_fg":"#ffaa88","btn_fg":"#0d0510",
        "entry_fg":"#ffe8f0","stat_num":"#ff6b6b","stat_lbl":"#884466","logo":"#ff6b6b",
    },
    "Lava":{
        "bg":"#0d0000","panel":"#1a0000","accent":"#330000",
        "highlight":"#ff2200","text":"#ffe8e0","muted":"#773300",
        "header_fg":"#ff6633","btn_fg":"#0d0000",
        "entry_fg":"#ffe8e0","stat_num":"#ff2200","stat_lbl":"#773300","logo":"#ff2200",
    },
    "Golden Hour":{
        "bg":"#0d0900","panel":"#1a1100","accent":"#332200",
        "highlight":"#ffcc00","text":"#fff8e0","muted":"#886600",
        "header_fg":"#ffd740","btn_fg":"#0d0900",
        "entry_fg":"#fff8e0","stat_num":"#ffcc00","stat_lbl":"#886600","logo":"#ffcc00",
    },
    "ronooosh pink":{
        "bg":"#120008","panel":"#1e0010","accent":"#3d0025",
        "highlight":"#ff4da6","text":"#ffe6f2","muted":"#b06688",
        "header_fg":"#ff80c0","btn_fg":"#120008",
        "entry_fg":"#ffe6f2","stat_num":"#ff4da6","stat_lbl":"#b06688","logo":"#ff4da6",
    },
}

COLORS: dict = dict(PRESETS["Almog Red"])
glass_on   = False
always_top = False

# ═══════════════════════════════════════════════════════
#  PERSISTENCE
# ═══════════════════════════════════════════════════════
def load_saved_themes():
    try:
        if os.path.exists(THEMES_FILE):
            with open(THEMES_FILE) as f: return json.load(f)
    except Exception: pass
    return {}
def write_saved_themes(d):
    with open(THEMES_FILE,"w") as f: json.dump(d,f,indent=2)
def load_stats():
    try:
        if os.path.exists(STATS_FILE):
            with open(STATS_FILE) as f: return json.load(f)
    except Exception: pass
    return {"total_clicks":0,"last_session_clicks":0}
def save_stats(d):
    with open(STATS_FILE,"w") as f: json.dump(d,f,indent=2)
def load_prefs():
    try:
        if os.path.exists(PREFS_FILE):
            with open(PREFS_FILE) as f: return json.load(f)
    except Exception: pass
    return {"hotkey":"f6","font":"Segoe UI"}
def save_prefs(d):
    with open(PREFS_FILE,"w") as f: json.dump(d,f,indent=2)

_stats         = load_stats()
_prefs         = load_prefs()
session_clicks = 0
total_clicks   = _stats.get("total_clicks",0)

# ═══════════════════════════════════════════════════════
#  FONT
# ═══════════════════════════════════════════════════════
CURRENT_FONT = _prefs.get("font","Segoe UI")
FONT_CHOICES = ["Segoe UI","Arial","Calibri","Verdana","Tahoma",
                "Georgia","Trebuchet MS","Courier New","Consolas","Lucida Console"]
def F(size, bold=False):
    return (CURRENT_FONT, size, "bold" if bold else "normal")

# ═══════════════════════════════════════════════════════
#  HOTKEY
# ═══════════════════════════════════════════════════════
HOTKEY_NAME  = _prefs.get("hotkey","f6")
_kb_listener = None
_capturing   = False

def key_to_name(key):
    try:
        if hasattr(key,"name"): return key.name.lower()
        return key.char.lower()
    except Exception: return "unknown"

def start_listener():
    global _kb_listener
    if _kb_listener:
        try: _kb_listener.stop()
        except Exception: pass
    def on_press(key):
        if _capturing: return
        if key_to_name(key)==HOTKEY_NAME: root.after(0,start_stop)
    _kb_listener = kb.Listener(on_press=on_press,daemon=True)
    _kb_listener.start()

# ═══════════════════════════════════════════════════════
#  COLOR UTILITIES
# ═══════════════════════════════════════════════════════
def hex_to_hsv(h):
    h=h.lstrip("#"); r,g,b=int(h[0:2],16)/255,int(h[2:4],16)/255,int(h[4:6],16)/255
    return colorsys.rgb_to_hsv(r,g,b)
def hsv_to_hex(hu,sa,va):
    r,g,b=colorsys.hsv_to_rgb(hu,sa,va)
    return "#{:02x}{:02x}{:02x}".format(int(r*255),int(g*255),int(b*255))
def lighten(h,amt=0.15):
    h=h.lstrip("#"); r,g,b=int(h[0:2],16),int(h[2:4],16),int(h[4:6],16)
    return "#{:02x}{:02x}{:02x}".format(int(r+(255-r)*amt),int(g+(255-g)*amt),int(b+(255-b)*amt))
def darken(h,amt=0.3):
    h=h.lstrip("#"); r,g,b=int(h[0:2],16),int(h[2:4],16),int(h[4:6],16)
    return "#{:02x}{:02x}{:02x}".format(int(r*(1-amt)),int(g*(1-amt)),int(b*(1-amt)))
def is_valid_hex(h):
    h=h.strip().lstrip("#")
    return len(h)==6 and all(c in "0123456789abcdefABCDEF" for c in h)
def norm(h): return "#"+h.strip().lstrip("#").lower()

# ═══════════════════════════════════════════════════════
#  CLICK LOGIC
# ═══════════════════════════════════════════════════════
mc           = Controller()
clicking     = False
click_thread = None

def _update_ui_after_click(c):
    status_var.set(f"Clicks this run: {c:,}")
    refresh_stats(); animate_counter()

def click_loop(interval, button, double, repeat):
    global clicking, session_clicks, total_clicks
    count=0
    while clicking:
        if _stop_requested:
            break
        if double:
            mc.click(button); time.sleep(0.05); mc.click(button)
        else:
            mc.click(button)
        count+=1; session_clicks+=1; total_clicks+=1
        root.after(0, lambda c=count: _update_ui_after_click(c))
        if repeat>0 and count>=repeat:
            clicking=False
            root.after(0, lambda: toggle_btn.config(text="▶  FIRE"))
            break
        time.sleep(interval)

def get_interval():
    try:
        t=(int(hv.get() or 0)*3600+int(mv.get() or 0)*60
           +float(sv.get() or 0)+float(msv.get() or 100)/1000)
        return max(t,0.001)
    except ValueError:
        messagebox.showerror("Error","Invalid time values"); return 0.0

def get_btn():
    v=btn_var.get()
    return Button.middle if v=="Middle" else Button.right if v=="Right" else Button.left

def get_repeat():
    try: v=rep_var.get().strip(); return int(v) if v and v!="0" else 0
    except ValueError: return 0

_stop_requested = False

def start_stop():
    global clicking, click_thread, session_clicks, _stop_requested
    if clicking:
        _stop_requested = True
        clicking=False
        toggle_btn.config(text="▶  FIRE")
        stop_pulse()
        save_stats({"total_clicks":total_clicks,"last_session_clicks":session_clicks})
        root.after(300, lambda: globals().update(_stop_requested=False))
    else:
        if _stop_requested:
            return
        interval=get_interval()
        if not interval: return
        clicking=True
        toggle_btn.config(text="⏹  STOP")
        status_var.set("Clicks this run: 0")
        start_pulse()
        click_thread=threading.Thread(
            target=click_loop,
            args=(interval,get_btn(),type_var.get()=="Double",get_repeat()),daemon=True)
        click_thread.start()

# ═══════════════════════════════════════════════════════
#  COLOR PICKER  (HSV wheel + RGB sliders)
# ═══════════════════════════════════════════════════════
class ColorPicker(tk.Toplevel):
    W=210; SW=16
    def __init__(self,parent,init_hex,label,on_pick):
        super().__init__(parent)
        self.on_pick=on_pick; self.label_str=label
        self.transient(parent); self.resizable(False,False)
        self.title(""); self.configure(bg=COLORS["panel"])
        hu,sa,va=hex_to_hsv(init_hex); self._h=hu; self._s=sa; self._v=va
        self._build_chrome(); self._build_hsv_panel(); self._build_rgb_panel()
        self._show_hsv(); self._draw_wheel(); self._draw_val_strip()
        self._place_marker(); self._place_val_marker(); self._update_all_previews()
        self.update_idletasks()
        px=parent.winfo_rootx()+parent.winfo_width()//2-self.winfo_width()//2
        py=parent.winfo_rooty()+parent.winfo_height()//2-self.winfo_height()//2
        self.geometry(f"+{px}+{py}"); self.grab_set()

    def _build_chrome(self):
        BG=COLORS["panel"]; HI=COLORS["highlight"]; AC=COLORS["accent"]
        MU=COLORS["muted"]; FG=COLORS["text"]; BFG=COLORS["btn_fg"]
        tk.Label(self,text=f"  Choose Colour  ·  {self.label_str}",
                 bg=BG,fg=HI,font=F(11,True),anchor="w").pack(fill="x",padx=16,pady=(12,4))
        tk.Frame(self,bg=AC,height=1).pack(fill="x",padx=16)
        self._mode=tk.StringVar(value="HSV")
        tab_row=tk.Frame(self,bg=BG); tab_row.pack(fill="x",padx=16,pady=(8,0))
        for m in ("HSV","RGB"):
            tk.Radiobutton(tab_row,text=m,variable=self._mode,value=m,
                           bg=BG,fg=FG,selectcolor=AC,activebackground=BG,
                           font=F(9,True),cursor="hand2",command=self._on_tab
                           ).pack(side="left",padx=(0,14))
        self._content=tk.Frame(self,bg=BG); self._content.pack(padx=16,pady=8)
        tk.Frame(self,bg=AC,height=1).pack(fill="x",padx=16)
        br=tk.Frame(self,bg=BG); br.pack(fill="x",pady=10,padx=16)
        tk.Button(br,text="Cancel",font=F(9),bg=AC,fg=MU,relief="flat",bd=0,
                  padx=14,pady=6,cursor="hand2",command=self.destroy).pack(side="left")
        tk.Button(br,text="Apply",font=F(9,True),bg=HI,fg=BFG,relief="flat",bd=0,
                  padx=14,pady=6,cursor="hand2",command=self._apply).pack(side="right")

    def _apply(self): self.on_pick(hsv_to_hex(self._h,self._s,self._v)); self.destroy()

    def _build_hsv_panel(self):
        BG=COLORS["panel"]; MU=COLORS["muted"]; FG=COLORS["text"]; AC=COLORS["accent"]
        self._hsv_frame=tk.Frame(self._content,bg=BG)
        self.wheel_c=tk.Canvas(self._hsv_frame,width=self.W,height=self.W,bg=BG,
                                highlightthickness=0,cursor="crosshair")
        self.wheel_c.grid(row=0,column=0,rowspan=2,padx=(0,10))
        self.wheel_c.bind("<Button-1>",self._wheel_click)
        self.wheel_c.bind("<B1-Motion>",self._wheel_click)
        self.val_c=tk.Canvas(self._hsv_frame,width=self.SW,height=self.W,bg=BG,
                              highlightthickness=0,cursor="sb_v_double_arrow")
        self.val_c.grid(row=0,column=1,rowspan=2,padx=(0,10))
        self.val_c.bind("<Button-1>",self._val_click)
        self.val_c.bind("<B1-Motion>",self._val_click)
        rp=tk.Frame(self._hsv_frame,bg=BG); rp.grid(row=0,column=2,sticky="n")
        self._hsv_prev=tk.Label(rp,width=8,height=3,bg="#ffffff",relief="flat",bd=0)
        self._hsv_prev.pack(pady=(0,8))
        tk.Label(rp,text="HEX",bg=BG,fg=MU,font=F(8)).pack()
        self._hsv_hex_var=tk.StringVar(); self._hsv_hex_typing=False
        tk.Entry(rp,textvariable=self._hsv_hex_var,width=9,font=("Consolas",11,"bold"),
                 justify="center",bg=AC,fg=FG,insertbackground=FG,relief="flat",bd=4
                 ).pack(pady=(2,10))
        self._hsv_hex_var.trace_add("write",self._on_hsv_hex_type)
        tk.Label(rp,text="QUICK",bg=BG,fg=MU,font=F(7,True)).pack(anchor="w")
        qf=tk.Frame(rp,bg=BG); qf.pack(pady=(2,0))
        for i,c in enumerate(["#e94560","#c084fc","#4fc3f7","#39d98a",
                               "#ff6b2b","#ff79c6","#cc0000","#ffffff"]):
            b=tk.Label(qf,bg=c,width=2,height=1,cursor="hand2",relief="flat")
            b.grid(row=i//4,column=i%4,padx=2,pady=2)
            b.bind("<Button-1>",lambda e,col=c:self._set_from_hex(col))

    def _build_rgb_panel(self):
        BG=COLORS["panel"]; MU=COLORS["muted"]; FG=COLORS["text"]; AC=COLORS["accent"]
        self._rgb_frame=tk.Frame(self._content,bg=BG)
        top=tk.Frame(self._rgb_frame,bg=BG); top.pack(fill="x",pady=(0,12))
        self._rgb_prev=tk.Label(top,width=6,height=3,bg="#ffffff",relief="flat",bd=0)
        self._rgb_prev.pack(side="left",padx=(0,12))
        sub=tk.Frame(top,bg=BG); sub.pack(side="left",anchor="w")
        tk.Label(sub,text="HEX",bg=BG,fg=MU,font=F(8)).pack(anchor="w")
        self._rgb_hex_var=tk.StringVar(); self._rgb_hex_typing=False
        tk.Entry(sub,textvariable=self._rgb_hex_var,width=9,font=("Consolas",11,"bold"),
                 justify="center",bg=AC,fg=FG,insertbackground=FG,relief="flat",bd=4
                 ).pack(pady=(2,0))
        self._rgb_hex_var.trace_add("write",self._on_rgb_hex_type)
        self._r_var=tk.IntVar(value=0); self._g_var=tk.IntVar(value=0); self._b_var=tk.IntVar(value=0)
        for lbl_t,var,col in [("R",self._r_var,"#e94560"),("G",self._g_var,"#39d98a"),("B",self._b_var,"#4fc3f7")]:
            row=tk.Frame(self._rgb_frame,bg=BG); row.pack(fill="x",pady=4)
            tk.Label(row,text=lbl_t,bg=BG,fg=MU,font=("Consolas",10,"bold"),width=2).pack(side="left")
            tk.Scale(row,from_=0,to=255,orient="horizontal",variable=var,length=260,showvalue=False,
                     bg=BG,fg=FG,troughcolor=AC,activebackground=col,highlightthickness=0,bd=0,
                     sliderlength=14,command=lambda _:self._on_rgb_slide()).pack(side="left",padx=(4,4))
            tk.Label(row,textvariable=var,bg=BG,fg=FG,font=("Consolas",9),width=4).pack(side="left")
        tk.Label(self._rgb_frame,text="QUICK",bg=BG,fg=MU,font=F(7,True)).pack(anchor="w",pady=(8,2))
        qf=tk.Frame(self._rgb_frame,bg=BG); qf.pack(anchor="w")
        for i,c in enumerate(["#e94560","#c084fc","#4fc3f7","#39d98a",
                               "#ff6b2b","#ff79c6","#cc0000","#ffffff"]):
            b=tk.Label(qf,bg=c,width=2,height=1,cursor="hand2",relief="flat")
            b.grid(row=0,column=i,padx=2,pady=2)
            b.bind("<Button-1>",lambda e,col=c:self._set_from_hex(col))

    def _show_hsv(self): self._rgb_frame.pack_forget(); self._hsv_frame.pack()
    def _show_rgb(self):
        self._hsv_frame.pack_forget()
        r2,g2,b2=colorsys.hsv_to_rgb(self._h,self._s,self._v)
        self._rgb_typing_internal=True
        self._r_var.set(int(r2*255)); self._g_var.set(int(g2*255)); self._b_var.set(int(b2*255))
        self._rgb_typing_internal=False
        self._sync_rgb_preview(); self._rgb_frame.pack()
    def _on_tab(self):
        if self._mode.get()=="HSV": self._show_hsv()
        else: self._show_rgb()

    def _draw_wheel(self):
        cx=cy=r=self.W//2; rows=[]
        for y in range(self.W):
            row=[]
            for x in range(self.W):
                dx,dy=x-cx,y-cy; dist=math.hypot(dx,dy)
                if dist<=r:
                    angle=(math.atan2(-dy,dx)/(2*math.pi))%1.0
                    sat=min(dist/r,1.0); r2,g2,b2=colorsys.hsv_to_rgb(angle,sat,self._v)
                    row.append("#{:02x}{:02x}{:02x}".format(int(r2*255),int(g2*255),int(b2*255)))
                else: row.append(COLORS["panel"])
            rows.append("{"+' '.join(row)+"}")
        self._wimg=tk.PhotoImage(width=self.W,height=self.W); self._wimg.put(' '.join(rows))
        self.wheel_c.create_image(0,0,anchor="nw",image=self._wimg)

    def _draw_val_strip(self):
        r2,g2,b2=colorsys.hsv_to_rgb(self._h,self._s,1.0); rows=[]
        for y in range(self.W):
            v=1.0-y/self.W; rr,gg,bb=int(r2*255*v),int(g2*255*v),int(b2*255*v)
            rows.append("{"+f"#{rr:02x}{gg:02x}{bb:02x} "*self.SW+"}")
        self._vimg=tk.PhotoImage(width=self.SW,height=self.W); self._vimg.put(' '.join(rows))
        self.val_c.delete("all"); self.val_c.create_image(0,0,anchor="nw",image=self._vimg)

    def _place_marker(self):
        cx=cy=r=self.W//2; angle=self._h*2*math.pi; dist=self._s*r
        mx=cx+dist*math.cos(angle); my=cy-dist*math.sin(angle)
        self.wheel_c.delete("marker")
        self.wheel_c.create_oval(mx-7,my-7,mx+7,my+7,outline="white",width=2,tags="marker")
        self.wheel_c.create_oval(mx-5,my-5,mx+5,my+5,outline="black",width=1,tags="marker")

    def _place_val_marker(self):
        y=(1-self._v)*self.W; self.val_c.delete("vm")
        self.val_c.create_line(0,y,self.SW,y,fill="white",width=2,tags="vm")

    def _wheel_click(self,e):
        cx=cy=r=self.W//2; dx,dy=e.x-cx,e.y-cy; dist=min(math.hypot(dx,dy),r)
        self._h=(math.atan2(-dy,dx)/(2*math.pi))%1.0; self._s=dist/r
        self._draw_wheel(); self._draw_val_strip()
        self._place_marker(); self._place_val_marker(); self._update_all_previews()

    def _val_click(self,e):
        self._v=max(0.0,min(1.0,1.0-e.y/self.W))
        self._draw_wheel(); self._draw_val_strip()
        self._place_marker(); self._place_val_marker(); self._update_all_previews()

    def _on_hsv_hex_type(self,*_):
        if self._hsv_hex_typing: return
        val=self._hsv_hex_var.get()
        if is_valid_hex(val): self._set_from_hex(norm(val))

    def _on_rgb_slide(self):
        if getattr(self,"_rgb_typing_internal",False): return
        r,g,b=self._r_var.get(),self._g_var.get(),self._b_var.get()
        self._h,self._s,self._v=colorsys.rgb_to_hsv(r/255,g/255,b/255)
        self._sync_rgb_preview()

    def _sync_rgb_preview(self):
        col=hsv_to_hex(self._h,self._s,self._v)
        try: self._rgb_prev.configure(bg=col)
        except Exception: pass
        self._rgb_hex_typing=True
        try: self._rgb_hex_var.set(col)
        except Exception: pass
        self._rgb_hex_typing=False

    def _on_rgb_hex_type(self,*_):
        if self._rgb_hex_typing: return
        val=self._rgb_hex_var.get()
        if is_valid_hex(val):
            h,s,v=hex_to_hsv(norm(val)); self._h,self._s,self._v=h,s,v
            r2,g2,b2=colorsys.hsv_to_rgb(h,s,v)
            self._rgb_typing_internal=True
            self._r_var.set(int(r2*255)); self._g_var.set(int(g2*255)); self._b_var.set(int(b2*255))
            self._rgb_typing_internal=False; self._sync_rgb_preview()

    def _set_from_hex(self,hexcol):
        h,s,v=hex_to_hsv(hexcol); self._h,self._s,self._v=h,s,v
        self._draw_wheel(); self._draw_val_strip()
        self._place_marker(); self._place_val_marker(); self._update_all_previews()
        if self._mode.get()=="RGB":
            r2,g2,b2=colorsys.hsv_to_rgb(h,s,v)
            self._rgb_typing_internal=True
            self._r_var.set(int(r2*255)); self._g_var.set(int(g2*255)); self._b_var.set(int(b2*255))
            self._rgb_typing_internal=False; self._sync_rgb_preview()

    def _update_all_previews(self):
        col=hsv_to_hex(self._h,self._s,self._v)
        try: self._hsv_prev.configure(bg=col)
        except Exception: pass
        self._hsv_hex_typing=True
        try: self._hsv_hex_var.set(col)
        except Exception: pass
        self._hsv_hex_typing=False

# ═══════════════════════════════════════════════════════
#  THEME ENGINE
# ═══════════════════════════════════════════════════════
swatch_labels:   dict = {}
hex_str_vars:    dict = {}
_bg_wids:        list = []
_panel_wids:     list = []
_accent_wids:    list = []
_muted_wids:     list = []
_entry_wids:     list = []
_entry_lbl_wids: list = []
BINDINGS:        list = []

def apply_theme():
    try:
        font_prev_lbl.configure(bg=COLORS["bg"],fg=COLORS["text"],font=(CURRENT_FONT,10))
    except Exception: pass
    root.configure(bg=COLORS["bg"])
    for w,a,k in BINDINGS:
        try: w.configure(**{a:COLORS[k]})
        except Exception: pass
    style.configure("TFrame",    background=COLORS["bg"])
    style.configure("TLabel",    background=COLORS["bg"],foreground=COLORS["text"])
    style.configure("TEntry",    fieldbackground=COLORS["accent"],
                    foreground=COLORS["entry_fg"],insertcolor=COLORS["entry_fg"])
    style.configure("TCombobox", fieldbackground=COLORS["accent"],
                    foreground=COLORS["entry_fg"],selectbackground=COLORS["highlight"],
                    selectforeground=COLORS["btn_fg"],
                    background=COLORS["accent"],
                    arrowcolor=COLORS["entry_fg"],
                    bordercolor=COLORS["accent"],
                    lightcolor=COLORS["accent"],
                    darkcolor=COLORS["accent"])
    style.map("TCombobox",
              fieldbackground=[("readonly",COLORS["accent"]),("disabled",COLORS["panel"])],
              foreground=[("readonly",COLORS["entry_fg"])],
              selectbackground=[("readonly",COLORS["highlight"])],
              background=[("readonly",COLORS["accent"]),("active",COLORS["highlight"])])
    # Style the dropdown popup listbox
    root.option_add("*TCombobox*Listbox.background",  COLORS["accent"])
    root.option_add("*TCombobox*Listbox.foreground",  COLORS["entry_fg"])
    root.option_add("*TCombobox*Listbox.selectBackground", COLORS["highlight"])
    root.option_add("*TCombobox*Listbox.selectForeground", COLORS["btn_fg"])
    root.option_add("*TCombobox*Listbox.relief",      "flat")
    root.option_add("*TCombobox*Listbox.borderWidth", "0")
    for w in _bg_wids:
        try: w.configure(bg=COLORS["bg"])
        except Exception: pass
    for w in _panel_wids:
        try: w.configure(bg=COLORS["panel"])
        except Exception: pass
    for w in _accent_wids:
        try: w.configure(bg=COLORS["accent"])
        except Exception: pass
    for w in _muted_wids:
        try: w.configure(bg=COLORS["bg"],fg=COLORS["muted"])
        except Exception: pass
    for e in _entry_wids:
        try: e.configure(bg=COLORS["accent"],fg=COLORS["entry_fg"],insertbackground=COLORS["entry_fg"])
        except Exception: pass
    for l in _entry_lbl_wids:
        try: l.configure(bg=COLORS["bg"],fg=COLORS["muted"])
        except Exception: pass
    for key in DEFAULT_KEYS:
        try:
            swatch_labels[key].configure(bg=COLORS[key])
            cur=hex_str_vars[key].get()
            if norm(cur)!=COLORS[key]: hex_str_vars[key].set(COLORS[key])
        except Exception: pass
    try:
        pc=lighten(COLORS["panel"],0.06) if glass_on else COLORS["panel"]
        for box in stat_boxes:
            box.configure(bg=pc)
            for child in box.winfo_children():
                try:
                    fnt=str(child.cget("font"))
                    is_num="16" in fnt or ("bold" in fnt and "7" not in fnt)
                    child.configure(bg=pc,fg=COLORS["stat_num"] if is_num else COLORS["stat_lbl"])
                except Exception: pass
    except Exception: pass
    try:
        hp=lighten(COLORS["panel"],0.08) if glass_on else COLORS["panel"]
        titlebar.configure(bg=hp)
        for w in titlebar.winfo_children():
            try: w.configure(bg=hp)
            except Exception: pass
        title_lbl.configure(bg=hp,fg=COLORS["header_fg"])
        badge_lbl.configure(bg=hp,fg=COLORS["muted"])
        close_btn.configure(bg=hp,fg=COLORS["muted"])
        min_btn.configure(bg=hp,fg=COLORS["muted"])
        _update_pin_btn_style()
        status_bar.configure(bg=COLORS["panel"],fg=COLORS["muted"])
    except Exception: pass
    try: indicator_bar.configure(bg=COLORS["highlight"])
    except Exception: pass
    try: draw_logo()
    except Exception: pass
    root.update_idletasks()

def open_picker(key):
    def on_pick(hexcol): COLORS[key]=hexcol; apply_theme()
    ColorPicker(root,COLORS[key],COLOR_LABELS[key],on_pick)

def on_hex_field_change(key,*_):
    val=hex_str_vars[key].get()
    if is_valid_hex(val):
        COLORS[key]=norm(val)
        try: swatch_labels[key].configure(bg=COLORS[key])
        except Exception: pass
        apply_theme()

# ═══════════════════════════════════════════════════════
#  ROOT — FRAMELESS WINDOW
# ═══════════════════════════════════════════════════════
root = tk.Tk()
root.title("Almog's Clicker")
root.overrideredirect(True)
root.attributes("-alpha", 0.0)
root.configure(bg=COLORS["bg"])
style = ttk.Style(); style.theme_use("clam")

_drag_x = 0
_drag_y = 0
def on_drag_start(e):
    global _drag_x,_drag_y; _drag_x=e.x_root; _drag_y=e.y_root
def on_drag_move(e):
    global _drag_x,_drag_y
    dx=e.x_root-_drag_x; dy=e.y_root-_drag_y
    _drag_x=e.x_root; _drag_y=e.y_root
    root.geometry(f"+{root.winfo_x()+dx}+{root.winfo_y()+dy}")

# ── HELPERS ──────────────────────────────────────────────
def mk_bg(parent,**kw):
    f=tk.Frame(parent,bg=COLORS["bg"],**kw); _bg_wids.append(f); return f

def gaming_section(parent,text):
    f=mk_bg(parent); f.pack(fill="x",pady=(14,4))
    lbl=tk.Label(f,text=f"// {text}",bg=COLORS["bg"],fg=COLORS["highlight"],font=F(8,True),anchor="w")
    lbl.pack(side="left")
    div=tk.Frame(f,bg=COLORS["accent"],height=1)
    div.pack(side="left",fill="x",expand=True,padx=(8,0))
    _accent_wids.append(div); BINDINGS.append((lbl,"fg","highlight")); return f

def field_row(parent,label,var,width=6):
    row=mk_bg(parent); row.pack(fill="x",pady=2)
    lbl=tk.Label(row,text=label,bg=COLORS["bg"],fg=COLORS["muted"],font=F(9),width=13,anchor="w")
    lbl.pack(side="left"); _entry_lbl_wids.append(lbl)
    e=tk.Entry(row,textvariable=var,width=width,font=("Consolas",10),justify="center",
               bg=COLORS["accent"],fg=COLORS["entry_fg"],insertbackground=COLORS["entry_fg"],
               relief="flat",bd=4)
    e.pack(side="left"); _entry_wids.append(e); return row,e

def drop_row(parent,label,var,choices):
    row=mk_bg(parent); row.pack(fill="x",pady=2)
    lbl=tk.Label(row,text=label,bg=COLORS["bg"],fg=COLORS["muted"],font=F(9),width=13,anchor="w")
    lbl.pack(side="left"); _entry_lbl_wids.append(lbl)
    cb=ttk.Combobox(row,textvariable=var,values=choices,state="readonly",width=10,font=("Consolas",10))
    cb.pack(side="left"); return row,cb

def hdiv(parent,pady=(4,4)):
    d=tk.Frame(parent,bg=COLORS["accent"],height=1)
    d.pack(fill="x",pady=pady); _accent_wids.append(d)

# ═══════════════════════════════════════════════════════
#  SPLASH SCREEN
# ═══════════════════════════════════════════════════════
def show_splash():
    splash=tk.Toplevel(root); splash.overrideredirect(True)
    splash.configure(bg="#0a0a0a"); splash.attributes("-alpha",0.0)
    SW,SH=320,320
    sx=root.winfo_screenwidth()//2-SW//2; sy=root.winfo_screenheight()//2-SH//2
    splash.geometry(f"{SW}x{SH}+{sx}+{sy}"); splash.lift()
    c=tk.Canvas(splash,width=SW,height=SH,bg="#0a0a0a",highlightthickness=0)
    c.pack(fill="both",expand=True)
    CX,CY=SW//2,SH//2-10; R=100; TRAIL=60; SPEED=3.2
    # Canvas logo in center
    _draw_splash_canvas_logo(c,CX,CY)
    status_id=c.create_text(CX,CY+R+26,text="",fill="#444444",font=("Consolas",8),anchor="center")
    c.create_text(CX,CY+R+42,text="ALMOG'S CLICKER  v9.0",fill="#1e1e1e",font=("Consolas",7),anchor="center")
    arc_items=[]; STEPS=[(0.0,0.25,"INITIALIZING..."),(0.25,0.55,"LOADING THEMES..."),
                         (0.55,0.80,"BINDING HOTKEYS..."),(0.80,1.0,"READY")]
    state={"alpha":0.0,"done_deg":0.0,"phase":"spin"}
    def _label(deg):
        p=deg/360.0
        for s,e,l in STEPS:
            if p<=e: return l
        return "READY"
    def _draw_arc(done_deg):
        for aid in arc_items:
            try: c.delete(aid)
            except Exception: pass
        arc_items.clear()
        head=-90.0+done_deg; span=min(done_deg,TRAIL)
        if span<=0: return
        for i in range(max(1,int(span))):
            t=i/max(1,int(span)); gray=int(28+210*t**1.8)
            col="#{0:02x}{0:02x}{0:02x}".format(gray)
            try:
                aid=c.create_arc(CX-R,CY-R,CX+R,CY+R,start=head-span+i,extent=1.5,
                                  style="arc",outline=col,width=2)
                arc_items.append(aid)
            except Exception: pass
        tr=math.radians(-head); tx=CX+R*math.cos(tr); ty=CY-R*math.sin(tr)
        arc_items.append(c.create_oval(tx-3,ty-3,tx+3,ty+3,fill="#ffffff",outline=""))
    def animate():
        if state["phase"]!="spin": return
        state["done_deg"]=min(state["done_deg"]+SPEED,360.0)
        _draw_arc(state["done_deg"])
        lbl=_label(state["done_deg"])
        c.itemconfig(status_id,text=lbl,fill="#666666" if lbl!="READY" else "#999999")
        if state["done_deg"]>=360.0: state["phase"]="done"; splash.after(400,_arc_out)
        else: splash.after(16,animate)
    def _arc_out(step=10):
        if step<=0: splash.after(60,_fadeout); return
        t=(step/10.0)**2
        for aid in arc_items:
            try:
                gray=int(220*t); col="#{0:02x}{0:02x}{0:02x}".format(gray)
                c.itemconfig(aid,outline=col,fill=col)
            except Exception: pass
        splash.after(22,lambda:_arc_out(step-1))
    def _fadeout():
        a=max(state["alpha"]-0.055,0.0); state["alpha"]=a; splash.attributes("-alpha",a)
        if a>0: splash.after(16,_fadeout)
        else:
            splash.destroy()
            root.after(0,lambda:fade_in(0.0))
            root.after(0,logo_idle)
    def _fadein():
        a=min(state["alpha"]+0.06,1.0); state["alpha"]=a; splash.attributes("-alpha",a)
        if a<1.0: splash.after(16,_fadein)
        else: animate()
    root.update_idletasks(); splash.after(60,_fadein); splash.grab_set()

def _draw_splash_canvas_logo(c,cx,cy):
    W,H=70,70; x0,y0=cx-W//2,cy-H//2; col="#cc0000"
    dark=darken(col,0.45)
    mid="#{:02x}{:02x}{:02x}".format(
        int(int(col[1:3],16)*0.72),int(int(col[3:5],16)*0.72),int(int(col[5:7],16)*0.72))
    def p(px,py): return (x0+int(px*W/28),y0+int(py*H/28))
    c.create_polygon([p(14,2),p(25,26),p(20,26),p(14,8),p(8,26),p(3,26)],fill=dark,outline="")
    c.create_polygon([p(14,2),p(8,26),p(12,26),p(14,10)],fill=col,outline="")
    c.create_polygon([p(14,2),p(20,26),p(18,26),p(14,10)],fill=mid,outline="")

# ═══════════════════════════════════════════════════════
#  CANVAS LOGO (titlebar)
# ═══════════════════════════════════════════════════════
LOGO_W,LOGO_H = 26,26
_canvas_logo_c = None

def draw_logo():
    global _canvas_logo_c
    if _canvas_logo_c is None: return
    c=_canvas_logo_c; col=COLORS["logo"]
    dark=darken(col,0.45)
    mid="#{:02x}{:02x}{:02x}".format(
        int(int(col[1:3],16)*0.72),int(int(col[3:5],16)*0.72),int(int(col[5:7],16)*0.72))
    bg_c=lighten(COLORS["panel"],0.08) if glass_on else COLORS["panel"]
    c.configure(bg=bg_c); c.delete("all")
    W,H=LOGO_W,LOGO_H
    c.create_polygon([W//2,2,W-3,H-2,W-8,H-2,W//2,8,8,H-2,3,H-2],fill=dark,outline="")
    c.create_polygon([W//2,2,8,H-2,12,H-2,W//2,10],fill=col,outline="")
    c.create_polygon([W//2,2,W-8,H-2,W-12,H-2,W//2,10],fill=mid,outline="")
    c.create_polygon([9,H-10,W-9,H-10,W-7,H-6,7,H-6],fill=dark,outline="")
    c.create_line(W//2,3,W//2,9,fill=lighten(col,0.5),width=1,tags="glint")

# ═══════════════════════════════════════════════════════
#  GAMING TITLE BAR
# ═══════════════════════════════════════════════════════
indicator_bar=tk.Frame(root,bg=COLORS["highlight"],height=3)
indicator_bar.pack(fill="x")

titlebar=tk.Frame(root,bg=COLORS["panel"],height=44)
titlebar.pack(fill="x"); titlebar.pack_propagate(False)
_panel_wids.append(titlebar)
titlebar.bind("<ButtonPress-1>",on_drag_start)
titlebar.bind("<B1-Motion>",on_drag_move)

# Canvas logo
logo_c=tk.Canvas(titlebar,width=LOGO_W,height=LOGO_H,bg=COLORS["panel"],highlightthickness=0)
logo_c.pack(side="left",padx=(12,6),pady=9)
_canvas_logo_c=logo_c; _panel_wids.append(logo_c)
logo_c.bind("<ButtonPress-1>",on_drag_start)
logo_c.bind("<B1-Motion>",on_drag_move)

title_lbl=tk.Label(titlebar,text="ALMOG'S CLICKER",bg=COLORS["panel"],fg=COLORS["header_fg"],font=F(13,True))
title_lbl.pack(side="left",pady=9)
title_lbl.bind("<ButtonPress-1>",on_drag_start)
title_lbl.bind("<B1-Motion>",on_drag_move)

badge_lbl=tk.Label(titlebar,text=" v9.0 ",bg=COLORS["panel"],fg=COLORS["muted"],font=("Consolas",7,"bold"))
badge_lbl.pack(side="left",padx=(6,0),pady=12)
badge_lbl.bind("<ButtonPress-1>",on_drag_start)
badge_lbl.bind("<B1-Motion>",on_drag_move)

def do_minimize(): root.iconify()
def do_close():
    global clicking; clicking=False
    save_stats({"total_clicks":total_clicks,"last_session_clicks":session_clicks})
    save_prefs({"hotkey":HOTKEY_NAME,"font":CURRENT_FONT})
    root.destroy()

close_btn=tk.Button(titlebar,text="✕",font=F(10,True),bg=COLORS["panel"],fg=COLORS["muted"],
                     relief="flat",bd=0,padx=12,pady=0,cursor="hand2",
                     activebackground="#cc2222",activeforeground="#ffffff",command=do_close)
close_btn.pack(side="right",fill="y")

min_btn=tk.Button(titlebar,text="—",font=F(10),bg=COLORS["panel"],fg=COLORS["muted"],
                   relief="flat",bd=0,padx=12,pady=0,cursor="hand2",
                   activebackground=COLORS["accent"],command=do_minimize)
min_btn.pack(side="right",fill="y")

# ── Always-On-Top toggle ─────────────────────────────
def _update_pin_btn_style():
    hp=lighten(COLORS["panel"],0.08) if glass_on else COLORS["panel"]
    pin_btn.configure(fg=COLORS["highlight"] if always_top else COLORS["muted"],bg=hp,
                      activebackground=COLORS["accent"])

def toggle_always_top():
    global always_top
    always_top=not always_top
    root.attributes("-topmost",always_top)
    _update_pin_btn_style()
    status_var.set("Always On Top: ON" if always_top else "Always On Top: OFF")
    root.after(1800,lambda:status_var.set(f"Ready  ·  {HOTKEY_NAME.upper()} to start")
               if not clicking else None)

pin_btn=tk.Button(titlebar,text="📌",font=F(10),bg=COLORS["panel"],fg=COLORS["muted"],
                   relief="flat",bd=0,padx=10,pady=0,cursor="hand2",
                   activebackground=COLORS["accent"],command=toggle_always_top)
pin_btn.pack(side="right",fill="y")

tb_div=tk.Frame(root,bg=COLORS["accent"],height=1)
tb_div.pack(fill="x"); _accent_wids.append(tb_div)

# ═══════════════════════════════════════════════════════
#  BODY
# ═══════════════════════════════════════════════════════
body=mk_bg(root); body.pack(fill="both",expand=True)
left=mk_bg(body); left.pack(side="left",fill="both",padx=20,pady=14)
vdiv=tk.Frame(body,bg=COLORS["accent"],width=1); vdiv.pack(side="left",fill="y",pady=10)
_accent_wids.append(vdiv)
right=mk_bg(body); right.pack(side="left",fill="both",padx=20,pady=14)

# ═══════════════════════════════════════════════════════
#  LEFT — SETTINGS
# ═══════════════════════════════════════════════════════
gaming_section(left,"INTERVAL")
hv=tk.StringVar(value="0");   field_row(left,"Hours",        hv, 6)
mv=tk.StringVar(value="0");   field_row(left,"Minutes",      mv, 6)
sv=tk.StringVar(value="0");   field_row(left,"Seconds",      sv, 6)
msv=tk.StringVar(value="100");field_row(left,"Milliseconds", msv,6)

gaming_section(left,"CLICK")
btn_var=tk.StringVar(value="Left");   drop_row(left,"Mouse Button",btn_var, ["Left","Right","Middle"])
type_var=tk.StringVar(value="Single");drop_row(left,"Click Type",  type_var,["Single","Double"])

gaming_section(left,"REPEAT")
rep_var=tk.StringVar(value="0"); field_row(left,"Count (0=∞)",rep_var,6)

gaming_section(left,"HOTKEY")
hk_row=mk_bg(left); hk_row.pack(fill="x",pady=4)
hotkey_btn=tk.Button(hk_row,text=f"  {HOTKEY_NAME.upper()}  ",font=F(11,True),
                      bg=COLORS["accent"],fg=COLORS["highlight"],
                      relief="flat",bd=0,padx=12,pady=6,cursor="hand2")
hotkey_btn.pack(side="left",padx=(0,10))
BINDINGS.extend([(hotkey_btn,"bg","accent"),(hotkey_btn,"fg","highlight")])
hk_hint=tk.Label(hk_row,text="Click to rebind",bg=COLORS["bg"],fg=COLORS["muted"],font=F(8))
hk_hint.pack(side="left"); _muted_wids.append(hk_hint)

def start_capture():
    global _capturing,HOTKEY_NAME
    _capturing=True; hotkey_btn.config(text="  ...  ",fg=COLORS["muted"])
    def on_capture(key):
        global _capturing,HOTKEY_NAME
        name=key_to_name(key)
        if name in ("escape","unknown"): name=HOTKEY_NAME
        HOTKEY_NAME=name; _capturing=False
        root.after(0,lambda:(
            hotkey_btn.config(text=f"  {HOTKEY_NAME.upper()}  ",fg=COLORS["highlight"]),
            hotkey_lbl.config(text=f"{HOTKEY_NAME.upper()}  —  toggle"),
            save_prefs({"hotkey":HOTKEY_NAME,"font":CURRENT_FONT}),
            start_listener()
        )); return False
    kb.Listener(on_press=on_capture,daemon=True).start()
hotkey_btn.config(command=start_capture)

# ── FIRE button ──────────────────────────────────────
tk.Frame(left,bg=COLORS["bg"],height=12).pack()
fire_top=tk.Frame(left,bg=COLORS["highlight"],height=2); fire_top.pack(fill="x")
BINDINGS.append((fire_top,"bg","highlight"))
toggle_btn=tk.Button(left,text="▶  FIRE",font=(CURRENT_FONT,15,"bold"),
                      bg=COLORS["highlight"],fg=COLORS["btn_fg"],
                      activebackground=COLORS["accent"],activeforeground=COLORS["btn_fg"],
                      relief="flat",bd=0,padx=0,pady=16,cursor="hand2",width=20,command=start_stop)
toggle_btn.pack(fill="x")
fire_bot=tk.Frame(left,bg=COLORS["highlight"],height=2); fire_bot.pack(fill="x")
BINDINGS.extend([(fire_bot,"bg","highlight"),(toggle_btn,"bg","highlight"),
                 (toggle_btn,"fg","btn_fg"),(toggle_btn,"activebackground","accent"),
                 (toggle_btn,"activeforeground","btn_fg")])
hotkey_lbl=tk.Label(left,text=f"{HOTKEY_NAME.upper()}  —  toggle",
                     bg=COLORS["bg"],fg=COLORS["muted"],font=F(8),pady=4)
hotkey_lbl.pack(); _muted_wids.append(hotkey_lbl)

# ═══════════════════════════════════════════════════════
#  RIGHT — STATS
# ═══════════════════════════════════════════════════════
gaming_section(right,"STATISTICS")
stats_frame=mk_bg(right); stats_frame.pack(fill="x",pady=(0,6))
stat_session_var=tk.StringVar(value="0")
stat_last_var   =tk.StringVar(value=f"{_stats.get('last_session_clicks',0):,}")
stat_total_var  =tk.StringVar(value=f"{total_clicks:,}")

def refresh_stats():
    stat_session_var.set(f"{session_clicks:,}")
    stat_total_var.set(f"{total_clicks:,}")

stat_boxes=[]
for t,v in [("THIS SESSION",stat_session_var),("LAST SESSION",stat_last_var),("ALL TIME",stat_total_var)]:
    outer=tk.Frame(stats_frame,bg=COLORS["bg"]); outer.pack(side="left",expand=True,fill="both",padx=3,pady=2)
    ab=tk.Frame(outer,bg=COLORS["highlight"],height=2); ab.pack(fill="x")
    BINDINGS.append((ab,"bg","highlight"))
    box=tk.Frame(outer,bg=COLORS["panel"],padx=10,pady=10); box.pack(fill="both",expand=True)
    tk.Label(box,textvariable=v,bg=COLORS["panel"],fg=COLORS["stat_num"],font=F(16,True)).pack()
    tk.Label(box,text=t,bg=COLORS["panel"],fg=COLORS["stat_lbl"],font=F(7)).pack()
    stat_boxes.append(box)

def reset_stats():
    global total_clicks,session_clicks
    if messagebox.askyesno("Reset","Reset ALL TIME counter?"):
        total_clicks=0; session_clicks=0
        _stats["total_clicks"]=0; _stats["last_session_clicks"]=0
        save_stats(_stats); refresh_stats(); stat_last_var.set("0")

rst_btn=tk.Button(right,text="↺  Reset Stats",font=F(8),bg=COLORS["bg"],fg=COLORS["muted"],
                   relief="flat",bd=0,padx=0,pady=2,cursor="hand2",command=reset_stats)
rst_btn.pack(anchor="e"); _muted_wids.append(rst_btn)

# ═══════════════════════════════════════════════════════
#  RIGHT — FONT
# ═══════════════════════════════════════════════════════
gaming_section(right,"FONT")
font_row=mk_bg(right); font_row.pack(fill="x",pady=(0,4))
font_lbl_w=tk.Label(font_row,text="UI Font",bg=COLORS["bg"],fg=COLORS["muted"],font=F(8),width=8,anchor="w")
font_lbl_w.pack(side="left"); _muted_wids.append(font_lbl_w)
font_var=tk.StringVar(value=CURRENT_FONT)
font_cb=ttk.Combobox(font_row,textvariable=font_var,values=FONT_CHOICES,state="readonly",width=16,font=("Consolas",9))
font_cb.pack(side="left",padx=(0,8))
font_prev_lbl=tk.Label(font_row,text="Aa Bb",bg=COLORS["bg"],fg=COLORS["text"],font=(CURRENT_FONT,10))
font_prev_lbl.pack(side="left")
BINDINGS.extend([(font_prev_lbl,"bg","bg"),(font_prev_lbl,"fg","text")])

def on_font_change(e=None):
    global CURRENT_FONT; CURRENT_FONT=font_var.get()
    font_prev_lbl.config(font=(CURRENT_FONT,10),text=f"Aa Bb · {CURRENT_FONT}")
    save_prefs({"hotkey":HOTKEY_NAME,"font":CURRENT_FONT})
    apply_fonts()
def apply_fonts():
    try:
        title_lbl.config(font=F(13,True)); toggle_btn.config(font=(CURRENT_FONT,15,"bold"))
        hotkey_btn.config(font=F(11,True)); hotkey_lbl.config(font=F(8)); hk_hint.config(font=F(8))
        rst_btn.config(font=F(8)); font_lbl_w.config(font=F(8))
        for box in stat_boxes:
            for child in box.winfo_children():
                try:
                    fnt=str(child.cget("font"))
                    is_num="16" in fnt or ("bold" in fnt and "7" not in fnt)
                    child.config(font=F(16,True) if is_num else F(7))
                except Exception: pass
        for l in _muted_wids:
            try: l.config(font=F(8))
            except Exception: pass
        for l in _entry_lbl_wids:
            try: l.config(font=F(9))
            except Exception: pass
    except Exception: pass
font_cb.bind("<<ComboboxSelected>>",on_font_change)

# ═══════════════════════════════════════════════════════
#  RIGHT — THEME
# ═══════════════════════════════════════════════════════
gaming_section(right,"THEME")
color_grid=mk_bg(right); color_grid.pack(fill="x")
for i,key in enumerate(DEFAULT_KEYS):
    ci=i%2; ri=i//2
    cell=mk_bg(color_grid); cell.grid(row=ri,column=ci,padx=(0,12 if ci==0 else 0),pady=2,sticky="w")
    lbl_c=tk.Label(cell,text=COLOR_LABELS[key],bg=COLORS["bg"],fg=COLORS["muted"],font=F(8),width=13,anchor="w")
    lbl_c.pack(side="left"); _muted_wids.append(lbl_c)
    sw=tk.Label(cell,width=2,height=1,bg=COLORS[key],relief="flat",cursor="hand2")
    sw.pack(side="left",padx=(4,4)); sw.bind("<Button-1>",lambda e,k=key:open_picker(k))
    swatch_labels[key]=sw
    hvar=tk.StringVar(value=COLORS[key]); hex_str_vars[key]=hvar
    he=tk.Entry(cell,textvariable=hvar,width=8,font=("Consolas",9),justify="center",
                bg=COLORS["accent"],fg=COLORS["entry_fg"],insertbackground=COLORS["entry_fg"],
                relief="flat",bd=3)
    he.pack(side="left"); _entry_wids.append(he)
    hvar.trace_add("write",lambda *_,k=key:on_hex_field_change(k))

hdiv(right,(8,4))
fx_row=mk_bg(right); fx_row.pack(fill="x",pady=(0,4))

def toggle_glass():
    global glass_on; glass_on=not glass_on
    glass_btn.config(text="🔵 Glass ON" if glass_on else "⚫ Glass OFF",
                     bg=COLORS["highlight"] if glass_on else COLORS["accent"],
                     fg=COLORS["btn_fg"] if glass_on else COLORS["muted"])
    apply_theme()
glass_btn=tk.Button(fx_row,text="⚫ Glass OFF",font=F(8,True),bg=COLORS["accent"],fg=COLORS["muted"],
                     relief="flat",bd=0,padx=10,pady=5,cursor="hand2",command=toggle_glass)
glass_btn.pack(side="left")

hdiv(right,(4,6))
p_row=mk_bg(right); p_row.pack(fill="x")
pre_lbl=tk.Label(p_row,text="Preset",bg=COLORS["bg"],fg=COLORS["muted"],font=F(8),width=6,anchor="w")
pre_lbl.pack(side="left",padx=(0,4)); _muted_wids.append(pre_lbl)
preset_var=tk.StringVar()
preset_cb=ttk.Combobox(p_row,textvariable=preset_var,state="readonly",width=16,font=("Consolas",9))
preset_cb.pack(side="left",padx=(0,6))

def refresh_preset_list():
    saved=load_saved_themes()
    names=list(PRESETS.keys())+(["── Saved ──"] if saved else [])+list(saved.keys())
    preset_cb["values"]=names
def apply_preset(e=None):
    n=preset_var.get()
    if n=="── Saved ──": return
    t=PRESETS.get(n) or load_saved_themes().get(n)
    if t: COLORS.update(t); apply_theme()
preset_cb.bind("<<ComboboxSelected>>",apply_preset)

save_name_var=tk.StringVar(value="My Theme")
save_entry=tk.Entry(p_row,textvariable=save_name_var,width=9,font=("Consolas",9),
                     bg=COLORS["accent"],fg=COLORS["entry_fg"],insertbackground=COLORS["entry_fg"],
                     relief="flat",bd=3)
save_entry.pack(side="left",padx=(0,4)); _entry_wids.append(save_entry)

def save_theme():
    n=save_name_var.get().strip()
    if not n: messagebox.showerror("Error","Enter a name"); return
    if n in PRESETS: messagebox.showerror("Error","Built-in name"); return
    saved=load_saved_themes(); saved[n]=dict(COLORS)
    write_saved_themes(saved); refresh_preset_list(); messagebox.showinfo("Saved",f'"{n}" saved!')
def delete_theme():
    n=preset_var.get()
    if n in PRESETS or n=="── Saved ──": messagebox.showerror("Error","Can't delete built-in"); return
    saved=load_saved_themes()
    if n not in saved: messagebox.showerror("Error","Select a saved theme"); return
    del saved[n]; write_saved_themes(saved); refresh_preset_list()


btn_row=mk_bg(right); btn_row.pack(fill="x",pady=(4,0))
save_btn=tk.Button(btn_row,text="💾 Save",font=F(8,True),bg=COLORS["highlight"],fg=COLORS["btn_fg"],
                    relief="flat",bd=0,padx=8,pady=4,cursor="hand2",command=save_theme)
save_btn.pack(side="left",padx=(0,4))
BINDINGS.extend([(save_btn,"bg","highlight"),(save_btn,"fg","btn_fg")])
del_btn=tk.Button(btn_row,text="🗑",font=F(8,True),bg=COLORS["accent"],fg=COLORS["muted"],
                   relief="flat",bd=0,padx=8,pady=4,cursor="hand2",command=delete_theme)
del_btn.pack(side="left",padx=(0,4))
BINDINGS.extend([(del_btn,"bg","accent"),(del_btn,"fg","muted")])
folder_btn=tk.Button(btn_row,text="📁",font=F(8,True),bg=COLORS["accent"],fg=COLORS["muted"],
                      relief="flat",bd=0,padx=8,pady=4,cursor="hand2",command=open_data_folder)
folder_btn.pack(side="left")
BINDINGS.extend([(folder_btn,"bg","accent"),(folder_btn,"fg","muted")])

path_lbl=tk.Label(right,text=f"📁 {_DATA_DIR}",bg=COLORS["bg"],fg=COLORS["muted"],
                   font=("Consolas",7),anchor="w",wraplength=280,justify="left")
path_lbl.pack(anchor="w",pady=(4,0)); _muted_wids.append(path_lbl)

# ═══════════════════════════════════════════════════════
#  STATUS BAR
# ═══════════════════════════════════════════════════════
sb_div=tk.Frame(root,bg=COLORS["accent"],height=1); sb_div.pack(fill="x"); _accent_wids.append(sb_div)
status_frame=tk.Frame(root,bg=COLORS["panel"]); status_frame.pack(fill="x")
status_pip=tk.Frame(status_frame,bg=COLORS["highlight"],width=3); status_pip.pack(side="left",fill="y")
BINDINGS.append((status_pip,"bg","highlight"))
status_var=tk.StringVar(value=f"Ready  ·  {HOTKEY_NAME.upper()} to start")
status_bar=tk.Label(status_frame,textvariable=status_var,bg=COLORS["panel"],fg=COLORS["muted"],
                     font=("Consolas",9),anchor="w",padx=10,pady=5)
status_bar.pack(fill="x",side="left",expand=True)
BINDINGS.append((status_bar,"fg","muted"))

# ═══════════════════════════════════════════════════════
#  ANIMATIONS
# ═══════════════════════════════════════════════════════
def fade_in(alpha=0.0):
    alpha=min(alpha+0.08,1.0); root.attributes("-alpha",alpha)
    if alpha<1.0: root.after(16,lambda:fade_in(alpha))

_pulse_job=None; _pulse_phase=0.0
def start_pulse():
    global _pulse_job,_pulse_phase; _pulse_phase=0.0; _pulse_step()
def _pulse_step():
    global _pulse_job,_pulse_phase
    if not clicking: return
    _pulse_phase=(_pulse_phase+0.09)%(2*math.pi)
    t=(math.sin(_pulse_phase)+1)/2
    base=COLORS["highlight"].lstrip("#")
    r,g,b=int(base[0:2],16),int(base[2:4],16),int(base[4:6],16)
    pc="#{:02x}{:02x}{:02x}".format(int(r+(255-r)*0.35*t),int(g+(255-g)*0.35*t),int(b+(255-b)*0.35*t))
    try: toggle_btn.config(bg=pc)
    except Exception: pass
    _pulse_job=root.after(35,_pulse_step)
def stop_pulse():
    global _pulse_job
    if _pulse_job:
        try: root.after_cancel(_pulse_job)
        except Exception: pass
        _pulse_job=None
    try: toggle_btn.config(bg=COLORS["highlight"])
    except Exception: pass

_tick_job=None
def animate_counter():
    global _tick_job
    try:
        box=stat_boxes[0]
        for child in box.winfo_children():
            fnt=str(child.cget("font"))
            if "16" in fnt or ("bold" in fnt and "7" not in fnt):
                child.configure(fg=lighten(COLORS["stat_num"],0.5))
    except Exception: pass
    if _tick_job:
        try: root.after_cancel(_tick_job)
        except Exception: pass
    _tick_job=root.after(100,_tick_restore)
def _tick_restore():
    try:
        for child in stat_boxes[0].winfo_children():
            fnt=str(child.cget("font"))
            if "16" in fnt or ("bold" in fnt and "7" not in fnt):
                child.configure(fg=COLORS["stat_num"])
    except Exception: pass

_logo_phase=0.0
def logo_idle():
    global _logo_phase
    _logo_phase=(_logo_phase+0.035)%(2*math.pi)
    if not clicking and _canvas_logo_c is not None:
        try:
            t=(math.sin(_logo_phase)+1)/2
            col=COLORS["logo"].lstrip("#")
            r,g,b=int(col[0:2],16),int(col[2:4],16),int(col[4:6],16)
            s="#{:02x}{:02x}{:02x}".format(int(r+(255-r)*0.18*t),int(g+(255-g)*0.18*t),int(b+(255-b)*0.18*t))
            _canvas_logo_c.itemconfig("glint",fill=s)
        except Exception: pass
    root.after(50,logo_idle)

# ═══════════════════════════════════════════════════════
#  LAUNCH
# ═══════════════════════════════════════════════════════
root.protocol("WM_DELETE_WINDOW",do_close)
refresh_preset_list()
apply_theme()
draw_logo()
start_listener()

root.update_idletasks()
sw=root.winfo_screenwidth(); sh=root.winfo_screenheight()
rw=root.winfo_reqwidth();    rh=root.winfo_reqheight()
root.geometry(f"+{sw//2-rw//2}+{sh//2-rh//2}")

root.after(10,show_splash)
root.mainloop()

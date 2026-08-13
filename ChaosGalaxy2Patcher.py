import os
import json
import UnityPy
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import shutil
import re
import time

# --- Multilingual Translation Dictionary ---
TRANSLATIONS = {
    "TC": {
        "title": "宇宙戰略 2 - 全屬性修改器 v16.1",
        "file_setting": "1. 檔案設定", "browse": "瀏覽 resources.assets",
        "status_none": "請先載入檔案", "status_loading": "正在載入資源並建立備份...",
        "status_success": "✅ 成功載入 {0} 個單位", "search": "單位搜尋 (支援多選):",
        "edit_area": "2. 屬性編輯 (黃色=已修改)", "mod_list": "待存檔清單 (*):",
        "revert_all": "🔙 放棄所有修改", "save_btn": "💾 永久寫入並備份 (Batch Save)",
        "revert_unit": "🔙 復原選中單位", "copy_stats": "📋 複製屬性", "paste_stats": "📥 貼上屬性至選中單位",
        "quick_mod": "⚡ 批量修改:", "god_mode": "批量神化", "mass_prod": "批量量產",
        "exp_preview": "升級需求：\nLV2: {0} | LV3: {1} | LV4: {2}\nLV5: {3} | LV6: {4} | LV7: {5}",
        "msg_revert_confirm": "確定要放棄所有未存檔修改嗎？", "msg_save_success": "存檔成功！已寫入 {0} 個單位並建立備份。",
        "multi_select_info": "目前已選中 {0} 個單位 (批量模式)",
        "none": "無",
        "attr_labels": {
            "Power": "戰力:", "Energy": "能量:", "Agile": "運動性:", "Assault": "強襲:", "Bombardment": "轟炸:",
            "Vision": "視野:", "Move": "移動力:", "Cost": "統率消耗:", "Limit": "數量限制:", "BuildGold": "建造金幣:",
            "BuildSupply": "建造物資:", "BuildGene": "建造基因:", "UpkeepSupply": "維護物資:", "UpkeepGene": "維護基因:",
            "Value": "單位價值(EXP):", "DiscardSupply": "回收物資:", "DiscardGene": "回收基因:", "Rank": "等級:",
            "Model": "模型 ID:", "BaseColor": "底色 ID:", "Weapon1Count": "武1彈藥:", "Weapon2Count": "武2彈藥:",
            "Kind": "單位種類:", "Type": "單位類型:", "Organism": "生命特性:", "IsTeam": "編制模式:",
            "Ablity1": "技能 1:", "Ablity2": "技能 2:", "Ablity3": "技能 3:", "Weapon1": "武器 1:", "Weapon2": "武器 2:", "Shield": "護盾裝備:"
        },
        "kind_opts": ["0: 未知", "1: 艦船", "2: 機甲"],
        "type_opts": ["0: 無", "1: 護衛/驅逐", "2: 巡洋艦", "3: 戰列艦", "4: 航空母艦", "5: 突擊艦", "6: 要塞/堡壘", "7: 補給/特殊"],
        "organ_opts": ["0: 機械", "1: 生物", "2: 生化/異種"],
        "team_opts": ["0: 單機", "1: 小隊"], "lang_label": "介面語言 (Language):"
    },
    "CN": {
        "title": "宇宙战略 2 - 全属性修改器 v16.1",
        "file_setting": "1. 文件设定", "browse": "浏览 resources.assets",
        "status_none": "请先载入文件", "status_loading": "正在载入资源并建立备份...",
        "status_success": "✅ 成功载入 {0} 個单位", "search": "单位搜索 (支持多选):",
        "edit_area": "2. 属性编辑 (黄色=已修改)", "mod_list": "待存档清单 (*):",
        "revert_all": "🔙 放弃所有修改", "save_btn": "💾 永久写入并备份 (Batch Save)",
        "revert_unit": "🔙 复原选中单位", "copy_stats": "📋 复制属性", "paste_stats": "📥 粘贴属性至选中单位",
        "quick_mod": "⚡ 批量修改:", "god_mode": "批量神化", "mass_prod": "批量量产",
        "exp_preview": "升级需求：\nLV2: {0} | LV3: {1} | LV4: {2}\nLV5: {3} | LV6: {4} | LV7: {5}",
        "msg_revert_confirm": "确定要放弃所有未存档修改吗？", "msg_save_success": "存档成功！已写入 {0} 个单位并建立备份。",
        "multi_select_info": "目前已选中 {0} 个单位 (批量模式)",
        "none": "无",
        "attr_labels": {
            "Power": "战力:", "Energy": "能量:", "Agile": "运动性:", "Assault": "强袭:", "Bombardment": "轰炸:",
            "Vision": "视野:", "Move": "移动力:", "Cost": "统率消耗:", "Limit": "数量限制:", "BuildGold": "建造金币:",
            "BuildSupply": "建造物资:", "BuildGene": "建造基因:", "UpkeepSupply": "维护物资:", "UpkeepGene": "维护基因:",
            "Value": "单位价值(EXP):", "DiscardSupply": "回收物资:", "DiscardGene": "回收基因:", "Rank": "等级:",
            "Model": "模型 ID:", "BaseColor": "底色 ID:", "Weapon1Count": "武1弹药:", "Weapon2Count": "武2弹药:",
            "Kind": "单位种类:", "Type": "单位类型:", "Organism": "生命特性:", "IsTeam": "编制模式:",
            "Ablity1": "技能 1:", "Ablity2": "技能 2:", "Ablity3": "技能 3:", "Weapon1": "武器 1:", "Weapon2": "武器 2:", "Shield": "护盾装备:"
        },
        "kind_opts": ["0: 未知", "1: 舰船", "2: 机甲"],
        "type_opts": ["0: 无", "1: 护卫/驱逐", "2: 巡洋舰", "3: 战列舰", "4: 航空母舰", "5: 突击舰", "6: 要塞/堡壘", "7: 补给/特殊"],
        "organ_opts": ["0: 机械", "1: 生物", "2: 生化/异种"],
        "team_opts": ["0: 单机", "1: 小队"], "lang_label": "界面语言 (Language):"
    },
    "EN": {
        "title": "Chaos Galaxy 2 - Editor v16.1",
        "file_setting": "1. File Settings", "browse": "Browse resources.assets",
        "status_none": "Please load file", "status_loading": "Loading...",
        "status_success": "✅ Loaded {0} units", "search": "Search (Multi-select):",
        "edit_area": "2. Stats (Yellow = Mod)", "mod_list": "Pending (*):",
        "revert_all": "🔙 Discard All", "save_btn": "💾 Save & Backup (Batch)",
        "revert_unit": "🔙 Revert selected", "copy_stats": "📋 Copy Stats", "paste_stats": "📥 Paste to Selected",
        "quick_mod": "⚡ Batch Mod:", "god_mode": "God Mode", "mass_prod": "Mass Prod",
        "exp_preview": "EXP Req:\nLV2:{0} | LV3:{1} | LV4:{2}\nLV5:{3} | LV6:{4} | LV7:{5}",
        "msg_revert_confirm": "Discard all changes?", "msg_save_success": "Saved {0} units.",
        "multi_select_info": "{0} units selected",
        "none": "None",
        "attr_labels": {
            "Power": "Power:", "Energy": "Energy:", "Agile": "Agility:", "Assault": "Assault:", "Bombardment": "Bomb:",
            "Vision": "Vision:", "Move": "Move:", "Cost": "Cost:", "Limit": "Limit:", "BuildGold": "Gold:",
            "BuildSupply": "Supply:", "BuildGene": "Gene:", "UpkeepSupply": "Maint. Sup:", "UpkeepGene": "Maint. Gen:",
            "Value": "Value(EXP):", "DiscardSupply": "Refund Sup:", "DiscardGene": "Refund Gen:", "Rank": "Rank:",
            "Model": "Model ID:", "BaseColor": "Color ID:", "Weapon1Count": "W1 Ammo:", "Weapon2Count": "W2 Ammo:",
            "Kind": "Kind:", "Type": "Type:", "Organism": "Organism:", "IsTeam": "Squad:",
            "Ablity1": "Abil 1:", "Ablity2": "Abil 2:", "Ablity3": "Abil 3:", "Weapon1": "Wep 1:", "Weapon2": "Wep 2:", "Shield": "Shield:"
        },
        "kind_opts": ["0: Unk", "1: Ship", "2: Mecha"],
        "type_opts": ["0: None", "1: Escort", "2: Cruiser", "3: Battleship", "4: Carrier", "5: Assault", "6: Fortress", "7: Support"],
        "organ_opts": ["0: Mech", "1: Bio", "2: Hybrid"],
        "team_opts": ["0: Single", "1: Squad"], "lang_label": "Language:"
    }
}

class ChaosGalaxyEditor:
    def __init__(self, root):
        self.root = root
        self.config_file = "config.json"
        self.copy_buffer = {} 
        self.current_lang = "TC" 
        self.load_config() 
        
        self.env = None
        self.game_path = ""
        self.lang_dict = {"0": "None"}
        self.ability_map = {"0": "0: None"}
        self.shield_map = {"0": "0: None"}
        self.unit_xml_root = None
        self.original_xml_root = None
        self.current_item = None
        self.modified_indices = set()
        self.raw_xml_data = {"lang": "", "unit": "", "ab": "", "wp": ""}

        self.setup_ui()
        self.apply_language_ui() 

    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding='utf-8') as f:
                    self.current_lang = json.load(f).get("language", "TC")
            except: self.current_lang = "TC"

    def save_config(self):
        with open(self.config_file, "w", encoding='utf-8') as f: 
            json.dump({"language": self.current_lang}, f)

    def setup_ui(self):
        # 語言與檔案設定
        top_frame = tk.Frame(self.root); top_frame.pack(fill="x", padx=20, pady=5)
        self.lbl_lang_choice = tk.Label(top_frame); self.lbl_lang_choice.pack(side="left")
        self.cb_lang = ttk.Combobox(top_frame, values=["TC", "CN", "EN"], width=5, state="readonly")
        self.cb_lang.set(self.current_lang); self.cb_lang.pack(side="left", padx=5)
        self.cb_lang.bind("<<ComboboxSelected>>", self.handle_language_change)

        self.path_frame = tk.LabelFrame(self.root); self.path_frame.pack(fill="x", padx=20, pady=5)
        self.ent_path = tk.Entry(self.path_frame, state="readonly")
        self.ent_path.pack(side="left", expand=True, fill="x", padx=5, pady=5)
        self.btn_browse = tk.Button(self.path_frame, command=self.handle_select_file); self.btn_browse.pack(side="right", padx=5)
        self.lbl_status = tk.Label(self.root); self.lbl_status.pack()

        main_body = tk.Frame(self.root); main_body.pack(fill="both", expand=True, padx=20)

        # 左側總清單
        left_container = tk.Frame(main_body); left_container.pack(side="left", fill="both", expand=True)
        self.lbl_search = tk.Label(left_container); self.lbl_search.pack()
        self.ent_search = tk.Entry(left_container); self.ent_search.pack(fill="x", pady=2)
        self.ent_search.bind("<KeyRelease>", lambda e: self.refresh_ui_lists())
        
        list_frame_left = tk.Frame(left_container); list_frame_left.pack(fill="both", expand=True)
        self.unit_listbox = tk.Listbox(list_frame_left, font=("微软雅黑", 10), exportselection=False, selectmode=tk.EXTENDED)
        self.unit_listbox.pack(side="left", fill="both", expand=True)
        self.scroll_left = tk.Scrollbar(list_frame_left, orient="vertical", command=self.unit_listbox.yview)
        self.scroll_left.pack(side="right", fill="y")
        self.unit_listbox.config(yscrollcommand=self.scroll_left.set)
        self.unit_listbox.bind("<<ListboxSelect>>", self.handle_unit_selection)

        # 中間編輯區
        mid_frame = tk.Frame(main_body); mid_frame.pack(side="left", fill="both", padx=15)
        self.edit_frame = tk.LabelFrame(mid_frame); self.edit_frame.pack(fill="both", expand=True)

        self.ent_fields, self.cb_fields, self.field_labels = {}, {}, {}
        numeric_layout = [
            ["Power", "Energy", "Agile"], ["Assault", "Bombardment", "Vision"],
            ["Move", "Cost", "Limit"], ["BuildGold", "BuildSupply", "BuildGene"],
            ["UpkeepSupply", "UpkeepGene", "Value"], ["DiscardSupply", "DiscardGene", "Rank"],
            ["Model", "BaseColor", "Weapon1Count"], ["Weapon2Count"]
        ]
        for r, row in enumerate(numeric_layout):
            for c, attr in enumerate(row):
                if not attr: continue
                lbl = tk.Label(self.edit_frame); lbl.grid(row=r, column=c*2, padx=2, pady=2, sticky="e")
                self.field_labels[attr] = lbl
                ent = tk.Entry(self.edit_frame, width=10)
                ent.grid(row=r, column=c*2+1, padx=2, pady=2, sticky="w")
                self.ent_fields[attr] = ent
                ent.bind("<KeyRelease>", self.handle_realtime_modification)
                if attr == "Value": ent.bind("<KeyRelease>", self.handle_exp_calculation, add="+")

        self.lbl_exp_preview = tk.Label(self.edit_frame, text="", fg="#1976D2", font=("Consolas", 9, "bold"), justify="left")
        self.lbl_exp_preview.grid(row=8, column=1, columnspan=5, sticky="w")

        # 快速批量按鈕
        quick_frame = tk.Frame(self.edit_frame); quick_frame.grid(row=11, column=0, columnspan=6, pady=10)
        self.lbl_quick = tk.Label(quick_frame); self.lbl_quick.pack(side="left")
        self.btn_god = tk.Button(quick_frame, command=self.quick_mod_god, bg="#FFF9C4", font=("", 9, "bold")); self.btn_god.pack(side="left", padx=5)
        self.btn_mass = tk.Button(quick_frame, command=self.quick_mod_mass, bg="#C8E6C9", font=("", 9, "bold")); self.btn_mass.pack(side="left", padx=5)

        # 下拉選單
        self.drop_frame = tk.Frame(self.edit_frame); self.drop_frame.grid(row=9, column=0, columnspan=6, sticky="ew")
        for attr in ["Kind", "Type", "Organism", "IsTeam"]:
            lbl = tk.Label(self.drop_frame); lbl.pack(side="left", padx=2); self.field_labels[attr] = lbl
            cb = ttk.Combobox(self.drop_frame, width=10, state="readonly")
            cb.pack(side="left", padx=2); self.cb_fields[attr] = cb
            cb.bind("<<ComboboxSelected>>", self.handle_realtime_modification)

        self.eq_frame = tk.Frame(self.edit_frame); self.eq_frame.grid(row=10, column=0, columnspan=6, sticky="ew")
        for i, attr in enumerate(["Ablity1", "Ablity2", "Ablity3", "Weapon1", "Weapon2", "Shield"]):
            lbl = tk.Label(self.eq_frame); lbl.grid(row=i//3, column=(i%3)*2, sticky="e"); self.field_labels[attr] = lbl
            cb = ttk.Combobox(self.eq_frame, width=12, state="readonly")
            cb.grid(row=i//3, column=(i%3)*2+1, sticky="w", padx=2, pady=2); self.cb_fields[attr] = cb
            cb.bind("<<ComboboxSelected>>", self.handle_realtime_modification)

        # 右側暫存清單
        right_container = tk.Frame(main_body); right_container.pack(side="left", fill="both", expand=True)
        self.lbl_mod_title = tk.Label(right_container, font=("", 10, "bold")); self.lbl_mod_title.pack()
        list_frame_right = tk.Frame(right_container); list_frame_right.pack(fill="both", expand=True)
        self.mod_listbox = tk.Listbox(list_frame_right, bg="#FFF8E1", font=("微软雅黑", 10), exportselection=False, selectmode=tk.EXTENDED)
        self.mod_listbox.pack(side="left", fill="both", expand=True)
        self.scroll_right = tk.Scrollbar(list_frame_right, orient="vertical", command=self.mod_listbox.yview)
        self.scroll_right.pack(side="right", fill="y")
        self.mod_listbox.config(yscrollcommand=self.scroll_right.set)
        self.mod_listbox.bind("<<ListboxSelect>>", self.handle_mod_selection)
        
        # 右鍵選單
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Copy Stats", command=self.copy_unit_stats)
        self.context_menu.add_command(label="Paste Stats to All Selected", command=self.paste_unit_stats)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Revert Selected", command=self.handle_revert_selected)
        self.unit_listbox.bind("<Button-3>", self.show_context_menu); self.mod_listbox.bind("<Button-3>", self.show_context_menu)

        bottom_frame = tk.Frame(self.root); bottom_frame.pack(fill="x", pady=20)
        self.btn_revert_all = tk.Button(bottom_frame, command=self.handle_revert_all, bg="#F44336", fg="white"); self.btn_revert_all.pack(side="left", padx=50)
        self.btn_save = tk.Button(bottom_frame, command=self.handle_save_batch, bg="#2E7D32", fg="white", font=("", 12, "bold"), state="disabled"); self.btn_save.pack(side="right", padx=50)

    # --- 邏輯功能 ---
    def apply_language_ui(self):
        t = TRANSLATIONS.get(self.current_lang, TRANSLATIONS["TC"])
        self.root.title(t["title"]); self.lbl_lang_choice.config(text=t["lang_label"])
        self.path_frame.config(text=t["file_setting"]); self.btn_browse.config(text=t["browse"])
        if not self.game_path: self.lbl_status.config(text=t["status_none"])
        self.lbl_search.config(text=t["search"]); self.edit_frame.config(text=t["edit_area"])
        self.lbl_mod_title.config(text=t["mod_list"]); self.btn_revert_all.config(text=t["revert_all"])
        self.btn_save.config(text=t["save_btn"]); self.lbl_quick.config(text=t["quick_mod"])
        self.btn_god.config(text=t["god_mode"]); self.btn_mass.config(text=t["mass_prod"])
        self.context_menu.entryconfigure(0, label=t["copy_stats"]); self.context_menu.entryconfigure(1, label=t["paste_stats"])
        self.context_menu.entryconfigure(3, label=t["revert_unit"])
        for attr, lbl in self.field_labels.items(): lbl.config(text=t["attr_labels"].get(attr, attr))
        self.cb_fields["Kind"].config(values=t["kind_opts"]); self.cb_fields["Type"].config(values=t["type_opts"])
        self.cb_fields["Organism"].config(values=t["organ_opts"]); self.cb_fields["IsTeam"].config(values=t["team_opts"])
        if self.raw_xml_data["lang"]: self.handle_assets_reparse()

    def handle_language_change(self, event):
        self.current_lang = self.cb_lang.get(); self.save_config(); self.apply_language_ui()

    def handle_select_file(self):
        f = filedialog.askopenfilename(title="Select resources.assets", filetypes=[("Assets", "resources.assets")])
        if f:
            self.game_path = f; self.ent_path.config(state="normal"); self.ent_path.delete(0, tk.END); self.ent_path.insert(0, f); self.ent_path.config(state="readonly")
            self.load_assets_logic()

    def load_assets_logic(self):
        try:
            self.lbl_status.config(text=TRANSLATIONS[self.current_lang]["status_loading"]); self.root.update()
            with open(self.game_path, "rb") as f: self.env = UnityPy.load(f.read())
            for obj in self.env.objects:
                if obj.type.name == "TextAsset":
                    d = obj.read(); n = (getattr(d, "name", "") or getattr(d, "m_Name", "") or "").lower()
                    if not n and obj.container: n = os.path.basename(obj.container).lower()
                    c = getattr(d, "m_Script", "") or getattr(d, "text", "")
                    if "languagedata" in n: self.raw_xml_data["lang"] = c
                    elif "unttypedata" in n or "unittypedata" in n: self.target_obj = obj; self.raw_xml_data["unit"] = c
                    elif "unitabilitydata" in n: self.raw_xml_data["ab"] = c
                    elif "unitweapondata" in n: self.raw_xml_data["wp"] = c
            self.unit_xml_root = ET.fromstring(self.raw_xml_data["unit"].strip().encode('utf-8').decode('utf-8-sig'))
            self.original_xml_root = ET.fromstring(self.raw_xml_data["unit"].strip().encode('utf-8').decode('utf-8-sig'))
            self.handle_assets_reparse(); self.btn_save.config(state="normal")
        except Exception as e: messagebox.showerror("Error", str(e))

    def handle_assets_reparse(self):
        def safe_p(s): return ET.fromstring(s.strip().encode('utf-8').decode('utf-8-sig'))
        lr = safe_p(self.raw_xml_data["lang"]); self.lang_dict = {"0": TRANSLATIONS[self.current_lang]["none"]}
        for i, it in enumerate(lr.findall(".//Item")): self.lang_dict[str(i+1)] = it.get(self.current_lang) or it.get("TC") or "???"
        def build_m(x, t):
            if not x: return
            r = safe_p(x)
            for it in r.findall(".//Item"): idx = it.get("Index"); t[idx] = f"{idx}: {self.lang_dict.get(it.get('Name'), '???')}"
        self.ability_map, self.shield_map = {"0": f"0: {TRANSLATIONS[self.current_lang]['none']}"}, {"0": f"0: {TRANSLATIONS[self.current_lang]['none']}"}
        build_m(self.raw_xml_data["ab"], self.ability_map); build_m(self.raw_xml_data["wp"], self.shield_map)
        for k in ["Ablity1", "Ablity2", "Ablity3"]: self.cb_fields[k]['values'] = sorted(list(self.ability_map.values()), key=lambda x: int(x.split(":")[0]))
        for k in ["Weapon1", "Weapon2", "Shield"]: self.cb_fields[k]['values'] = sorted(list(self.shield_map.values()), key=lambda x: int(x.split(":")[0]))
        self.refresh_ui_lists()
        if self.current_item is not None: self.load_unit_ui(self.current_item.get("Index"))
        self.lbl_status.config(text=TRANSLATIONS[self.current_lang]["status_success"].format(len(self.unit_xml_root.findall('.//Item'))), fg="green")

    def get_selected_ids(self, lb):
        ids = []
        for i in lb.curselection():
            m = re.search(r'\[(\d+)\]', lb.get(i))
            if m: ids.append(m.group(1))
        return ids

    def handle_realtime_modification(self, e=None):
        if self.current_item is None: return
        idx = self.current_item.get("Index")
        for a, ent in self.ent_fields.items():
            self.current_item.set(a, ent.get())
            if "Discard" in a: self.current_item.set(a.replace("Discard", "Disband"), ent.get())
        for a, cb in self.cb_fields.items(): self.current_item.set(a, cb.get().split(":")[0])
        self.modified_indices.add(idx); self.highlight_field_changes()
        y = self.unit_listbox.yview()[0]; self.refresh_ui_lists(); self.unit_listbox.yview_moveto(y)

    def highlight_field_changes(self):
        if self.current_item is None: return
        idx = self.current_item.get("Index")
        orig = next(it for it in self.original_xml_root.findall(".//Item") if int(it.get("Index")) == int(idx))
        for a, ent in self.ent_fields.items():
            curr, o_val = ent.get(), orig.get(a) or orig.get(a.replace("Discard", "Disband"), "0")
            ent.config(bg="#FFF9C4" if curr != o_val else "white", fg="red" if curr != o_val else "black", font=("", 9, "bold" if curr != o_val else "normal"))
        for a, cb in self.cb_fields.items():
            curr, o_val = cb.get().split(":")[0], orig.get(a, "0")
            cb.config(background="#FFF9C4" if curr != o_val else "white")

    def refresh_ui_lists(self):
        kw = self.ent_search.get().lower(); self.unit_listbox.delete(0, tk.END); self.mod_listbox.delete(0, tk.END)
        for it in self.unit_xml_root.findall(".//Item"):
            idx, name = it.get("Index"), self.lang_dict.get(it.get("Name"), "???")
            disp = f"[{idx.zfill(3)}] {name}"
            if not kw or kw in disp.lower(): self.unit_listbox.insert(tk.END, disp + (" *" if idx in self.modified_indices else ""))
            if idx in self.modified_indices: self.mod_listbox.insert(tk.END, disp)

    def handle_unit_selection(self, e):
        ids = self.get_selected_ids(self.unit_listbox)
        if len(ids) == 1: self.load_unit_ui(ids[0])
        elif len(ids) > 1: self.edit_frame.config(text=TRANSLATIONS[self.current_lang]["multi_select_info"].format(len(ids)))

    def handle_mod_selection(self, e):
        ids = self.get_selected_ids(self.mod_listbox)
        if len(ids) == 1: self.load_unit_ui(ids[0])

    def load_unit_ui(self, idx):
        try:
            self.current_item = next(it for it in self.unit_xml_root.findall(".//Item") if int(it.get("Index")) == int(idx))
            self.edit_frame.config(text=f"Editing: [{self.current_item.get('Index')}] {self.lang_dict.get(self.current_item.get('Name'), '???')}")
            for a, e in self.ent_fields.items():
                e.delete(0, tk.END); e.insert(0, self.current_item.get(a) or self.current_item.get(a.replace("Discard", "Disband"), "0"))
            for a, c in self.cb_fields.items():
                val = self.current_item.get(a, "0")
                if a in ["Kind", "Type", "Organism", "IsTeam"]:
                    c.set(next((o for o in c['values'] if o.startswith(f"{val}:")), c['values'][0]))
                else: c.set(self.ability_map.get(val, f"{val}: ???"))
            self.highlight_field_changes(); self.handle_exp_calculation()
        except: pass

    def handle_exp_calculation(self, e=None):
        try:
            val = int(self.ent_fields["Value"].get()); t = TRANSLATIONS[self.current_lang]
            lv = [val+1000, val*3+3000, val*6+6000, val*10+10000, val*16+15000, val*24+20000]
            self.lbl_exp_preview.config(text=t["exp_preview"].format(*lv))
        except: self.lbl_exp_preview.config(text="")

    def quick_mod_god(self):
        ids = self.get_selected_ids(self.unit_listbox)
        for uid in ids:
            item = next(it for it in self.unit_xml_root.findall(".//Item") if int(it.get("Index")) == int(uid))
            for a, v in {"Power":"9999","Energy":"9999","Agile":"999","Assault":"999","Bombardment":"999","Move":"9","Vision":"50"}.items(): item.set(a,v)
            self.modified_indices.add(item.get("Index"))
        if ids: self.load_unit_ui(ids[0]); self.refresh_ui_lists()

    def quick_mod_mass(self):
        ids = self.get_selected_ids(self.unit_listbox)
        for uid in ids:
            item = next(it for it in self.unit_xml_root.findall(".//Item") if int(it.get("Index")) == int(uid))
            for a, v in {"Limit":"0","BuildGold":"1","BuildSupply":"1","BuildGene":"0","Cost":"1"}.items(): item.set(a,v)
            self.modified_indices.add(item.get("Index"))
        if ids: self.load_unit_ui(ids[0]); self.refresh_ui_lists()

    def copy_unit_stats(self):
        if self.current_item is not None:
            self.copy_buffer = {a: self.current_item.get(a) for a in self.current_item.attrib if a not in ["Index", "Name"]}
            messagebox.showinfo("Copy", "Copied!")

    def paste_unit_stats(self):
        ids = self.get_selected_ids(self.unit_listbox)
        for uid in ids:
            item = next(it for it in self.unit_xml_root.findall(".//Item") if int(it.get("Index")) == int(uid))
            for a, v in self.copy_buffer.items(): item.set(a, v)
            self.modified_indices.add(item.get("Index"))
        if ids: self.load_unit_ui(ids[0]); self.refresh_ui_lists()

    def handle_revert_selected(self):
        ids = self.get_selected_ids(self.mod_listbox) or self.get_selected_ids(self.unit_listbox)
        for uid in ids:
            orig = next(it for it in self.original_xml_root.findall(".//Item") if int(it.get("Index")) == int(uid))
            target = next(it for it in self.unit_xml_root.findall(".//Item") if int(it.get("Index")) == int(uid))
            for k, v in orig.attrib.items(): target.set(k, v)
            if target.get("Index") in self.modified_indices: self.modified_indices.remove(target.get("Index"))
        self.refresh_ui_lists()

    def handle_revert_all(self):
        if messagebox.askyesno("Revert", TRANSLATIONS[self.current_lang]["msg_revert_confirm"]):
            self.unit_xml_root = ET.fromstring(ET.tostring(self.original_xml_root)); self.modified_indices.clear(); self.current_item = None; self.refresh_ui_lists()

    def handle_save_batch(self):
        if not self.modified_indices: return
        try:
            shutil.copy(self.game_path, f"{self.game_path}.{time.strftime('%Y%m%d_%H%M%S')}.bak")
            new_xml = ET.tostring(self.unit_xml_root, encoding='utf-8', xml_declaration=True).decode('utf-8')
            ud = self.target_obj.read()
            if hasattr(ud, "m_Script"): ud.m_Script = new_xml
            else: ud.text = new_xml
            ud.save()
            with open(self.game_path, "wb") as f:
                f.write(self.env.file.save())
            self.original_xml_root = ET.fromstring(new_xml.strip().encode('utf-8').decode('utf-8-sig'))
            count = len(self.modified_indices); self.modified_indices.clear(); self.refresh_ui_lists()
            messagebox.showinfo("Success", TRANSLATIONS[self.current_lang]["msg_save_success"].format(count))
        except Exception as e: messagebox.showerror("Save Error", str(e))

    def show_context_menu(self, event):
        if event.widget.curselection(): self.context_menu.post(event.x_root, event.y_root)

if __name__ == "__main__":
    root = tk.Tk(); app = ChaosGalaxyEditor(root); root.mainloop()
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageDraw, ImageFont, ImageTk, ImageFilter
import random
import os
import numpy as np
from tkinter import font as tkfont

class ModernCaptchaGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ 验证码生成器 ✨")
        self.root.geometry("600x700")
        self.root.configure(bg="#f0f2f5")
        
        # 初始化变量
        self.type_var = tk.StringVar(value="alnum")
        self.diff_var = tk.StringVar(value="中等")
        self.current_img = None
        self.font = None
        self.img_size = (400, 150)
        
        # 自定义干扰强度配置
        self.custom_config = {
            "lines": 5,
            "shapes": 3, 
            "blur": 1,
            "noise_text": 2
        }
        
        # 干扰强度预设
        self.difficulty_presets = {
            "简单": {"lines": 3, "shapes": 2, "blur": 0, "noise_text": 1},
            "中等": {"lines": 5, "shapes": 3, "blur": 1, "noise_text": 2},
            "困难": {"lines": 8, "shapes": 5, "blur": 2, "noise_text": 3},
            "自定义": self.custom_config
        }
        
        # 汉语词库 (200+个常用词)
        self.chinese_words = [
            # 水果
            "苹果", "香蕉", "橙子", "西瓜", "葡萄", "草莓", "菠萝", "芒果", "桃子", "梨子",
            "柠檬", "荔枝", "龙眼", "柿子", "石榴", "樱桃", "蓝莓", "猕猴桃", "哈密瓜", "椰子",
            
            # 动物
            "大象", "老虎", "狮子", "熊猫", "长颈鹿", "猴子", "斑马", "河马", "犀牛", "袋鼠",
            "孔雀", "鹦鹉", "鸵鸟", "企鹅", "海豚", "鲸鱼", "鲨鱼", "海龟", "章鱼", "螃蟹",
            
            # 交通工具
            "汽车", "飞机", "火车", "轮船", "自行车", "摩托车", "公交车", "出租车", "地铁", "卡车",
            "拖拉机", "直升机", "帆船", "潜艇", "火箭", "热气球", "滑板车", "轮椅", "雪橇", "马车",
            
            # 家电
            "电脑", "手机", "电视", "冰箱", "空调", "洗衣机", "微波炉", "电风扇", "吸尘器", "电饭煲",
            "烤箱", "榨汁机", "吹风机", "剃须刀", "电熨斗", "加湿器", "空气炸锅", "扫地机器人", "投影仪", "音响",
            
            # 城市
            "北京", "上海", "广州", "深圳", "杭州", "成都", "重庆", "武汉", "西安", "南京",
            "天津", "苏州", "厦门", "青岛", "大连", "长沙", "郑州", "沈阳", "哈尔滨", "昆明",
            
            # 天气
            "春天", "夏天", "秋天", "冬天", "晴天", "雨天", "阴天", "雪天", "雾天", "台风",
            "彩虹", "冰雹", "霜冻", "干旱", "洪水", "沙尘暴", "龙卷风", "寒潮", "暖冬", "梅雨",
            
            # 颜色
            "红色", "蓝色", "绿色", "黄色", "白色", "黑色", "紫色", "粉色", "灰色", "棕色",
            "橙色", "金色", "银色", "青色", "米色", "咖啡色", "藏青色", "天蓝色", "玫红色", "墨绿色",
            
            # 职业
            "医生", "老师", "警察", "工人", "农民", "司机", "厨师", "护士", "律师", "记者",
            "演员", "歌手", "作家", "画家", "科学家", "工程师", "程序员", "设计师", "运动员", "飞行员",
            
            # 运动
            "跑步", "游泳", "篮球", "足球", "网球", "乒乓球", "羽毛球", "排球", "高尔夫", "滑雪",
            "滑冰", "跳水", "体操", "拳击", "击剑", "射箭", "举重", "柔道", "跆拳道", "自行车",
            
            # 艺术
            "音乐", "电影", "书籍", "绘画", "舞蹈", "戏剧", "摄影", "雕塑", "建筑", "设计",
            "诗歌", "小说", "散文", "书法", "国画", "油画", "版画", "陶艺", "剪纸", "刺绣",
            
            # 情感
            "高兴", "悲伤", "愤怒", "惊讶", "恐惧", "厌恶", "期待", "信任", "怀疑", "爱慕",
            "思念", "嫉妒", "羞愧", "骄傲", "孤独", "幸福", "痛苦", "焦虑", "平静", "兴奋"
        ]
        
        # 英语词库 (200+个常用短单词)
        self.english_words = [
            # 水果
            "apple", "banana", "orange", "grape", "pear", "peach", "lemon", "melon", "berry", "kiwi",
            "mango", "papaya", "cherry", "plum", "fig", "date", "lime", "pear", "quince", "prune",
            
            # 动物
            "dog", "cat", "bird", "fish", "lion", "tiger", "bear", "wolf", "fox", "deer",
            "frog", "duck", "goose", "swan", "owl", "eagle", "shark", "whale", "dolphin", "seal",
            
            # 交通工具
            "car", "bus", "train", "ship", "plane", "bike", "boat", "truck", "taxi", "subway",
            "jeep", "yacht", "canoe", "ferry", "scooter", "tram", "van", "cart", "sled", "raft",
            
            # 日常物品
            "book", "pen", "pencil", "paper", "desk", "chair", "table", "lamp", "door", "window",
            "clock", "phone", "watch", "glass", "plate", "bowl", "knife", "spoon", "fork", "cup",
            
            # 家居
            "house", "home", "room", "kitchen", "bath", "bed", "sofa", "wall", "floor", "roof",
            "shelf", "mirror", "couch", "stove", "fridge", "sink", "toilet", "shower", "curtain", "carpet",
            
            # 颜色
            "red", "blue", "green", "yellow", "black", "white", "pink", "gray", "brown", "purple",
            "orange", "gold", "silver", "violet", "indigo", "maroon", "navy", "teal", "olive", "cyan",
            
            # 自然
            "sun", "moon", "star", "sky", "cloud", "rain", "snow", "wind", "storm", "fog",
            "tree", "flower", "grass", "leaf", "rock", "sand", "hill", "lake", "river", "ocean",
            
            # 情感
            "love", "like", "hate", "happy", "sad", "angry", "kind", "good", "bad", "nice",
            "calm", "brave", "proud", "shy", "fear", "hope", "pain", "joy", "rage", "envy",
            
            # 尺寸
            "big", "small", "long", "short", "tall", "wide", "narrow", "high", "low", "deep",
            "thin", "thick", "fat", "slim", "huge", "tiny", "giant", "petite", "vast", "mini",
            
            # 数字
            "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
            "zero", "first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth",
            
            # 动作
            "run", "walk", "jump", "swim", "play", "read", "write", "sing", "dance", "draw",
            "eat", "drink", "sleep", "talk", "laugh", "cry", "think", "study", "work", "drive",
            
            # 食物
            "food", "meal", "rice", "meat", "soup", "egg", "milk", "tea", "cake", "bread",
            "fish", "beef", "pork", "chicken", "salad", "pizza", "pasta", "cheese", "butter", "fruit"
        ]
        
        # 验证码类型选项
        self.type_options = {
            "chinese": "纯中文",
            "mixed": "中英混合",
            "alnum": "字母数字",
            "chinese_word": "汉语单词",
            "english_word": "英语单词"
        }
        
        # 初始化语言设置
        self.current_language = "简体中文"
        self.languages = {
            "简体中文": self.setup_chinese_simplified,
            "繁体中文": self.setup_chinese_traditional,
            "English": self.setup_english,
            "日本語": self.setup_japanese,
            "한국어": self.setup_korean
        }
        self.setup_chinese_simplified()
        
        # 创建UI
        self.create_widgets()
        
        # 加载字体
        self.font = self.load_font()

    def create_widgets(self):
        """创建所有UI组件"""
        self.create_menu()
        self.create_main_frame()
        self.create_input_section()
        self.create_options_section()
        self.create_button_section()
        self.create_image_section()
        self.configure_styles()

    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        
        # 语言菜单
        language_menu = tk.Menu(menubar, tearoff=0)
        for lang in self.languages:
            language_menu.add_command(
                label=lang,
                command=lambda l=lang: self.change_language(l)
            )
        menubar.add_cascade(label="语言/Language", menu=language_menu)
        
        # 干扰强度设置菜单
        config_menu = tk.Menu(menubar, tearoff=0)
        config_menu.add_command(
            label=self.ui_text["config_menu"],
            command=self.edit_custom_config
        )
        menubar.add_cascade(label=self.ui_text["config_menu"], menu=config_menu)
        
        self.root.config(menu=menubar)

    def create_main_frame(self):
        """创建主框架"""
        self.main_frame = ttk.Frame(self.root, style="Card.TFrame")
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # 标题
        self.title_label = ttk.Label(
            self.main_frame, 
            text=self.ui_text["title"],
            font=("Helvetica", 18, "bold"),
            style="Title.TLabel"
        )
        self.title_label.pack(pady=(20, 10))

    def create_input_section(self):
        """创建输入区域"""
        input_frame = ttk.Frame(self.main_frame, style="Card.TFrame")
        input_frame.pack(pady=10, padx=20, fill="x")
        
        self.content_label = ttk.Label(input_frame, text=self.ui_text["content_label"])
        self.content_label.pack(anchor="w", padx=10, pady=(10,0))
        
        self.entry = ttk.Entry(input_frame, width=30)
        self.entry.pack(padx=10, pady=(0,10), fill="x")
        
        self.length_label = ttk.Label(input_frame, text=self.ui_text["length_label"])
        self.length_label.pack(anchor="w", padx=10)
        
        self.length_entry = ttk.Entry(input_frame, width=5)
        self.length_entry.insert(0, "0")
        self.length_entry.pack(anchor="w", padx=10, pady=(0,10))

    def create_options_section(self):
        """创建选项区域"""
        options_frame = ttk.Frame(self.main_frame, style="Card.TFrame")
        options_frame.pack(pady=10, padx=20, fill="x")
        
        # 验证码类型选择
        self.type_label = ttk.Label(options_frame, text=self.ui_text["type_label"])
        self.type_label.pack(anchor="w", padx=10, pady=(10,5))
        
        type_frame = ttk.Frame(options_frame)
        type_frame.pack(padx=10, pady=5, fill="x")
        
        # 动态生成类型选项
        for value, text in self.type_options.items():
            ttk.Radiobutton(
                type_frame, 
                text=text, 
                variable=self.type_var, 
                value=value
            ).pack(side="left", padx=5)
        
        # 干扰强度选择
        self.difficulty_label = ttk.Label(options_frame, text=self.ui_text["difficulty_label"])
        self.difficulty_label.pack(anchor="w", padx=10, pady=(10,5))
        
        diff_frame = ttk.Frame(options_frame)
        diff_frame.pack(padx=10, pady=(5,10), fill="x")
        
        ttk.Radiobutton(
            diff_frame, 
            text=self.ui_text["easy"], 
            variable=self.diff_var, 
            value="简单"
        ).pack(side="left", padx=5)
        
        ttk.Radiobutton(
            diff_frame, 
            text=self.ui_text["medium"], 
            variable=self.diff_var, 
            value="中等"
        ).pack(side="left", padx=5)
        
        ttk.Radiobutton(
            diff_frame, 
            text=self.ui_text["hard"], 
            variable=self.diff_var, 
            value="困难"
        ).pack(side="left", padx=5)
        
        ttk.Radiobutton(
            diff_frame,
            text=self.ui_text["custom"],
            variable=self.diff_var,
            value="自定义"
        ).pack(side="left", padx=5)

    def create_button_section(self):
        """创建按钮区域"""
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=10, fill="x")
        
        self.generate_btn = ttk.Button(
            button_frame,
            text=self.ui_text["generate"],
            style="Primary.TButton",
            command=self.generate
        )
        self.generate_btn.pack(side="left", padx=10, expand=True, fill="x")
        
        self.random_btn = ttk.Button(
            button_frame,
            text=self.ui_text["random"],
            style="Secondary.TButton",
            command=self.random_gen
        )
        self.random_btn.pack(side="left", padx=10, expand=True, fill="x")

    def create_image_section(self):
        """创建图片显示区域"""
        image_frame = ttk.Frame(self.main_frame, style="Card.TFrame")
        image_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.preview_label = ttk.Label(image_frame, text=self.ui_text["preview"])
        self.preview_label.pack(anchor="w", padx=10, pady=(10,0))
        
        # 图片显示
        self.img_label = ttk.Label(image_frame, background="white")
        self.img_label.pack(pady=10, padx=10, fill="both", expand=True)
        
        # 保存按钮
        self.save_btn = ttk.Button(
            image_frame,
            text=self.ui_text["save"],
            style="Primary.TButton",
            command=self.save
        )
        self.save_btn.pack(pady=(0,10), padx=10, fill="x")

    def configure_styles(self):
        """配置UI样式"""
        style = ttk.Style()
        style.theme_use("clam")
        
        # 卡片样式
        style.configure("Card.TFrame", 
                      background="white", 
                      borderwidth=2, 
                      relief="groove",
                      bordercolor="#d1d8e0")
        
        # 标题样式
        style.configure("Title.TLabel", 
                      foreground="#3d5af1", 
                      background="white")
        
        # 按钮样式
        style.configure("Primary.TButton", 
                      foreground="white", 
                      background="#3d5af1",
                      font=("Helvetica", 12),
                      padding=10)
        style.map("Primary.TButton",
                background=[("active", "#3651d6")])
        
        style.configure("Secondary.TButton",
                     foreground="white",
                     background="#22d1ee",
                     font=("Helvetica", 12),
                     padding=10)
        style.map("Secondary.TButton",
                background=[("active", "#1cb8d1")])
        
        # 单选按钮样式
        style.configure("TRadiobutton", 
                     background="white",
                     font=("Helvetica", 10))
        
        # 标签样式
        style.configure("TLabel", 
                     background="white",
                     font=("Helvetica", 10))
        
        # 输入框样式
        style.configure("TEntry",
                     fieldbackground="white",
                     bordercolor="#d1d8e0",
                     lightcolor="#d1d8e0",
                     darkcolor="#d1d8e0")

    def load_font(self):
        """加载字体，增强兼容性"""
        try:
            # 尝试加载中文字体
            chinese_font = ImageFont.truetype("simhei.ttf", 30)
        except:
            # 如果找不到字体文件，尝试使用系统默认字体
            try:
                # 使用tkinter的系统字体
                default_font = tkfont.nametofont("TkDefaultFont")
                font_path = default_font.actual()["family"]
                chinese_font = ImageFont.truetype(font_path, 30)
            except:
                # 如果所有尝试都失败，使用PIL默认字体
                chinese_font = ImageFont.load_default()
        
        try:
            # 尝试加载英文字体
            alnum_font = ImageFont.truetype("arial.ttf", 30)
        except:
            try:
                # 尝试使用TkDefaultFont作为英文字体
                default_font = tkfont.nametofont("TkDefaultFont")
                font_path = default_font.actual()["family"]
                alnum_font = ImageFont.truetype(font_path, 30)
            except:
                alnum_font = ImageFont.load_default()
        
        return {
            "chinese": chinese_font,
            "alnum": alnum_font,
            "mixed": chinese_font,
            "chinese_word": chinese_font,
            "english_word": alnum_font
        }

    def setup_chinese_simplified(self):
        """简体中文语言设置"""
        self.ui_text = {
            "title": "验证码生成器",
            "content_label": "验证码内容 (最多8位):",
            "length_label": "随机长度 (1-8, 0=随机):",
            "type_label": "验证码类型:",
            "difficulty_label": "干扰强度:",
            "easy": "简单",
            "medium": "中等",
            "hard": "困难",
            "custom": "自定义",
            "generate": "生成验证码",
            "random": "随机生成",
            "preview": "验证码预览:",
            "save": "保存图片",
            "warning": "提示",
            "content_warning": "请输入1-8位验证码内容",
            "save_success": "图片已保存到:\n{}",
            "save_error": "保存失败:\n{}",
            "config_title": "自定义干扰强度设置",
            "lines_label": "干扰线条数量:",
            "shapes_label": "干扰形状数量:",
            "blur_label": "模糊程度(0-5):",
            "noise_label": "干扰文字数量:",
            "save_btn": "保存",
            "config_success": "自定义干扰强度设置已保存",
            "config_error": "请输入有效的数字",
            "config_menu": "干扰强度设置",
            "type_options": {
                "chinese": "纯中文",
                "mixed": "中英混合",
                "alnum": "字母数字",
                "chinese_word": "汉语单词", 
                "english_word": "英语单词"
            }
        }
        self.type_options = self.ui_text["type_options"]

    def setup_chinese_traditional(self):
        """繁体中文语言设置"""
        self.ui_text = {
            "title": "驗證碼生成器",
            "content_label": "驗證碼內容 (最多8位):",
            "length_label": "隨機長度 (1-8, 0=隨機):",
            "type_label": "驗證碼類型:",
            "difficulty_label": "幹擾強度:",
            "easy": "簡單",
            "medium": "中等",
            "hard": "困難",
            "custom": "自定義",
            "generate": "生成驗證碼",
            "random": "隨機生成",
            "preview": "驗證碼預覽:",
            "save": "保存圖片",
            "warning": "提示",
            "content_warning": "請輸入1-8位驗證碼內容",
            "save_success": "圖片已保存到:\n{}",
            "save_error": "保存失敗:\n{}",
            "config_title": "自定義幹擾強度設置",
            "lines_label": "幹擾線條數量:",
            "shapes_label": "幹擾形狀數量:",
            "blur_label": "模糊程度(0-5):",
            "noise_label": "幹擾文字數量:",
            "save_btn": "保存",
            "config_success": "自定義幹擾強度設置已保存",
            "config_error": "請輸入有效的數字",
            "config_menu": "幹擾強度設置",
            "type_options": {
                "chinese": "純中文",
                "mixed": "中英混合",
                "alnum": "字母數字",
                "chinese_word": "漢語單詞", 
                "english_word": "英語單詞"
            }
        }
        self.type_options = self.ui_text["type_options"]

    def setup_english(self):
        """英语语言设置"""
        self.ui_text = {
            "title": "CAPTCHA Generator",
            "content_label": "CAPTCHA Content (max 8 chars):",
            "length_label": "Random Length (1-8, 0=random):",
            "type_label": "CAPTCHA Type:",
            "difficulty_label": "Noise Level:",
            "easy": "Easy",
            "medium": "Medium",
            "hard": "Hard",
            "custom": "Custom",
            "generate": "Generate CAPTCHA",
            "random": "Random Generate",
            "preview": "CAPTCHA Preview:",
            "save": "Save Image",
            "warning": "Warning",
            "content_warning": "Please enter 1-8 characters",
            "save_success": "Image saved to:\n{}",
            "save_error": "Save failed:\n{}",
            "config_title": "Custom Noise Settings",
            "lines_label": "Noise Lines:",
            "shapes_label": "Noise Shapes:",
            "blur_label": "Blur Level (0-5):",
            "noise_label": "Noise Text Count:",
            "save_btn": "Save",
            "config_success": "Custom noise settings saved",
            "config_error": "Please enter valid numbers",
            "config_menu": "Noise Settings",
            "type_options": {
                "chinese": "Chinese Only",
                "mixed": "Mixed Chinese-English",
                "alnum": "Alphanumeric",
                "chinese_word": "Chinese Word",
                "english_word": "English Word"
            }
        }
        self.type_options = self.ui_text["type_options"]

    def setup_japanese(self):
        """日语语言设置"""
        self.ui_text = {
            "title": "CAPTCHA ジェネレーター",
            "content_label": "CAPTCHA 内容 (最大8文字):",
            "length_label": "ランダム長さ (1-8, 0=ランダム):",
            "type_label": "CAPTCHA タイプ:",
            "difficulty_label": "ノイズレベル:",
            "easy": "簡単",
            "medium": "中級",
            "hard": "難しい",
            "custom": "カスタム",
            "generate": "CAPTCHA生成",
            "random": "ランダム生成",
            "preview": "CAPTCHA プレビュー:",
            "save": "画像保存",
            "warning": "警告",
            "content_warning": "1-8文字を入力してください",
            "save_success": "画像を保存しました:\n{}",
            "save_error": "保存に失敗しました:\n{}",
            "config_title": "カスタムノイズ設定",
            "lines_label": "ノイズ線数:",
            "shapes_label": "ノイズ形状数:",
            "blur_label": "ぼかし度(0-5):",
            "noise_label": "ノイズテキスト数:",
            "save_btn": "保存",
            "config_success": "カスタムノイズ設定を保存しました",
            "config_error": "有効な数字を入力してください",
            "config_menu": "ノイズ設定",
            "type_options": {
                "chinese": "中国語のみ",
                "mixed": "中国語-英語混合",
                "alnum": "英数字",
                "chinese_word": "中国語単語",
                "english_word": "英語単語"
            }
        }
        self.type_options = self.ui_text["type_options"]

    def setup_korean(self):
        """韩语语言设置"""
        self.ui_text = {
            "title": "CAPTCHA 생성기",
            "content_label": "CAPTCHA 내용 (최대 8자):",
            "length_label": "랜덤 길이 (1-8, 0=랜덤):",
            "type_label": "CAPTCHA 유형:",
            "difficulty_label": "노이즈 레벨:",
            "easy": "쉬움",
            "medium": "중간",
            "hard": "어려움",
            "custom": "사용자 정의",
            "generate": "CAPTCHA 생성",
            "random": "랜덤 생성",
            "preview": "CAPTCHA 미리보기:",
            "save": "이미지 저장",
            "warning": "경고",
            "content_warning": "1-8자를 입력하세요",
            "save_success": "이미지가 저장되었습니다:\n{}",
            "save_error": "저장 실패:\n{}",
            "config_title": "사용자 정의 노이즈 설정",
            "lines_label": "노이즈 선 수:",
            "shapes_label": "노이즈 모양 수:",
            "blur_label": "흐림 정도(0-5):",
            "noise_label": "노이즈 텍스트 수:",
            "save_btn": "저장",
            "config_success": "사용자 정의 노이즈 설정이 저장되었습니다",
            "config_error": "유효한 숫자를 입력하세요",
            "config_menu": "노이즈 설정",
            "type_options": {
                "chinese": "중국어 전용",
                "mixed": "중국어-영어 혼합",
                "alnum": "영숫자",
                "chinese_word": "중국어 단어",
                "english_word": "영어 단어"
            }
        }
        self.type_options = self.ui_text["type_options"]

    def change_language(self, language):
        """切换语言"""
        self.current_language = language
        self.languages[language]()
        self.update_ui_text()

    def update_ui_text(self):
        """更新UI文本"""
        # 更新标题
        self.title_label.config(text=self.ui_text["title"])
        
        # 更新输入区域
        self.content_label.config(text=self.ui_text["content_label"])
        self.length_label.config(text=self.ui_text["length_label"])
        
        # 更新选项区域
        self.type_label.config(text=self.ui_text["type_label"])
        
        # 更新类型单选按钮
        for widget in self.type_label.master.winfo_children():
            if isinstance(widget, ttk.Radiobutton):
                widget.config(text=self.type_options[widget.cget("value")])
        
        self.difficulty_label.config(text=self.ui_text["difficulty_label"])
        self.easy_radio.config(text=self.ui_text["easy"])
        self.medium_radio.config(text=self.ui_text["medium"])
        self.hard_radio.config(text=self.ui_text["hard"])
        self.custom_radio.config(text=self.ui_text["custom"])
        
        # 更新按钮
        self.generate_btn.config(text=self.ui_text["generate"])
        self.random_btn.config(text=self.ui_text["random"])
        
        # 更新图片区域
        self.preview_label.config(text=self.ui_text["preview"])
        self.save_btn.config(text=self.ui_text["save"])
        
        # 更新菜单
        self.create_menu()

    def edit_custom_config(self):
        """编辑自定义干扰强度配置"""
        config_window = tk.Toplevel(self.root)
        config_window.title(self.ui_text["config_title"])
        config_window.geometry("300x250")
        
        tk.Label(config_window, text=self.ui_text["lines_label"]).pack()
        lines_entry = tk.Entry(config_window)
        lines_entry.insert(0, str(self.custom_config["lines"]))
        lines_entry.pack()
        
        tk.Label(config_window, text=self.ui_text["shapes_label"]).pack()
        shapes_entry = tk.Entry(config_window)
        shapes_entry.insert(0, str(self.custom_config["shapes"]))
        shapes_entry.pack()
        
        tk.Label(config_window, text=self.ui_text["blur_label"]).pack()
        blur_entry = tk.Entry(config_window)
        blur_entry.insert(0, str(self.custom_config["blur"]))
        blur_entry.pack()
        
        tk.Label(config_window, text=self.ui_text["noise_label"]).pack()
        noise_entry = tk.Entry(config_window)
        noise_entry.insert(0, str(self.custom_config["noise_text"]))
        noise_entry.pack()
        
        def save_config():
            """保存配置"""
            try:
                self.custom_config["lines"] = int(lines_entry.get())
                self.custom_config["shapes"] = int(shapes_entry.get())
                self.custom_config["blur"] = int(blur_entry.get())
                self.custom_config["noise_text"] = int(noise_entry.get())
                messagebox.showinfo("成功", self.ui_text["config_success"])
                config_window.destroy()
            except ValueError:
                messagebox.showerror("错误", self.ui_text["config_error"])
        
        tk.Button(config_window, text=self.ui_text["save_btn"], command=save_config).pack(pady=10)

    def random_gen(self):
        """随机生成验证码内容，支持单词类型"""
        length = self.length_entry.get()
        length = random.randint(4,6) if length == "0" else int(length)
        
        captcha_type = self.type_var.get()
        
        if captcha_type == "chinese":
            chars = "的一是在不了有和人这中大为上个国我以要他时来用们生到作地于出就分对成会可主发年动同工也能下过子说产种面而方后多定行学法所民得经十三之进着等部度家电力里如水化高自二理起小物现实加量都两体制机当使点从业本去把性好应开它合还因由其些然前外天政四日那社义事平形相全表间样与关各重新线内数正心反你明看原又么利比或但质气第向道命此变条只没结解问意建月公无系军很情者最立代想已通并提直题党程展五果料象员革位入常文总次品式活设及管特件长求老头基资边流路级少图山统接知较将组见计别她手角期根论运农指几九区强放决西被干做必战先回则任取据处队南给色光门即保治北造百规热领七海口东导器压志世金增争济阶油思术极交受联什认六共权收证改清己美再采转更单风切打白教速花带安场身车例真务具万每目至达走积示议声报斗完类八离华名确才科张信马节话米整空元况今集温传土许步群广石记需段研界拉林律叫且究观越织装影算低持音众书布复容儿须际商非验连断深难近矿千周委素技备半办青省列习响约支般史感劳便团往酸历市克何除消构府称太准精值号率族维划选标写存候毛亲快效斯院查江型眼王按格养易置派层片始却专状育厂京识适属圆包火住调满县局照参红细引听该铁价严龙飞"
            text = ''.join(random.choices(chars, k=length))
        elif captcha_type == "mixed":
            chars = "的一是在不了有和人这中大为上个国我以要他时来用们生到作地于出就分对成会可主发年动同工也能下过子说产种面而方后多定行学法所民得经十三之进着等部度家电力里如水化高自二理起小物现实加量都两体制机当使点从业本去把性好应开它合还因由其些然前外天政四日那社义事平形相全表间样与关各重新线内数正心反你明看原又么利比或但质气第向道命此变条只没结解问意建月公无系军很情者最立代想已通并提直题党程展五果料象员革位入常文总次品式活设及管特件长求老头基资边流路级少图山统接知较将组见计别她手角期根论运农指几九区强放决西被干做必战先回则任取据处队南给色光门即保治北造百规热领七海口东导器压志世金增争济阶油思术极交受联什认六共权收证改清己美再采转更单风切打白教速花带安场身车例真务具万每目至达走积示议声报斗完类八离华名确才科张信马节话米整空元况今集温传土许步群广石记需段研界拉林律叫且究观越织装影算低持音众书布复容儿须际商非验连断深难近矿千周委素技备半办青省列习响约支般史感劳便团往酸历市克何除消构府称太准精值号率族维划选标写存候毛亲快效斯院查江型眼王按格养易置派层片始却专状育厂京识适属圆包火住调满县局照参红细引听该铁价严龙飞" + "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz23456789"
            text = ''.join(random.choices(chars, k=length))
        elif captcha_type == "alnum":
            chars = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz23456789"
            text = ''.join(random.choices(chars, k=length))
        elif captcha_type == "chinese_word":
            # 随机选择1-2个汉语单词
            word_count = min(max(length//2, 1), 2)
            text = ''.join(random.sample(self.chinese_words, word_count))
        elif captcha_type == "english_word":
            # 随机选择1个英语单词(不超过8字符)
            valid_words = [w for w in self.english_words if len(w) <= 8]
            text = random.choice(valid_words).upper()  # 转为大写更清晰
        
        self.entry.delete(0, tk.END)
        self.entry.insert(0, text)
        self.generate()

    def generate(self):
        """生成验证码图片，改进干扰文字效果"""
        text = self.entry.get().strip()
        if not text:
            messagebox.showwarning(self.ui_text["warning"], self.ui_text["content_warning"])
            return
        
        # 获取当前干扰强度配置
        difficulty = self.diff_var.get()
        config = self.difficulty_presets[difficulty]
        
        width, height = self.img_size
        img = Image.new('RGB', (width, height), (random.randint(200,255), random.randint(200,255), random.randint(200,255)))
        draw = ImageDraw.Draw(img)
        
        # 应用干扰设置
        for _ in range(config["lines"]):
            draw.line([(random.randint(0,width), random.randint(0,height)), 
                     (random.randint(0,width), random.randint(0,height))], 
                    fill=(random.randint(0,255), random.randint(0,255), random.randint(0,255)), width=1)
        
        for _ in range(config["shapes"]):
            shape_type = random.choice(["rectangle", "ellipse"])
            coords = [random.randint(0,width//2), random.randint(0,height//2),
                     random.randint(width//2,width), random.randint(height//2,height)]
            if shape_type == "rectangle":
                draw.rectangle(coords, outline=(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
            else:
                draw.ellipse(coords, outline=(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
        
        # 改进的干扰文字效果
        chars = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz23456789"
        for _ in range(config["noise_text"]):
            # 创建干扰文字图层
            noise_img = Image.new('RGBA', (width, height), (0,0,0,0))
            noise_draw = ImageDraw.Draw(noise_img)
            
            # 随机位置和大小
            x = random.randint(0, width-30)
            y = random.randint(0, height-30)
            char = random.choice(chars)
            font_size = random.randint(12, 20)  # 比主文字小
            
            try:
                # 尝试加载更小的字体
                noise_font = ImageFont.truetype("arial.ttf", font_size)
            except:
                noise_font = ImageFont.load_default()
            
            # 绘制干扰文字（半透明）
            noise_draw.text((x,y), char, font=noise_font, 
                          fill=(random.randint(0,150), random.randint(0,150), random.randint(0,150), random.randint(100,150)))
            
            # 添加虚化效果
            noise_img = noise_img.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.5, 1.5)))
            
            # 添加噪点效果
            noise_img = self.add_noise(noise_img)
            
            # 合并到主图像
            img.paste(noise_img, (0,0), noise_img)
        
        # 绘制主文字
        char_count = len(text)
        font_size = 36 if char_count <=4 else (32 if char_count<=6 else 28)
        spacing = 70 if char_count<=4 else (60 if char_count<=6 else 50)
        
        x = 20
        for char in text:
            y = random.randint(10, height-60)
            char_img = Image.new('RGBA', (60,70), (255,255,255,0))
            char_draw = ImageDraw.Draw(char_img)
            char_draw.text((5,5), char, font=self.font[self.type_var.get()], 
                         fill=(random.randint(0,150), random.randint(0,150), random.randint(0,150)))
            char_img = char_img.rotate(random.randint(-20,20), expand=1)
            img.paste(char_img, (x,y), char_img)
            x += spacing + random.randint(-5,5)
        
        # 整体模糊效果
        if config["blur"] > 0:
            img = img.filter(ImageFilter.GaussianBlur(config["blur"]))
        
        self.current_img = img
        photo = ImageTk.PhotoImage(img)
        self.img_label.config(image=photo)
        self.img_label.image = photo

    def add_noise(self, image):
        """为图像添加噪点效果"""
        # 将图像转换为数组
        arr = np.array(image)
        
        # 随机生成噪点
        noise = np.random.randint(0, 50, arr.shape, dtype=np.uint8)
        
        # 只对alpha通道大于0的区域添加噪点
        mask = arr[:,:,3] > 0
        for c in range(3):  # RGB通道
            arr[:,:,c][mask] = np.clip(arr[:,:,c][mask] + noise[:,:,c][mask], 0, 255)
        
        # 降低噪点区域的不透明度
        arr[:,:,3][mask] = np.clip(arr[:,:,3][mask] - noise[:,:,0][mask]//3, 50, 255)
        
        return Image.fromarray(arr)

    def save(self):
        """保存验证码图片"""
        if not self.current_img:
            messagebox.showwarning(self.ui_text["warning"], "请先生成验证码")
            return
        
        file = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG图片", "*.png"), ("所有文件", "*.*")],
            title="保存验证码图片"
        )
        if file:
            try:
                self.current_img.save(file)
                messagebox.showinfo("成功", self.ui_text["save_success"].format(file))
            except Exception as e:
                messagebox.showerror("错误", self.ui_text["save_error"].format(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernCaptchaGenerator(root)
    root.mainloop()

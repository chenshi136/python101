import random
import tkinter as tk
from tkinter import messagebox, ttk


class GuessNumberGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🔢 猜数字游戏")
        self.root.geometry("600x700")
        self.root.configure(bg="#f0f0f0")
        
        # 游戏变量
        self.target_number = 0
        self.min_range = 1
        self.max_range = 100
        self.guess_count = 0
        self.game_started = False
        
        # 初始化界面
        self.setup_ui()
        self.new_game()
    
    def setup_ui(self):
        # 标题
        title_frame = tk.Frame(self.root, bg="#4a90e2", height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="🔢 猜数字游戏", 
            font=("微软雅黑", 24, "bold"),
            bg="#4a90e2",
            fg="white"
        )
        title_label.pack(pady=20)
        
        # 游戏规则
        rules_frame = tk.Frame(self.root, bg="#f0f0f0", padx=20, pady=15)
        rules_frame.pack(fill=tk.X)
        
        rules_text = "我已经在1到100之间随机选择了一个数字\n每次输入一个数字来猜测，我会告诉你答案在哪个范围内"
        rules_label = tk.Label(
            rules_frame,
            text=rules_text,
            font=("微软雅黑", 11),
            bg="#f0f0f0",
            fg="#333333",
            justify=tk.CENTER
        )
        rules_label.pack()
        
        # 范围显示区域
        self.range_frame = tk.Frame(self.root, bg="#fff3cd", relief=tk.RIDGE, bd=2, padx=20, pady=15)
        self.range_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.range_label = tk.Label(
            self.range_frame,
            text=f"当前范围：{self.min_range} - {self.max_range}",
            font=("微软雅黑", 14, "bold"),
            bg="#fff3cd",
            fg="#856404"
        )
        self.range_label.pack()
        
        # 猜测次数显示
        self.count_label = tk.Label(
            self.range_frame,
            text=f"猜测次数：{self.guess_count}",
            font=("微软雅黑", 12),
            bg="#fff3cd",
            fg="#856404"
        )
        self.count_label.pack(pady=(5, 0))
        
        # 输入区域
        input_frame = tk.Frame(self.root, bg="#f0f0f0", padx=20, pady=15)
        input_frame.pack(fill=tk.X)
        
        input_label = tk.Label(
            input_frame,
            text="请输入你的猜测（1-100）：",
            font=("微软雅黑", 12),
            bg="#f0f0f0",
            fg="#333333"
        )
        input_label.pack(anchor=tk.W)
        
        # 输入框和按钮框架
        entry_button_frame = tk.Frame(input_frame, bg="#f0f0f0")
        entry_button_frame.pack(fill=tk.X, pady=10)
        
        # 输入框
        self.entry = tk.Entry(
            entry_button_frame,
            font=("微软雅黑", 16),
            width=15,
            justify=tk.CENTER,
            relief=tk.SOLID,
            bd=2
        )
        self.entry.pack(side=tk.LEFT, padx=(0, 10))
        self.entry.bind("<Return>", lambda e: self.make_guess())  # 按Enter键提交
        
        # 提交按钮
        submit_btn = tk.Button(
            entry_button_frame,
            text="提交猜测",
            font=("微软雅黑", 12, "bold"),
            bg="#28a745",
            fg="white",
            relief=tk.RAISED,
            bd=2,
            padx=20,
            pady=8,
            command=self.make_guess,
            cursor="hand2"
        )
        submit_btn.pack(side=tk.LEFT)
        
        # 重置按钮
        reset_btn = tk.Button(
            entry_button_frame,
            text="重新开始",
            font=("微软雅黑", 12),
            bg="#6c757d",
            fg="white",
            relief=tk.RAISED,
            bd=2,
            padx=15,
            pady=8,
            command=self.new_game,
            cursor="hand2"
        )
        reset_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # 结果显示区域（带滚动条）
        result_frame = tk.Frame(self.root, bg="#f0f0f0", padx=20, pady=10)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        result_label_title = tk.Label(
            result_frame,
            text="游戏记录：",
            font=("微软雅黑", 12, "bold"),
            bg="#f0f0f0",
            fg="#333333",
            anchor=tk.W
        )
        result_label_title.pack(fill=tk.X)
        
        # 创建文本框和滚动条
        text_frame = tk.Frame(result_frame, bg="#ffffff", relief=tk.SUNKEN, bd=2)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        self.result_text = tk.Text(
            text_frame,
            font=("微软雅黑", 11),
            bg="#ffffff",
            fg="#333333",
            wrap=tk.WORD,
            relief=tk.FLAT,
            padx=10,
            pady=10,
            state=tk.DISABLED
        )
        
        scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 初始化时添加欢迎信息
        self.add_result("游戏已开始！我已经在1-100之间选择了一个数字。\n")
    
    def new_game(self):
        """开始新游戏"""
        self.target_number = random.randint(1, 100)
        self.min_range = 1
        self.max_range = 100
        self.guess_count = 0
        self.game_started = True
        
        # 更新界面
        self.range_label.config(text=f"当前范围：{self.min_range} - {self.max_range}")
        self.count_label.config(text=f"猜测次数：{self.guess_count}")
        self.entry.delete(0, tk.END)
        self.entry.focus()
        
        # 清空结果区域
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)
        
        self.add_result("🎮 新游戏开始！我已经在1-100之间选择了一个数字。\n")
    
    def make_guess(self):
        """处理用户猜测"""
        if not self.game_started:
            return
        
        try:
            # 获取输入
            user_input = self.entry.get().strip()
            
            if not user_input:
                messagebox.showwarning("提示", "请输入一个数字！")
                return
            
            # 转换为整数
            guess = int(user_input)
            
            # 验证范围
            if guess < 1 or guess > 100:
                messagebox.showwarning("提示", "请输入1到100之间的数字！")
                self.entry.delete(0, tk.END)
                return
            
            self.guess_count += 1
            self.count_label.config(text=f"猜测次数：{self.guess_count}")
            
            # 添加猜测记录
            self.add_result(f"第 {self.guess_count} 次猜测：{guess}\n")
            
            # 判断猜测结果
            if guess == self.target_number:
                # 猜对了！
                self.add_result(f"🎉 恭喜你猜对了！正确答案是 {self.target_number}！\n")
                self.add_result(f"你一共猜了 {self.guess_count} 次。\n")
                self.game_started = False
                messagebox.showinfo("恭喜", f"🎉 恭喜你猜对了！\n正确答案是：{self.target_number}\n你一共猜了 {self.guess_count} 次。")
                
            elif guess > self.target_number:
                # 猜测值太大了，更新最大值
                self.max_range = guess
                self.range_label.config(text=f"当前范围：{self.min_range} - {self.max_range}")
                
                if self.min_range < self.max_range:
                    self.add_result(f"📊 答案在 {self.min_range}-{self.max_range} 之间（你猜大了）\n\n")
                else:
                    self.add_result(f"📊 答案在 {self.max_range} 以内（你猜大了）\n\n")
                    
            else:
                # 猜测值太小了，更新最小值
                self.min_range = guess
                self.range_label.config(text=f"当前范围：{self.min_range} - {self.max_range}")
                
                if self.min_range < self.max_range:
                    self.add_result(f"📊 答案在 {self.min_range}-{self.max_range} 之间（你猜小了）\n\n")
                else:
                    self.add_result(f"📊 答案在 {self.min_range} 以上（你猜小了）\n\n")
            
            # 清空输入框并聚焦
            self.entry.delete(0, tk.END)
            self.entry.focus()
            
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字！")
            self.entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("错误", f"发生错误：{str(e)}")
    
    def add_result(self, text):
        """添加结果到文本区域"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.insert(tk.END, text)
        self.result_text.see(tk.END)  # 滚动到底部
        self.result_text.config(state=tk.DISABLED)

# 主程序
if __name__ == "__main__":
    root = tk.Tk()
    app = GuessNumberGame(root)
    root.mainloop()
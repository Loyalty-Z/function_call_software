from email.mime import image
import tkinter as tk
from tkinter import messagebox
import tkinter.filedialog
from function_call import *
from tkinter.messagebox import *
from tkinter import PhotoImage

# 显示解析的函数调用关系图
def show_img(image_path,func_list):
    img_window = tk.Toplevel(root)   # 显示图像的子窗口
    img_window.geometry('800x800')
    img_window.resizable(False,False)
    global img       # 
    img = PhotoImage(file=image_path)  # 函数调用关系图
    func_desc = ''
    for i in range(len(func_list)):
        func_desc += f'{func_list[i]}:v{i} '
    lb = tk.Label(img_window,text=func_desc,image=img,compound='top')    # compound='top'表示图像居上，文本在下面
    lb.place(relx=0.1,rely=0.1,relwidth=0.8,relheight=0.8)


# 上传文件
def upload_file():
    filenames = tkinter.filedialog.askopenfilenames()  # 打开文件输入对话框，获取用户选择打开的文件，可以打开多个文件
    if filenames:
        print(filenames)
        parse_code(list(filenames))
    else:
        print('未选择文件')

# 解析代码
def parse_code(files):
    try:
        dest = get_function_call(*files)
        image_path,func_list = draw_call_grap(dest)  # 生成函数调用关系图，以及函数信息
        show_img(image_path,func_list)    # 显示图像

    except Exception as e:   # 当解析错误时如何处理
        print(e)
        messagebox.showerror('错误','代码解析错误，请检查代码')

# 解析文本框代码
def parse():
    code = text_input.get('1.0',"end")  # 获取文本框输入的内容
    with open('./.cache/cache.py','w') as f: # 将输入的代码写入到文件中再进行解析
        f.write(code)
    parse_code(['./.cache/cache.py'])  # 解析


root = tk.Tk()
root.title('function call relation graph')  # 设置窗口标题
root.geometry('500x500')               # 设置窗口大小
root.resizable(False,False)



# 设置文本输入框
text_input = tk.Text(root)
text_input.place(relx=0.2,rely=0.2,relheight=0.6,relwidth=0.6)

# 添加菜单
main_menu = tk.Menu(root)            # 菜单栏
menu_function = tk.Menu(main_menu,tearoff=False)   # 子菜单
main_menu.add_cascade(label='功能',menu=menu_function)
menu_function.add_command(label='上传文件',command=upload_file)
menu_function.add_separator()     # 分割线
menu_function.add_command(label='解析文本框代码',command=parse)



root.config(menu=main_menu)
root.mainloop()

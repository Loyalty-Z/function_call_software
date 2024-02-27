import ast
import networkx as nx
import random as rd
import os
import numpy as np




class CodeVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        super().__init__()
        self.userfunc = []
        self.info = []
        self.filename = ''
    def generic_visit(self, node):
        # print(type(node).__name__)
        ast.NodeVisitor.generic_visit(self, node)
    def visit_FunctionDef(self, node):
        # print('User Function Name:%s' % node.name)
        self.info.append('User Function Name:'+self.filename+'.'+node.name)
        self.userfunc.append(self.filename+'.'+node.name)
        ast.NodeVisitor.generic_visit(self, node)
    def visit_Call(self, node):
        # print(node._fields)
        def recur_visit(node):
            if type(node) == ast.Name:
                return node.id
            elif type(node) == ast.Attribute:
                # Recursion on series of calls to attributes.
                # print(node.attr)
                func_name = recur_visit(node.value)
                if type(node.attr) == str and type(func_name) == str:
                    func_name += '.' + node.attr
                # else:
                    # print('attention!!!', type(node.attr), type(func_name))
                return func_name
            elif type(node) == ast.Str:
                return node.s
            elif type(node) == ast.Subscript:
                return node.value.id

        func = node.func
        # print(type(func), func._fields)
        func_name = recur_visit(func)
        if(type(func_name)==str):
            self.info.append('\tUser function Call:'+self.filename+'.'+func_name)
        ast.NodeVisitor.generic_visit(self, node)

# 输入文件对文件中的代码进行解析
def get_function_call(*args):
    visitor = CodeVisitor()
    for infile in args:
        with open(infile,'r') as f:
            r_node = ast.parse(f.read())  # 将代码解析成ast
        visitor.filename = os.path.basename(infile).split('.')[0]  # 获取文件名
        visitor.visit(r_node)    # 访问ast的所有结点

    # visitor.info 记录的顺序规律是如果两个函数存在调用关系，先有函数定义信息，后有函数被调用信息
    # 'User Function Name:test.main'(函数定义信息), '\tUser function Call:test.print1(函数被调用信息)'
    dest = {}     # dest存放每个userfunc下调用了哪些userfunc
    for line in visitor.info:
        if line.startswith('User Function Name'):   # 找出所有定义的函数
            defnow = line.split(':')[1]
            dest[defnow] = []
            continue
    
        for func in visitor.userfunc:         # 对调用信息进行处理  User function Call:test.print
            basename = func.split('.')[-1]
            line_tail = line.split(':')[-1]
            line_tail = line_tail.split('.')[-1]
            if basename == line_tail:
                dest[defnow].append(func)
                break

    return dest

# 计算每个点与现有点的距离,要求两点之间的距离要大于某个阈值
def get_distance(point,points):
    if len(points) == 0:
        return True
    point = np.array(point).reshape((2,1))
    points = np.array(points).reshape((2,len(points)))
    distance = np.sqrt(np.sum((points - point) ** 2,axis=0))
    print(distance)
    count = len(np.where(distance < 20)[0])           # 计算距离小于阈值的点对个数
    if count == 0:
        return True
    return False

# 绘制函数调用关系图
def draw_call_grap(dest):
    import matplotlib.pyplot as plt
    graph = nx.DiGraph()    # 创建图
    # 添加图中的点和边
    func_point = {}       # 函数名与点的映射关系
    func_list = list(dest.keys())
    for i in range(len(func_list)):
        func_point[func_list[i]] = i
    # 向图中添加点
    for i in range(len(func_list)):
        graph.add_node(i,desc=f'v{i}')
    # 向图中添加边
    for k in dest.keys():
        for p in dest[k]:
            graph.add_edge(func_point[k], func_point[p],name='')  # 添加边
    
    # 绘图
    points = []
    for i in range(len(func_list)):
        x, y = rd.randint(0,100),rd.randint(0,100)
        while (x , y) in points and not get_distance((x,y),points):  # 要求新加入的点满足不与原来的点重复以及点与点之间距离大于4
            x, y = rd.randint(0,100),rd.randint(0,100)
        points.append((x,y))
    

    # 绘图

    nx.draw_networkx(graph,points,with_labels=None,edge_color='r',node_size=200,node_shape='o')

    node_labels = nx.get_node_attributes(graph,'desc')
    nx.draw_networkx_labels(graph,points,labels=node_labels,font_size=8,font_color='w')
    
    # edge_labels = nx.get_edge_attributes(graph, 'name')
    # nx.draw_networkx_edge_labels(graph,points,edge_labels=edge_labels)


    plt.figure(1)
    plt.title('code function call relationship',fontsize=10)
    plt.savefig('./.graph/graph.png')
    plt.clf()
    return './.graph/graph.png',func_list

    



strs = """
def main(s):
    s = print1(s)
    print(s)
    print2(s)
def print1(s):
    s += 10 
    return s
def print2(s):
    pass
"""

# with open('./test_code/cache.py','w') as f:
#     f.write(strs)
# dest = get_function_call('./test_code/cache.py')
# print(dest)
# draw_call_grap(dest)
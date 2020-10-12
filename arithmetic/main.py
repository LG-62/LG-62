import numpy as np
import fractions
import decimal
import sys
import operator


# 将中缀表达式改成后缀表达式
def suffix_ex(expression):
    if not expression:
        return []
    operators = {
        '+': 1,
        '-': 1,
        'x': 2,
        '÷': 2,
    }
    suffix_stack = []  # 后缀表达式结果
    operators_stack = []  # 操作符栈
    exp_split = expression.split(' ')  # 去掉空格
    for it in exp_split:
        if it in ['+', '-', 'x', '÷']:  # 遇到操作符
            while len(operators_stack) >= 0:
                if len(operators_stack) == 0:
                    operators_stack.append(it)  # 空栈，直接压入
                    break
                op = operators_stack.pop()  # 如果运算符栈不为空，则取出栈顶元素op
                # 如果op是'('或者当前操作符算术优先级高于op,直接入栈
                if op == '(' or operators[it] > operators[op]:
                    operators_stack.append(op)
                    operators_stack.append(it)
                    break
                # 否则就入栈后缀表达式栈
                else:
                    suffix_stack.append(op)  # 运算数直接入后缀表达式栈
        elif it == '(':  # 左括号直接入栈
            operators_stack.append(it)
        elif it == ')':
            # 如果运算符栈不为空，那么直接出栈，添加到后缀表达式栈，直到遇到左括号
            while len(operators_stack) > 0:
                op = operators_stack.pop()
                if op == "(":
                    break
                else:
                    suffix_stack.append(op)
        else:
            suffix_stack.append(it)  # 操作数直接入栈

    while len(operators_stack) > 0:
        suffix_stack.append(operators_stack.pop())

    return suffix_stack


# 二叉树的结点
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


# 生成二叉树
def new_tree(exp):
    tree_stack = []
    for item in exp:
        # print(item)
        parent = Node(item)
        if not item in ['+', '-', 'x', '÷']:
            # 操作数
            tree_stack.append(parent)
        else:
            # 操作符
            right = tree_stack.pop()
            left = tree_stack.pop()
            parent.right = right
            parent.left = left
            tree_stack.append(parent)

    parent = tree_stack[-1]
    return parent


# 判断二叉树是否相同
def same_judge(root):
    if not root.left:
        if not root.right:
            return root.value
    elif root.value == '+' or root.value == 'x':
        left = same_judge(root.left)
        right = same_judge(root.right)
        if operator.le(left, right):
            return root.value + left + right
        else:
            return root.value + right + left
    else:
        return root.value + same_judge(root.left) + same_judge(root.right)


# 判断重复方法
def is_repeat(express_set, expression):
    a = suffix_ex(expression)  # expression转化为后缀表达式
    a_tree = new_tree(a)  # 再生成二叉树
    for it in express_set:
        b_suffix = suffix_ex(it)  # expression_set的其中一个expression转化为后缀表达式转化为后缀表达式
        b_binary_tree = new_tree(b_suffix)
        if same_judge(a_tree) == same_judge(b_binary_tree):  # 判断两个二叉树是否相同
            return True
    return False


# 检查分数形式，真分数不用改变，假分数变为带分数
def check_frac(fraction):
    if fraction.numerator > fraction.denominator:  # 分子大于分母，即假分数
        mixed = fraction.numerator // fraction.denominator  # 提取带分数前面的整数
        if fraction - mixed == 0:
            frac_str = '{}'.format(mixed)
        else:
            frac_str = '{}`{}'.format(mixed, fraction - mixed)
    else:
        frac_str = str(fraction)
    return frac_str


# 格式化式子:遇到不同的字符串，转为不同的字母f,o,e,n
def elem_type_judge(elem):
    if type(elem) != str:
        raise TypeError
    if '/' in elem or '`' in elem:  # 出现分数即返回f
        return 'f'
    elif elem in ['+', '-', 'x', '÷']:
        return 'o'  # 出现四则运算符号则返回o
    elif elem is '=':
        return 'e'  # 出现等号则返回e
    elif elem.isdigit():
        return 'n'  # 若字符串只由数字组成即自然整数，则返回n
    else:
        print(elem)
        raise ValueError


# 随机式子生成器
def generate_equation(erange):
    # erange = 20  # 控制题目中数的大小
    operator = [' + ', ' - ', ' x ', ' ÷ ']
    end_opt = ' ='
    # 随机生成自然数和分数的个数，但控制总和不超过4，从此控制题目不超过三个运算符
    nnature, nfraction = np.random.randint(1, 3, size=2)
    # print(nnature,nfraction)
    lnature = [str(x) for x in np.random.randint(1, erange, size=nnature)]  # 产生1-erange之间的自然整数
    # print(lnature)
    # np.random.rand()产生的是0-1之间的小数，产生的个数是根据参数nfraction来定的，round()根据四舍五入来取值，+0.5是为了防止取值后为0
    lfloat = [str(round(x + 0.5, 1)) for x in np.random.rand(nfraction)]
    lfraction = list()
    # decimal.Decimal()把lfloat中字符串类型转化为十进制数据，然后用fractions.Fraction()再次转化为分数，最后通过check_frac来整理为带分数，添加至lfraction
    for fraction in [fractions.Fraction(decimal.Decimal(x)) for x in lfloat]:
        lfraction.append(check_frac(fraction))
    equation = ''
    bag = lnature + lfraction  # 将生成的自然整数和分数存在bag里
    # print(bag)
    len_bag = len(bag)
    for it in range(len_bag):
        randint = np.random.randint(len(bag))
        equation += bag[randint]  # 取数
        if it < len_bag - 1:  # len_bag-1即是it的最大取值，所以当it<len_bag时，后面加随机操作符
            equation += operator[randint]  # 当it>=len_bag时，把等号补上，式子完成，跳出循环
        else:
            equation += end_opt
        bag.pop(randint)  # 当数取出的时候，应该把它从bag里去除
    # print(equation)
    return equation


# 计算出式子的答案
def compute_equation(equation):
    lequation = equation.split(' ')  # 将式子进行分割，则遇到空格就截取，分割完成后显示[数字+符号]
    # print(lequation)
    for it in range(len(lequation)):
        etype = elem_type_judge(lequation[it])
        if etype is 'f':
            if '`' in lequation[it]:
                tnum, frac = lequation[it].split('`')  # 把带分数分割成整数和分数
                # print(tnum,frac)
                lequation[it] = '({}+fractions.Fraction(\'{}\'))'.format(tnum, frac)
                # print(lequation[it])
            else:
                lequation[it] = 'fractions.Fraction(\'{}\')'.format(lequation[it])
        elif etype is 'n':
            lequation[it] = 'fractions.Fraction(\'{}\')'.format(lequation[it])
        elif etype is 'o':
            if lequation[it] is '÷':
                lequation[it] = '/'
            if lequation[it] is 'x':
                lequation[it] = '*'
        elif etype is 'e':
            lequation[it] = ''
    fequation = ''.join(lequation)
    try:
        result = eval(fequation)
        if result < 0:
            return '-1'
        else:
            # print(check_frac(result))
            return check_frac(result)
    except ValueError:
        print('the equation is wrong')
        return '-1'


# 把原始式子和结果都装进txt文件
def generate_file(q_num, erange):
    # q_num = int(input('the number of equation:'))
    # erange = int(input('the range of the number:'))
    q_num = int(q_num)
    erange = int(erange)
    q_list = list()
    a_list = list()
    cnt = 0
    while cnt < q_num:
        equation = generate_equation(erange=erange)
        answer = compute_equation(equation)
        repeat = is_repeat(q_list, equation)
        if answer != '-1' and repeat == False:
            q_list.append(equation)
            a_list.append(answer)
            cnt += 1
    for lt, name in zip([q_list, a_list], ['Exercises.txt', 'Answers.txt']):
        with open(name, 'w') as f:
            for row in lt:
                f.write(row)
                f.write('\n')
            # f.close()


# 检查校对部分
# qf='Exercises.txt', af='Answers.txt'
def proofreading(qf, af):
    '''
    qf=D:\学习资料\软工\结对编程\Sexercise1.txt
    af=D:\学习资料\软工\结对编程\Sanswer1.txt
    '''

    q_list, a_list = [list(), list()]
    for lt, name in zip([q_list, a_list], [qf, af]):
        try:
            with open(name) as f:
                for line in f.readlines():
                    lt.append(line.strip())
        except FileNotFoundError:
            print('error:No such file or directory')

    ita = min(len(q_list), len(a_list))
    proof = {'Correct': list(), 'Wrong': list()}
    for it in range(ita):
        if compute_equation(q_list[it]) == a_list[it]:
            proof['Correct'].append(it + 1)
        else:
            proof['Wrong'].append(it + 1)
    # print('校对成功！请在Grade.txt查看结果:\n')
    # print('Correct\t:{}'.format(len(proof['Correct'])))
    # print('Wrong\t:{}'.format(len(proof['Wrong'])))
    file_str = 'Correct:{}{}\nWrong:{}{}'.format(
        len(proof['Correct']), str(proof['Correct']),
        len(proof['Wrong']), str(proof['Wrong']))
    with open('Grade.txt', 'w') as f:
        f.write(file_str)


# 在运行程序时输入参数，主动抛异常
def raise_ex(s1, s2):
    if s1 == '-n' and s2 == '-r':  # 当输入-n xx -r xx 时，即是生成题目和答案的过程
        return 1
    elif s1 == '-e' and s2 == '-a':  # 当输入-e xx -a xx 时，即是校对给定题目和答案的过程
        return 2
    else:
        ex = Exception('Error:参数格式错误！')
        raise ex


# main函数
def main():
    try:
        # sys.argv[1:5]只读取前四个输入字符   parameter1/parameter2为两个参数
        s1, parameter1, s2, parameter2 = sys.argv[1:5]
        res = raise_ex(s1, s2)
        if res == 1:
            n = parameter1
            r = parameter2
            generate_equation(r)
            generate_file(n, r)
            print("生成题目成功！请查看 'Exercises.txt' 和 'Answers.txt'\n")
        elif res == 2:
            e = parameter1
            a = parameter2
            proofreading(e, a)
            print("校对完成！请在 'Grade.txt' 查看结果\n")
    except BaseException:
        print("Error:输入命令错误,请检查后重新输入")


if __name__ == '__main__':
    main()

import sys
# dataは以下の3つを使用する
data1 = "( ( ( x ) ) )( ()"
# data2 = "2[3 5(7{11}13)17]19"
# data3 = "{ {x(y)((z) x) {x} {y} }"
left = ["(", "[", "{"]
right = [")", "]", "}"]

def main(data):
    brackets_judge(data)

def brackets_judge(str1):
    # 判定する括弧
    stk = []
    isOK = False
    print("input: " + str1)
    print("  文字\t操作\tスタック")
    print("-"*30)
    for i,inputstr in enumerate(str1):
        print(str(i + 1) + ": " + inputstr, end = "\t")
        # (か[か{ならpush
        if inputstr in left:
            print("push" + "\t" + str(" ".join(stk)) , end = "")
            stk.append(inputstr)

        elif inputstr in right:
            # stackがからの時と括弧の対応が取れない時
            if len(stk) == 0 or brackets_dict(stk[-1]) != inputstr:
                return print("\nerror")
            else:
                stk.pop()
                print("pop", end="")
                # stackがからの時
                if len(stk) == 0:
                    isOK = True
        # 括弧以外の文字の時
        else:
            print("pass" + "\t" + str(" ".join(stk)), end="")
        print()
    # 最後まで探索してstackがからの時
    if isOK and len(stk) == 0:
        print("OK")
    else:
        print("error")

def brackets_dict(str1):
    for i in range(len(left)):
        if str1 == left[i]:
            return right[i]

if __name__ == '__main__':
    # コマンドラインでデータの入力を行った場合
    if len(sys.argv) == 2:
        main(sys.argv[1])
    # コマンドラインで指定しなかった場合
    else:
        main(data1)    

data1 = "( ( ( x ) ) )"
data2 = "2[3 5(7{11}13)17]19"
data3 = "{ {x(y)((z) x) {x} {y} }"

left = ["(", "[", "{"]
right = [")", "]", "}"]

def brackets_judge(str1):
    # 判定する括弧
    stk = []
    isOK = False
    for i,inputstr in enumerate(str1):
        print(str(i + 1) + ": " + inputstr, end = "\t")
        # (か[か{ならpush
        if inputstr in left:
            print("push" + "\t" + str(stk) , end = "")
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
            print("pass" + "\t" + str(stk), end="")
        print()
    # 最後まで探索してstackがからの時
    if isOK:
        print("OK")
    else:
        print("error")


def brackets_dict(str1):
    if str1 == left[0]:
        return right[0]
    elif str1 == left[1]:
        return right[1]
    elif str1 == left[2]:
        return right[2]

brackets_judge(data1)


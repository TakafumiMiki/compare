#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
式をトークン分割，演算子優先括弧付け，後置記法，前置記法，構文木,Graphvizの図を作成する
"""
expr = [
        'a = b+c**2 ^ d/e&f',
        ]

Debug = True        # 詳細表示
Graphviz = True     # graphviz dotコマンドの実行

from pyparsing import *
import subprocess


# pyparsing parser
Number = Word( nums )                       # 数字
Ident  = Word(alphas,alphanums)             # 識別子
Opera  = oneOf('= + - * / % ** ^ &')            # 演算子
Paren  = oneOf( '( )' )                     # 括弧
token  = Number ^ Ident ^ Opera ^ Paren   # トークン

def main():
    ''' 式をトークンに分割し，後置(逆ポーランド)記法を生成する
        l0 トークン分割
        l1 後置(逆ポーランド)記法に変換
        l2 優先度により括弧で括る
        l3 優先度からRPNを確認 (確認するならコメントを外す)
        l4 抽象構文木の作成, 前置(ポーランド記法)に変換
           接続リスト作成しGraphvizで描画
    '''
    sp1 = '%-10s'
    for no, st0 in enumerate(expr):
        print('expr%02d\n'%no + sp1%'original:', st0)
        l0 = tokenize(st0)      ; print(sp1%'token:  ', ' '.join(l0) )
        l1 = makeRPN(l0)        ; print(sp1%'rpn:    ', ' '.join(l1) )
        l2 = makePri(st0)       ; print(sp1%'pri:    ', list2str(l2) )
        pass                    ; print(sp1%'list:   ', '%s'%(l2[0]) )
        l4, lc = makePolish(l1) ; print(sp1%'polish: ', ' '.join(l4) )
        makeGraphviz(no,  st0, connList(lc) )


def tokenize(s):
    ''' トークン分割  scanString:[ ((token, name), start, end), ...] '''
    return [x[0][0] for x in token.scanString(s)]

def makeRPN(l):
    ''' 操車場アルゴリズムで逆ポーランド記法に変換 右結合,関数 未対応 '''
    deb=True                # token, queue, stackの表示
    if deb:
        print('token queue'+' '*25+'stack')
        print('-'*5+'-'*30+'-'*30)
    q, s = list(), list()   # que, stack
    for i in l:             # トークン順に評価
        if isIdent(i): q.append(i)  # 数値，変数
        elif i=='(':  s.append(i)   # 括弧開始
        elif i==')':                # 閉じ括弧なら
            while True:                 # 括弧開始までスタックを出力
                k=s.pop(-1)
                if k=='(': break
                q.append(k)
        else:                   # 演算子の場合
            n=opePri2(i)            # 優先順位取得(0が最優先)
            while len(s)>0 and n>=opePri2(s[-1]): # スタックトップが現トークンより優先
                q.append( s.pop(-1) )   # スタックトップを出力
            s.append( i )       # 現トークンをスタックへ
        if deb: print('%-5s %-30s %-30s'%(i, ' '.join(q), ' '.join(s)) )
    if deb: print()

    return q+[x for x in reversed(s)]   # キューとスタックの逆順を結合

def isIdent(s):
    ''' 変数と数はTrueを，演算子と()はFalseを返す '''
    if len( [x for x in (Ident^Number).scanString(s)] )>0:
        return True
    return False

def opePri2(s):
    ''' 演算子の優先順位
        ( ) は演算子ではないが=より優先度を低くしてrpn生成に使用する　'''
    op = [ ['**', '++'],
           ['*', '/', '%'],
           ['+', '-'],
           ['&', '^', '|'],
           ['(', ')'],
           ['='],]

    for n, i in enumerate(op):
        if s in i: return n
    return -1

def makePri(str):
    ''' 演算子優先法 '''
    expr = operatorPrecedence( (Ident^Number),
           [ (oneOf('** ++ --'), 2, opAssoc.LEFT),
             (oneOf('* /'),      2, opAssoc.LEFT),
             (oneOf('+ -'),      2, opAssoc.LEFT),
             (Literal('='),      2, opAssoc.LEFT) ] )
    return expr.parseString(str).asList()

def list2str(l):
    ''' リストの階層を()に変え文字列にする '''
    t=( ('[', '('), (']', ')'), ("'",''), (',','') )
    s='%s'%l[0]
    for i in t: s=s.replace(i[0], i[1])
    return s[1:-1]  # 最初と最後の()をとる

def makePolish(l):
    ''' 前置(ポーランド)記法生成 '''
    deb=True
    # ノード，左，右の辞書作成
    # print("debug: ",l)
    s, o, n = list(), list(), 0
    for i in l:
        if isIdent(i): s.append(i)  # 変数,値ならスタックへ
        elif len(s)>=2:             # 演算子ならスタックを2つpop
            s1, s2, m =s.pop(-1), s.pop(-1), '_%d'%n
            o.append( dict(no=m, val=i, right=s1, left=s2) )
            s.append(m)   # 別ノードへのリンク
            n+=1
    if deb:
        for i in reversed(o): print(i) # 下位からを上位からへ
    # 接続構造をたどり前置記法生成  r:既知，w:後で追加する場合, x:調査対象ノード
    r, w, x = list(), list(), [ s[-1] ] # 最上位から探索
    while x:
        flg=False                   # 左側要探索フラグ
        h=x.pop(0)
        k=[i for i in reversed(o) if i['no']==h][0]  # 該当辞書検索
        r.append(k['val'])          # 演算子を出力へ
        if k['left'][0]!='_':
            r.append(k['left'])     # 左がリンクでなければ出力
        else:
            x.append( k['left'])    # リンクなら調査対象へ
            flg=True                # 左がリンクだった
        if k['right'][0]!='_':
            if flg:
                w.append(k['right'])    # 左がリンクの場合、後で追加
            else:
                r.append(k['right'])    # 右の変数・値を出力
        else:
            x.append( k['right'])       # 右がリンクなので調査対象へ
    if deb: print(r,w)
    return r+w,reversed(o)

def isList(s):
    ''' 型がリストならば真 '''
    if type(s)==type(list()): return True
    return False

def isStr(s):
    ''' 型が文字列ならば真 '''
    if type(s)==type(str()): return True
    return False

def connList(l):
    ''' Graphviz用接続リストの作成
        graphvizの描画は出現順のため深さ優先探索のリンクを先に出力することに注意 '''
    l1=[x for x in l]
    sn, sl, q ='', '', [ [x for x in l1][0]['no'] ]
    while q:
        h=q.pop(-1)
        i=[x for x in l1 if x['no']==h][0]
    # center
        sn += '%sC [label="%s"];\n'%(i['no'], i['val'])
    # left
        if i['left'][0]!='_':
            sn += '%sL [label="%s"];\n'%(i['no'], i['left'])
            sl += '%sC -- %sL;\n'%(i['no'], i['no'])
        else:   # リンク先がある
            q.append(i['left'])
            sl += '%sC -- %sC;\n'%(i['no'], i['left'])
    # right
        if i['right'][0]!='_':
            sn += '%sR [label="%s"];\n'%(i['no'], i['right'])
            sl += '%sC -- %sR;\n'%(i['no'], i['no'])
        else:   # リンク先がある
            q.append(i['right'])
            sl += '%sC -- %sC;\n'%(i['no'], i['right'])
    return sl+sn    # 先にリンクリストを出力しないと左右が矛盾する

def makeGraphviz(no, expr0, ne):
    ''' graphvizのdotファイルを作成しdotからpng画像を作成 '''
    print(ne)
    st='''\
graph expr%d {
  graph [label="%s", labelloc="t", labeljust="c"];
'''%(no,expr0)
    st+=ne
    st+='}\n'
    with open('./expr%d.dot'%no, 'w') as f: f.write(st)

# dot -Tpng -o exprX.png exprX.dotを実行
    if Graphviz:
        cmd=['dot', '-Tpng', '-o', 'expr%d.png'%no, 'expr%d.dot'%no]
        p=subprocess.check_call(cmd) #, stdout=sp.PIPE, stderr=sp.PIPE)
        print('graphviz dot:',p)

if __name__=='__main__': main()

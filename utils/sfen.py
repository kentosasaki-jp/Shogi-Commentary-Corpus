import re
import cshogi
from cshogi import *

Number = {
    '11':'1a', '12':'1b', '13':'1c', '14':'1d', '15':'1e', '16':'1f', '17':'1g', '18':'1h', '19':'1i',
    '21':'2a', '22':'2b', '23':'2c', '24':'2d', '25':'2e', '26':'2f', '27':'2g', '28':'2h', '29':'2i',
    '31':'3a', '32':'3b', '33':'3c', '34':'3d', '35':'3e', '36':'3f', '37':'3g', '38':'3h', '39':'3i',
    '41':'4a', '42':'4b', '43':'4c', '44':'4d', '45':'4e', '46':'4f', '47':'4g', '48':'4h', '49':'4i',
    '51':'5a', '52':'5b', '53':'5c', '54':'5d', '55':'5e', '56':'5f', '57':'5g', '58':'5h', '59':'5i',
    '61':'6a', '62':'6b', '63':'6c', '64':'6d', '65':'6e', '66':'6f', '67':'6g', '68':'6h', '69':'6i',
    '71':'7a', '72':'7b', '73':'7c', '74':'7d', '75':'7e', '76':'7f', '77':'7g', '78':'7h', '79':'7i',
    '81':'8a', '82':'8b', '83':'8c', '84':'8d', '85':'8e', '86':'8f', '87':'8g', '88':'8h', '89':'8i',
    '91':'9a', '92':'9b', '93':'9c', '94':'9d', '95':'9e', '96':'9f', '97':'9g', '98':'9h', '99':'9i',
}

Kanji = {
    '１一':'1a', '１二':'1b', '１三':'1c', '１四':'1d', '１五':'1e', '１六':'1f', '１七':'1g', '１八':'1h', '１九':'1i',
    '２一':'2a', '２二':'2b', '２三':'2c', '２四':'2d', '２五':'2e', '２六':'2f', '２七':'2g', '２八':'2h', '２九':'2i',
    '３一':'3a', '３二':'3b', '３三':'3c', '３四':'3d', '３五':'3e', '３六':'3f', '３七':'3g', '３八':'3h', '３九':'3i',
    '４一':'4a', '４二':'4b', '４三':'4c', '４四':'4d', '４五':'4e', '４六':'4f', '４七':'4g', '４八':'4h', '４九':'4i',
    '５一':'5a', '５二':'5b', '５三':'5c', '５四':'5d', '５五':'5e', '５六':'5f', '５七':'5g', '５八':'5h', '５九':'5i',
    '６一':'6a', '６二':'6b', '６三':'6c', '６四':'6d', '６五':'6e', '６六':'6f', '６七':'6g', '６八':'6h', '６九':'6i',
    '７一':'7a', '７二':'7b', '７三':'7c', '７四':'7d', '７五':'7e', '７六':'7f', '７七':'7g', '７八':'7h', '７九':'7i',
    '８一':'8a', '８二':'8b', '８三':'8c', '８四':'8d', '８五':'8e', '８六':'8f', '８七':'8g', '８八':'8h', '８九':'8i',
    '９一':'9a', '９二':'9b', '９三':'9c', '９四':'9d', '９五':'9e', '９六':'9f', '９七':'9g', '９八':'9h', '９九':'9i',
}

Piece_Black = {
    '歩': 'P', '香': 'L', '桂': 'N', '銀': 'S', '金': 'G', '角': 'B', '飛': 'R', 
}

promotion = ['と金', '成香', '成桂', '成銀', '馬', '龍']


board  = cshogi.Board()

# ex) '３四歩(33)' -> '3c3d', '５一銀打' -> '5a*S'
def sfen_format(number, move, tmp):

    # '同'が含まれる場合
    if '同' in move:
        if len(move) == 6: #同銀(56)
            piece_from = Number[re.findall("(?<=\().+?(?=\))", move)[0]] # 6h
            tmp = tmp.replace('+', '') # +を削除(tmpが成の場合に対応)
            piece_to = tmp[-2:] # tmpの後ろ2文字を抽出
            sfen_move = piece_from + piece_to
            
        elif len(move) == 7: #同香成(99), 同成香(99)
            if '成香' in move or '成桂' in move or '成銀' in move:
                piece_from = Number[re.findall("(?<=\().+?(?=\))", move)[0]]
                tmp = tmp.replace('+', '') # +を削除(tmpが成の場合に対応)
                piece_to = tmp[-2:] # tmpの後ろ2文字を抽出
                sfen_move = piece_from + piece_to
            else:
                piece_from = Number[re.findall("(?<=\().+?(?=\))", move)[0]]
                tmp = tmp.replace('+', '') # +を削除(tmpが成の場合に対応)
                piece_to = tmp[-2:] # tmpの後ろ2文字を抽出
                sfen_move = piece_from + piece_to + '+'
            
    # '打'が含まれる場合   
    elif move[-1] == '打':
        a = Piece_Black[move[-2]] + '*'
        b = move[:2].replace(move[:2], Kanji[move[:2]])     
        sfen_move = a + b
    
    # '成'が含まれる場合
    elif '成' in move:
        # '成香', '成桂', '成銀'の場合
        if '成香' in move or '成桂' in move or '成銀' in move:
            r = re.findall("(?<=\().+?(?=\))", move) 
            a = r[0].replace(r[0], Number[r[0]])
            b = move[:2].replace(move[:2], Kanji[move[:2]])
            sfen_move = a + b
        else:
            r = re.findall("(?<=\().+?(?=\))", move) 
            a = r[0].replace(r[0], Number[r[0]])
            b = move[:2].replace(move[:2], Kanji[move[:2]])
            sfen_move = a + b + '+'
        
    # '投了'が含まれる場合
    elif move == '投了':
        return 'resign'
    
    #　普通の指し手
    else:
        r = re.findall("(?<=\().+?(?=\))", move) 
        a = r[0].replace(r[0], Number[r[0]])
        b = move[:2].replace(move[:2], Kanji[move[:2]])
        sfen_move = a + b
    return sfen_move
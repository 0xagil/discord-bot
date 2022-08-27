import getopt
import random
import sys
from itertools import product

class BracketUnbalanced(Exception):
    pass

def spin_text(text):
    opening_b = text.find('{')

    if opening_b == -1:
        return text

    opening_b2 = text.find('{', opening_b+1)
    closing_b = text.find('}', opening_b+1)

    if closing_b == -1:
        raise BracketUnbalanced()

    if opening_b2 != -1 and opening_b2 < closing_b:
        # brackets inside
        text = text[:opening_b2] + spin_text(text[opening_b2:])
        return spin_text(text)

    content = text[opening_b+1:closing_b]
    choice = random.choice(content.split('|'))
    text = text[:opening_b] + choice + text[closing_b+1:]
    return spin_text(text)

latin_script = {
    'a': ['á','à','â','ǎ','ă','ã','ả','ȧ','ạ','å','ḁ','ā','ą','ᶏ','ⱥ','ȁ','ấ','ầ','ẫ','ẩ','ậ','ắ','ằ','ẵ','ẳ','ặ','ǻ','ǡ','ǟ','ȁ','ȃ','ɑ'],
    'b': ['ḃ','ḅ','ḇ','ƀ','ᵬ','ᶀ','ｂ'],
    'c': ['ć','ĉ','č','ċ','̄c̄','Ç','ç','Ḉ','ḉ','ƈ','ɕ','ᴄ','ｃ'],
    'd': ['ď','ḋ','ḑ','ḍ','ḓ','ḏ','đ','ð','̦d̦','ɖ','ɗ','ᵭ','ᶁ','ᶑ','ȡ','ᴅ','ｄ'],
    'e': ['é','è','ê','ḙ','ě','ĕ','ẽ','ḛ','ẻ','ė','ë','ē','ȩ','ę','ᶒ','ȅ','ế','ề','ễ','ể','ḝ','ḗ','ḕ','ȇ','ẹ','ệ','ⱸ','ｅ'],
    'f': ['ḟ','ƒ','ᵮ','ᶂ','ꜰ','ｆ'],
    'g': ['ǵ','ğ','ĝ','ǧ','ġ','ģ','ḡ','ǥ','ᶃ'],
    'h': ['ĥ','ȟ','ḧ','ḣ','ḩ','ḥ','ḫ','̱ẖ','ħ','ⱨ'],
    'i': ['Í','í','ì','Ĭ','ĭ','î','Ǐ','ǐ','ï','ḯ','Ĩ','ĩ','Į','į','ī','Ỉ','ỉ','ȉ','Ȋ','ȋ','Ị','ị','Ḭ','ḭ','ɨ','ᶖ','İ','ı','ｉ'],
    'j': ['ĵ','ɉ','̌ǰ','ȷ','ʝ','ｊ'],
    'k': ['ḱ','Ǩ','ǩ','Ķ','ķ','Ḳ','ḳ','Ḵ','ḵ','ƙ','Ⱪ','ⱪ','ᶄ','ᶄ','ꝁ','ᴋ'],
    'l': ['ĺ','ľ','ļ','Ḷ','ḷ','ḹ','ḽ','Ḻ','ḻ','Ŀ','ŀ','Ƚ','ƚ','Ⱡ','ⱡ','Ɫ','ɭ','ȴ','ʟ','Ｌ','ｌ'],
    'm': ['ḿ','ṁ','ṃ','ᵯ','ᶆ','ɱ','ｍ'],
    'n': ['ń','ǹ','ň','ñ','ṅ','ņ','ṇ','ṋ','ṉ','̈n̈','ɲ','ƞ','ᶇ','ɳ','ȵ','ɴ','ŋ'],
    'o': ['ó','ò','ŏ','ô','ố','ồ','ỗ','ổ','Ǒ','ǒ','Ö','ö','ȫ','Ő','ő','Õ','õ','ṍ','Ṏ','ṏ','ȭ','Ȯ','ȯ','ȱ','Ø','ø','Ǿ','ǿ','Ǫ','ǫ','Ǭ','ǭ','Ō','ō','Ṓ','ṓ','Ṑ','ṑ','Ỏ','ỏ','ȍ','ȏ','Ơ','ơ','ớ','ờ','ỡ','ở','ợ','Ọ','ọ','ộ','Ɵ','ɵ','ⱺ','ｏ'],
    'p': ['ṕ','Ṗ','ṗ','Ᵽ','ᵽ','Ƥ','ƥ','̃p','ᶈ','ᴘ'],
    'q': ['ɋ','ʠ','ｑ'],
    'r': ['ŕ','ř','ṙ','ŗ','ȑ','ȓ','ṛ','ṝ','ṟ','ɽ','ᶉ','ɼ','ɾ','ｒ'],
    's': ['ś','ṥ','Ŝ','ŝ','Š','š','Ṧ','ṧ','ṡ','ẛ','ş','ṣ','ṩ','ș','̩s̩','ᵴ','ᶊ','ʂ','ȿ','ꜱ','ｓ'],
    't': ['ť','ṫ','ţ','ṭ','ț','ṱ','ṯ','ƭ','ʈ','ƫ','ȶ','ｔ'],
    'u': ['Ú','ú','ù','Ŭ','ŭ','Û','û','Ǔ','ǔ','Ů','ů','Ü','ü','Ǘ','ǘ','Ǜ','ǜ','Ǚ','ǚ','Ǖ','ǖ','ű','ũ','ų','ū','Ṻ','ṻ','ủ','ȕ','ȗ','Ư','ư','ứ','Ừ','ừ','ữ','Ử','ử','Ự','ự','ụ','Ṳ','ṳ','ᴜ','ｕ','ᵫ'],
    'v': ['Ṽ','ṽ','Ṿ','ṿ','Ʋ','ⱱ','ⱴ','ᴠ'],
    'w': ['Ẃ','ẃ','Ẁ','ẁ','Ŵ','ŵ','Ẅ','ẅ','Ẇ','ẇ','Ẉ','ẉ','ẘ','ẘ','Ⱳ','ⱳ','ᴡ','ｗ'],
    'x': ['Ẍ','ẍ','Ẋ','ẋ','ᶍ''ｘ'],
    'y': ['Ý','ý','Ỳ','ỳ','Ŷ','ŷ','ẙ','Ÿ','ÿ','Ỹ','ỹ','Ẏ','ẏ','Ȳ','ȳ','Ỷ','ỷ','Ỵ','ỵ','Ɏ','ɏ','Ƴ','ƴ','ｙ'],
    'z': ['Ź','ź','Ẑ','ẑ','Ž','ž','Ż','ż','Ẓ','ẓ','Ẕ','ẕ','Ƶ','ƶ','Ȥ','ȥ','Ⱬ','ⱬ','ᵶ','ᶎ','ʐ','ʑ','ɀ','ᴢ','ｚ']
}

def punycode_maker(text):
    possible = []
    for letter in text:
        if letter in latin_script:
            other = random.choice(latin_script[letter])
            new = text.replace(letter, other)
            possible.append(new)
    return random.choice(list(set(possible)))
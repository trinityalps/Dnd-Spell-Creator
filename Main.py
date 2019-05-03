import gc

from PIL import Image
import csv
from collections import OrderedDict
import re
from PIL import ImageFont
from PIL import ImageDraw
import time

#Cause roman numerals look more magic.
def write_roman(num):

    roman = OrderedDict()
    roman[1000] = "M"
    roman[900] = "CM"
    roman[500] = "D"
    roman[400] = "CD"
    roman[100] = "C"
    roman[90] = "XC"
    roman[50] = "L"
    roman[40] = "XL"
    roman[10] = "X"
    roman[9] = "IX"
    roman[5] = "V"
    roman[4] = "IV"
    roman[1] = "I"

    def roman_num(num):
        for r in roman.keys():
            x, y = divmod(num, r)
            yield roman[r] * x
            num -= (r * x)
            if num > 0:
                roman_num(num)
            else:
                break

    return "".join([a for a in roman_num(num)])

#Defines components of a spell.
class Spell:
    def __init__(self, name, level, casttime, duration, com, rng, school):
        self.name = name
        self.level = level
        self.casttime = casttime
        self.duration = duration
        self.com = com
        self.rng = rng
        self.school = school

#Basically where to place the various spell elements in each picture.
class School:
    def __init__(self, image, point1, point2, point3, point4, point5):
        self.image = image
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3
        self.point4 = point4
        self.point5 = point5

#Each element is around 175*175 pixels
i = 175
j = 87
#This is the awful function that places each element in the pictures. Yep it's rough....
#(rangepic, scho.point4), (durpic, scho.point3)castpic, scho.point1)(levelpic, scho.point)(compic, scho.point5)
abjuration = School("School-A.png", (75, 3), (1255, 73), (1255, 650), (0, 650), (668, 1325))
conjuration = School(
    "School-C.png", (250-i, 650-i), (755-j, 290-i), (1250, 650-i), (1050, 1225), (440-i, 1225))
divination = School(
    "School-D.png", (80, 900-i), (755-j, 250-i), (1250, 900-i), (1210, 1250), (275-i, 1250))
enchantment = School(
    "School-EN.png", (410-i, 620-i), (755-j, 250-i), (1100, 620-i), (840, 1250), (665-i, 1250))
evocation = School(
    "School-EV.png", (250-i, 540-i), (650-j, 250-i), (1250, 655), (650-j, 1250), (250-i, 965))
illusion = School(
    "School-I.png", (450-i, 675-i), (755-j, 450-i), (1060, 600), (940, 1045), (560-i, 1045))
necromancy = School(
    "School-N.png", (375-i, 450-i), (755-j, 1250), (1125, 450-i), (1125, 1250), (375-i, 1250))
transmutation = School(
    "School-T.png", (260-i, 260-i), (690, 700-i), (1245, 260-i), (1245, 1245), (260-i, 1245))

L = []

#Where the spellbook csv is located on the disk
SpellCSVLocation = 'C:/path'
#Rows needed Name, School, Level, Cast_Time, Duration, Components, Range
with open(SpellCSVLocation, newline='') as csvfile:
    spamreader = csv.DictReader(csvfile)
    for row in spamreader:
        school = row['School']
        level = row['Level']
        name = row['Name']
        casttime = row['Cast_Time']
        duration = row['Duration']
        com = row['Components']
        rng = row['Range']
        x = Spell(re.sub('[^0-9a-zA-Z]+', '', name), level, casttime, duration, com, rng, school)
        L.append(x)

gc.enable()
for s in L:
    gc.collect()
    scho = 0
    
#Picking the image corresponding to the school of magic
    if 'Necromancy' in s.school:
        scho = necromancy
    elif 'Abjuration' in s.school:
        scho = abjuration
    elif 'Conjuration' in s.school:
        scho = conjuration
    elif 'Divination' in s.school:
        scho = divination
    elif 'Evocation' in s.school:
        scho = evocation
    elif 'Enchantment' in s.school:
        scho = enchantment
    elif 'Illusion' in s.school:
        scho = illusion
    elif 'Transmutation' in s.school:
        scho = transmutation
    else:
        scho = abjuration

    image_copy = Image.open(scho.image)
    rangepic = 0
    castpic = 0
    durpic = 0
    levelpic = 0
    compic = 0
    font = ImageFont.truetype("Livingst.ttf", 48)
    print(rangepic)

    #region Range
    #Sets the range pick and adds text if there is a distance measure.
    if 'Self' in s.rng:
        if 'radius' in s.rng:
            rangepic = Image.open('Range-R.png')
            rnum = write_roman(int(re.search(r'\d+', s.rng).group()))
            draw = ImageDraw.Draw(rangepic)
            w, h = draw.textsize(rnum)
            draw.text((175-w, 175-h), rnum, (0, 0, 0), font=font)
            del draw
        elif 'cone' in s.rng:
            rangepic = Image.open('Range-C.png')
            rnum = write_roman(int(re.search(r'\d+', s.rng).group()))
            draw = ImageDraw.Draw(rangepic)
            draw.text((0, 0), rnum, (0, 0, 0), font=font)
            del draw
        elif 'cube' in s.rng:
            rangepic = Image.open('Range-CU.png')
            rnum = write_roman(int(re.search(r'\d+', s.rng).group()))
            draw = ImageDraw.Draw(rangepic)
            draw.text((0, 0), rnum, (0, 0, 0), font=font)
            del draw
        elif 'line' in s.rng:
            rangepic = Image.open('Range-L.png')
            rnum = write_roman(int(re.search(r'\d+', s.rng).group()))
            draw = ImageDraw.Draw(rangepic)
            draw.text((0, 0), rnum, (0, 0, 0), font=font)
            del draw
        else:
            rangepic = Image.open('Range-F.png')
    elif 'feet' in s.rng:
        rangepic = Image.open('Range-F.png')
        rnum = write_roman(int(re.search(r'\d+', s.rng).group()))
        draw = ImageDraw.Draw(rangepic)
        draw.text((0, 0), rnum, (0, 0, 0), font=font)
        del draw
    elif 'Touch' in s.rng:
        rangepic = Image.open('Range-T.png')
    else:
        rangepic = Image.open('Range-F.png')

    image_copy.paste(rangepic, scho.point4, rangepic)
    rangepic.close()
    #endregion

    #region Casting Time

    if 'reaction' in s.casttime:
        castpic = Image.open('Cast-R.png')
    elif 'bonus action' in s.casttime:
        castpic = Image.open('Cast-BA.png')
    elif 'action' in s.casttime:
        castpic = Image.open('Cast-A.png')
    elif 'minute' in s.casttime:
        castpic = Image.open('Cast-M.png')
        cnum = write_roman(int(re.search(r'\d+', s.casttime).group()))
        draw = ImageDraw.Draw(castpic)
        w, h = draw.textsize(cnum)
        draw.text((0, 82), cnum, (0, 0, 0), font=font)
        del draw
    elif 'hour' in s.casttime:
        castpic = Image.open('Cast-H.png')
        cnum = write_roman(int(re.search(r'\d+', s.casttime).group()))
        draw = ImageDraw.Draw(castpic)
        w, h = draw.textsize(cnum)
        draw.text((175-w, 175-h), cnum, (0, 0, 0), font=font)
        del draw
    else:
        castpic = Image.open('Cast-A.png')
    image_copy.paste(castpic, scho.point1, castpic)
    castpic.close()
    #endregion

    #region Duration
    print(s.name)
    if 'Instant' in s.duration:
        print("Instant")
        durpic = Image.open('Dur-I.png')
        durpic.load()
    elif 'min' in s.duration:
        print("min")
        if 'Concentration' in s.duration:
            durpic = Image.open('Dur-CM.png')
            durpic.load()
        else:
            durpic = Image.open('Dur-M.png')
            durpic.load()
        dnum = write_roman(int(re.search(r'\d+', s.duration).group()))
        draw = ImageDraw.Draw(durpic)
        w, h = draw.textsize(dnum)
        draw.text((15, 50), dnum, (0, 0, 0), font=font)
        del draw
    elif 'hour' in s.duration:
        print("hour")
        dnum = write_roman(int(re.search(r'\d+', s.duration).group()))
        if 'Concentration' in s.duration:
            durpic = Image.open('Dur-CH.png')
            durpic.load()
            draw = ImageDraw.Draw(durpic)
            w, h = draw.textsize(dnum)
            draw.text((20, 140), dnum, (0, 0, 0), font=font)
            del draw
        else:
            durpic = Image.open('Dur-H.png')
            durpic.load()
            draw = ImageDraw.Draw(durpic)
            w, h = draw.textsize(dnum)
            draw.text((20, 50), dnum, (0, 0, 0), font=font)
            del draw
    elif 'day' in s.duration:
        print("day")
        dnum = write_roman(int(re.search(r'\d+', s.duration).group()))
        if 'Concentration' in s.duration:
            durpic = Image.open('Dur-CD.png')
            durpic.load()
            draw = ImageDraw.Draw(durpic)
            w, h = draw.textsize(dnum)
            draw.text((5, 10), dnum, (0, 0, 0), font=font)
            del draw
        else:
            durpic = Image.open('Dur-D.png')
            durpic.load()
            draw = ImageDraw.Draw(durpic)
            w, h = draw.textsize(dnum)
            draw.text((0, 0), dnum, (0, 0, 0), font=font)
            del draw
    elif 'round' in s.duration:
        print("round")
        durpic = Image.open('Dur-R.png')
        durpic.load()
        dnum = write_roman(int(re.search(r'\d+', s.duration).group()))
        draw = ImageDraw.Draw(durpic)
        w, h = draw.textsize(dnum)
        draw.text((70, 20), dnum, (0, 0, 0), font=font)
        del draw
    elif 'Until' in s.duration:
        print("Until")
        durpic = Image.open('Dur-R.png')
        durpic.load()
    else:
        print("Hell if I know")
        durpic = Image.open('Dur-S.png')
        durpic.load()
    image_copy.paste(durpic, scho.point3, durpic)
    durpic.close()
    #endregion

    #region Components
    if 'V,S,M' in s.com:
        compic = Image.open('Com-VSM.png')
    elif "V,S" in s.com:
        compic = Image.open('Com-VS.png')
    elif "V,M" in s.com:
        compic = Image.open('Com-VM.png')
    elif "S,M" in s.com:
        compic = Image.open('Com-SM.png')
    elif "V" in s.com:
        compic = Image.open('Com-V.png')
    elif "S" in s.com:
        compic = Image.open('Com-S.png')
    elif "M" in s.com:
        compic = Image.open('Com-M.png')
    else:
        compic = Image.open('Com-VSM.png')
    image_copy.paste(compic, scho.point5, compic)
    compic.close()
    #endregion

    #region Level
    levelroman = 0
    if '0' in s.level:
        levelroman = 'O'
    else:
        levelroman = write_roman(int(re.search(r'\d+', s.level).group()))
    levelpic = Image.new('RGBA', (175, 175), (255, 0, 0, 0))
    d = ImageDraw.Draw(levelpic)
    fnt = ImageFont.truetype("Livingst.ttf", 150)
    w, h = d.textsize(levelroman)
    d.text((0, 0), levelroman, (0, 0, 0), font=fnt)
    del d
    image_copy.paste(levelpic, scho.point2, levelpic)
    levelpic.close()
    #endregion
    #The files are saved as the spell name, so for instance Aid.png
    imgpath = 'C:/output/' + s.name + '.png'
    image_copy.save(imgpath)
    image_copy.close()
    gc.collect()


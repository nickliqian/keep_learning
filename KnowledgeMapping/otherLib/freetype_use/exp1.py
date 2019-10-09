import freetype


face = freetype.Face(r"D:\FeigeDownload\微软雅黑繁简完全版.ttf")
face.set_char_size(48*64)
face.load_char('S')
bitmap = face.glyph.bitmap
print(bitmap.buffer)

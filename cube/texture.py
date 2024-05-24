from PIL import Image
from OpenGL.GL import *

class Texture:
    def __init__(self, name, path):
        self.tex_path = path
        self.name = name
        self.img = Image.open(path)
        if 'tex' in path:
            self.img = self.img.rotate(90, expand=True)
        self.img = self.img.transpose(Image.FLIP_TOP_BOTTOM)
        self.img_buffer = self.img.convert('RGBA').tobytes()

    def load_texture(self):
        self.texture_id = glGenTextures(1)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.img.width, self.img.height,
                     0, GL_RGBA, GL_UNSIGNED_BYTE, self.img_buffer)

    def use(self):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)

    def destroy(self):
        glDeleteTextures(1,(self.texture_id,))
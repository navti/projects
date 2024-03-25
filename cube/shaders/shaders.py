from OpenGL.GL.shaders import *
from OpenGL.GL import *

__all__ = ['create_shader_program']

def create_shader_program(vertex_shader_filepath, fragment_shader_filepath):
    vertex_shader = compile_shader_module(vertex_shader_filepath, GL_VERTEX_SHADER)
    fragment_shader = compile_shader_module(fragment_shader_filepath, GL_FRAGMENT_SHADER)
    program_shader = compileProgram(vertex_shader, fragment_shader)
    return program_shader

def compile_shader_module(shader_source_filepath, shader_type):
    with open(shader_source_filepath, "r") as f:
        source = f.readlines()    
    return compileShader(source, shader_type)
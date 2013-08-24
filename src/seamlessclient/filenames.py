from seamlessclient import compiled_filename_extension, scad_extension

def get_filename_for_compiled_file(scadfilename):
    if has_scad_extension(scadfilename) and not is_compiled_file(scadfilename):
        return scadfilename[:-len(scad_extension)] + compiled_filename_extension
    else:
        raise NotAScadFile()

def has_scad_extension(filename):
    return len(filename) > len(scad_extension) and filename[-len(scad_extension):] == scad_extension

def is_compiled_file(filename):
    return len(filename) > len(compiled_filename_extension) and filename[-len(compiled_filename_extension):] == compiled_filename_extension

class NotAScadFile:
    pass
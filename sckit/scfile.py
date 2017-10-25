import os


cl_for_mkdir = set()
def mkdir_if_missing( dir_pth ):
    '''
    create directory for the specified path, pass if it already exists or being checked
    '''
    global cl_for_mkdir
    if dir_pth in cl_for_mkdir:
        pass
    else:
        if not os.path.exists( dir_pth ):
            os.makedirs( dir_pth )
        cl_for_mkdir.add( dir_pth )

cl_for_rmdir = set()
def rmdir_if_exists( dir_pth ):
    '''
    remove directory for the specified path, pass if it already exists or being checked
    '''
    global cl_for_rmdir
    if dir_pth in cl_for_rmdir:
        pass
    else:
        if os.path.exists( dir_pth ):
            os.removedirs( dir_pth )
        cl_for_rmdir.add( dir_pth )


if __name__ == '__main__':

    mkdir_if_missing( 'test' )
    mkdir_if_missing( 'test' )
    mkdir_if_missing( 'test2' )

    rmdir_if_exists( 'test3' )
    rmdir_if_exists( 'test2' )


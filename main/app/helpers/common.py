from inspect import getframeinfo

def whoami(frame): 
    """
    Docstring for whoami
    
    :param frame: Description
    :return: Description
    :rtype: Any
    """

    frame_info = getframeinfo(frame)
    #print(f'Frame Function = {frame_info.function}')
    filename = frame_info.filename.split('\\')[-1]
    if frame_info.function == "<module>":
        #print("It's a file...")
        return filename
    return f'{filename}::{getframeinfo(frame).function}'

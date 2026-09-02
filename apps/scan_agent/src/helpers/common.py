from inspect import getframeinfo

def whoami(frame): 
    """
    Docstring for whoami
    
    :param frame: Description
    :return: Description
    :rtype: Any
    """

    frame_info = getframeinfo(frame)
    #print(f'{frame=}')
    #print(f'{frame_info.__module__=}')
    #print(f'{frame_info.function=}')
    good = False
    module_name = ''
    for o in frame_info.filename.split('\\'):
        if good:
            if not module_name == '':
                module_name += '.'
            module_name += o.split('.')[0]
        if o == 'app':
            good = True
    #print(f'{module_name=}')
    #filename = frame_info.filename.split('\\')[-1]
    if frame_info.function == "<module>":
        #print("It's a file...")
        return module_name
    return f'{module_name}::{frame_info.function}'

def extract_info(script):
    title = None
    music = None
    desc = None
    tags = None
    print(script)
    if '[Title: ' in script:
        title = script.split('[Title: ')[1].split(']')[0]
        script = script.replace(f'[Title: {title}]', '')
        print(f'Title: {title}')
    if '[Music: ' in script:
        music = script.split('[Music: ')[1].split(']')[0]
        script = script.replace(f'[Music: {music}]', '')
        print(f'Music: {music}')
    if '[Description: ' in script:
        desc = script.split('[Description: ')[1].split(']')[0]
        script = script.replace(f'[Description: {desc}]', '')
        print(f'Description: {desc}')
    if '[Tags: ' in script:
        tags = script.split('[Tags: ')[1].split(']')[0]
        script = script.replace(f'[Tags: {tags}]', '')
        print(f'Tags: {tags}')
    return title, music, desc, tags, script
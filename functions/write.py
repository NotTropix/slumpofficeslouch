def write_files(titlefix, desc, tags):
    with open(f'{titlefix}_desc.txt', 'w') as f:
        f.write(desc)
    print("Description written to file")
    with open(f'{titlefix}_tags.txt', 'w') as f:
        f.write(tags)
    print("Tags written to file")
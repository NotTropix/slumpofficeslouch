from opengpt.models.completion.usesless.model import Model

def get_video_input(prompt_file='prompt.txt'):
    with open(prompt_file, 'r') as f:
        prompt = f.read()
    video_input = input("What is the video about: ")
    return prompt + " " + video_input
    
def generate_script(prompt):
    usesless = Model()
    usesless.SetupConversation(prompt)
    script = ""
    for r in usesless.SendConversation():
        script += r.choices[0].delta.content

    return script

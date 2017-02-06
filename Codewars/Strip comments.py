def solution(inp_t,markers):
    text = inp_t.split("\n")
    result = []
    for i in range(len(text)):
        for j in range(len(markers)):
            if text[i].find(markers[j]) != -1:
                text[i] = text[i][:text[i].find(markers[j])].rstrip()
            else: continue
    return '\n'.join(text)

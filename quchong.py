def remove_duplicate_lines():
    lines_seen = set()
    result_lines = []
    with open('readme.md', 'r') as file:
        for line in file:
            line = line.rstrip("\n")  # 去除每行末尾的换行符
            if line not in lines_seen:
                lines_seen.add(line)
                result_lines.append(line)
    with open('readme.md', 'w') as file:
        for line in result_lines:
            file.write(line + "\n")

if __name__ == "__main__":
    weibo = remove_duplicate_lines()
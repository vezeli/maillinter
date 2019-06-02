import textcontent


def read_email(email_path):
    with open(email_path, 'r') as f:
        text = f.read()
    paragraphs = text.split('\n\n')
    paragraphs = [
        textcontent.Paragraph(i, content, 'simple') for i, content in
                                                    enumerate(paragraphs)
    ]

    return textcontent.TextContent(paragraphs)

if __name__ == '__main__':
    email_file = 'input_file.txt'
    mail = read_email(email_file)

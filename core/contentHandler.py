"""ContentHandler.py: transforms the JSON into an acceptable data format."""
import requests
import json


class ContentHandler(object):
    """returns a string of HTML with the relevant content."""

    def create_katex(self, latex_string):
        """Convert string of latex into katex."""
        resp = requests.post(
            "http://localhost:8080/",
            data=json.dumps({'latex': latex_string}),
            headers={'Content-Type': 'application/json'})
        return resp.text

    def create_image(self, latex):
        """Create image from latex."""
        pass

    def break_into_lines(self, list_of_blocks):
        """Return an array of arrays, each array denoting lines."""
        lines = []

        line = [list_of_blocks[0]]
        if len(list_of_blocks) == 1:
            lines.append(line)
            return lines
        # separate content into lines
        else:
            print("boop!")
            for block in list_of_blocks[1:]:
                if "inline" in block and block["inline"] is True:
                    # print("It's inline")
                    # print(line)
                    line.append(block)
                    # print(line)
                    # print("---------")
                else:
                    print("It's not inline!")
                    # add line to lines
                    lines.append(line)
                    # start a new line
                    line = [block]
        # case where last line is True,
        if line != []:
            lines.append(line)

        return lines

    def get_formatted_content(self, list_of_blocks):
        """Convert list of block content and returns HTML."""
        lines = self.break_into_lines(list_of_blocks)
        content = ""

        for line in lines:
            line_of_text = ""

            for block in line:
                if 'text' in block:
                    line_of_text += block["text"]

                elif 'latex' in block:
                    line_of_text += self.create_katex(block["latex"])

                elif 'image' in block:
                    # TODO: process the image
                    # get the URL where image is stored
                    line_of_text += "<img src='{}' />".format(block['image'])

                else:
                    raise Exception(
                        "Block does not contain image, text or latex")
            # check if it is a simgle image and don't wrap with p tags
            content += "<p>" + line_of_text + "</p>"

        return content

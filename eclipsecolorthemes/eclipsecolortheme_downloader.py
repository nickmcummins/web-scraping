import requests
import sys
from bs4 import BeautifulSoup

COLOR_SETTINGS = ["searchResultIndication", "filteredSearchResultIndication", "occurrenceIndication",
                  "writeOccurrenceIndication", "findScope", "deletionIndication", "sourceHoverBackground",
                  "singleLineComment", "multiLineComment", "commentTaskTag", "javadoc", "javadocLink", "javadocTag",
                  "javadocKeyword", "class", "interface", "method", "methodDeclaration", "bracket", "number", "string",
                  "operator", "keyword", "annotation", "staticMethod", "localVariable", "localVariableDeclaration",
                  "field", "staticField", "staticFinalField", "deprecatedMember", "enum", "inheritedMethod",
                  "abstractMethod", "parameterVariable", "typeArgument", "typeParameter", "constant", "background",
                  "currentLine", "foreground", "lineNumber", "selectionBackground", "selectionForeground"]


class SettingEntry:
    def __init__(self, setting_entry):
        self.setting_entry = setting_entry
        self.name = self.parse_name()
        self.value = self.parse_value()

    def parse_name(self):
        return self.setting_entry.find_all('div', {'class': 'setting'})[0].text

    def parse_value(self):
        return self.setting_entry.find_all('input')[0].attrs['value']

    def __repr__(self):
        return f'<{self.name} color="{self.value}" />'


class EclipseColorTheme:
    XML_LINE = '<?xml version="1.0" encoding="utf-8"?>\n'

    def __init__(self, url):
        self.id = url.split('&')[-1].split('=')[1]
        self.soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        self.name = self.soup.h2.b.text
        self.author = self.soup.h2.span.span.text
        self.colors_dict = self.build_colors_dict()

    def build_colors_dict(self):
        setting_entries = list(map(lambda entry: SettingEntry(entry), self.soup.find_all('div', {'class': 'setting-entry'})))
        colors_dict = {}
        for setting_entry in setting_entries:
            colors_dict[setting_entry.name] = setting_entry

        return colors_dict

    def __repr__(self):
        color_tags = "\n".join(list(map(lambda color: f'\t{str(color)}', self.colors_dict.values())))
        return """<?xml version="1.0" encoding="utf-8"?>
<colorTheme id="%s" name="%s" author="%s">
%s
</colorTheme>""" % (self.id, self.name, self.author, color_tags)

    def write_to_file(self):
        filename = self.name.replace(' ', '-') + '.xml'
        with open(filename, 'w') as file:
            file.write(str(self))
            print(f'Wrote {filename}.')


if __name__ == '__main__':
    theme = EclipseColorTheme(sys.argv[1])
    print(theme)
    theme.write_to_file()

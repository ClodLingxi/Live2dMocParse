class Live2DMotionParser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = {}
        self.fps = 30
        self.fadein = 1000
        self.fadeout = 1000
        self.parse()

    def parse(self):
        with open(self.filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            if line.startswith('$fps='):
                self.fps = int(line.split('=')[1])
            elif line.startswith('$fadein='):
                self.fadein = int(line.split('=')[1])
            elif line.startswith('$fadeout='):
                self.fadeout = int(line.split('=')[1])
            elif line.startswith('$fadein:'):
                param, duration = self._parse_fade_line(line)
                self._add_fade_data(param, duration, 'fadein')
            elif line.startswith('$fadeout:'):
                param, duration = self._parse_fade_line(line)
                self._add_fade_data(param, duration, 'fadeout')
            else:
                param_name, values = self._parse_param_line(line)
                self.data[param_name] = [float(v) for v in values.split(',')]

    def _add_fade_data(self, param, duration, fade_type):
        if 'fade' not in self.data:
            self.data['fade'] = {}
        if fade_type not in self.data['fade']:
            self.data['fade'][fade_type] = {}
        self.data['fade'][fade_type][param] = duration

    @staticmethod
    def _parse_fade_line(line):
        parts = line.split(':')
        param = parts[1].split('=')[0]
        duration = int(parts[1].split('=')[1])
        return param, duration

    @staticmethod
    def _parse_param_line(line):
        data = line.split(':')
        if len(data) == 2:
            return data[0], float(data[1])
        raise ValueError(f"Unexpected line format: {line}")


# Example usage
if __name__ == "__main__":
    parser = Live2DMotionParser('temp/angry01.mtn')
    print("FPS:", parser.fps)
    print("Fade In Duration:", parser.fadein)
    print("Fade Out Duration:", parser.fadeout)
    for i in parser.data:
        print(i, parser.data[i], len(parser.data[i]))
    for i in parser.data['fade']:
        print(i, parser.data['fade'][i], len(parser.data['fade'][i]))
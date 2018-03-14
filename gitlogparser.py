import re

source_line_matcher = re.compile('\d+\s+\d+\s+([\w\/\\\.]+)$')


class GitLogParser(object):
    def __init__(self):
        self.commit_set = []
    def feed(self, text):
        for line in text:
            match = source_line_matcher.match(line)
            if match:
                filename = match.group(1)
                self.commit_set.append(filename)
            else:
                if self.commit_set:
                    yield self.commit_set
                    self.commit_set = []
        if self.commit_set:
            yield self.commit_set

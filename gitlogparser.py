import re

source_line_matcher = re.compile('\d+\s+\d+\s+([\w\/\\\.]+)$')


class GitLogParser(object):

    def feed(self, text):
        commit_set = []
        for line in text:
            match = source_line_matcher.match(line)
            if match:
                filename = match.group(1)
                commit_set.append(filename)
            else:
                if commit_set:
                    yield commit_set
                    commit_set = []
        if commit_set:
            yield commit_set
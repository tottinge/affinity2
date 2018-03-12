import unittest
import os
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


class Test_Parser(unittest.TestCase):
    """
    The git log parser will take in the text created by 'git log --numstat'
    and produce a series of records that tell about files being committed together.
    """
    sample = """$ clear
commit 6587e9d905fc35b557f9ebfc4cb2f950b8e30002
Author: Tim Ottinger <tottinge@industriallogic.com>
Date:   Fri Mar 2 00:31:39 2018 -0600

    Revert "Switch to use org.Json rather than strings - WIP"

    This reverts commit 1a4996743563de9ec568180d4f1eaff74c0fbcfa.

30      25      src/main/java/com/industriallogic/action/PageAction.java
1       0       src/main/java/com/industriallogic/shared/action/Action.java
36      33      src/test/java/com/industriallogic/action/NavigationPageActionTest.java
9       37      src/test/java/com/industriallogic/storytests/CompletionTest.java
""".split("\n")
    sample_files = [
        "PageAction.java",
        "Action.java",
        "NavigationPageActionTest.java",
        "CompletionTest.java",
    ]


    sample2 = sample + """
    
commit 714d0440ca00bbf33540e027bfeffcf6227a76d4
Author: Tim Ottinger <tottinge@industriallogic.com>
Date:   Thu Mar 1 15:30:40 2018 -0600

    Trying to get the language & album selection to agree: a step

6       5       src/main/java/com/industriallogic/action/admin/WorkshopMgmtAdmin.java
16      4       src/main/java/com/industriallogic/action/admin/WorkshopSetupAction.java
18      5       src/templates/admin/workshopMgmt.stg
""".split("\n")
    sample2_files = [
        "WorkshopMgmtAdmin.java",
        "WorkshopSetupAction.java",
        "workshopMgmt.stg"
    ]

    def test_sample(self):
        subject = GitLogParser()
        result = [commit for commit in subject.feed(self.sample)]
        self.assertEqual(1, len(result), "Should be one commit only. [%s]" % result)

        [commit] = result
        self.assertEqual(4, len(commit))
        filenames = self.raw_filenames_from(commit)
        for name in self.sample_files:
            self.assertIn(name, filenames)

    def raw_filenames_from(self, file_list):
        return [os.path.split(s)[1] for s in file_list]

    def test_two_commits(self):
        subject = GitLogParser()
        result = [ commit for commit in subject.feed(self.sample2)]
        self.assertEqual(2, len(result), "Should be two commits [%s]" % result)
        [_, commit] = result;
        commit_files = self.raw_filenames_from(commit)
        for filenames in self.sample2_files:
            self.assertIn(filenames, commit_files)



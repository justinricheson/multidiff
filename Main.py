import pysvn
import argparse
from builtins import print

__author__ = 'justinricheson'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-url", "--url", help="Root url of SVN repository")
    parser.add_argument("-u", "--user", help="SVN username")
    parser.add_argument("-pw", "--password", help="SVN password")
    parser.add_argument("revisions", nargs='+', type=int, help="List of revisions")
    args = parser.parse_args()

    print_changes(args.url, args.user, args.password, args.revisions)


def print_changes(url, username, password, revisions):
    client = pysvn.Client()
    client.set_default_username(username)
    client.set_default_password(password)

    adds = []
    deletes = []
    changes = []
    for i in range(len(revisions)):

        endrev = revisions[i]
        startrev = endrev - 1

        #skip this case for now
        if startrev < 1:
            continue

        summary = client.diff_summarize(
            url,
            revision1=pysvn.Revision(pysvn.opt_revision_kind.number, startrev),
            revision2=pysvn.Revision(pysvn.opt_revision_kind.number, endrev))

        for change in summary:
            if change.data['node_kind'] == pysvn.node_kind.file:
                path = change.data['path']
                changetype = change.data['summarize_kind']
                if changetype == pysvn.diff_summarize_kind.added:
                    if not path in adds:
                        adds.append(path)
                elif changetype == pysvn.diff_summarize_kind.delete:
                    if not path in deletes:
                        deletes.append(path)
                elif changetype == pysvn.diff_summarize_kind.modified:
                    if not path in changes:
                        changes.append(path)

    adds.sort()
    print('\r\nADDED FILES-----------------')
    for add in adds:
        print(add)

    deletes.sort()
    print('\r\nDELETED FILES---------------')
    for delete in deletes:
        print(delete)

    changes.sort()
    print('\r\nCHANGED FILES---------------')
    for change in changes:
        print(change)


if __name__ == "__main__":
    main()

import re
from itertools import permutations
from validate_email import validate_email
import argparse


def mail_exists(mail):
    try:
        return validate_email(mail, verify=True)
    except Exception as e:
        print e
        return False


def letters_appended(split_name):
    strings = []
    for index in range(0, len(split_name)):
        subset = "".join(split_name[0:index + 1])
        for i in range(0, len(subset) + 1):
            strings.append(subset[0:i] + "".join(split_name[index + 1:]))
    return list(set(strings))


def find_emails(name, website):
    split_name = [s.strip() for s in name.lower().split(" ")]

    pattern = re.compile('[a-z0-9][a-z0-9\-]+\.[a-z\.]{2,6}$', re.IGNORECASE)
    actual_domain = pattern.search(website).group().lower()

    possible_emails = []
    for index in range(1, len(split_name) + 1):
        for splits in permutations(split_name, index):
            possible_emails += letters_appended(list(splits))
    emails = list(set(possible_emails))
    emails.sort(lambda a, b: len(b) - len(a))
    return [user + '@' + actual_domain for user in emails[:-1]]


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", "--name", required=True, help="Enter Full Name (Jyothi Babu Araja)")
    ap.add_argument("-d", "--domain", required=True, help="Enter Domain (google.com)")
    args = vars(ap.parse_args())
    name = args["name"]
    domain = args["domain"]
    emails = find_emails(name, domain)
    print "Checking ", len(emails), " emails"
    counter = 0
    for email in emails:
        counter += 1
        if mail_exists(email):
            print email
            break
    if counter == len(emails):
        print "No email address found."

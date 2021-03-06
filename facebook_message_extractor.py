#!env/bin/python3

import argparse
import bs4
import json
import sys

def main(args):
    if args.aliasfile is None:
        aliases = {
                'users': {},
                'threads': {},
                }
    else:
        aliases = json.load(args.aliasfile)

    # Parse ALL the HTML, then extract the contents, and then the threads.
    soup = bs4.BeautifulSoup(args.messages_html, 'html.parser')
    html_threads = soup.body.find('div', 'contents').find_all('div', 'thread')

    # Maintain a list of the threads. We'll apply aliases as we make these.
    threads = {}

    # Loop through the HTML threads.
    for html_thread in html_threads:
        # Initialize the thread to build information for
        thread = {}

        # Names aren't shown here, so we go by aliases if available.
        user_aliases = aliases['users']
        orig_users = [u.strip() for u in html_thread.div.previous_sibling.split(',')]
        thread['users'] = [user_aliases.get(u, u) for u in orig_users]

        thread['messages'] = []
        for html_message in html_thread.find_all('div', 'message'):
            message = {}

            header = html_message.find('div', 'message_header')
            raw_author = header.find('span', 'user').text.strip()
            message['author'] = user_aliases.get(raw_author, raw_author)
            message['date'] = header.find('span', 'meta').text.replace('\n', ' ').strip()

            # For some ABSURD reason, content is outside the message div. We
            # iterate over p tags in the next siblings until we encounter
            # another message. This is probably only 1, but better safe than sorry.
            message['content'] = ''
            for sibling in html_message.next_siblings:
                if type(sibling) is not bs4.element.Tag:
                    continue
                elif sibling.name == 'p':
                    message['content'] += sibling.text.replace('\n', ' ').strip() + '\n'
                else:
                    break
            message['content'] = message['content'].strip()

            thread['messages'].append(message)

        # Construct ID from unique collection of users.
        thread_id = ','.join(sorted(orig_users))
        threads[aliases['threads'].get(thread_id, thread_id)] = thread

    if args.prompt_aliases:
        for thread_id,thread in threads.items():
            for user in thread['users']:
                if user.endswith('@facebook.com') and user not in aliases['users']:
                    facebook_id = user[0:-len('@facebook.com')]
                    alias = input("Who is https://facebook.com/{} ".format(facebook_id))
                    if alias != None:
                        aliases['users'][user] = alias

            if thread_id not in aliases['threads']:
                re_aliased_users = [aliases['users'].get(u, u) for u in thread['users']]
                alias = input("What should this chat with {} be called? "\
                        .format(', '.join(re_aliased_users)))
                if alias != None:
                    aliases['threads'][thread_id] = alias

        aliasfile = input("Where should these aliases be saved? ")
        with open(aliasfile, 'w') as f:
            json.dump(aliases, f, sort_keys=True, indent="    ")

    with open(args.savefile, 'w') as f:
        json.dump(threads, f, sort_keys=True, indent="    ")

def apply_alias(id, aliases):
    if id in aliases['users']:
        return aliases[id]
    else:
        return id

def parse(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("messages_html", type=argparse.FileType('r'))
    parser.add_argument("--aliasfile", "-a", type=argparse.FileType('r'), default=None)
    parser.add_argument("--savefile", "-o", default="messages.json")
    parser.add_argument("--prompt_aliases", "-p", action='store_true')
    return parser.parse_args(args)

if __name__ == "__main__":
    sys.exit(main(parse()))

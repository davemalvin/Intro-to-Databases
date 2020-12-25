import psycopg2
import argparse
import csv
import os, glob
from io import StringIO
import re
from collections import Counter

def parse_args():
    parser = argparse.ArgumentParser( add_help=False )
    parser.add_argument( '--help', action='help',
                         help="print this help message and exit" )
    parser.add_argument( '-v', '--verbose', action='store_true',
                         help="outputs whether the requirements are satisfied (it has no effect with '-a')" )
    parser.add_argument( '-d', '--dbname', metavar='<dbname>', type=str,
                         help=("name of the PostgreSQL database") )
    parser.add_argument( '-u', '--user', metavar='<username>', type=str,
                         help="connect to the database as '%(metavar)s'" )
    parser.add_argument( '-h', '--host', metavar='<hostname>', type=str,
                         help="the machine on which the server is running" )
    parser.add_argument( '-p', '--port', metavar='<port>', type=str,
                         help="the port on which the server is listening" )
    parser.add_argument( '-a', '--answers', metavar='<path/to/answers>', type=str,
                         help="CSV answers file" )
    parser.add_argument( '-f', '--forbidden', metavar='<path/to/forbidden/keywords>', type=str,
                         help="text file with list of forbidden keywords" )
    parser.add_argument( 'query', metavar='<path/to/query>', type=str,
                         help="SQL query file" )
    return parser.parse_args()

def check(solution, candidate):
    sol = Counter(solution)
    ans = Counter(candidate)
    tot_sol = sum(sol.values())
    tot_ans = sum(ans.values())
    correct = sum((sol & ans).values())
    wrong   = sum((ans - sol).values())
    return tot_sol, tot_ans, wrong, correct

def db_connect(args):
    conn_str = ''
    if args.dbname is not None:
        conn_str += (' dbname=' + args.dbname)
    if args.user is not None:
        conn_str += (' user=' + args.user)
    if args.host is not None:
        conn_str += (' host=' + args.host)
    if args.port is not None:
        conn_str += (' port=' + args.port)
    conn = psycopg2.connect(conn_str)
    conn.autocommit = True
    return conn

def load_answers(args):
    if args.answers is None:
        return None
    answers = []
    with open(args.answers, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            answers.append(tuple(line))
    return answers

def load_query(args):
    query = None
    warning = None
    filename = args.query
    k = filename.rfind('/')
    if k >= 0:
        filename = filename[k+1:]
    pattern = "^(0[1-9]|10)\.sql$"
    with open(args.query, 'r') as sqlfile:
        if not re.match(pattern, filename):
            warning = "WARNING: The file name '{}' does not comply with the naming rules".format(filename)
        query = sqlfile.read()
    semicolons = query.count(';')
    if semicolons != 1:
        msg = "ERROR: The query file contains {} semicolons instead of *exactly* 1"
        raise Exception(msg.format(semicolons))
    return (query, warning)

def load_forbidden(args):
    if args.forbidden is None:
        return None
    forbidden = None
    with open(args.forbidden, 'r') as kwfile:
        forbidden = list(map(lambda x: x.strip().upper(), kwfile.readlines()))
    return forbidden

def execute(conn, query):
    cur = conn.cursor()
    cur.execute(query)
    memfile = StringIO()
    writer = csv.writer(memfile)
    writer.writerows(cur.fetchall())
    memfile.flush()
    candidate = []
    reader = csv.reader(memfile.getvalue().splitlines())
    for line in reader:
        candidate.append(tuple(line))
    cur.close()
    return candidate

def check_forbidden(query, forbidden):
    tokens = [x.upper() for x in re.split('\s+|\s*\n+\s*|\s*[,;\(\)]\s*', query) if len(x) > 1]
    for kw in forbidden:
        if kw in tokens:
            msg = "ERROR: The query contains the forbidden keyword '{}'"
            raise Exception(msg.format(kw))

def main():
    args = parse_args()
    forbidden = load_forbidden(args)
    (query, warning) = load_query(args)
    if forbidden is not None:
        check_forbidden(query, forbidden)
    conn = db_connect(args)
    candidate = execute(conn, query)
    answers = load_answers(args)
    if args.verbose and answers is None:
        if warning is not None:
            print("{}: {}".format(args.query, warning))
        else:
            print("{}: OK".format(args.query))
    if answers is not None:
        result = check(answers, candidate)
        print("Expected: {:6} | Returned: {:6} | Wrong: {:6} | Correct: {:6}".format(*result))
    conn.close()

if __name__ == "__main__":
    main()

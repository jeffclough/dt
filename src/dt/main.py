#!/usr/bin/env python3
import os,sys
from argparse import ArgumentParser,RawDescriptionHelpFormatter
from datetime import date,datetime,time,timedelta,timezone,tzinfo
from debug import DebugChannel
from handy import die,gripe
from parsedatetime import Calendar

ap=ArgumentParser(
    formatter_class=RawDescriptionHelpFormatter,
    epilog="""
Examples:
    % dt
    Monday, 2026-06-08 00:12:18
    % dt tomorrow
    Tuesday, 2026-06-09 09:00:00
    % dt 2 weeks from now
    Monday, 2026-06-22 00:12:38
    % dt --base "July 5" 2 weeks from now
    Sunday, 2026-07-19 00:13:27
""")
ap.add_argument('--debug',action='store_true',help="Turn on debugging output.")
ap.add_argument('--doc',metavar='MODULE',action='store',help="Get help with the given Python module.")
ap.add_argument('--base',metavar='T',action='store',help="Set the base date and time used to interpret the date and time on the command line.")
ap.add_argument('t',action='store',nargs='*',help="Some English expression of date and/or time.")
opt=ap.parse_args()
opt.t=' '.join(opt.t)

dc=DebugChannel(opt.debug)
if dc:
    dc(f"{opt.doc=}")
    dc(f"{opt.base=}")
    dc(f"{opt.t=}")

def main():
    if opt.doc:
        m=sys.modules.get(opt.doc)
        if not m:
            die(f"No module named {opt.doc!r}")
        help(m)
        sys.exit(0)
    # Parse any --base value.
    if opt.base:
        opt.base=Calendar().parse(datetimeString=opt.base)[0]
    else:
        opt.base=Calendar().parse(datetimeString="now")[0]
    dc(f"{opt.base=}")
    # Parse our command line arguments.
    opt.t=Calendar().parse(datetimeString=opt.t,sourceTime=opt.base)[0]
    print(datetime(*opt.t[:6]).strftime("%A, %Y-%m-%d %H:%M:%S"))

if __name__=="__main__":
    main()

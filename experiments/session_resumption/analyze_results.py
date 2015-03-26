#! /usr/bin/env python

import os
import sys
import logging
import argparse
import pickle

sys.path.append(os.path.join(os.path.dirname(__file__), '../web-profiler'))
from webloader.tls_loader import TLSLoader
from webloader.loader import LoadResult, PageResult


def print_session_resumption_stats(loader):
    '''Print session resumption stats for manual inspection'''
    print 'TLS Session Resumption Statuses:'
    for url, page_result in loader.page_results.iteritems():
        if page_result.status == PageResult.SUCCESS:
            print '{:<30}{:<}'.format(url, page_result.tls_session_resumption_support_statuses)

def print_errors(loader):
    '''Print success/error statuses for manual inspection'''
    print 'Errors:'
    for url, page_result in loader.page_results.iteritems():
        if page_result.status != PageResult.SUCCESS:
            print '{:<30}{:<25}{:<}'.format(url, page_result.status,\
                [result.status for result in loader.load_results[url]])

def print_summary_stats(loader):
    success_count = 0  # number of pages successfully loaded
    success_with_session_resumption_count = 0  # page successfully loaded AND supported TFO
    urls_with_session_resumption = []

    for url, page_result in loader.page_results.iteritems():
        if page_result.status == PageResult.SUCCESS:
            success_count += 1
            if True in page_result.tls_session_resumption_support_statuses:
                success_with_session_resumption_count += 1
                urls_with_session_resumption.append(url)

    print 'TLS session resumption support (out of sites that support HTTPS):\t%d/%d  (%.02f %%)\n' % \
        (success_with_session_resumption_count, success_count,\
         float(success_with_session_resumption_count)/success_count*100.0)

    print 'URLs with TLS session resumption support:'
    for url in urls_with_session_resumption:
        print url


def main():
    logging.info('Loading pickled loader: %s' % args.loader)

    with open(args.loader, 'r') as f:
        loader = pickle.load(f)

    print_summary_stats(loader)

    if args.verbose:
        print '\n\n'
        print_errors(loader)
        print '\n\n'
        print_session_resumption_stats(loader)



if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Web page profiler.')
    parser.add_argument('loader', help='Pickled loader file generated by crawler')
    parser.add_argument('-o', '--outdir', default='.', help='Destination directory for pickled results.')
    parser.add_argument('-q', '--quiet', action='store_true', default=False, help='only print errors')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='print debug info. --quiet wins if both are present')
    args = parser.parse_args()

    if not os.path.isdir(args.outdir):
        try:
            os.makedirs(args.outdir)
        except Exception as e:
            logging.getLogger(__name__).error('Error making output directory: %s' % args.outdir)
            sys.exit(-1)
    
    # set up logging
    if args.quiet:
        level = logging.WARNING
    elif args.verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logfmt = "%(levelname) -10s %(asctime)s %(module)s:%(lineno) -7s %(message)s"
    config = {
        'format' : logfmt,
        'level' : level
    }
    logging.basicConfig(**config)

    main()
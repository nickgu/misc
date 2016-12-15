#! /bin/env python
# encoding=utf-8
# author: nickgu 
#   
#   split_file.py <probability> <input_file> <output_A> <output_B>
#   
#   split the input file into output_A and output_B line-wise.
#   each line will dispatched to output_A by prob
#

import random
import sys

if __name__=='__main__':
    if len(sys.argv) != 5:
        print >> sys.stderr, 'Usage'
        print >> sys.stderr, '  split_file.py <probability> <input> <output_A> <output_B>'
        sys.exit(-1)

    prob = float(sys.argv[1])
    in_file = file(sys.argv[2])
    out_file_a = file(sys.argv[3], 'w')
    out_file_b = file(sys.argv[4], 'w')

    count_a = 0
    count_b = 0
    print >> sys.stderr, 'Try to split file <%s> as %.2f%% to <%s>, and %.2f%% to <%s>' % (
                    sys.argv[2], prob * 100., sys.argv[3], (1-prob)*100., sys.argv[4]
            )
    while 1:
        l = in_file.readline()
        if not l:
            break

        if random.random() < prob:
            count_a += 1
            out_file_a.write(l)
        else:
            count_b += 1
            out_file_b.write(l)

    print >> sys.stderr, 'Split over.'
    print >> sys.stderr, '%d line(s) write to [%s]' % (count_a, sys.argv[3])
    print >> sys.stderr, '%d line(s) write to [%s]' % (count_b, sys.argv[4])


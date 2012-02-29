#!/usr/bin/env python

import numpy as np
import op4

for in_file in [ '../test/mat_b_dn.op4' ,
                 '../test/mat_b_s2.op4' ,
                 '../test/mat_t_s1.op4' ,
                 '../test/mat_b_s1.op4' ,
                 '../test/mat_t_dn.op4' ,
                 '../test/mat_t_s2.op4' , ]:
    try:
        fh = op4.File(in_file, 'r')
    except:
        print('Failed to get header of %s' % (in_file))
        raise SystemExit

    print('%s' % ('=' * 60))
    print('%s' % (in_file))
    print('%-8s %5s %5s %8s %8s %1s %2s %2s %9s' % (
          'Name', 'nRow', 'nCol', 'nStr', 'nNnz', 'T', 'Fr', 'Dg', 'Offset'))
    for i in range(fh['nMat']):
        print('%-8s %5d %5d %8d %8d %1d %2d %2d %9d' % (
               fh['name'][i],
               fh['nRow'][i],
               fh['nCol'][i],
               fh['nStr'][i],
               fh['nNnz'][i],
               fh['type'][i],
               fh['form'][i],
               fh['digits'][i],
               fh['offset'][i],))

a = op4.load(10)

print 'The array created is %s' % a
print 'It carries a reference to our deallocator: %s ' % a.base
# np.testing.assert_allclose(a, np.arange(10))

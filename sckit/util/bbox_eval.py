import numpy as np

def IoU( bbox_a, bbox_b ):
    """ Intersection over Union
        
        Inputs:
            bbox_a/b: int tuple (x, y, w, h)
        Outputs:
            floating value with formula = Intersect( bbox_a, bbox_b ) / Union ( bbox_a, bbox_b )
    """

    tl_x = max( bbox_a[0], bbox_b[0] )
    tl_y = max( bbox_a[1], bbox_b[1] )
    br_x = min( bbox_a[0]+bbox_a[2], bbox_b[0]+bbox_b[2] )
    br_y = min( bbox_a[1]+bbox_a[3], bbox_b[1]+bbox_b[3] )

    if (tl_x <= br_x) and (tl_y <= br_y):
        intersect_sz = (br_x-tl_x) * (br_y-tl_y) * 1.0
    else:
        intersect_sz = 0.0

    return intersect_sz / (bbox_a[2]*bbox_a[3]+bbox_b[2]*bbox_b[3]-intersect_sz)


def CumSum( pairs ):
    """ cumulative sum

        Input:
            pairs: list of vector [ confidence_value, number_to_cumulate ] in the format of [ float, int ]
        Output:
            cumsum: list of the cumlative sum 
        Ref:
            https://github.com/weiliu89/caffe/blob/b4bacbbdc40945c6c91d29c10003b0057a54e70c/src/caffe/util/bbox_util.cpp#L1980
    """
    # Sort the pairs based on first item of the pair.
    pairs = np.array( pairs )
    sort_pairs = pairs[ pairs[:,0].argsort()[::-1] ]

    cumsum = []
    for i in xrange( len(sort_pairs) ):
        if (i == 0):
            cumsum.append( sort_pairs[i][1] )
        else:
            cumsum.append( cumsum[-1] + sort_pairs[i][1] )

    return cumsum


def ComputeAP( tp, num_pos, fp, ap_version='11point' ):
    """ compute average precision (AP) 

        Inputs:
            tp: true positive; list of vectors  [ confidence_value, 0/1 ] in the format of [ float, int ]
            fp: false positive; list of vectors [ confidence_value, 1/0 ] in the format of [ float, int ]
            num_pos: number of ground truth positives; integer
            ap_version: string
        Outputs
            prec: list of precision
            rec: list of recall
            ap: average precision; single float
        Ref:
            https://github.com/weiliu89/caffe/blob/b4bacbbdc40945c6c91d29c10003b0057a54e70c/src/caffe/util/bbox_util.cpp#L1996
    """
    assert len(tp)==len(fp), 'tp must have same size as fp.'
    
    eps = 1e-6;
    num = len(tp)

    # Make sure that tp and fp have complement value.
    for i in xrange(num):
        assert tp[i][0]-fp[i][0] < eps
        assert tp[i][1] == 1 - fp[i][1]

    # init
    prec = []
    rec = []
    ap = 0
    if len(tp)==0 or num_pos==0:
        return prec, rec, ap

    # Compute cumsum of tp.
    tp_cumsum = CumSum( tp )
    assert len(tp_cumsum)==num

    # Compute cumsum of fp.
    fp_cumsum = CumSum( fp )
    assert len(fp_cumsum)==num

    # Compute precision.
    for i in xrange(num):
        prec.append( float(tp_cumsum[i]) / ( tp_cumsum[i] + fp_cumsum[i] ) )

    # Compute recall.
    for i in xrange(num):
        rec.append( float(tp_cumsum[i]) / num_pos )


    if ap_version == '11point':
        # VOC2007 style for computing AP.
        max_precs = np.zeros( 11 )
        start_idx = num - 1
        for j in range(10, -1, -1):
            for i in range(start_idx, -1, -1):
                if (rec[i] < j / 10.):
                    start_idx = i
                    if (j > 0):
                        max_precs[j-1] = max_precs[j]
                    break
                else:
                    if (max_precs[j] < prec[i]):
                        max_precs[j] = prec[i]
        for j in range(10, -1, -1):
            ap = ap + max_precs[j] / 11

    elif ap_version == 'MaxIntegral':
        # VOC2012 or ILSVRC style for computing AP.
        cur_rec = rec[-1]
        cur_prec = prec[-1]
        for i in range( num-2, -1, -1 ):
            cur_prec = np.max( prec[i], cur_prec )
            if( np.fabs(cur_rec - rec[i]) > eps ):
                ap = ap + cur_prec * np.fabs(cur_rec - rec[i])
            cur_rec = rec[i]
        ap = ap + cur_rec * cur_prec

    elif ap_version == 'Integral':
        # Natural Integral.
        prev_rec = 0.
        for i in xrange(num):
            if( np.fabs(rec[i] - prev_rec) > eps ):
                ap = ap + prec[i] * np.fabs(rec[i] - prev_rec)
            prev_rec = rec[i]
    else:
        assert 'Unknown ap_version'

    return prec, rec, ap
    

if __name__ == '__main__':

    bbox_a = ( 8, 10, 5, 5 )
    bbox_b = ( 1, 1, 5, 5 )
            
    print IoU(bbox_a, bbox_b)


    tp = [ [0.1, 0], [0.8, 1], [0.6, 1], [0.5, 0], [0.2, 1] ]
    fp = [ [0.1, 1], [0.8, 0], [0.6, 0], [0.5, 1], [0.2, 0] ]
    print ComputeAP( tp, 4, fp )

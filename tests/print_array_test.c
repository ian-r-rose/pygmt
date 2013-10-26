#include <stdio.h>

void multiplyarray(const void * indatav, int nrows, int ncols, void * outdatav,) {
    const double * indata = (double *) indatav;
    double * outdata = (double *) outdatav;
    int i;
    puts("Currently Doing stuff lots of important stuff to our array");
    for (i = 0; i < nrows*ncols; ++i) {
	outdata[i] = indata[i] * 5;
    }
    puts("Like Multiplying by 5");
}

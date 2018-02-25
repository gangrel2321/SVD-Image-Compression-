This code works by computing the Singular Value Decomposition of the Pixel Matrix for a 
grayscale image then removing the lowest singular values which can reduce noise in the image 
for small reductions in the matrix rank. This method results in a lossy compression of the 
original image via an n-rank matrix approximation of the pixel matrix. While running the 
program, the user is allowed to specific which n-value he/she would like to use to approximate 
the pixel matrix to. 

Note: Currently I have implemented several functions for either compressing the entire image at 
once, in wedges, or in blocks of the image to allow for better visual fidelity across 
compression; however, this is not yet currently supported in the gui. Expect future releases to 
implement these features fully. 

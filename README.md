# Bachelor Thesis: stochastic computing

To model probabilities on circuits (0,1)-bitstreams are used. 
The probability displayed by a bitstream is determined by the number on 1s in the stream divided by the length of it.

For example:
[0101, 00110110, 10] all have the probability 1/2,

[100010, 0100, 000100010001] have the probability 1/4.


__To investigate the properties of these stochastic bitstreams I implemented a simulator in Python.__

### Low Density Parity Check
The first proof of concept implementation is a Low Denstiy Parity Check decoder (short LDPC). "The LDPC code is a linear error correcting code, a method of transmitting a message over a noisy transmission channel" <https://en.wikipedia.org/wiki/Low-density_parity-check_code>.


## Edge Detection on stochastic circuits
The main part of this bachelor thesis is edge detection of images using stochastic circuits.
Approach: 
* Grayscale image (value between 0 and 255)
* for every pixel: stochastic bitstream which describes the intensity of the pixel, bitstream adapts over time/number of iterations
* for every iteration
  * generate a random threshold between 0 and 255 and generate a binary mask 
  * every value below the threshold is 0, every value above is a 1
  
Example for Binary Image:

[binary image](https://user-images.githubusercontent.com/33347624/121353841-97f49800-c92e-11eb-9902-f6f9e369fbe4.png)

  * apply the stochastic version of the roberts cross operator to detect the edges
  * add the edge detected pixel value to the stochastic bitstream for every pixel 

Over Time this image gets more and more precise:

![First Iteration](https://user-images.githubusercontent.com/33347624/121482454-772f4f80-c9cd-11eb-9a73-23952f8fe55d.png)


![100th Iteration](https://user-images.githubusercontent.com/33347624/121482520-86ae9880-c9cd-11eb-9432-bce3c3ba1e2e.png)








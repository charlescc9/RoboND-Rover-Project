## Project: Search and Sample Return
### Writeup Template: You can use this file as a template for your writeup if you want to submit it as a markdown file, but feel free to use some other method and submit a pdf if you prefer.

---


**The goals / steps of this project are the following:**  

**Training / Calibration**  

* Download the simulator and take data in "Training Mode"
* Test out the functions in the Jupyter Notebook provided
* Add functions to detect obstacles and samples of interest (golden rocks)
* Fill in the `process_image()` function with the appropriate image processing steps (perspective transform, color threshold etc.) to get from raw images to a map.  The `output_image` you create in this step should demonstrate that your mapping pipeline works.
* Use `moviepy` to process the images in your saved dataset with the `process_image()` function.  Include the video you produce as part of your submission.

**Autonomous Navigation / Mapping**

* Fill in the `perception_step()` function within the `perception.py` script with the appropriate image processing functions to create a map and update `Rover()` data (similar to what you did with `process_image()` in the notebook). 
* Fill in the `decision_step()` function within the `decision.py` script with conditional statements that take into consideration the outputs of the `perception_step()` in deciding how to issue throttle, brake and steering commands. 
* Iterate on your perception and decision function until your rover does a reasonable (need to define metric) job of navigating and mapping.  

[//]: # (Image References)

[image1]: ./dataset/IMG/robocam_2018_09_22_13_41_11_970.jpg

## [Rubric](https://review.udacity.com/#!/rubrics/916/view) Points
### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---
### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf.  

You're reading it!

### Notebook Analysis
#### 1. Run the functions provided in the notebook on test images (first with the test data provided, next on data you have recorded). Add/modify functions to allow for color selection of obstacles and rock samples.
After experimenting on the test dataset given, I recorded a new dataset of 404 images, including:

![alt text][image1]

In order to obtain pixel values for obstacles and rocks, I modified the `color_thresh()` function.
I first calculated the binary image of the terrain by extracting pixels from the image that were above the given (160, 160, 160) threshold.
I then calculated the binary image of the obstacles by extracting the inverse pixels as when calculating the terrain, those below (160, 160, 160).
Finally, I calculated the binary image of the rocks by first converting the images to HSV via `cv2.cvtColor(img, cv2.COLOR_RGB2HSV)` (making sure to use RGB, not BGR), 
then used the lower and upper bounds of (20, 100, 100) and (30, 255, 255) respectively to extract yellow pixels. 
I returned all three binary images for use in later functions. 

#### 2. Populate the `process_image()` function with the appropriate analysis steps to map pixels identifying navigable terrain, obstacles and rock samples into a worldmap.  Run `process_image()` on your test data using the `moviepy` functions provided to create video output of your result.

I made a series of modifications to the `process_image()` function in order to map the terrain, obstacle, and rock pixels extracted
in the `color_thresh()` function to the Rover's worldmap. I first transformed the images from the Rover camera's view to a top-down view
via the `perspect_transform()` function, using the given source and destination coordinates. Then I obtained the terrain, obstacle,
and rock pixels from the `color_thresh()` function. I then converted these pixels from the 160 by 320 image space to the 200 by 200
space by changing the x-axis and y-axis to the Rover's and the performing the appropriate rotation and translation. I completed this
section by overplotting the pixels directly onto the worldmap. This world map, along with the original image and transformed image, were
combined into a mosaic images. I also added the terrain, obstacle, and rock pixels without the worldmap, to directly display them.

### Autonomous Navigation and Mapping

#### 1. Fill in the `perception_step()` (at the bottom of the `perception.py` script) and `decision_step()` (in `decision.py`) functions in the autonomous mapping scripts and an explanation is provided in the writeup of how and why these functions were modified as they were.

My modification of the `perception_step()` function closely mirrored my modification of the 'process_image()` function. I performed the
same extraction of the terrain, obstacle, and rock pixels and mapping onto the Rover's worldmap. The only addition step was to generate
the Rover's vision_image by displaying the terrain, obstacle, and rock binary images in the B, R, and G channels respectively.

I also modified the `decision_step()` function to allow the Rover to decide which actions to take based on the information gathered
from the `perception_step()` function. I largely adopted the given functionality, but made some adjustments. The logic first checks
whether the Rover sees navigable terrain pixels (extracted in the `perception_step()` function). If not, it either stops if in forward mode,
or performs a 4-point turn if in stop mode. In the much more common case where the Rover sees navigable terrain, the next Rover variable
I consider is mode, either forward or stop. If the Rover is in forward mode, we finally check if there are enough navigable terrain
pixels via the stop_forward property, and if so continue forward, and if not stop the Rover. If the Rover is in stop mode, we first check
to see if it is actually stopped (velocity <= 0.2), and if not continue to break. If so, however, we then check if there are enough
navigable terrain pixels to start forward. If so, we do so, and is not we turn at a constant steering angle of -15 (experimenting with
changing this angle based on the nav_angels lead to a back-and-forth motion sometimes that essentially broke the navigation).
The critical step that I changed from the given code was also checking the mean nav_angle when deciding to start forward when in stop mode.
I found that the Rover often began moving too quickly after coming to a stop and ran into obstacles. To fix this, I made sure that the
mean nav_angle direction was within the Rover's possible steering range (-15 to 15) before switching to forward mode.


#### 2. Launching in autonomous mode your rover can navigate and map autonomously.  Explain your results and how you might improve them in your writeup.  

**Note: running the simulator with different choices of resolution and graphics quality may produce different results, particularly on different machines!  Make a note of your simulator settings (resolution and graphics quality set on launch) and frames per second (FPS output to terminal by `drive_rover.py`) in your writeup when you submit the project so your reviewer can reproduce your results.**

Here I'll talk about the approach I took, what techniques I used, what worked and why, where the pipeline might fail and how I might improve it if I were going to pursue this project further.  

The general approach I used was to flush out the project skeleton that consisted of a Rover which had perception, decision making, and
action functionality. Designing the solution this way allowed for a very clear delineation and generalization of the Rover's core
functionality and made it easy to understand and implement all necessary functions. This general approach/pipeline worked very well,
though each specific aspect may have been improved upon. The action step (giving the Rover throttle, break, and steering angle input)
was fully constrained by the (simulated) hardware of our Rover, and consequently couldn't really be improved upon in this project.
However, both the perception and decision making steps could be improved upon in a number of ways, making the final solution much more
robust. For perception, finding navigable terrain, obstacles, and rocks via color thresholding worked fairly well, but it didn't take
into account distinctions such as obstacles being both the ridge on the side of the path and big rocks in the path itself, and it
wouldn't generalize well to other environments that don't have a similar color profile. Utilizing different visual properties in the
images beyond color, such as object detection, depth, etc., would have almost certainly improved performance. A more modern deep
learning CNN implementation would be very interesting here. Similarly, implementing the decision making step as a decision tree
worked fairly well, but was obviously fundamentally limited in the number of potential states it could handle uniquely. Representing
and traversing the state space in a more sophisticated way would have improved performance greatly. Again, more modern AI techniques,
including deep reinforcement learning, would be interesting to experiment with.

However, since the problem was very well defined and tightly constrained, these relatively naive approached worked quite well. With a
resolution of TODO and an average FPS around 35, I was able to map the environment fairly well, obtained around 75% TODO when mapping
more than half of the terrain.

FPS and result
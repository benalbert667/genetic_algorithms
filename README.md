# genetic_algorithms

As a small self-intorudction to genetic algorithms, I created a general genetic algorithm that can model any object of a given size based on some given success function.  The algorithm (general_genetic_alg.py) is simply a Python object whose constructor takes these as parameters (along with some hyperparameters for the algorithm).

I tested the object for a simple case of modeling a specific string (generate_string.py), where the success function is simply how many characters of an invididual are shared with the target string.  Because of the simplicity of the task the results are pretty good (with the hyperparameters defined in the file strings under 50 characters usually take around 20 generations to be exactly matched).

I tested it again on images, originally with a similar success function (score = number of matching pixels), but found that since pixel space is much larger than character space idividuals were receiving constant 0 scores.  I changed the success function to what it is currently in generate_image.py, which is a difference between the current value of each pixel and it's target.  Still, the size of each individual (image) was a bit too large for my computer to handle (I was hoping for a neat visual of a randomized image slowly morphing into a specific one).  Nonetheless I included it here.

The algorithim is based on this implementation: https://github.com/frogamic/GeneticHelloWorldJs

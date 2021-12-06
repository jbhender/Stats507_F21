---
jupyter:
  jupytext:
    cell_metadata_json: true
    notebook_metadata_filter: rise
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.13.0
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
  rise:
    autolaunch: true
    enable_chalkboard: true
    header: <a href="#/slide-0-0"> <h3> Stats 507 - Deep Learning </a>
    progress: true
    scroll: true
    theme: solarized
    transition: convex
---

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Deep Learning with Keras and Tensorflow
*Stats 507, Fall 2021*

James Henderson, PhD  
December 2, 2021
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Overview
 - [Neural Networks](#/slide-2-0)
 - [Tensorflow](#/slide-3-0)
 - [Keras](#/slide-4-0)
 - [Keras Pipeline](#/slide-5-0)
 - [Regularization](#/slide-6-0)
 - [Takeaways](#/slide-7-0)
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Demo
 - Read these slides alongside the demo `keras_demo.py` from the course repo.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Neural Networks
 - Neural networks models related features (inputs) to targets (outputs) using
   layers of activation units ("neurons").
 - The dimensions of the target(s) and features determine the size of the input
   and output layers.
 - The "hidden" layers in between are determined by the modeler.  
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Deep Learning
 - *Deep Learning* refers to learning with neural network models containing 
   multiple hidden layers. 
 - Works well for *representational* data (e.g. images) as layers allow for
   "learning" abstractions that can lead to good regression and classification
   performance. 
 - *Deep neural networks* are universal function approximators. 
<!-- #endregion -->


<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Activation Units  
 - Activation units in one layer are functions of the units in a previous layer
   (or layers). 
 - Each activation unit represents a nonlinear transform ("activation function")
   of a linear function of other units.
 - This linear function is determined by a vector of *weights* and a *bias* 
   (intercept) term.
 - Here is a model $f$ with two hidden layers relating $x \mapsto y$:

   $$
   f(x) = g_2(W_2g_1(W_1x + b_1) + b_2). 
   $$
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Training 
- The *weights* and *biases* represent the parameters to be trained using 
  the training data. 
- Training is done to minimize the training loss, based on a loss function
  measuring how well/poorly the models outputs (predictions) match the training
  labels. 
- This is done by using the gradient of the loss function with respect to these
  parameters. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Training 
- Parameters (weights and biases) are optimized using the gradient and some
  variation of *stochastic gradient descent*.
- *Stochastic* optimization helps to avoid local minima. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Optimizers 
- Because neural networks can be complicated, the gradient - computed through
  back-propagation (chain rule) - often *vanishes* or *explodes*. 
- This is generally solved by adapting the learning rate or using *momentum* -
  smoothing the gradient at each step using a local/running average.
- The "RMSprop" and "ADAM" optimizers automatically adapt the learning rate and 
  tend to be the best default options.  
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Batch size
- A *batch* is a subset of the data used for computing a gradient update. 
- An *epoch* is how many training steps are needed to use each sample once,
  based on the batch size.
- Smaller batch size leads to slower learning rate and longer computation time.
- Larger batch size leads to larger learning rate and shorter computation time.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## TensorFlow
 - TensorFlow is an "end-to-end ML platform" developed at Google.  
 - It helps to think of TensorFlow as the "backend" engine for deep learning
   with Keras. 
 - Efficient and highly scalable tensor (array) operations on CPU, GPU, and TPU. 
 - Automatically computes gradients - enabling quick training of arbitrary
   differentiable models. 
 - (You should be using TensorFlow 2.)
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Keras
 - Keras is the (official) high-level interface (API) for TensorFlow. 
 - Keras [aims][ka] to be: *simple*, *flexible*, and *powerful*. 
 - Using Keras allows you to quickly specify, train, and evaluate deep learning
   models.  
 [ka]: keras.io/about/
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Keras APIs
 - There are three ways to build DNN models with Keras:
   - Using the `Sequential` model class, 
   - Using the functional API,
   - Defining a sub-class inheriting from the model class.
 - The `Sequential` model class is simplest, but limited to a linear
   topology for layers. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Keras in 5 steps: 0
- Prepare the data in the TensorFlow format, shuffle, and batch after
  range normalizing. 
- To read from a pandas DataFrame use `tf.data.Dataset.from_tensor_slices()`.
- Use the dataset's `.shuffle()` and `.batch()` methods.  
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Keras in 5 steps: 1
- Define your model topology. 
- Use `Sequential()` and the resulting model's `.add()` method to add layers.
- Or pass a list of layers to `Sequential()`. 
- `Sequential()` is in `tf.keras.models`.
- Layers are defined in `tf.keras.layers`.
- Input layer can be inferred, output layer and activation should match target 
  and loss. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Keras in 5 steps: 2
- Compile the model using its `.compile()` method. 
- Choose an optimizer and loss function.
- Can add *metrics* for evaluation in addition to the loss. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Keras in 5 steps: 3
- Call the compiled model's `.fit()` method with the training and fit methods.
- Choose a number of *epochs* -- passes over the entire dataset for gradient
  updates. 
- Can define a batch-size here as well.
- Can pass validation data for epoch-by-epoch hold out evaluation. 
- Can also define *callbacks* here, e.g. for early stopping. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Keras in 5 steps: 4
- Evaluate using training history or use the `.evaluate()` and/or `.predict()`
  methods. 
- Modify model and repeat steps 1-4 as needed. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Regularization
 - There are several ways to regularize a neural network model:
   + Reduce the number of parameters by using smaller or fewer layers,
   + Impose $L1$ or $L2$ penalties on weights from one or more layers,
   + Using "dropout" to encourage redundancy of key abstractions.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Regularizing weights  
 - Implement $L1$ or $L2$ regularization for a layer using the
   `kernel_regularizer` argument and an `l1()` or `l2()` instance from
   `tf.keras.regularizers`.  
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Dropout
  - Dropout is a regularization technique in which a fraction of weights
    are randomly selected to be fixed at 0 ("dropped out") for each training
    iteration.
  - This causes other weights to "compensate" and can reduce over-fitting. 
  - `Dropout()` can be added as a layer affecting the previous `Dense()` layer. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Takeaways
 - The Keras API is a powerful high-level interface to the TensorFlow library
   for specifying, training, and evaluating neural network models.
 - Use the `Sequential()` model class for models with a linear topology of 
   layers, the functional API for more complex topologies.
 - Build model, compile, train, evaluate, adjust and repeat. 
 - Increase the number or sizes of layers or train longer to reduce under
   fitting.
 - Use regularization in the form of penalized weights, dropout layers, or
   early stopping to reduce over fitting.
<!-- #endregion -->

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
    header: <a href="#/slide-0-0"> <h3> Stats 507 - ML & sci-kit learn </a>
    progress: true
    scroll: true
    theme: solarized
    transition: convex
---

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Machine Learning and Sci-Kit Learn
*Stats 507, Fall 2021*

James Henderson, PhD  
November 4 & 9, 2021
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Overview
 - [Machine Learning](#/slide-2-0)
 - [Scikit-learn](#/slide-3-0)
 - [Isolet Demo](#/slide-4-0)
 - [Training, Validation, and Testing](#/slide-5-0)
 - [Cross-Validation](#/slide-6-0)
 - [SVD](#/slide-7-0)
 - [Regularization](#/slide-8-0)
 - [Takeaways](#/slide-9-0)
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Machine Learning
 + The Wikipedia entry on [Machine Learning][ml] begins ...

> Machine learning (ML) is the study of computer algorithms that can improve
> automatically through experience and by the use of data ...
> Machine learning algorithms build a model based on sample data, 
> known as "training data", in order to make predictions or decisions without 
> being explicitly programmed to do so.

[ml]: https://en.wikipedia.org/wiki/Machine_learning
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## ML Domains

+ *Supervised learning* uses labeled data and is akin to regression methods
    in statistics in that one (or more) variables are treated as dependent.

    - Regression - continuous (or at least *interval-valued*) labels,
    - Classification - discrete/categorical (often binary) labels.

+ *Unsupervised learning* includes clustering, visualization, and
   distance-based methods. Seeks to understand structure rather than use
   some variables to predict others.  

<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Machine Learning
> A subset of machine learning is closely related to computational statistics,
> which focuses on making predictions using computers; 
> but not all machine learning is statistical learning. 

+ All or most of what we cover in this class can be thought of as 
  *statistical learning*. 

+ If you want to know more, I highly recommend reading and referring to 
  *The Elements of Statistical Learning*. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## ML vs Statistics
  - There is no clear boundary between ML and statistics.
  - ML tends to focus more on prediction and less on inference.
  - ML uses hold-out data rather than sampling-theory for evaluation. 
  - As a practical matter, I like to make the following distinction:
  
  > If you evaluate your model using hold out data you're doing ML. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Scikit-learn
  - Many ML algorithms and models are available in [scikit-learn][skl] (SKL).
  - We'll cover a very small fraction of what's available:
     + regularized regression: ridge, lasso, and elastic-net,
     + random forests,
     + gradient-boosted trees. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Scikit-learn
  - I'll be using `sklearn` version 1.0.1.
  - I'll typically import individual estimators and functions from `sklearn`.
  - Most of what I'll use comes from the `linear_model` and `ensemble` APIs.

```python
from sklearn.linear_model import LogisticRegression
```
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Isolet Demo
- These slides are without examples and are intended to be used
  alongside the Isolet demo from the course repo. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Training, Validation, and Testing
  - In supervised ML, we evaluate our models based on their ability to 
    make predictions on new cases. 
  - *Test data* is data set aside to evaluate our (final) model(s). 
  - *Training* data is used to learn model parameters (to *train* our model).
  - A *validation* dataset is data set aside to compare different models fit
    to the training data and for tuning *hyper-parameters*. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Over-fitting
- We use*out-of-sample data* for validation and testing to get unbiased
  estimates of the out of sample error.
- This helps us avoid *over-fitting*, which occurs when our model fits the
  training data well but does so in a way that doesn't *generalize* to new
  data.
- Over-fitting is an instance of a *bias-variance* tradeoff. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Cross-Validation 
 - *Cross validation* is often used in place of a designated validation dataset.
 - *Cross-validation* makes efficient use of available non-test data by
    repeatedly interchanging which observations are considered training and
    which validation.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Cross-Validation 
 - *Cross-validation* is (typically) done by dividing the data into sub-groups 
   called *folds*.
 - If we have *k* of these groups we refer to it as *k-fold* cross-validation.
 - The special case when *k* equals the total number of not-test samples is 
    known as _leave-one-out cross-validation_. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Cross-Validation 
 - When dividing data into folds it is important that observations be 
   randomly distributed among the groups. 
 - For example, if you had previously sorted your data set you would not want 
   to assign folds using adjacent rows. 
 - You can avoid this by randomly shuffling the rows (cases). 
 - This is also true when generating the test-train split. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Cross-Validation 
 - If you're data are not *iid* additional care is needed for data splitting.
 - If you have *block* structured data, with dependence isolated within blocks,
   and distinct blocks independent, you generally want keep block together
   across folds. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Singular Value Decomposition
 - The [singular value decomposition][svd] or SVD is a generalized version
   of the Eigen decomposition.  
 - The SVD breaks a matrix $X$ into three parts - two orthonormal matrices 
   $U$ and $V$ and a diagonal matrix $D$: $X = UDV'$. 
 - By convention $U$, $D$, and $V$ are ordered so that the diagonal of $D$
   is largest in the upper left and smallest in the lower right.  
 - The values of$D$ are called _singular values_, the columns of $U$ are called 
   _left singular vectors_ and the columns of $V$ _right singular vectors_. 

[svd]: https://en.wikipedia.org/wiki/Singular-value_decomposition
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Principle Components Analysis (PCA)
 - The *Eigen* decomposition of $X'X$ is, $X'X = \Gamma \Lambda \Gamma'$ 
   where $\Gamma'\Gamma = I$ and $\Lambda$ is diagonal.
 - If the columns of $X$ have mean zero, then $X'X$ is proportional to the
   sample covariance of $X$.   
 - The columns of $\Gamma$ are called *eigenvectors* and the entries along the
   diagonal of $\Lambda$ are the corresponding *eigenvalues*. 
 - The columns of $X\Gamma$ are the *principle components* of $X$. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## SVD & PCA
 - PCA: $X'X = \Gamma \Lambda \Gamma'$ 
 - SVD: $X = UDV'$
 - $X'X = (VD'U')(UDV') = VD^2V$ 
 - Therefore $V = \Gamma$ and $D^2 = \Lambda$. 
 - $XV = UD$ are the principle components of $X$. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## SVD in NumPy
  - `np.linalg.svd()`
  - Returns a tuple `(u, d, vh)` - the `h` is for Hermitian 
  - The Hermitian is just the transpose for a real matrix.   
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Regularization
 - Regularization is used to limit over-fitting and to make models 
   identifiable. 
 - One way to regularize, is to limit the number of singular-vectors 
   (or other features) used in your model.
 - Another common way to achieve regularization is to penalize the loss
   function used to measure fit. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Ridge Regression 
- In ridge regression - or $L_2$ regularization - we penalize the loss using
  the sum of the squared coefficients (the squared $L_2$ norm). 
- Logistic regression with a ridge penalty has the following *objective* 
  function (with $g$ the logistic function):

  $$
  \mathscr{L}(b) = \sum_{i=1^n} -y_i \log g(x_ib) - (1 - y_i)\log(1 - g(x_ib)) + 
    \lambda \sum_{k=1}^p b_k^2.
  $$ 

- $\lambda$ is a *hyper-parameter* that controls the amount of regularization. 

<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Ridge Regression - Tuning  
- For logistic regression, we can use the function `LogisticRegressionCV()`
  to select the penalty $\lambda$ for ridge regression.
- Use `penalty="l2"` and provide a sequence of regularization parameters `C`.
- `C` = $\frac{1}{\lambda}$
- Defaults to 5-fold CV, pass custom folds to `cv`. 
- Data are passed to the `.fit()` method. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Ridge Regression - Tuning  
- Key attributes of object returned by `LogisticRegressionCV()` after
  calling `.fit()`:
   - `.C_` - value of C where loss is minimized,
   - `Cs_` - sequence of C's used,
   - `.scores_` - *dictionary* of CV scores for each class,
   - `.coefs_`, `.intercept_` - model coefficients at best `.C_`.

<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Ridge Regression - Tuning  
- Key methods of object returned by `LogisticRegressionCV()`:
   - `.fit(X, y)` - fit the model using training data `X` and `y`, 
   - `.predict()` - predict class labels,
   - `.predict_proba()` - predict probabilities,
   - `.score()` - compute the score (loss) on a (new) dataset. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Lasso
- In the Lasso - or $L_1$ regularized regression - we penalize the loss using
  the sum of the absolute value of the coefficients (the $L_1$ norm). 
- Logistic regression with a Lasso penalty has the following *objective* 
  function:

  $$
  \mathscr{L}(b) = \sum_{i=1^n} -y_i \log g(x_ib) - (1 - y_i)\log(1 - g(x_ib)) + 
    \lambda \sum_{k=1}^p |b_k|. 
  $$ 
  
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Lasso - Tuning
- Use `LogisticRegressionCV()` and select penalty `l1`. 
- Also need a compatible solver (e.g. `solver="saga"`). 
- Otherwise the same as before.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Elastic-net
- The elastic-net interpolates between the $L_1$ and $L_2$ penalties.  

  $$
  \mathscr{L}(b) = \sum_{i=1^n} -y_i \log g(x_ib) - (1 - y_i)\log(1 - g(x_ib)) + 
    \alpha \lambda \sum_{k=1}^p |b_k| +
     (1 - \alpha)\frac{\lambda}{2}\sum_{k=1}^p b_k^2. 
  $$ 
  
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Elastic-net - Tuning
- Use `LogisticRegressionCV()` and select penalty `elasticnet` and a
  compatible solver.
- Control the mixing parameter ($\alpha$) using `l1_ratio`. 
- Consider using Ridge to find an appropriate range for `C` first. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Takeaways
- Set aside test data to evaluate your ML models.
- Use regularization to play the bias-variance tradeoff and avoid 
  over-fitting.
- Use cross validation (or a dedicated validation dataset) to tune 
  hyper parameters and make model-building decisions. 
<!-- #endregion -->

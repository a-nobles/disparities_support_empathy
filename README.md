# Examining Disparities in Social Support Across Demographics for Peer-to-Peer and Patient-Provider Interactions on Social Media

This project was [published](https://ojs.aaai.org//index.php/ICWSM/article/view/7315) in the 14th International AAAI Conference on Web and Social Media (ICWSM). A publicly available version of the paper can be found [here](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7386284/).  

#### -- Project Status: [Completed]

## Project Introduction and Research Questions
The purpose of this project is to examine if biases present in traditional brick-and-mortar healthcare settings transcend mediums into communications in digital settings. To do this, using the following four research questions, we examined peer-to-peer and layperson-to-physician interactions on the subreddit r/AskDocs, which facilitates Q&A between the public and healthcare professionals. 

* **RQ1:** What are the self-reported demographics (gender/sex and race/ethnicity) of posters on r/AskDocs? _We use a rule-based approach automatically extract self-reported gender/sex and race/ethnicity from posts._

* **RQ2:** What health topics do posters commonly ask about on r/AskDocs and how does this vary across demographics? _We conduct a topic model analysis and examine how topics vary across demographics using odds ratios._

* **RQ3:** Does receipt of a response in general or by a physician vary across demographics? _We examine the association between demographics and the probability of receiving at least one response (in general and by a physician) using logistic regression._

* **RQ4:** Does the empathy of response(s) by a peer or a physician vary across demographics or health topics? _We examine variation in empathetic responses among the posters’ demographics and health topics using language style matching._

## Overview of Methods
* Methods
	* Descriptive statistics
	* Rule-based methods (based on regular expressions) 
	* Topic modeling
	* Odds ratios 
	* Logistic regression
	* Language style matching
	* Qualitative analysis
	* Data visualization
* Languages (libraries/packages)
	* R (glm, zelig)
	* Python (gensim, pandas, numpy, json, urlextract)

## Steps for Analysis
Below is an overview of the steps of the analysis to support our [paper](https://ojs.aaai.org//index.php/ICWSM/article/view/7315) with additional details supplied wihtin the paper.

1. We collected all r/AskDocs posts, comments, and associated
2. Comments authored by a physician were identified using the flair in the comment metadata.
3. We developed a set of regular expressions to extract a self-reported demographics of a poster including binary sex, if the person identified as transgender, and race/ethnicity based on qualitative review of iterative samples of posts. We negated common
	1. [demo\_rules.py](insert link)
4. We applied topic modeling to discover the health topics that people were seeking information about using the Latent Dirichlet Allocation implemntation of MALLET provided via the wrapper in gensim.
	1. 	 [topic\_model.py](insert link)
5. We used multivariable logistic regression to assess the relationship
	1. [zelig\_modeling.R]()
4. We measured the langauge style matching (LSM) of each conversation (i.e., the post and associated response(s)) as a proxy for empathy. We included all posts with at least one response that was not the original poster (follow-up comments from original posters were excluded). To calculate the conversational LSM for peer-to-peer interactions,
	1. [empathy\_analysis\_non-physician.py]()
	2. [empathy\_analysis\_physician.py]()
3. Data visualization to support the paper
	1. [topic\_viz.R]()


## Results
Using self-reported demographics and discovered health

## Discussion
In our [paper]((https://ojs.aaai.org//index.php/ICWSM/article/view/7315)), we contextualize our findings using previous research on online patient-provider interactions, bias and barriers in traditional healthcare settings, and peer-to-peer and patient-provider interactions in the health information exchange. We discuss implications for human-computer interaction to facilitate these organic interactions on a publicly available social media setting.


## Authors

**Team Lead: [Alicia Nobles](https://github.com/[github handle])**

Other Members: [Eric Leas](https://profiles.ucsd.edu/eric.leas), [Mark Dredze](http://www.cs.jhu.edu/~mdredze/), [John Ayers](https://www.johnwayers.com/)

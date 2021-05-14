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

1. We collected all r/AskDocs posts, comments, and associatedmetadata (e.g., usernames, timestamps) from its inceptionin July 2013 through December 2018 from the [pushshift.io](https://ojs.aaai.org/index.php/ICWSM/article/view/7347)archives. 
2. Comments authored by a physician were identified using the flair in the comment metadata.
3. We developed a set of regular expressions to extract a self-reported demographics of a poster including binary sex, if the person identified as transgender, and race/ethnicity based on qualitative review of iterative samples of posts. We negated commonEnglish patterns that are not references to race (e.g.,Indian food). Performance of our rule-based approach was evaluated on a held out dataset. 
	1. [demo\_rules.py](https://github.com/a-nobles/disparities_support_empathy/blob/master/demo_rules.py)
4. We applied topic modeling to discover the health topics that people were seeking information about using the Latent Dirichlet Allocation implemntation of MALLET provided via the wrapper in gensim.
	1. 	 [topic\_model.py](https://github.com/a-nobles/disparities_support_empathy/blob/master/topic_model.py)
5. We used multivariable logistic regression to assess the relationshipbetween the explanatory variables of gender/sex andrace/ethnicity in the post and the probability of (1) receivingany response and (2) receiving a response from a physician.While holding the other explanatory variables at theirmeans, we estimated the probability of receiving a response(any response or a response from a physician) for each variableand corresponding 95% confidence intervals (CIs) byusing 1000 simulations.
	1. [zelig\_modeling.R](https://github.com/a-nobles/disparities_support_empathy/blob/master/zelig_modeling.R)
4. We measured the langauge style matching (LSM) of each conversation (i.e., the post and associated response(s)) as a proxy for empathy. We included all posts with at least one response that was not the original poster (follow-up comments from original posters were excluded). To calculate the conversational LSM for peer-to-peer interactions,we only included responses from non-physicians. To calculatethe conversational LSM for patient-provider interactions,we only included responses from physicians. Confidenceintervals were calculated from bootstrapped samples.
	1. [empathy\_analysis\_non-physician.py](https://github.com/a-nobles/disparities_support_empathy/blob/master/empathy_analysis_non-physician.py)
	2. [empathy\_analysis\_physician.py](https://github.com/a-nobles/disparities_support_empathy/blob/master/empathy_analysis_physician.py)
3. Data visualization to support the paper
	1. [topic\_viz.R](https://github.com/a-nobles/disparities_support_empathy/blob/master/topic_viz.R)


## Results
Using self-reported demographics and discovered healthtopics on a social media platform with AtD services, weidentified that this online community was primarily maleand white, users most commonly sought help for low acuityconditions like dermatology, and females and transgenderpeople sought help on sensitive topics at a higherrate than their male counterparts. There were also smalldifferences in how empathetic a response was across demographics,where females received more empathetic responsesthan males and racial/ethnic minorities received lessempathetic responses than their white counterparts. In general,physicians responses were also less empathetic thannon-physicians across demographics and topics.

## Discussion
In our [paper]((https://ojs.aaai.org//index.php/ICWSM/article/view/7315)), we contextualize our findings using previous research on online patient-provider interactions, bias and barriers in traditional healthcare settings, and peer-to-peer and patient-provider interactions in the health information exchange. We discuss implications for human-computer interaction to facilitate these organic interactions on a publicly available social media setting.


## Authors

**Team Lead: [Alicia Nobles](https://a-nobles.github.io/)**

Other Members: [Eric Leas](https://profiles.ucsd.edu/eric.leas), [Mark Dredze](http://www.cs.jhu.edu/~mdredze/), [John Ayers](https://www.johnwayers.com/)


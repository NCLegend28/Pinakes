---
title: "Large Language Models as Financial Data Annotators: A Study on Effectiveness and Efficiency"
source: "https://arxiv.org/html/2403.18152v1"
author:
published:
created: 2026-06-11
description:
tags:
  - "clippings"
---
Toyin Aguda, Suchetha Siddagangappa, Elena Kochkina, Simerjot Kaur,  
Dongsheng Wang, Charese Smiley, Sameena Shah  
JPMorgan AI Research  
{toyin.d.aguda, suchetha.siddagangappa, elena.kochkina, simerjot.kaur, dongsheng.wang,charese.h.smiley, sameena.shah}@jpmchase.com

###### Abstract

Collecting labeled datasets in finance is challenging due to scarcity of domain experts and higher cost of employing them. While Large Language Models (LLMs) have demonstrated remarkable performance in data annotation tasks on general domain datasets, their effectiveness on domain specific datasets remains underexplored. To address this gap, we investigate the potential of LLMs as efficient data annotators for extracting relations in financial documents. We compare the annotations produced by three LLMs (GPT-4, PaLM 2, and MPT Instruct) against expert annotators and crowdworkers. We demonstrate that the current state-of-the-art LLMs can be sufficient alternatives to non-expert crowdworkers. We analyze models using various prompts and parameter settings and find that customizing the prompts for each relation group by providing specific examples belonging to those groups is paramount. Furthermore, we introduce a reliability index (LLM-RelIndex) used to identify outputs that may require expert attention. Finally, we perform an extensive time, cost and error analysis and provide recommendations for the collection and usage of automated annotations in domain-specific settings.

## Introduction

Financial NLP (FinNLP) is an active and growing research area with numerous applications in analyzing and comprehending financial texts. The development of effective FinNLP models relies on well-annotated datasets derived from financial documents. However, annotating such datasets is challenging as it requires a deep understanding of financial concepts to decipher the complex terminologies and calculations present in the documents. Crowdsourcing platforms are generally used for annotations. While they are generally effective for tasks that do not require high levels of expertise, they often produce inconsistent and inaccurate annotations when it comes to domain-specific datasets. This approach requires careful instruction crafting, multiple annotation rounds, increased number of workers, and, finally, expert intervention for enhanced accuracy and consistency.

Text: The predecessor Mississippi Power Company was incorporated under the laws of the State of Maine on November 24, 1924 and was admitted to do business in Mississippi on December 23, 1924 and in Alabama on December 7, 1962.

Relation type: Organization–Date

Expert Label: No/other relation

Crowdworker Label: Formed on

Figure 1: Example of relation extraction task from REFinD dataset.

The wide array of tasks in which Large Language Models (LLMs), such as GPTs [^5] [^22], have demonstrated state-of-the-art zero-shot capabilities naturally raises the question of whether these models have the potential to substitute for human annotators. Using LLMs as data annotators can offer a lot of advantages such as cost-effectiveness, scalability and potential for iterative improvement. However, strong performance on benchmark datasets alone does not ensure a model’s suitability to replace human annotators. In addition to accuracy, consistency and biases associated with this approach needs to be carefully studied.

While positive results of using LLMs as annotators for general-domain tasks have been reported in recent papers and preprints [^14] [^30], their performance in specialized domains such as finance remains underexplored. In this work, we assess the efficacy of LLMs as data annotators for financial relation extraction task using REFinD dataset [^17]. <sup>*</sup>

The relation extraction task in financial documents involves identifying specific relations between financial entities such as companies and persons. Financial relation extraction presents unique challenges due to the domain-specific nature of financial language and the scarcity of labeled data. General relation extraction models trained on generic tasks may lack the necessary understanding of finance-specific terms, leading to difficulties in capturing nuanced patterns. For example, certain relations, such as board membership versus employment, require domain expertise for accurate interpretation. Ambiguity further complicates the task, as implicit relationships, like company acquisitions based on stock ownership, may be challenging for generic models to identify. Furthermore, financial sentences are notably more complex, with longer average lengths and greater entity pair distances compared to generic domains, as demonstrated in REFinD.

Figure 1 shows an example from the REFinD dataset where we are interested in finding a relation between an organization-date entity pair, wherein we are interested in extracting the relation between an organization - Mississippi Power Company and date - December 23, 1924. For this entity pair, the relation label options presented to experts and crowdworkers are (i) formed on (ii) acquired on and (iii) no/other relations. The label chosen by experts is no/other relation, the reason being Mississippi Power Company was formed on November 24, 1924 and not on December 23, 1924. However, crowdworkers incorrectly identified the label as formed on. This discrepancy between expert labels and crowdworker labels highlights the difficulty of financial relation extraction tasks.

In this work, we compare the output of LLMs and crowdworkers against expert annotations, extending our analysis beyond performance metrics and addressing time, cost and reliability aspects of the annotation process. Our contributions are the following: (i) To the best of our understanding, we are the first in the financial domain to demonstrate the capabilities of LLMs as data annotation tools by evaluating them against domain experts and crowdworkers. (ii) We compare 3 models (GPT-4, PaLM 2, and MPT Instruct) and parameters (varying temperature, random seed and prompting approaches) to identify the most accurate and reliable configuration. (iii) We introduce reliability index, a metric designed to identify trustworthy samples and filter out those requiring human intervention. (iv) We demonstrate that LLMs can replace non-expert crowdworkers for a significant portion of the dataset, while expert intervention is necessary for the remaining instances to ensure accurate annotations. We also offer guidance on best practices for implementing LLMs in the annotation process.

## Related Work

[^32] pioneered the use of GPT-3 [^5] as a cost-effective data labeler for training models. The potential of LLMs as data annotators has been explored in various tasks including relevance, stance, topic and frame classification [^14], sentiment analysis, hate speech detection [^34] [^16], political affiliation [^30] and news classification [^27] [^1]. Since the majority of these tasks do not require the domain expertise of a human annotator, the effectiveness of LLMs in domain-specific datasets remains underexplored. This study investigates LLMs’ potential in the financial domain.

Existing literature on the application of LLMs in the financial domain remains sparse. [^19] have evaluated the performance of GPT-3.5 and GPT-4 on various finance benchmark datasets and reported strong performance on arithmetic reasoning, news classification and financial named entity recognition. However, this study did not consider the potential use of LLMs as annotators in comparison to non-expert crowdworkers, or the relation extraction task, which is the focus of our paper.

Several approaches assess the potential of LLMs as data annotators. Studies like [^18] [^6] [^10] explore different aspects of LLMs including comparing zero-shot performance of ChatGPT against a task-specific fine-tuned model, and measuring the alignment of LLM and human evaluations. [^15] [^30] [^14] compare the model outcomes with crowdworkers and expert annotators. While the latter approach is more costly, we adopt it in this study due to its direct relevance to our research question.

LLMs as annotators yield mixed results, with some studies showing higher performance than humans [^14] [^30], while others highlight limitations in new domains [^34] and consistency issues [^27]. [^34] report GPT’s overestimation of certain classes. This further motivates our study to evaluate these aspects for finance domain specifically.

It is also worth noting that most studies focus on GPT models only [^16] [^27] [^30] [^34] [^10]. We address this limitation by comparing three generative LLMs, GPT-4 [^22], PaLM 2 [^4], MPT Instruct [^21], each with different size, training data, and procedures.

## Dataset

Our experiments utilize the REFinD dataset [^17]. Derived from texts within quarterly and annual reports of publicly traded companies (10-X), REFinD is the largest dataset available for financial relation extraction. This is also the only financial domain dataset for which we were able to obtain annotations broken down into expert and individual crowdworkers. REFinD dataset has 28,676 instances and 22 relations types across 8 entity pairs. The only other available Financial relation extraction dataset FinRED [^28] is significantly smaller (6,767 instances and 29 relation types) and does not release annotations provided by individual crowdworkers.

These 8 entity pairs covered in REFinD include person–title, person–organization, person–university, person–government agency, organization–gpe, organization–date, organization–organization and organization–money. Each entity pair includes several finance-oriented relation types. The choice of this dataset is further justified by the fact that it was released in mid 2023, which makes it unlikely to have been part of the training data for the selected LLMs. For our experiments, we utilize 3598 instances from the test set of REFinD, due to the costs associated with LLMs usage.

## Experiments

In this section, we present comprehensive descriptions of the generative models, prompts, and evaluation metrics utilized in our study.

### Models

In our experiments, we employed three Large Language Models (LLMs), GPT-4, PaLM 2, and MPT Instruct, selected based on their exceptional performance in benchmark leaderboards [^2], accessibility, API availability, and permissive licenses. These models vary in size: GPT-4 comprises approximately 1.7 trillion parameters, PaLM 2 has 340 billion, and MPT Instruct is the smallest with 7 billion parameters. This diverse range enables us to evaluate the influence of model size on performance. For each model, we conducted experiments using two temperature settings (0.2 and 0.7) to examine the effects of randomness on model performance. Every model was run twice at each temperature setting. However, users cannot set a random seed for GPT-4 and PaLM 2, resulting in varying outputs between runs. In contrast, MPT Instruct was executed twice using two distinct random seeds.

### Prompts

The quality of prompts used to guide LLMs significantly impacts their performance, akin to the instructions given to crowdworkers. We tailored the instruction around the prompt set up to focus on understanding the financial context around each question. Each input prompt comprises: (1) textual description of the task, (2) a sentence with highlighted entities [^3], and (3) a numbered list of relation options (labels) specific to the entity pair. To avoid bias towards particular label orderings, we shuffle the option list. We experimented with 6 distinct prompt types which fall into 3 categories: zero-shot, few-shot and few-shot chain-of-thought (CoT) prompts. These prompts are based on the annotation instructions provided to MTurk <sup>4</sup> crowdworkers for the REFinD annotations (taken from [^17]), facilitating a better comparison with their outputs.

For zero-shot prompts, we used: (1) simple prompt, a brief task description in basic English and (2) full instruction prompt, an extended version with a more comprehensive task description from the REFinD MTurk annotation instructions, an example of this is provided in Figure 2. Few-shot prompts, include: (3) 1-shot and (4) 5-shot, which build upon the full instruction prompt by adding a few task examples, tailored to the specific entity-pair type. Lastly, we experimented with few-shot CoT prompts: (5) 1-shot CoT and (6) 5-shot CoT. CoT prompts incorporates both the task descriptions and examples, as well as the reasoning behind each example’s decision, as this approach has proven beneficial for other annotation tasks [^33].

Select date of formation relationship described in one sentence. Given a single sentence: The predecessor \*\*Mississippi Power Company\*\* was incorporated under the laws of the State of Maine on November 24, 1924 and was admitted to do business in Mississippi on \_\_December 23, 1924\_\_ and in Alabama on December 7, 1962. With 2 highlighted phrases: Mississippi Power Company and December 23, 1924. Select a multiple choice answer from options below, which best describes the relation between Mississippi Power Company and December 23, 1924.

Please choose the MOST appropriate relation from the following options:

1. Mississippi Power Company is/was formed on December 23, 1924
2. Mississippi Power Company is/was acquired on December 23, 1924
3. no/other relation between Mississippi Power Company and December 23, 1924

Figure 2: Full instruction prompt example.

### Evaluation

We assess the performance in comparison to expert annotators using accuracy and micro-averaged F1 scores. These metrics are calculated separately for each entity pair, and we report the mean average across entity pairs. Since each model’s experiment is run twice, we also average these metrics from the two runs and report this as the final metric. Additionally, we measure the agreement between experiments, the time and cost of annotations, and the reliability index to analyze the efficiency and robustness of LLMs as annotators.

#### Inter Annotator Agreement (IAA)

We evaluate the agreement between different experiment settings to capture the model’s self-consistency and assess the quality and reliability of the annotations. This metric demonstrates how uniformly annotators interpret the given task. To calculate the agreement between two annotators, we use Cohen’s Kappa [^8] and for agreement among more than two annotators, we use Fleiss’ Kappa [^13].

<table><tbody><tr><td colspan="9">Micro-Averaged F1 Score/ Accuracy(%)</td></tr><tr><td></td><td></td><td></td><td colspan="2">Zero-Shot Prompt</td><td colspan="2">Few-Shot Prompt</td><td colspan="2">Few-Shot CoT Prompt</td></tr><tr><td>Annotator</td><td>Type</td><td>Temperature Setting</td><td>simple prompt</td><td>full instruction</td><td>1-shot</td><td>5-shot</td><td>1-shot CoT</td><td>5-shot CoT</td></tr><tr><td></td><td>GPT-4</td><td>[HTML]FFFFFF0.2</td><td>[HTML]FFFFFF67.4/63.4</td><td>68.5/64.6</td><td>65.0/60.1</td><td>67.6/63.8</td><td>64.5/58.4</td><td>68.4/65.4</td></tr><tr><td></td><td>GPT-4</td><td>0.7</td><td>67.6/63.6</td><td>68.4/64.6</td><td>65.0/60.0</td><td>67.7/63.9</td><td>64.6/58.4</td><td>68.4/65.4</td></tr><tr><td></td><td>PaLM 2</td><td>0.2</td><td>62.3/53.9</td><td>62.2/53.8</td><td>66.4/60.1</td><td>66.0/59.2</td><td>64.7/55.9</td><td>65.6/57.2</td></tr><tr><td></td><td>PaLM 2</td><td>0.7</td><td>64.5/56.0</td><td>64.4/56.0</td><td>67.3/60.9</td><td>68.7/63.8</td><td>64.9/57.4</td><td>65.9/59.2</td></tr><tr><td></td><td>MPT Instruct</td><td>0.2</td><td>20.0/21.9</td><td>31.1/27.6</td><td>18.6/18.0</td><td>42.5/36.7</td><td>20.1/18.5</td><td>45.2/36.1</td></tr><tr><td>LLM</td><td>MPT Instruct</td><td>0.7</td><td>20.8/24.7</td><td>24.8/27.3</td><td>22.7/24.2</td><td>30.5/31.1</td><td>22.2/23.2</td><td>33.9/30.8</td></tr><tr><td></td><td>Ensemble (All LLMs)</td><td>0.2</td><td>65.2/60.1</td><td>66.0/60.7</td><td>63.9/58.1</td><td>68.1/63.3</td><td>63.3/56.4</td><td>68.8/63.8</td></tr><tr><td></td><td>Ensemble (GPT-4 w Palm 2)</td><td>0.2</td><td>67.2/63.2</td><td>68.6/64.7</td><td>65.0/60.1</td><td>67.8/64.0</td><td>64.3/58.1</td><td>68.2/65.2</td></tr><tr><td></td><td>Ensemble (GPT-4 w MPT Instruct)</td><td>0.2</td><td>67.2/63.2</td><td>68.6/64.7</td><td>65.0/60.1</td><td>67.8/64.0</td><td>64.3/58.1</td><td>68.2/65.2</td></tr><tr><td></td><td>Ensemble (Palm 2 w MPT Instruct)</td><td>0.2</td><td>62.6/54.3</td><td>61.9/53.6</td><td>66.7/60.5</td><td>66.1/59.4</td><td>64.5/55.7</td><td>65.4/56.9</td></tr><tr><td>Human</td><td>Mturk Annotators</td><td>-</td><td>-</td><td>38.6/40.7</td><td>-</td><td>-</td><td>-</td><td>-</td></tr></tbody></table>

Table 1: Annotator performance in terms of micro-averaged F1-Score and accuracy against expert assigned labels.

#### Reliability Index (LLM-RelIndex)

To aggregate the label for each sample from multiple annotators, we could simply calculate the raw voting counts for each label from K annotators. However, this approach has an issue when annotators all choose distinct labels, then an arbitrary label would be selected. As those distinct labels could be semantically related, such as member of, employee of and founder of, incorporating such label similarity can improve the aggregation precision. Thus, we refine the voting approach by taking label similarity into account i.e., the similarities between its assessments $a_{i}$ and each label $l$. The refined voting score, which considers the assessments of multiple annotators, measures the agreement for each label $l$ as $\text{vote}(i,l)=sim(a_{i},l)$. We then define the confidence as $\text{confid}(l)=\frac{1}{K}\sum_{i=1}^{K}\text{vote}(i,l)$. Note that similarity is defined as per the judgements of domain experts.

Additionally, we introduce the Reliability-Index, defined as the maximum confidence score $\text{confid}(l)$ of the label $l$:

$$
\text{LLM-RelIndex}_{i}=\arg\max_{l\in L}\text{confid}(l)
$$

The Reliability-Index aids in identifying the most reliable label for each instance. It enables the detection of outputs that warrant human expert attention.

#### Time & cost

For models served via API, the price per instance depends on the number of tokens (GPT-4 <sup>5</sup>) or characters (PaLM 2 <sup>6</sup>) in both the prompt and generated outputs. Consequently, the annotation cost was calculated by multiplying the average number of tokens/characters in the prompt and output, the number of instances, and the price per instance. For the open-source MPT-Instruct model, the cost was based on the per-hour price of the AWS machine utilized. Due to high GPU memory requirements, we used p3.2xlarge machines with 1 Tesla V100 GPU [^7]. The annotation cost was calculated by multiplying the average time taken per instance in hours, the number of instances, and the price per hour.

## Results

In this section, we discuss our experimental findings, focusing on model performance, annotator agreement, error analysis and reliability.

### Model Performance

Table 1 presents the micro-averaged F1 score and accuracy for each LLM by prompt type and temperature setting, as well as the performance of MTurk annotators. We observe that GPT-4 and PaLM 2 significantly outperform crowdsourced annotations, with a margin of up to 29%. Both models exhibit comparable performance, with GPT-4 being the best. MPT Instruct demonstrates lower overall performance but still outperforms the human annotators in terms of F1-score when using 5-shot CoT prompt. These results highlight the potential of LLMs as annotators. However, none of the models reach the expert performance, indicating that domain-specific settings still require expert’s involvement. Figure 3 visualizes the results for the full instruction prompt, which is identical to the MTurk instructions.

Regarding the impact of prompt type on model performance, Table 1 reveals that the input prompt design significantly influences LLM performance. GPT-4 and PaLM 2 exhibit higher robustness under different prompts (5-7% difference), whereas prompt type has a strong effect on MPT Instruct performance (19%). MPT Instruct benefits considerably from additional examples (5-shot and 5-shot CoT). Interestingly, few-shot and few-shot CoT prompts do not consistently outperform the zero-shot full instruction prompt. GPT-4 achieve its highest micro-averaged F1 score using the zero-shot full instruction prompt.

![Refer to caption](https://arxiv.org/html/2403.18152v1/extracted/2403.18152v1/Figs/full_instru_score.png)

Figure 3: Annotator performance in terms of micro-averaged F1-Score under full instruction prompt.

Comparing performance at 0.2 and 0.7 temperature settings, we find that GPT-4 and PaLM 2 outputs remains stable regardless of the randomness introduced by the temperature parameter. While PaLM 2 consistently exhibits higher performance at 0.7, the observed performance differences are not statistically significant at the 0.05 significance level using a two-tailed t-test 9. MPT Instruct performance is heavily affected by temperature settings, but no consistent pattern of superiority emerges for either setting. The highest scores are achieved at 0.2 with 5-shot example prompts.

Additionally, we evaluate the performance of an ensemble of models using a simple majority voting approach, which mimics having multiple annotators. While this approach results in the highest overall accuracy score, it does not consistently improve performance across all prompt types compared to a single model approach.

<table><tbody><tr><td rowspan="2">LLM</td><td colspan="2">Zero-Shot Prompt</td><td colspan="2">Few-Shot Prompt</td><td colspan="2">Few-Shot CoT Prompt</td></tr><tr><td>simple</td><td>full instruction</td><td>1-shot</td><td>5-shot</td><td>1-shot CoT</td><td>5-shot CoT</td></tr><tr><td>GPT-4</td><td>69.3</td><td>70.2</td><td>71</td><td>68.8</td><td>72.5</td><td>66.2</td></tr><tr><td>PaLM 2</td><td>74.5</td><td>73.8</td><td>74.9</td><td>76.1</td><td>79.8</td><td>80.7</td></tr><tr><td>MPT Instruct</td><td>46.4</td><td>52.5</td><td>48.4</td><td>57.5</td><td>49.7</td><td>64.9</td></tr></tbody></table>

Table 2: Proportion of LLM Hallucinations for instances labelled as no/other relation by experts

### Inter-Annotator Agreement

High performance alone is insufficient for LLMs to serve as annotators, their output must also be consistent to be considered reliable. Therefore, we assess the consistency of the output by measuring agreement scores for models in different experiment settings shown in Table 3. First, we evaluate whether the models produce consistent outputs with the exact same parameters. For each experiment setting, we measure the IAA between the two runs of each model and then present an average score (row 1).

We observe that none of the models exactly replicate the outputs. GPT-4 and PaLM 2 exhibit high levels of agreement, while MPT runs with two different random seeds display significant differences.

|  | GPT-4 | PaLM 2 | MPT |
| --- | --- | --- | --- |
| Random seed run1 vs run2 | 0.95 | 0.88 | 0.395 |
| Temperature 0.2 vs 0.7 | 0.95 | 0.85 | 0.30 |
| Zero-shot: simple vs full | \[HTML\]FFFFFF0.87 | \[HTML\]FFFFFF0.88 | \[HTML\]FFFFFF0.39 |
| Few-shot: 1- vs 5-shot | \[HTML\]FFFFFF0.84 | \[HTML\]FFFFFF0.79 | \[HTML\]FFFFFF0.28 |
| Few-shot CoT: 1- vs 5-shot | \[HTML\]FFFFFF0.8 | \[HTML\]FFFFFF0.82 | \[HTML\]FFFFFF0.28 |
| All prompts (Fleiss) | \[HTML\]FFFFFF0.83 | \[HTML\]FFFFFF0.79 | \[HTML\]FFFFFF0.31 |

Table 3: Pairwise IAA in terms of Cohen Kappa (top 5 rows) and IAA between outputs for all prompts in terms of Fleiss Kappa (last row). First two rows present mean averaged values of pairwise Cohen Kappa for each prompt type.

We then evaluate the agreement between outputs produced under two different temperature settings (row 2). GPT-4 agreement remains high even when varying the temperature parameter, while scores of PaLM 2 and MPT decrease. Furthermore, we compare the agreement between outputs produced using different prompts, both pairwise (using Cohen’s Kappa, rows 3-5) and between the group of prompts (using Fleiss Kappa, row 6). We find that the choice of prompt has a more substantial impact on the outputs of the model, reducing the agreement for all LLMs. Overall, GPT-4 and PaLM 2 demonstrate reasonably high agreement across various experiment settings, indicating their overall reliability for the annotation task.

### Error Analysis

In our error analysis, we aim to identify and categorize common issues encountered by LLMs during the annotation process. By examining instances with incorrect answers, hallucinated relations, and confident misannotations, we aim to gain insights into the challenges faced by LLMs and explore potential improvements for their performance in complex tasks, such as relation extraction.

#### Semantic Ambiguity

We analyze instances where LLMs return incorrect answers and observe that these errors often stem from the proximity and similarity of the answer options, causing confusion in identifying the most accurate response. Common trends include member of instead of employee of and formed in rather than operations in. This highlights the need to improve LLM’s comprehension of subtle differences. For instance, in the example “W. Howard Keenan, Jr. has served as a director of Midstream Management since February 2014”, both GPT-4 and PaLM 2 incorrectly choose member of over the correct relation employee of. Although MPT Instruct’s result is also inaccurate, its answer varies significantly by prompt type, exhibiting a level of randomness not observed in the other two LLMs. Its also worth noting that MPT Instruct returns blanks for some instances. 0.5% of the responses from MPT Instruct for each prompt variation were blanks.

#### Relation Hallucinations

In our relation extraction task, we provide the LLMs with limited label options, including an option for no/other relation available for every entity pair. Consequently, we expect minimal instances of hallucinations, i.e., LLMs inventing new relations between specified entities not present in the label set or generating off-topic responses. We analyze the LLM outputs for instances labeled as no/other relation by the experts and report the proportion of hallucinations among them (Table 2). We observe that hallucinations primarily emerge from PaLM 2 for 5-shot CoT, where 80.7% of instances labeled as no/other relation by the experts were misidentified by PaLM 2 as hallucinations. Overall, LLMs exhibit a higher tendency to generate new relations when the expert label is no/other relation. GPT-4 and PaLM 2 tend to hallucinate more than MPT Instruct. We post-process the hallucinated relations to extract relation styles similar to those in the label options. The most common relations extracted from these are agreement with, shares of, member of and subsidiary of.

Scenario 1 (Crowdworkers incorrect, LLMs correct):  
Instance: Personal Lines underwriting profit for the three months ended September 30, 2017 was $ 40.8 million, compared to $ 23.3 million for the three months ended September 30, 2016, an improvement of $ 17.5 million.

Expert Label: Profit of

Crowdworker Label: Profit of, No/Other Relation, Loss of  
LLMs Label: Profit of

Scenario 2 (Crowdworkers and LLMs incorrect):  
Instance: Our Hawaii Gas entered into licensing agreements with Utility Service Partners, Inc. and America’s Water Heater Rentals, LLC, both indirect subsidiaries of Macquarie Group Limited, to enable these entities to offer products and services to Hawaii Gas’s customer base.

Expert Label: Subsidiary of

Crowdworker Label: No/Other Relation, Subsidiary of, Shares of

LLMs Label: Agreement with

Scenario 3 (Crowdworkers correct, LLMs incorrect):  
Instance: On December 10, 2014, Orbital Tracking Corp. purchased certain contracts from Global Telesat Corp, a Virginia corporation ( GTC ) for $ 250,000 pursuant to an asset purchase agreement by and among Orbital Tracking Corp., its wholly owned subsidiary Orbital Satcom, GTC and World Surveillance Group, Inc. ( World ), GTC’s parent.

Expert Label: Subsidiary of

Crowdworker Label: Subsidiary of  
LLMs Label: Agreement with

Figure 4: Error Analysis: Qualitative examples illustrating different scenarios of how MTurk Crowdworkers and LLMs demonstrated high confidence on incorrect answer choices.

#### Confident Misannotations

We analyze instances where LLMs and crowdworkers return incorrect answers with high confidence (answers selected by majority of annotators). The relationship between high confidence and incorrect answer choice varies, and we observe three scenarios: (i) the majority of crowdworker labels are incorrect while the majority of LLM labels are correct, (ii) the majority of both crowdworker and LLM annotations are incorrect, and (iii) the majority of crowdworker labels are correct while the majority of LLM labels are incorrect. Qualitative examples of these can be found in Figure 4. This analysis demonstrates that the varying dynamics between LLMs and crowdworkers emphasize the importance of refining LLMs to better understand nuanced distinctions and improve their reliability in annotation tasks. Furthermore, the analysis highlights the potential benefits of combining the expertise of both LLMs and human annotators to achieve more accurate and reliable annotations in complex tasks, such as relation extraction.

### LLM-RelIndex Based Accuracy Analysis

In this analysis, we employ the LLM-RelIndex majority voting scheme to assess the accuracy derived from human votes and LLM results across all six prompt variations on the dataset. The data is arranged in descending order of LLM-RelIndex that is we moved from instances that were simple to annotate to the more complex ones and we present the accuracy for incremental percentages of the dataset. We showcase the plots for three distinct cases: (i) zero-shot (Figure 5), (ii) few-shot (Figure 6), and (iii) few-shot CoT (Figure 7).

![Refer to caption](https://arxiv.org/html/2403.18152v1/extracted/2403.18152v1/Figs/zs_rellndex.png)

Figure 5: Human vs LLMs at Zero-shot using LLM-RelIndex

Our observations indicate that for all three cases, GPT-4 and PaLM 2 outperform both Human Votes and MPT Instruct when considering $\sim$ 65% of the dataset. However we also observed a drop in accuracy in the top 20% of the dataset where there were high level agreements among LLMs. This can be attributed to the instances which were simple to annotate but easier to error on. Hence we observe that in those instances most of the LLMs made the same mistakes as human annotators which were inconsistent with expert choices. For example “The number of shares that are sold by Cowen after delivering a sales notice will fluctuate based on the market price of Dermira, Inc common stock during the sales period and limits Dermira, Inc. set with Cowen.” Most of the LLMs chose Agreement with over Shares of where the latter is the correct relation.

Additionally, PaLM 2’s performance exhibits an upward trend, as we transition from zero-shot to few-shot, and ultimately to few-shot CoT scenarios. We also find that all LLMs demonstrate improved results for 5-shot and 5-shot CoT, suggesting that having more examples and explanations enhances the reliability of LLM-generated annotations.

![Refer to caption](https://arxiv.org/html/2403.18152v1/extracted/2403.18152v1/Figs/fs_rellndex.png)

Figure 6: Human vs LLMs at Few-shot using LLM-RelIndex

As we progress towards complete dataset coverage, again we see a decline in performance is noted. This outcome is anticipated since instances with lower LLM-RelIndex scores become more prevalent as we approach more complex instances. Here the LLMs likely lack confidence in relations between specific entity pairs.

![Refer to caption](https://arxiv.org/html/2403.18152v1/extracted/2403.18152v1/Figs/cot_rellndexupd.png)

Figure 7: Human vs LLMs at Few-shot CoT using LLM-RelIndex

Overall, LLM-RelIndex allows us to confidently assert that LLMs can serve as more reliable annotators for $\sim$ 65% of this dataset. For cases beyond this threshold, expert intervention is necessary to determine the appropriate annotation. This strategy effectively reduces the cost and time associated with human annotation of the entire dataset, streamlining the process considerably.

### Time and Cost Analysis

We calculate the annotation cost for each of the LLMs (detailed in Evaluation section) and compare it to our estimated cost of MTurk annotations. The average input prompt size ranges from 191 tokens (814 characters) for simple prompts to 441 tokens (1954 characters) for 5-shot CoT prompts. On average, GPT-4 generates an output of 17 tokens (65 characters) for all prompt types. The outputs of PaLM 2 vary more in size, from 70 to 36 tokens (298 and 147 characters), with shorter outputs for longer prompts like few-shot and few-shot CoT. Each model can process an instance within 1-5 seconds, with longer prompts requiring more processing time. MPT Inference on average takes 0.96 seconds for simple prompts and 1.81 for the longest 5-shot CoT prompts. The annotation price increases with the prompt size, and for our dataset of 3598 instances, it ranges from $24-51 for GPT-4, $5-9 for PaLM 2 and $29-55 for MPT Instruct.

For crowdsourced human annotators, the time and associated cost would be higher. Assuming a human annotator takes 45 seconds per instance and is paid the US minimum wage of $7.25 per hour <sup>8</sup>, the dataset’s annotation cost using a single annotator amounts to $389. However, the crowdsourced annotation process typically involves multiple annotators per instance. These outcomes demonstrate that automated annotations are more efficient in terms of time and cost compared to human labelling.

## Discussion

In this section we discuss our findings and share recommendations for future annotation tasks. Our experiments demonstrated the potential of LLMs as data annotators for tasks within the financial domain. Specifically, GPT-4 and PaLM 2 have exhibited exceptional performance, surpassing the accuracy of the non-expert crowdworkers, while delivering time and cost savings. PaLM 2 has achieved comparable results to GPT-4, despite its smaller size, at a fraction of the cost ($\sim$ 5 times less). These models have also displayed robustness by producing consistent outputs across various parameter and prompt configurations. However, it is crucial to recognize that LLMs’ performance does not yet match that of domain experts and expert involvement remains necessary for obtaining high-quality annotations with minimal or no noise.

The next generation of annotation approaches in domain-specific contexts should consider adopting a hybrid strategy, harnessing both automated and expert-generated annotations to optimize results. In these settings, approximating model uncertainty, e.g., via the LLM-RelIndex, can help prioritize instances that require expert attention. In all annotation tasks, the ability to formulate detailed instructions is a vital factor, regardless of whether annotators are human or LLMs. Carefully crafting prompts, guided by an understanding of the task and the specific LLM being used helps optimize the outputs generated by the LLMs.

We, therefore, recommend that researchers conduct small preliminary experiment on a data subset to assess model capabilities and identify optimal parameter and prompt configurations. The specifics of the task should inform researchers about the tolerance for annotation noise, allowing them to train new models using automatically annotated data accordingly. Moreover, future annotation tasks can benefit from more open task formulations, leveraging the generative abilities of LLMs. For instance, in our task, LLMs have the potential to help identify more relations than the original pre-defined set. As such, future experiment can be done to check if these LLM-annotated data boost downstream performances. Lastly, it is essential to remain mindful that model biases may differ from those of crowdworkers and to account for these differences where necessary.

## Limitations

One of the main limitations of this work is that the evaluation is performed only on a single dataset, covering a single task. The dataset contains the texts from one particular source, SEC filings, and it would be interesting to compare the results when the texts come from other financial sources, such as news or earning calls. This limitation partially comes from the costs of using the LLMs, and partially from the absence of financial datasets with annotations produced by individual crowdworkers released publicly.

In this work we present the breakdown of the results and their analysis by relation categories in the Appendix due to the page limit. We found that model performance varies strongly between the entity pair groups similar to [^17] with organization-organization being the most challenging category. In future work, we aim to expand our analysis further with respect to categories of errors frequently associated with this task and financial domain such as numerical inference, semantic and directional ambiguity.

We observe that our LLM-Rellndex metric is subject to error, particularly with instances that are easy to annotate. Efforts are underway to enhance this metric. Furthermore, we are exploring the adoption of an automated and systematic approach for calculating similarity scores rather than depending on experts’ judgment. Additionally, we intend to incorporate multi-label samples into our approach, given that some similar labels may closely align for some cases.

Finally, while providing the discussion, we do not experimentally demonstrate how the automatically annotated dataset can be used, either to improve relation extraction model performance, or to develop smaller efficient models. We recognize the importance of this and leave this to future work.

## Conclusion

In this study, we have showcased the remarkable potential of using LLMs as a robust alternative to non-expert crowdworkers for domain-specific task by comparing three LLMs of varying sizes. Due to large volume of unstructured documents within financial domain, leveraging LLMs for annotations significantly reduces the time spent by humans on manual annotation, while providing valuable insights for making well-informed downstream decisions and driving efficient business outcomes. Our evaluation shows that larger models like GPT-4 and PaLM 2 excel in these tasks, while incorporating more examples into prompts for smaller models like MPT Instruct can yield improved results. We also introduced the reliability index, a metric that identifies reliable labels and detects outputs requiring expert attention, enhancing quality control and decision-making. Our error analysis provides valuable insights for future improvements.

The integration of LLMs streamlines the annotation process, delivering consistent, high-quality outputs that result in substantial time savings and cost-effectiveness. However, their performance does not yet match that of experts who possess a nuanced understanding of the subject matter. While LLMs offer scalability and reduced time and costs compared to employing experts, there exists a trade-off between the convenience and efficiency of LLMs and the precision provided by expert annotators. Consequently, the decision to employ LLMs as annotators should be carefully guided by the desired level of accuracy and the complexity of the task at hand, striking the right balance between automation and human expertise.

## Acknowledgments

We would like to thank Armineh Nourbakhsh, Natraj Raman, Xiaomo Liu, Manuela Veloso, and our anonymous reviewers for their thoughtful comments and feedback which greatly contributed to the quality of this work.

Disclaimer. This paper was prepared for informational purposes by the Artificial Intelligence Research group of JPMorgan Chase & Co. and its affiliates (“JP Morgan”), and is not a product of the Research Department of JP Morgan. JP Morgan makes no representation and warranty whatsoever and disclaims all liability, for the completeness, accuracy or reliability of the information contained herein. This document is not intended as investment research or investment advice, or a recommendation, offer or solicitation for the purchase or sale of any security, financial instrument, financial product or service, or to be used in any way for evaluating the merits of participating in any transaction, and shall not constitute a solicitation under any jurisdiction or to any person, if such solicitation under such jurisdiction or to such person would be unlawful.

## Ethical Considerations

This paper explores the use of LLMs for data annotation. As such, the prevailing concerns around the use of LLMs apply to this work. This includes the potential to generate text containing bias, stereotypes, misinformation and, as noted in the discussion, hallucinations. Outside of issues concerning LLM usage, we do not anticipate other ethical concerns with this work.

## Bibliographical References

## References

## Appendix A Appendices

### Dataset relation distribution

| Entity-Pair | No. ofInstances |
| --- | --- |
| ORG-GPE | 710 |
| ORG-ORG | 913 |
| ORG-DATE | 554 |
| ORG-MONEY | 281 |
| PER-ORG | 485 |
| PER-TITLE | 655 |
| Total | 3598 |

Table 4: Dataset Relation Distribution

### Metrics for MTurk Annotators

<table><tbody><tr><td colspan="2">Micro F1 Score/ Accuracy (%)</td></tr><tr><td>Entity Pair</td><td>MTurk Annotators</td></tr><tr><td>ORG-GPE</td><td>37.3/35.8</td></tr><tr><td>ORG-ORG</td><td>13.5/21.6</td></tr><tr><td>ORG-DATE</td><td>31.4/45.0</td></tr><tr><td>ORG-MONEY</td><td>26.4/29.1</td></tr><tr><td>PER-ORG</td><td>33.9/32.3</td></tr><tr><td>PER-TITLE</td><td>89.0/80.4</td></tr><tr><td>Total</td><td>38.6/40.7</td></tr></tbody></table>

Table 5: MTurk Annotator Micro-average F1 Score/Accuracy by Entity Pair

### LLM Setup and Configuration

The setup and configuration of each LLMs have some overlap such as specifying the location of each entity in the text, however, there are notable differences as well. These differences enabled each LLM to perform at its best. Figure 1 explains the different piece of LLM setup and configuration. Unlike GPT-4, where we had ”system role”, in PaLM 2 we had ”Additional Instruction”. This is the unique prompt design for the different prompt type.

Setup & Configuration: ORG-DATE

Instruction:Select the statement that best describes the relation in the example sentence below. Ignore any grammatical errors. If there are multiple options, please choose the one that is clearest and most obvious from the sentence.

Prompt: The predecessor Mississippi Power Company was incorporated under the laws of the State of Maine on November 24, 1924 and was admitted to do business in Mississippi on December 23, 1924 and in Alabama on December 7, 1962.

Prompt+: Please choose the MOST appropriate relation from the following options:

1. Entity1 is/was formed on Entity2.
2. Entity1 is/was acquired on Entity2.
3. No/other relation between Entity1 and Entity2.

System role: You are an AI assistant and relation extraction checker. You read the prompt, note where the entities in question are and determine the relation between them. Once done, please select from option which best suite the relation.

GPT-4 setup follows: Using the context from ”setup piece and configuration”

Zero-shot:

This starts with Prompt, followed by Prompt+ and finally System role and Response.

Few-shot:

This starts with Instruction, followed by Prompt with example(s), Prompt+ and finally System role and Response.

Few-shot CoT:

This starts with Instruction followed by Prompt with example(s), Reasoning, Prompt+ and finally System role and Response.

PaLM 2 setup follows: Using the context from ”setup piece and configuration”

Zero-shot:

This starts with System role called Additional Instruction in PaLM 2, followed by Prompt and finally Prompt+ and Response.

Few-shot:

This starts with System role called Additional Instruction followed by Instruction, Prompt with example(s), and finally Prompt+ and Response.

Few-shot CoT:

This starts with Instruction followed by Prompt with example(s), Reasoning, Prompt+ and finally System role and Response.

MPT Instruct setup follows: Using the context from ”setup piece and configuration”

Zero-shot:

This starts with System role also called Instruction in MPT Instruct, followed by Prompt and finally Prompt+ and Response.

Few-shot:

This starts with System role called Instruction, followed by Prompt with example(s), and finally Prompt+ and Response.

Few-shot CoT:

This starts with Instruction, followed by Prompt with example(s), Reasoning, Prompt+ and finally System role.

Figure 8: LLM Setup and Configuration.

### Prompt Description

| Title | Prompt style based on LLM setup |
| --- | --- |
| Simple Prompt | In the context of this sentence: The predecessor \*\*Mississippi Power Company\*\* was incorporated under the laws of the State of Maine on November 24, 1924 and was admitted to do business in Mississippi on \_\_December 23, 1924\_\_ and in Alabama on December 7, 1962. Note the location of the Mississippi Power Company and December 23, 1924 as highlighted to help determine the relation given the listed options below. Please choose the MOST appropriate relation from the following options: 1. Mississippi Power Company is/was acquired on December 23, 1924. 2. Mississippi Power Company is/was formed on December 23, 1924. 3. no/other relation between Mississippi Power Company and December 23, 1924. |
| Full Instruction Prompt | Select date of formation relationship described in one sentence. Given a single sentence: The predecessor \*\*Mississippi Power Company\*\* was incorporated under the laws of the State of Maine on November 24, 1924 and was admitted to do business in Mississippi on \_\_December 23, 1924\_\_ and in Alabama on December 7, 1962. With 2 highlighted phrases:Mississippi Power Company and December 23, 1924, select a multiple choice answer from options below, which best describes the relation between Mississippi Power Company and December 23, 1924. Please choose the MOST appropriate relation from the following options: 1. Mississippi Power Company is/was formed on December 23, 1924. 2. Mississippi Power Company is/was acquired on December 23, 1924. 3. no/other relation between Mississippi Power Company and December 23, 1924. |
| 1-Shot Prompt | Select the statement that best describes the relation in the example sentence below. Ignore any grammatical errors. If there are multiple options, please choose the one that is clearest and most obvious from the sentence. \\n\\nExample Sentence 1:\*\*LecTec\*\* was organized in 1977 as a Minnesota corporation and went public in \_\_December 1986\_\_. \\n Answer to Example 1: LecTec was formed/incorporated on/in December 1986. \\n Following the example above, read through this sentence: The predecessor \*\*Mississippi Power Company\*\* was incorporated under the laws of the State of Maine on November 24, 1924 and was admitted to do business in Mississippi on \_\_December 23, 1924\_\_ and in Alabama on December 7, 1962. Given the location of the Mississippi Power Company and December 23, 1924 as highlighted, choose an answer from listed options below. \\n Please choose the MOST appropriate relation from the following options: \\n 1. Mississippi Power Company is/was acquired on December 23, 1924\\n 2. Mississippi Power Company is/was formed on December 23, 1924\\n 3. no/other relation between Mississippi Power Company and December 23, 1924. |
| 5-Shot Prompt | Select the statement that best describes the relation in the example sentence below. Ignore any grammatical errors. If there are multiple options, please choose the one that is clearest and most obvious from the sentence. \\n\\n Example Sentence 1:\*\*LecTec\*\* was organized in 1977 as a Minnesota corporation and went public in \_\_December 1986\_\_. \\n Answer to Example 1: LecTec was formed/incorporated on/in December 1986. \\n Example Sentence 2: The assets of \*\*Unified Payments, LLC\*\* were acquired by us in \_\_April 2013\_\_.\\n Answer to Example 2: Unified Payments, LLC was acquired in April 2013. \\n Example Sentence 3: Since \_\_July 6, 2016\_\_, Pinnacle West has issued four parental guarantees for 4CA relating to payment obligations arising from 4CA s acquisition of El Paso s 7 % interest in \*\*Four Corners\*\*, and pursuant to the Four Corners participation agreement payment obligations arising from 4CA s ownership interest in Four Corners. \\n Answer to Example 3: No relation between Four Corners and July 6, 2016. \\n Example Sentence 4: In\_\_ 2014\_\_, $ 148 million cash proceeds, net of cash sold, from Sempra Renewables sale of 50 - percent equity interests in \*\*Copper Mountain Solar 3\*\* ( $ 66 million ) and Broken Bow 2 Wind ( $ 58 million ), and Sempra Mexico s sale of a 50 - percent equity interest in Energ a Sierra Ju rez ( $ 24 million ); and.\\n Answer to Example 4: No relation between Copper Mountain Solar 3 and 2014.\\n Example Sentence 5: \*\*Zendex\*\* was incorporated in the state of Utah in \_\_March 2011\_\_ to create an online platform for the sale of art.\\n Answer to Example 5:Zendex was formed in March 2011. \\n\\n Following the example above, read through this sentence: The predecessor \*\*Mississippi Power Company\*\* was incorporated under the laws of the State of Maine on November 24, 1924 and was admitted to do business in Mississippi on \_\_December 23, 1924\_\_ and in Alabama on December 7, 1962. Given the location of the Mississippi Power Company and December 23, 1924 as highlighted, choose an answer from listed options below. \\n Please choose the MOST appropriate relation from the following options: \\n 1. Mississippi Power Company is/was formed on December 23, 1924\\n 2. Mississippi Power Company is/was acquired on/in December 23, 1924\\n 3. no/other relation between Mississippi Power Company and December 23, 1924. |

| Title | Prompt style based on LLM setup |
| --- | --- |
| 1-Shot CoT Prompt | Select the statement that best describes the relation in the example sentence below. Ignore any grammatical errors. If there are multiple options, please choose the one that is clearest and most obvious from the sentence. \\n\\n Example Sentence 1:\*\*LecTec\*\* was organized in \_\_1977\_\_ as a Minnesota corporation and went public in December 1986. \\n Answer to Example 1: LecTec was formed/incorporated on/in 1977. \\n The reasoning for the above answer is that the highlighted portion of the question, LecTec, corresponds with the entity being discussed, and the year 1977 refers to when LecTec was organized or incorporated, both of which are accurately reflected in the answer.\\n Following the example above, read through this sentence: The predecessor \*\*Mississippi Power Company\*\* was incorporated under the laws of the State of Maine on November 24, 1924 and was admitted to do business in Mississippi on \_\_December 23, 1924\_\_ and in Alabama on December 7, 1962. Given the location of the Mississippi Power Company and December 23, 1924 as highlighted, choose an answer from listed options below. \\n Please choose the MOST appropriate relation from the following options: \\n 1. Mississippi Power Company is/was acquired on December 23, 1924\\n 2. Mississippi Power Company is/was formed on December 23, 1924\\n 3. no/other relation between Mississippi Power Company and December 23, 1924. |
| 5-Shot CoT Prompt | Select the statement that best describes the relation in the example sentence below. Ignore any grammatical errors. If there are multiple options, please choose the one that is clearest and most obvious from the sentence. \\n\\n Example Sentence 1:\*\*LecTec\*\* was organized in \_\_1977\_\_ as a Minnesota corporation and went public in December 1986. \\n Answer to Example 1: LecTec was formed/incorporated on/in 1977. \\n The reasoning for the above answer is that the highlighted portion of the question, LecTec, corresponds with the entity being discussed, and the year 1977 refers to when LecTec was organized or incorporated, both of which are accurately reflected in the answer. \\n Example Sentence 2: The assets of \*\*Unified Payments, LLC\*\* were acquired by us in \_\_April 2013\_\_.\\n Answer to Example 2: Unified Payments, LLC was acquired in April 2013. \\n The reasoning for the answer above is that the highlighted portions of the question indicate the key elements of the event being asked about: Unified Payments, LLC being the entity that was acquired and April 2013 being the time when the acquisition took place, both of which are directly stated in the answer. \\n Example Sentence 3: Since \_\_July 6, 2016\_\_, Pinnacle West has issued four parental guarantees for 4CA relating to payment obligations arising from 4CA s acquisition of El Paso s 7 % interest in \*\*Four Corners\*\*, and pursuant to the Four Corners participation agreement payment obligations arising from 4CA s ownership interest in Four Corners. \\n Answer to Example 3: No relation between Four Corners and July 6, 2016. \\n We are only interested in identifying if the organization mentioned was formed on the specified date or acquired by another organization on the specified date. Since Four Corners was neither formed on July 6, 2016 nor acquired by another company on July 6, 2016, there is no relation between Four Corners and July 6, 2016.\\n Example Sentence 4: In\_\_ 2014\_\_, $ 148 million cash proceeds, net of cash sold, from Sempra Renewables sale of 50 - percent equity interests in \*\*Copper Mountain Solar 3\*\* ( $ 66 million ) and Broken Bow 2 Wind ( $ 58 million ), and Sempra Mexico s sale of a 50 - percent equity interest in Energ a Sierra Ju rez ( $ 24 million ); and.\\n Answer to Example 4: No relation between Copper Mountain Solar 3 and 2014.\\n We are only interested in identifying if the organization mentioned was formed on the specified date or acquired by another organization on the specified date. Since Copper Mountain Solar 3 was neither formed in 2014 nor acquired by another company in 2014, there is no relation between Copper Mountain Solar 3 and 2014. \\n Example Sentence 5: \*\*Zendex\*\* was incorporated in the state of Utah in \_\_March 2011\_\_ to create an online platform for the sale of art.\\n Answer to Example 5:Zendex was formed in March 2011. \\n\\n The incorporation of Zendex in March 2011 suggests that this is the official date when the company was legally established and recognized as a corporate entity in the state of Utah. Hence Zendex was formed on March 2011. \\n Following the example above, read through this sentence: The predecessor \*\*Mississippi Power Company\*\* was incorporated under the laws of the State of Maine on November 24, 1924 and was admitted to do business in Mississippi on \_\_December 23, 1924\_\_ and in Alabama on December 7, 1962. Given the location of the Mississippi Power Company and December 23, 1924 as highlighted, choose an answer from listed options below. \\n Please choose the MOST appropriate relation from the following options: \\n 1. Mississippi Power Company is/was formed on December 23, 1924\\n 2. Mississippi Power Company is/was acquired on/in December 23, 1924\\n 3. no/other relation between Mississippi Power Company and December 23, 1924. |

Table 6: Prompts for Entity-Pair: ORG-DATE

### Metrics for LLM Annotators

<table><tbody><tr><td colspan="10">RUN 1: Micro F1 Score / Accuracy(%)</td></tr><tr><td rowspan="2">LLM</td><td rowspan="2">Annotator</td><td rowspan="2">Annotator Description</td><td colspan="6">Entity-Pair</td><td rowspan="2">Total</td></tr><tr><td>ORG-GPE</td><td>ORG-ORG</td><td>ORG-DATE</td><td>ORG-MONEY</td><td>PER-ORG</td><td>PER-TITLE</td></tr><tr><td rowspan="12">GPT-4</td><td>annotator1</td><td>simple prompt, temp=0.2</td><td>80.1/74.8</td><td>15.4/38.4</td><td>48.9/67.0</td><td>48.4/43.4</td><td>70.8/67.8</td><td>92.7/86.9</td><td>67.2/63.2</td></tr><tr><td>annotator2</td><td>simple prompt, temp=0.7</td><td>80.3/74.6</td><td>15.1/37.1</td><td>51.6/70.0</td><td>48.9/44.5</td><td>72.1/69.3</td><td>93.2/87.6</td><td>67.8/63.7</td></tr><tr><td>annotator3</td><td>full instruction, temp=0.2</td><td>80.9/75.8</td><td>15.7/36.7</td><td>56.3/74.5</td><td>47.8/43.1</td><td>72.8/69.9</td><td>93.7/88.7</td><td>68.6/64.7</td></tr><tr><td>annotator4</td><td>full instruction, temp=0.7</td><td>80.9/75.8</td><td>15.5/36.9</td><td>55.4/73.8</td><td>47.6/42.7</td><td>71.8/69.3</td><td>93.5/88.2</td><td>68.2/64.4</td></tr><tr><td>annotator5</td><td>1-shot, temp=0.2</td><td>79.6/73.9</td><td>15.4/30.1</td><td>48.0/65.7</td><td>47.4/42.0</td><td>62.5/60.0</td><td>94.4/89.9</td><td>65.0/60.1</td></tr><tr><td>annotator6</td><td>1-shot, temp=0.7</td><td>79.8/73.9</td><td>14.5/28.9</td><td>50.3/68.1</td><td>48.0/42.3</td><td>62.5/60.0</td><td>94.3/89.8</td><td>65.1/60.1</td></tr><tr><td>annotator7</td><td>5-shot, temp=0.2</td><td>79.3/73.9</td><td>15.7/35.5</td><td>59.3/78.0</td><td>48.0/41.3</td><td>71.1/67.8</td><td>93.3/87.9</td><td>67.8/64.0</td></tr><tr><td>annotator8</td><td>5-shot, temp=0.7</td><td>78.9/73.5</td><td>15.0/35.3</td><td>58.9/77.6</td><td>47.1/40.2</td><td>72.0/69.1</td><td>93.2/87.8</td><td>67.6/63.8</td></tr><tr><td>annotator9</td><td>COT 1-shot, temp=0.2</td><td>79.6/74.1</td><td>16.1/32.5</td><td>36.8/47.3</td><td>48.9/43.4</td><td>63.7/61.0</td><td>94.4/89.8</td><td>64.3/58.1</td></tr><tr><td>annotator10</td><td>COT 1-shot, temp=0.7</td><td>80.2/74.6</td><td>16.2/32.7</td><td>37.8/48.9</td><td>47.5/41.3</td><td>63.7/60.8</td><td>94.7/90.2</td><td>64.6/58.4</td></tr><tr><td>annotator11</td><td>COT 5-shot, temp=0.2</td><td>79.4/73.7</td><td>16.2/37.8</td><td>65.4/83.2</td><td>46.3/42.7</td><td>70.6/67.6</td><td>92.8/87.0</td><td>68.2/65.2</td></tr><tr><td>annotator12</td><td>COT 5-shot, temp=0.7</td><td>79.6/73.8</td><td>17.0/38.4</td><td>65.2/83.0</td><td>46.0/43.1</td><td>70.9/67.8</td><td>92.9/87.0</td><td>68.4/65.5</td></tr><tr><td rowspan="12">PaLM 2</td><td>annotator1</td><td>simple prompt, temp=0.2</td><td>81.0/76.9</td><td>13.5/14.7</td><td>50.1/67.0</td><td>43.5/29.2</td><td>68.3/62.9</td><td>87.2/78.5</td><td>62.6/54.3</td></tr><tr><td>annotator2</td><td>simple prompt, temp=0.7</td><td>80.0/76.1</td><td>13.5/13.3</td><td>49.3/65.9</td><td>43.7/29.9</td><td>69.0/63.5</td><td>93.8/90.4</td><td>64.4/55.9</td></tr><tr><td>annotator3</td><td>full instruction, temp=0.2</td><td>79.3/75.5</td><td>13.2/14.0</td><td>49.3/66.2</td><td>44.2/31.3</td><td>67.7/62.1</td><td>87.0/77.9</td><td>61.9/53.6</td></tr><tr><td>annotator4</td><td>full instruction, temp=0.7</td><td>80.5/76.5</td><td>13.2/12.5</td><td>49.9/66.6</td><td>43.7/29.9</td><td>68.0/62.7</td><td>94.1/90.7</td><td>64.3/55.8</td></tr><tr><td>annotator5</td><td>1-shot, temp=0.2</td><td>86.4/81.4</td><td>13.0/33.0</td><td>48.7/64.6</td><td>42.7/29.2</td><td>67.5/63.7</td><td>90.9/84.0</td><td>66.7/60.5</td></tr><tr><td>annotator6</td><td>1-shot, temp=0.7</td><td>87.1/82.1</td><td>13.0/22.1</td><td>57.8/77.6</td><td>42.2/31.0</td><td>64.2/60.4</td><td>95.9/93.0</td><td>67.5/61.3</td></tr><tr><td>annotator7</td><td>5-shot, temp=0.2</td><td>81.3/74.9</td><td>12.4/20.2</td><td>55.4/73.3</td><td>41.4/31.3</td><td>70.6/67.2</td><td>95.2/91.9</td><td>66.1/59.4</td></tr><tr><td>annotator8</td><td>5-shot, temp=0.7</td><td>86.5/82.3</td><td>12.6/27.2</td><td>63.8/81.8</td><td>44.6/35.9</td><td>68.4/64.9</td><td>95.0/91.5</td><td>69.0/63.9</td></tr><tr><td>annotator9</td><td>COT 1-shot, temp=0.2</td><td>84.7/81.0</td><td>12.4/12.7</td><td>46.7/63.7</td><td>43.2/28.5</td><td>67.2/63.3</td><td>93.2/87.6</td><td>64.5/55.7</td></tr><tr><td>annotator10</td><td>COT 1-shot, temp=0.7</td><td>84.4/80.0</td><td>12.2/16.9</td><td>49.0/68.6</td><td>40.8/29.5</td><td>65.3/61.0</td><td>93.5/88.9</td><td>64.9/57.3</td></tr><tr><td>annotator11</td><td>COT 5-shot, temp=0.2</td><td>81.6/77.7</td><td>13.4/11.4</td><td>50.4/66.6</td><td>40.7/32.4</td><td>71.4/67.6</td><td>95.5/92.4</td><td>65.4/56.9</td></tr><tr><td>annotator12</td><td>COT 5-shot, temp=0.7</td><td>83.5/79.3</td><td>12.6/16.0</td><td>54.2/73.5</td><td>41.6/34.2</td><td>70.0/66.6</td><td>93.2/89.6</td><td>65.8/59.0</td></tr><tr><td rowspan="12">MPT Instruct</td><td>annotator1</td><td>simple prompt, temp=0.2</td><td>16.7/16.2</td><td>6.2/14.9</td><td>18.4/31.0</td><td>25.0/27.4</td><td>40.2/37.5</td><td>17.1/15.4</td><td>19.9/21.8</td></tr><tr><td>annotator2</td><td>simple prompt, temp=0.7</td><td>25.3/23.1</td><td>5.8/20.8</td><td>16.5/35.7</td><td>13.1/29.2</td><td>31.3/28.5</td><td>23.5/20.3</td><td>20.9/25.2</td></tr><tr><td>annotator3</td><td>full instruction, temp=0.2</td><td>39.2/34.8</td><td>5.4/15.2</td><td>24.2/24.7</td><td>34.0/30.2</td><td>31.8/30.1</td><td>41.8/35.1</td><td>30.3/27.3</td></tr><tr><td>annotator4</td><td>full instruction, temp=0.7</td><td>31.9/28.6</td><td>5.3/24.9</td><td>19.6/29.2</td><td>22.8/31.0</td><td>31.0/29.1</td><td>32.4/27.6</td><td>25.4/27.8</td></tr><tr><td>annotator5</td><td>1-shot, temp=0.2</td><td>25.7/24.1</td><td>5.9/7.2</td><td>21.4/29.8</td><td>29.4/22.8</td><td>16.2/15.3</td><td>17.5/16.5</td><td>18.3/18.0</td></tr><tr><td>annotator6</td><td>1-shot, temp=0.7</td><td>27.6/25.2</td><td>5.5/17.0</td><td>13.0/28.0</td><td>23.5/23.5</td><td>22.1/21.0</td><td>36.1/31.5</td><td>22.9/24.0</td></tr><tr><td>annotator7</td><td>5-shot, temp=0.2</td><td>49.5/45.9</td><td>4.4/9.4</td><td>23.1/43.5</td><td>20.5/15.7</td><td>54.3/50.1</td><td>69.5/56.9</td><td>41.6/36.5</td></tr><tr><td>annotator8</td><td>5-shot, temp=0.7</td><td>37.2/33.7</td><td>5.0/24.4</td><td>13.2/35.9</td><td>16.5/18.5</td><td>37.6/33.8</td><td>46.1/36.0</td><td>29.8/30.9</td></tr><tr><td>annotator9</td><td>COT 1-shot, temp=0.2</td><td>22.7/21.4</td><td>6.5/6.2</td><td>17.5/23.5</td><td>29.8/21.7</td><td>16.1/15.1</td><td>30.1/27.6</td><td>20.0/18.2</td></tr><tr><td>annotator10</td><td>COT 1-shot, temp=0.7</td><td>25.5/23.0</td><td>8.5/18.8</td><td>14.0/28.0</td><td>19.3/19.9</td><td>18.3/16.9</td><td>37.7/33.0</td><td>22.3/23.5</td></tr><tr><td>annotator11</td><td>COT 5-shot, temp=0.2</td><td>58.7/55.1</td><td>6.5/7.4</td><td>23.6/22.4</td><td>21.6/14.6</td><td>64.1/59.0</td><td>67.8/58.8</td><td>45.2/36.0</td></tr><tr><td>annotator12</td><td>COT 5-shot, temp=0.7</td><td>41.9/37.7</td><td>5.6/18.8</td><td>22.3/27.3</td><td>11.8/13.9</td><td>49.1/44.1</td><td>47.7/39.7</td><td>33.7/30.7</td></tr></tbody></table>

Table 7: First Run LLM Annotators: Micro-Averaged F1 Score/Accuracy

<table><tbody><tr><td colspan="10">RUN 2: Micro F1 Score/ Accuracy(%)</td></tr><tr><td rowspan="2">LLM</td><td rowspan="2">Annotator</td><td rowspan="2">Annotator Description</td><td colspan="6">Entity-Pair</td><td rowspan="2">Total</td></tr><tr><td>ORG-GPE</td><td>ORG-ORG</td><td>ORG-DATE</td><td>ORG-MONEY</td><td>PER-ORG</td><td>PER-TITLE</td></tr><tr><td rowspan="12">GPT-4</td><td>annotator1</td><td>simple prompt, temp=0.2</td><td>80.5/75.2</td><td>15.3/38.0</td><td>50.6/68.4</td><td>48.6/44.8</td><td>71.1/68.0</td><td>92.9/87.2</td><td>67.6/63.6</td></tr><tr><td>annotator2</td><td>simple prompt, temp=0.7</td><td>80.3/74.9</td><td>15.0/38.3</td><td>49.9/67.9</td><td>48.7/44.1</td><td>71.0/68.2</td><td>92.7/86.9</td><td>67.4/63.4</td></tr><tr><td>annotator3</td><td>full instruction, temp=0.2</td><td>81.3/75.9</td><td>15.4/36.6</td><td>55.9/74.4</td><td>47.4/42.0</td><td>72.3/69.5</td><td>93.5/88.4</td><td>68.4/64.5</td></tr><tr><td>annotator4</td><td>full instruction, temp=0.7</td><td>80.9/75.8</td><td>15.4/37.5</td><td>57.7/75.6</td><td>47.6/42.7</td><td>72.4/69.7</td><td>93.1/87.8</td><td>68.5/64.8</td></tr><tr><td>annotator5</td><td>1-shot, temp=0.2</td><td>79.9/74.5</td><td>14.3/29.4</td><td>48.8/66.4</td><td>47.4/42.0</td><td>62.8/60.2</td><td>94.2/89.6</td><td>65.0/60.1</td></tr><tr><td>annotator6</td><td>1-shot, temp=0.7</td><td>79.1/73.4</td><td>14.3/29.1</td><td>48.2/65.7</td><td>48.0/42.3</td><td>62.5/60.0</td><td>94.7/90.4</td><td>64.8/59.8</td></tr><tr><td>annotator7</td><td>5-shot, temp=0.2</td><td>78.5/73.5</td><td>15.9/34.9</td><td>58.2/76.9</td><td>47.6/40.2</td><td>71.1/67.8</td><td>93.4/88.1</td><td>67.4/63.5</td></tr><tr><td>annotator8</td><td>5-shot, temp=0.7</td><td>79.7/74.4</td><td>15.0/35.2</td><td>58.9/77.6</td><td>48.0/41.3</td><td>71.7/68.2</td><td>93.2/87.8</td><td>67.8/64.0</td></tr><tr><td>annotator9</td><td>COT 1-shot, temp=0.2</td><td>80.4/74.8</td><td>16.4/32.9</td><td>37.3/48.0</td><td>48.3/43.1</td><td>64.7/61.9</td><td>94.5/89.9</td><td>64.7/58.6</td></tr><tr><td>annotator10</td><td>COT 1-shot, temp=0.7</td><td>80.2/74.8</td><td>16.3/32.2</td><td>36.4/46.9</td><td>47.2/41.6</td><td>65.5/62.9</td><td>94.5/89.9</td><td>64.6/58.3</td></tr><tr><td>annotator11</td><td>COT 5-shot, temp=0.2</td><td>79.9/74.5</td><td>16.6/37.7</td><td>65.2/83.0</td><td>47.0/43.1</td><td>71.3/68.2</td><td>92.9/87.0</td><td>68.5/65.5</td></tr><tr><td>annotator12</td><td>COT 5-shot, temp=0.7</td><td>80.2/74.5</td><td>16.5/37.9</td><td>64.9/82.9</td><td>46.8/42.7</td><td>70.7/67.4</td><td>92.9/87.0</td><td>68.4/65.3</td></tr><tr><td rowspan="12">PaLM 2</td><td>annotator1</td><td>simple prompt, temp=0.2</td><td>80.1/75.9</td><td>14.0/14.1</td><td>49.7/67.0</td><td>43.5/29.2</td><td>66.9/60.8</td><td>87.0/77.7</td><td>62.0/53.5</td></tr><tr><td>annotator2</td><td>simple prompt, temp=0.7</td><td>80.6/76.6</td><td>13.8/13.8</td><td>48.4/65.3</td><td>43.9/30.6</td><td>67.8/61.9</td><td>94.1/91.1</td><td>64.5/56.0</td></tr><tr><td>annotator3</td><td>full instruction, temp=0.2</td><td>80.2/76.3</td><td>13.6/13.8</td><td>49.6/66.2</td><td>43.9/30.6</td><td>69.1/63.7</td><td>87.1/78.0</td><td>62.4/53.9</td></tr><tr><td>annotator4</td><td>full instruction, temp=0.7</td><td>79.9/75.8</td><td>14.1/14.7</td><td>49.5/66.1</td><td>43.6/29.5</td><td>68.5/63.1</td><td>94.1/91.0</td><td>64.5/56.2</td></tr><tr><td>annotator5</td><td>1-shot, temp=0.2</td><td>86.1/81.0</td><td>13.1/31.7</td><td>47.3/63.0</td><td>42.5/28.5</td><td>67.2/63.3</td><td>90.3/83.1</td><td>66.1/59.6</td></tr><tr><td>annotator6</td><td>1-shot, temp=0.7</td><td>87.4/82.0</td><td>13.1/21.8</td><td>55.3/74.7</td><td>42.2/29.9</td><td>63.5/60.0</td><td>95.7/92.2</td><td>67.1/60.4</td></tr><tr><td>annotator7</td><td>5-shot, temp=0.2</td><td>82.1/75.8</td><td>11.8/18.3</td><td>56.1/74.0</td><td>41.6/32.7</td><td>69.6/66.4</td><td>94.4/90.5</td><td>65.8/59.0</td></tr><tr><td>annotator8</td><td>5-shot, temp=0.7</td><td>86.0/81.8</td><td>13.3/27.3</td><td>64.3/82.1</td><td>43.2/35.9</td><td>68.5/65.4</td><td>93.6/89.3</td><td>68.4/63.6</td></tr><tr><td>annotator9</td><td>COT 1-shot, temp=0.2</td><td>84.7/81.0</td><td>12.5/12.8</td><td>47.4/65.2</td><td>43.3/28.8</td><td>68.7/64.7</td><td>92.7/87.0</td><td>64.8/56.1</td></tr><tr><td>annotator10</td><td>COT 1-shot, temp=0.7</td><td>84.6/80.1</td><td>11.7/16.3</td><td>49.1/68.6</td><td>41.1/29.2</td><td>65.5/61.9</td><td>94.0/89.8</td><td>64.9/57.5</td></tr><tr><td>annotator11</td><td>COT 5-shot, temp=0.2</td><td>82.4/78.6</td><td>13.3/11.8</td><td>50.7/67.0</td><td>43.2/35.2</td><td>71.5/67.8</td><td>95.1/92.1</td><td>65.8/57.5</td></tr><tr><td>annotator12</td><td>COT 5-shot, temp=0.7</td><td>82.4/78.2</td><td>14.1/17.6</td><td>54.5/74.2</td><td>41.5/32.4</td><td>69.0/65.6</td><td>94.6/91.6</td><td>66.1/59.4</td></tr><tr><td rowspan="12">MPT Instruct</td><td>annotator1</td><td>simple prompt, temp=0.2</td><td>17.7/17.0</td><td>6.5/15.8</td><td>17.7/31.2</td><td>25.2/26.0</td><td>40.4/37.5</td><td>16.7/14.7</td><td>20.1/21.9</td></tr><tr><td>annotator2</td><td>simple prompt, temp=0.7</td><td>21.0/20.3</td><td>6.4/20.0</td><td>15.1/34.7</td><td>15.1/22.4</td><td>33.2/30.5</td><td>25.5/21.7</td><td>20.6/24.2</td></tr><tr><td>annotator3</td><td>full instruction, temp=0.2</td><td>42.2/38.0</td><td>7.2/13.9</td><td>24.0/24.2</td><td>31.2/28.5</td><td>32.9/30.7</td><td>44.7/37.4</td><td>31.9/27.9</td></tr><tr><td>annotator4</td><td>full instruction, temp=0.7</td><td>31.4/28.3</td><td>5.2/23.3</td><td>19.0/31.8</td><td>18.2/27.0</td><td>26.9/24.9</td><td>33.0/26.9</td><td>24.2/26.8</td></tr><tr><td>annotator5</td><td>1-shot, temp=0.2</td><td>28.2/25.9</td><td>4.7/5.7</td><td>21.5/29.6</td><td>33.4/23.1</td><td>16.3/15.3</td><td>17.3/16.5</td><td>18.9/18.0</td></tr><tr><td>annotator6</td><td>1-shot, temp=0.7</td><td>28.7/26.1</td><td>5.3/17.5</td><td>16.3/29.6</td><td>25.6/27.8</td><td>19.1/19.4</td><td>33.2/29.3</td><td>22.4/24.3</td></tr><tr><td>annotator7</td><td>5-shot, temp=0.2</td><td>54.9/51.1</td><td>4.5/7.3</td><td>22.6/38.3</td><td>18.8/14.6</td><td>55.4/52.2</td><td>71.1/59.8</td><td>43.3/36.9</td></tr><tr><td>annotator8</td><td>5-shot, temp=0.7</td><td>41.1/36.3</td><td>4.4/21.7</td><td>13.0/35.9</td><td>16.2/17.1</td><td>34.3/31.1</td><td>50.2/41.7</td><td>31.1/31.3</td></tr><tr><td>annotator9</td><td>COT 1-shot, temp=0.2</td><td>24.1/22.4</td><td>7.8/8.5</td><td>17.1/24.0</td><td>31.2/22.1</td><td>15.0/14.2</td><td>28.4/26.3</td><td>20.1/18.7</td></tr><tr><td>annotator10</td><td>COT 1-shot, temp=0.7</td><td>28.3/26.6</td><td>7.0/16.1</td><td>11.5/25.3</td><td>19.8/21.0</td><td>17.0/16.9</td><td>37.1/31.8</td><td>22.1/22.9</td></tr><tr><td>annotator11</td><td>COT 5-shot, temp=0.2</td><td>58.8/55.5</td><td>6.0/8.0</td><td>25.4/23.5</td><td>20.1/13.9</td><td>61.2/56.3</td><td>68.6/59.7</td><td>45.2/36.1</td></tr><tr><td>annotator12</td><td>COT 5-shot, temp=0.7</td><td>45.5/40.8</td><td>4.3/15.3</td><td>15.9/26.9</td><td>21.0/22.1</td><td>46.2/42.1</td><td>48.2/40.6</td><td>34.0/30.9</td></tr></tbody></table>

Table 8: LLM Annotators: Micro-average F1-Score / Accuracy for second run

### Statistical Tests

<table><tbody><tr><td colspan="4">Are Difference Statistically significant at alpha = 0.05?</td></tr><tr><td>Null Hypothesis</td><td>LLM</td><td>Micro-Averaged F1 ScoresP-values</td><td>AccuracyP-values</td></tr><tr><td rowspan="3">Ho:There is no significant difference in metric when we change temperature setting i.e. Ho: metrics at temp0.2 =metrics at temp0.7</td><td>GPT-4</td><td>0.950</td><td>0.975</td></tr><tr><td>PaLM 2</td><td>0.053</td><td>0.062</td></tr><tr><td>MPT Instruct</td><td>0.481</td><td>0.734</td></tr><tr><td rowspan="3">Ho:At temperature setting = 0.2, there is no significant difference in metric when we compare run1 and run2 i.e. Ho: metrics at temp0.2_first_run =metrics at temp0.2_second_run</td><td>GPT-4</td><td>0.935</td><td>0.959</td></tr><tr><td>PaLM 2</td><td>0.964</td><td>0.932</td></tr><tr><td>MPT Instruct</td><td>0.921</td><td>0.954</td></tr><tr><td rowspan="3">Ho:At temperature setting = 0.7, there is no significant difference in metric when we compare run1 and run2 i.e. Ho: metrics at temp0.7_first_run =metrics at temp0.7_second_run</td><td>GPT-4</td><td>0.973</td><td>0.976</td></tr><tr><td>PaLM 2</td><td>0.948</td><td>0.992</td></tr><tr><td>MPT Instruct</td><td>0.974</td><td>0.889</td></tr><tr><td rowspan="3">Ho:There is no significant difference when we compare average metrics across first run and second for the different temperature setting i.e Ho: avg_metric at temp0.2 =avg_metric at temp0.7</td><td>GPT-4</td><td>0.967</td><td>0.983</td></tr><tr><td>PaLM 2</td><td>0.195</td><td>0.213</td></tr><tr><td>MPT Instruct</td><td>0.493</td><td>0.909</td></tr><tr><td rowspan="3">Ho:There is no significant difference between LLM metrics when we compare one to the other. i.e Ho: LLM1 avg_metric at temp 0.2 = LLM2 avg_metric at temp 0.2</td><td>GPT-4-vs-PaLM 2</td><td>0.055</td><td>0.004*</td></tr><tr><td>GPT-4-vs-MPT Instruct</td><td>0.000*</td><td>0.000*</td></tr><tr><td>PaLM 2-vs-MPT Instruct</td><td>0.000*</td><td>0.000*</td></tr></tbody></table>

Table 9: Statistical Significance of Metric Difference: At alpha = 0.05, we test if the difference captured are statistical significant. For these hypotheses, we either reject or fail to reject the null hypothesis.

### Inter Annotator Agreement

<table><tbody><tr><td></td><td></td><td colspan="3">Inter annotator agreement (IAA)</td></tr><tr><td>What we measure</td><td>Prompt Type</td><td>GPT-4</td><td>PaLM 2</td><td>MPT Instruct</td></tr><tr><td></td><td>simple_prompt, temp = 0.2</td><td>[HTML]FFFFFF0.96</td><td>[HTML]FFFFFF0.88</td><td>[HTML]FFFFFF0.62</td></tr><tr><td></td><td>simple_prompt, temp = 0.7</td><td>0.94</td><td>0.89</td><td>0.19</td></tr><tr><td></td><td>full_instructn_prompt, temp = 0.2</td><td>0.97</td><td>0.87</td><td>0.67</td></tr><tr><td></td><td>full_instructn_prompt, temp = 0.7</td><td>0.94</td><td>0.89</td><td>0.23</td></tr><tr><td></td><td>1shot_prompt, temp = 0.2</td><td>0.96</td><td>0.91</td><td>0.55</td></tr><tr><td></td><td>1shot_prompt, temp = 0.7</td><td>0.95</td><td>0.86</td><td>0.2</td></tr><tr><td></td><td>5shot_prompt, temp = 0.2</td><td>0.96</td><td>0.92</td><td>0.51</td></tr><tr><td></td><td>5shot_prompt, temp = 0.7</td><td>0.95</td><td>0.86</td><td>0.19</td></tr><tr><td></td><td>cot 1shot_prompt, temp = 0.2</td><td>0.95</td><td>0.94</td><td>0.53</td></tr><tr><td></td><td>cot 1shot_prompt, temp = 0.7</td><td>[HTML]FFFFFF0.93</td><td>0.84</td><td>0.22</td></tr><tr><td></td><td>cot 5shot_prompt, temp = 0.2</td><td>[HTML]FFFFFF0.97</td><td>0.93</td><td>0.6</td></tr><tr><td>Same Prompt at same temperature setting (run twice).Using Cohen Kappa</td><td>cot 5shot_prompt, temp = 0.7</td><td>[HTML]FFFFFF0.96</td><td>0.82</td><td>0.23</td></tr><tr><td></td><td>simple_prompt</td><td>[HTML]FFFFFF0.94</td><td>0.87</td><td>0.3</td></tr><tr><td></td><td>full_instructn_prompt</td><td>[HTML]FFFFFF0.95</td><td>[HTML]FFFFFF0.86</td><td>[HTML]FFFFFF0.34</td></tr><tr><td></td><td>1shot_prompt</td><td>[HTML]FFFFFF0.95</td><td>[HTML]FFFFFF0.82</td><td>[HTML]FFFFFF0.27</td></tr><tr><td></td><td>5shot_prompt</td><td>[HTML]FFFFFF0.96</td><td>[HTML]FFFFFF0.84</td><td>[HTML]FFFFFF0.26</td></tr><tr><td></td><td>cot1shot_prompt</td><td>0.95</td><td>0.85</td><td>0.28</td></tr><tr><td>Same Prompt at different temperature setting (0.2 and 0.7) for only run 1. Using Cohen Kappa</td><td>cot5shot_prompt</td><td>0.96</td><td>0.83</td><td>0.34</td></tr><tr><td></td><td>simple_prompt</td><td>0.95</td><td>0.87</td><td>0.34</td></tr><tr><td></td><td>full_instructn_prompt</td><td>0.95</td><td>0.87</td><td>0.37</td></tr><tr><td></td><td>1shot_prompt</td><td>0.95</td><td>0.84</td><td>0.31</td></tr><tr><td></td><td>5shot_prompt</td><td>0.96</td><td>0.86</td><td>0.3</td></tr><tr><td></td><td>cot1shot_prompt</td><td>0.94</td><td>0.86</td><td>0.31</td></tr><tr><td>Same Prompt at different temperature setting (run twice). Using Fleiss Kappa</td><td>cot5shot_prompt</td><td>0.96</td><td>0.85</td><td>0.36</td></tr><tr><td></td><td>zero shot: simple_vs_full_instruction</td><td>[HTML]FFFFFF0.87</td><td>[HTML]FFFFFF0.88</td><td>[HTML]FFFFFF0.39</td></tr><tr><td></td><td>few shot: 1_shot_vs_5_shot</td><td>[HTML]FFFFFF0.84</td><td>[HTML]FFFFFF0.79</td><td>[HTML]FFFFFF0.28</td></tr><tr><td>Compare prompts within prompt types. Using Cohen Kappa</td><td>cot few shot: cot_1_shot_vs_cot_5_shot</td><td>[HTML]FFFFFF0.8</td><td>[HTML]FFFFFF0.82</td><td>[HTML]FFFFFF0.28</td></tr><tr><td>Compare among prompt types. Using Fleiss Kappa</td><td>simple_vs_full_instruction_1_shot_vs_5shot_vs_cot_1_shot_vs_cot_5_shot</td><td>[HTML]FFFFFF0.83</td><td>[HTML]FFFFFF0.79</td><td>[HTML]FFFFFF0.31</td></tr></tbody></table>

Table 10: LLM Inter Annotator Agreement: This table shows how consistent outputs from each LLMs are within and accross prompt types and within and accross different temperature settings.

![Refer to caption](https://arxiv.org/html/2403.18152v1/extracted/2403.18152v1/Figs/IAA_plot.png)

Figure 9: Plots from Inter Annotator Agreement scores

### Error Analysis

| Entity Pair | Scenario 1:Crowd workers = Wrong Answer, LLMs = Correct Answer | Scenario 2:Crowd workers = Wrong Answer, LLMs = Wrong Answer | Scenario 3:Crowd workers = Correct Answer, LLMs = Wrong Answer |
| --- | --- | --- | --- |
| ORG-GPE | Properties Atlas Financial Holdings, Inc.corporate headquarters is locatedat 150 Northwest Point Boulevard, Elk Grove Village, Illinois 60007, USA.Expert Label:Headquartered in Crowd worker Label: Operations in LLMs Label:Headquartered in | Our eWellness Corporate Office is located in Culver City, California. eWELLNESSExpert Label: Operations in Crowd worker Label: Formed in LLMs Label: Headquartered in | This Settlement Agreement ( ” Agreement ” ) is made effectivethis 20th day of May, 2015 by and betweenActiveCare, Inc, a Delaware corporation ( the ” Company ” ), and Advance Technology Investors, LLC ( ” ATI ” ).Expert Label:Operations in Crowd worker Label: Operations in LLMs Label: No/Other Relation, Formed in |
| ORG-ORG | Michael D. Huddy, President / CEO and Director, joined INTERNATIONAL BARRIER TECHNOLOGY INC inFebruary 1993 as President of the newly - formedUS Subsidiary, Barrier Technology Corporation.Expert Label:Subsidiary of Crowd worker Label: No/Other Relation, Shares of LLMs Label: Subsidiary of | Our Hawaii Gas entered into licensing agreements withUtility Service Partners, Inc. and America’s Water HeaterRentals, LLC, both indirect subsidiaries of Macquarie Group Limited, to enable these entitiesto offer products and services to Hawaii Gas’s customer baseExpert Label:Subsidiary of Crowd worker Label: No/Other Relation, Subsidiary of, Shares of LLMs Label: Agreement with | On December 10, 2014, Orbital Tracking Corp. purchasedcertain contracts from Global Telesat Corp,a Virginia corporation ( GTC )for $ 250,000 pursuant to an asset purchase agreement by and amongOrbital Tracking Corp i, its wholly owned subsidiary Orbital Satcom, GTC and World Surveillance Group, Inc. ( World ), GTC’s parentExpert Label: Subsidiary of Crowd worker Label: Subsidiary of LLMs Label: Agreement with |
| ORG-DATE | Wishbone Pet Products Inc. was incorporated in theState of Nevada on July 30, 2009. Expert Label: Formed on Crowd worker Label: No/Other Relation LLMs Label: Formed on | None | None |
| ORG-MONEY | Personal Lines underwriting profit for thethree months ended September 30, 2017was $40.8 million, compared to $23.3million for the three months endedSeptember 30,2016, an improvementof $17.5 million.Expert Label: Profit of Crowd worker Label: No/Other Relation, Loss of LLMs Label: Profit of | None | None |
| PERS-ORG | Mr. Untermeyer also serves as senior program managerwith Southwest Research institute, San AntonioExpert Label: Employee of Crowd worker Label: Founder of, Member of LLMs Label: Employee of | Currently, Mr. Morrison serves on the board of directorsof the Texas AM university, kingsville foundationand the Rockport center for the arts.Expert Label: Employee of Crowd worker Label: Founder of, Member of LLMs Label: Member of | From September 2012 through June 2015, Mr. Kimmel has alsoserved on the board of directors of Electronic Magnetic PowerSolutions, which implements disruptive patented technologylicensed from Virginia Tech University for the express purposeof alternative energy use in the consumer space.Expert Label: Employee of Crowd worker Label: Employee of LLMs Label: Member of, No/Other Relation |
| PERS-TITLE | Information regarding Harel Gadot, Microbot Medical Inc. Chairman, President and Chief Executive Officer, is setforth above under Board of Directors.Expert Label:Title Crowd worker Label: No/Other Relation LLMs Label:Title | None | Yvonne should contact her manager,segment or region leader, or FTI Consulting sChief Ethics and Compliance Officer to discuss the gift.Expert Label: Title Crowd worker Label: Title LLMs Label: No/Other Relation |

Table 11: Qualitative Examples from our Error Analysis depicting the 3 prominent scenarios of how MTurk Crowd workers and LLMs demonstrated high confidence on answer choice

![[Uncaptioned image]](https://arxiv.org/html/2403.18152v1/extracted/2403.18152v1/Figs/ZS_CM_GPT.png)

Figure 10: Confusion Matrix for GPT-4 Zero Shot Prompt

![Refer to caption](https://arxiv.org/html/2403.18152v1/extracted/2403.18152v1/Figs/FS_CM_GPT.png)

Figure 11: Confusion Matrix for GPT-4 Few Shot Prompt

![Refer to caption](https://arxiv.org/html/2403.18152v1/extracted/2403.18152v1/Figs/CoT_CM_GPT.png)

Figure 12: Confusion Matrix for GPT-4 Few Shot CoT Prompt

[^1]: Alizadeh, M.; Gilardi, F.; Hoes, E.; Klüser, K. J.; Kubli, M.; and Marchal, N. 2022. Content Moderation As a Political Issue: The Twitter Discourse Around Trump’s Ban. *Journal of Quantitative Description: Digital Media*, 2.

[^2]: Alkhalifa, R.; Kochkina, E.; and Zubiaga, A. 2021. Opinions are made to be changed: Temporally adaptive stance classification. In *Proceedings of the 2021 workshop on open challenges in online social networks*, 27–32.

[^3]: Alkhalifa, R.; Kochkina, E.; and Zubiaga, A. 2023. Building for tomorrow: Assessing the temporal persistence of text classifiers. *Information Processing & Management*, 60(2): 103200.

[^4]: Anil, R.; Dai, A. M.; Firat, O.; Johnson, M.; Lepikhin, D.; Passos, A.; Shakeri, S.; Taropa, E.; Bailey, P.; Chen, Z.; et al. 2023. Palm 2 technical report. *arXiv preprint arXiv:2305.10403*.

[^5]: Brown, T. B.; Mann, B.; Ryder, N.; Subbiah, M.; Kaplan, J.; Dhariwal, P.; Neelakantan, A.; Shyam, P.; Sastry, G.; Askell, A.; Agarwal, S.; Herbert-Voss, A.; Krueger, G.; Henighan, T.; Child, R.; Ramesh, A.; Ziegler, D. M.; Wu, J.; Winter, C.; Hesse, C.; Chen, M.; Sigler, E.; Litwin, M.; Gray, S.; Chess, B.; Clark, J.; Berner, C.; McCandlish, S.; Radford, A.; Sutskever, I.; and Amodei, D. 2020. Language Models Are Few-Shot Learners. In *Proceedings of the 34th International Conference on Neural Information Processing Systems*, NIPS’20. Red Hook, NY, USA: Curran Associates Inc. ISBN 9781713829546.

[^6]: Chiang, C.-H.; and Lee, H.-y. 2023. Can Large Language Models Be an Alternative to Human Evaluations? In Rogers, A.; Boyd-Graber, J.; and Okazaki, N., eds., *Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, 15607–15631. Toronto, Canada: Association for Computational Linguistics.

[^7]: Clark, C.; Lee, K.; Chang, M.-W.; Kwiatkowski, T.; Collins, M.; and Toutanova, K. 2019. BoolQ: Exploring the Surprising Difficulty of Natural Yes/No Questions. In *Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers)*, 2924–2936. Minneapolis, Minnesota: Association for Computational Linguistics.

[^8]: Cohen, J. 1960a. A coefficient of agreement for nominal scales. *Educational and psychological measurement*, 20(1): 37–46.

[^9]: Cohen, J. 1960b. A Coefficient of Agreement for Nominal Scales. Educational and Psychological Measurement, 20(1), 37–46. Accessed: 2023-07-24.

[^10]: Ding, B.; Qin, C.; Liu, L.; Chia, Y. K.; Li, B.; Joty, S.; and Bing, L. 2023. Is GPT-3 a Good Data Annotator? In Rogers, A.; Boyd-Graber, J.; and Okazaki, N., eds., *Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, 11173–11195. Toronto, Canada: Association for Computational Linguistics.

[^11]: ElSherief, M.; Ziems, C.; Muchlinski, D.; Anupindi, V.; Seybolt, J.; De Choudhury, M.; and Yang, D. 2021. Latent Hatred: A Benchmark for Understanding Implicit Hate Speech. In *Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing*, 345–363.

[^12]: Fan, A.; Lewis, M.; and Dauphin, Y. 2018. Hierarchical Neural Story Generation. In *Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, 889–898.

[^13]: Fleiss, J. L. 1971. Measuring nominal scale agreement among many raters. *Psychological bulletin*, 76(5): 378.

[^14]: Gilardi, F.; Alizadeh, M.; and Kubli, M. 2023. ChatGPT outperforms crowd workers for text-annotation tasks. *Proceedings of the National Academy of Sciences*, 120(30): e2305016120.

[^15]: He, X.; Lin, Z.; Gong, Y.; Jin, A.-L.; Zhang, H.; Lin, C.; Jiao, J.; Yiu, S. M.; Duan, N.; and Chen, W. 2023. AnnoLLM: Making Large Language Models to Be Better Crowdsourced Annotators. arXiv:2303.16854.

[^16]: Huang, F.; Kwak, H.; and An, J. 2023. Is ChatGPT Better than Human Annotators? Potential and Limitations of ChatGPT in Explaining Implicit Hate Speech. In *Companion Proceedings of the ACM Web Conference 2023*, WWW ’23 Companion, 294–297. New York, NY, USA: Association for Computing Machinery. ISBN 9781450394192.

[^17]: Kaur, S.; Smiley, C.; Gupta, A.; Sain, J.; Wang, D.; Siddagangappa, S.; Aguda, T.; and Shah, S. 2023. REFinD: Relation Extraction Financial Dataset. SIGIR ’23. Taipei, Taiwan: Association for Computing Machinery.

[^18]: Kuzman, T.; Ljubešić, N.; and Mozetič, I. 2023. ChatGPT: Beginning of an End of Manual Annotation? Use Case of Automatic Genre Identification.

[^19]: Li, X.; Chan, S.; Zhu, X.; Pei, Y.; Ma, Z.; Liu, X.; and Shah, S. 2023. Are ChatGPT and GPT-4 General-Purpose Solvers for Financial Text Analytics? A Study on Several Typical Tasks. In Wang, M.; and Zitouni, I., eds., *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing: Industry Track*, 408–422. Singapore: Association for Computational Linguistics.

[^20]: Liu, N.; Lee, T.; Jia, R.; and Liang, P. 2021. Can Small and Synthetic Benchmarks Drive Modeling Innovation? A Retrospective Study of Question Answering Modeling Approaches.

[^21]: MosaicML, N. 2023. Introducing MPT-7B: A New Standard for Open-Source, Commercially Usable LLMs.

[^22]: OpenAI. 2023. GPT-4 Technical Report. *ArXiv*, abs/2303.08774.

[^23]: Ouyang, L.; Wu, J.; Jiang, X.; Almeida, D.; Wainwright, C.; Mishkin, P.; Zhang, C.; Agarwal, S.; Slama, K.; Ray, A.; et al. 2022. Training language models to follow instructions with human feedback. *Advances in Neural Information Processing Systems*, 35: 27730–27744.

[^24]: Pan, A.; Chan, J. S.; Zou, A.; Li, N.; Basart, S.; Woodside, T.; Zhang, H.; Emmons, S.; and Hendrycks, D. 2023. Do the Rewards Justify the Means? Measuring Trade-Offs Between Rewards and Ethical Behavior in the Machiavelli Benchmark. In Krause, A.; Brunskill, E.; Cho, K.; Engelhardt, B.; Sabato, S.; and Scarlett, J., eds., *Proceedings of the 40th International Conference on Machine Learning*, volume 202 of *Proceedings of Machine Learning Research*, 26837–26867. PMLR.

[^25]: Pilehvar, M. T.; and Camacho-Collados, J. 2019. WiC: the Word-in-Context Dataset for Evaluating Context-Sensitive Meaning Representations. In *Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers)*, 1267–1273. Minneapolis, Minnesota: Association for Computational Linguistics.

[^26]: Plank, B. 2022. The “Problem” of Human Label Variation: On Ground Truth in Data, Modeling and Evaluation. In Goldberg, Y.; Kozareva, Z.; and Zhang, Y., eds., *Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing*, 10671–10682. Abu Dhabi, United Arab Emirates: Association for Computational Linguistics.

[^27]: Reiss, M. V. 2023. Testing the Reliability of ChatGPT for Text Annotation and Classification: A Cautionary Remark. *arXiv preprint arXiv:2304.11085*.

[^28]: Sharma, S.; Nayak, T.; Bose, A.; Meena, A. K.; Dasgupta, K.; Ganguly, N.; and Goyal, P. 2022. FinRED: A dataset for relation extraction in financial domain. In *Companion Proceedings of the Web Conference 2022*, 595–597.

[^29]: Son, G.; Jung, H.; Hahm, M.; Na, K.; and Jin, S. 2023. Beyond Classification: Financial Reasoning in State-of-the-Art Language Models. In Chen, C.-C.; Takamura, H.; Mathur, P.; Sawhney, R.; Huang, H.-H.; and Chen, H.-H., eds., *Proceedings of the Fifth Workshop on Financial Technology and Natural Language Processing and the Second Multimodal AI For Financial Forecasting*, 34–44. Macao: -.

[^30]: Törnberg, P. 2023. ChatGPT-4 Outperforms Experts and Crowd Workers in Annotating Political Twitter Messages with Zero-Shot Learning. *arXiv preprint arXiv:2304.06588*.

[^31]: Van Vliet, L.; Törnberg, P.; and Uitermark, J. 2020. The Twitter parliamentarian database: Analyzing Twitter politics across 26 countries. *PLoS one*, 15(9): e0237073.

[^32]: Wang, S.; Liu, Y.; Xu, Y.; Zhu, C.; and Zeng, M. 2021. Want To Reduce Labeling Cost? GPT-3 Can Help. In *Findings of the Association for Computational Linguistics: EMNLP 2021*, 4195–4205. Punta Cana, Dominican Republic: Association for Computational Linguistics.

[^33]: Wei, J.; Wang, X.; Schuurmans, D.; Bosma, M.; Xia, F.; Chi, E.; Le, Q. V.; Zhou, D.; et al. 2022. Chain-of-thought prompting elicits reasoning in large language models. *Advances in Neural Information Processing Systems*, 35: 24824–24837.

[^34]: Zhu, Y.; Zhang, P.; Haq, E.-U.; Hui, P.; and Tyson, G. 2023. Can ChatGPT Reproduce Human-Generated Labels? A Study of Social Computing Tasks. *arXiv preprint arXiv:2304.10145*.
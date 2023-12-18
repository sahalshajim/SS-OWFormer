# SS-OWFormer : Semi-Supervised Open-World Object Detection (AAAI24)

![](https://i.imgur.com/waxVImv.png)

[Sahal Shaji Mullappilly](https://scholar.google.com/citations?user=LJWxVpUAAAAJ&hl=en), [Abhishek Singh Gehlot](https://scholar.google.com/citations?view_op=list_works&hl=en&hl=en&user=wyEeF60AAAAJ), [Rao Muhammad Anwer](https://scholar.google.com/citations?hl=en&authuser=1&user=_KlvMVoAAAAJ), [Fahad Shahbaz Khan](https://scholar.google.es/citations?user=zvaeYnUAAAAJ&hl=en), [Hisham Cholakkal](https://scholar.google.com/citations?hl=en&user=bZ3YBRcAAAAJ).


**Mohamed bin Zayed University of Artificial Intelligence, UAE**

## :rocket: News
<hr>

+ Dec-9 : Accepted to AAAI 2024 (Main Track)

## Introduction

Conventional open-world object detection (OWOD) problem setting first distinguishes known and unknown classes and then later incrementally learns the unknown objects when introduced with labels in the subsequent tasks. However, the current OWOD formulation heavily relies on the external human oracle for knowledge input during the incremental learning stages. Such reliance on run-time makes this formulation less realistic in a real-world deployment. To address this, we introduce a more realistic formulation, named semi-supervised open-world detection (SS-OWOD), that reduces the annotation cost by casting the incremental learning stages of OWOD in a semi-supervised manner. We demonstrate that the performance of the state-of-the-art OWOD detector dramatically deteriorates in the proposed SS-OWOD setting. Therefore, we introduce a novel SS-OWOD detector, named SS-OWFormer, that utilizes a feature-alignment scheme to better align the object query representations between the original and  augmented images to leverage the large unlabeled and few labeled data. We further introduce a pseudo-labeling scheme for unknown detection that exploits the inherent capability of decoder object queries to capture object-specific information. On the COCO dataset, our SS-OWFormer using only 50% of the labeled data achieves detection performance that is on par with the state-of-the-art (SOTA) OWOD detector using all the 100% of labeled data. Further, our SS-OWFormer achieves an absolute gain of 4.8% in unknown recall over the SOTA OWOD detector. Lastly, we demonstrate the effectiveness of our SS-OWOD problem setting and approach for remote sensing object detection, proposing carefully curated splits and baseline performance evaluations. Our experiments on 4 datasets including MS COCO, PASCAL, Objects365 and DOTA demonstrate the effectiveness of our approach.

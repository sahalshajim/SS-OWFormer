# SS-OWFormer : Semi-Supervised Open-World Object Detection (AAAI24)

![](https://i.imgur.com/waxVImv.png)

[Sahal Shaji Mullappilly](https://scholar.google.com/citations?user=LJWxVpUAAAAJ&hl=en), [Abhishek Singh Gehlot](https://scholar.google.com/citations?view_op=list_works&hl=en&hl=en&user=wyEeF60AAAAJ), [Rao Muhammad Anwer](https://scholar.google.com/citations?hl=en&authuser=1&user=_KlvMVoAAAAJ), [Fahad Shahbaz Khan](https://scholar.google.es/citations?user=zvaeYnUAAAAJ&hl=en), [Hisham Cholakkal](https://scholar.google.com/citations?hl=en&user=bZ3YBRcAAAAJ).


**Mohamed bin Zayed University of Artificial Intelligence, UAE**

## :rocket: News
<hr>

+ Dec-9 : Accepted to AAAI 2024 (Main Track)

## Introduction

Conventional open-world object detection (OWOD) problem setting first distinguishes known and unknown classes and then later incrementally learns the unknown objects when introduced with labels in the subsequent tasks. However, the current OWOD formulation heavily relies on the external human oracle for knowledge input during the incremental learning stages. Such reliance on run-time makes this formulation less realistic in a real-world deployment. To address this, we introduce a more realistic formulation, named semi-supervised open-world detection (SS-OWOD), that reduces the annotation cost by casting the incremental learning stages of OWOD in a semi-supervised manner. We demonstrate that the performance of the state-of-the-art OWOD detector dramatically deteriorates in the proposed SS-OWOD setting. Therefore, we introduce a novel SS-OWOD detector, named SS-OWFormer, that utilizes a feature-alignment scheme to better align the object query representations between the original and augmented images to leverage the large unlabeled and few labeled data. We further introduce a pseudo-labeling scheme for unknown detection that exploits the inherent capability of decoder object queries to capture object-specific information. On the COCO dataset, our SS-OWFormer using only 50% of the labeled data achieves detection performance that is on par with the state-of-the-art (SOTA) OWOD detector using all the 100% of labeled data. Further, our SS-OWFormer achieves an absolute gain of 4.8% in unknown recall over the SOTA OWOD detector. Lastly, we demonstrate the effectiveness of our SS-OWOD problem setting and approach for remote sensing object detection, proposing carefully curated splits and baseline performance evaluations. Our experiments on 4 datasets including MS COCO, PASCAL, Objects365 and DOTA demonstrate the effectiveness of our approach.
<p align="center" ><img width='450' src = "https://i.imgur.com/FTo8iMT.png"></p> 

<p align="center" ><img width='900' src = "https://i.imgur.com/bp1ET4Q.png"></p> 

## Getting Started
### Installation

```bash
conda create -n ssowod python=3.7 pip
conda activate ssowod
conda install pytorch==1.8.0 torchvision==0.9.0 torchaudio==0.8.0 cudatoolkit=10.2 -c pytorch
pip install -r requirements.txt
```
### Compiling CUDA operators
```bash
cd ./models/ops
sh ./make.sh
# unit test (should see all checking is True)
python test.py
```

## Experimental Results
### SS-OWOD Results on OWOD Splits

<table align="center">
<thead>
  <tr>
    <th rowspan="2">Method</th>
    <th colspan="2">Task2</th>
    <th colspan="2">Task3</th>
    <th>Task4</th>
  </tr>
  <tr>
    <th>U-Recall</th>
    <th>mAP</th>
    <th>U-Recall</th>
    <th>mAP</th>
    <th>mAP</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>ORE-EBUI</td>
    <td>2.9</td>
    <td>39.4</td>
    <td>3.9</td>
    <td>29.7</td>
    <td>25.3</td>
  </tr>
  <tr>
    <td>OW-DETR</td>
    <td>6.2</td>
    <td>42.9</td>
    <td>5.7</td>
    <td>30.8</td>
    <td>27.8</td>
  </tr>
  <tr>
    <td>OW-DETR (50%)</td>
    <td>6.94</td>
    <td>34.91</td>
    <td>7.64</td>
    <td>24.85</td>
    <td>19.49</td>
  </tr>
  <tr>
    <td>SS-OWFormer (50%)</td>
    <td>10.56</td>
    <td>39.2</td>
    <td>13.16</td>
    <td>30.85</td>
    <td>25.35</td>
  </tr>
  <tr>
    <td>OW-DETR (25%)</td>
    <td>5.03</td>
    <td>32.42</td>
    <td>6.94</td>
    <td>23.72</td>
    <td>18.77</td>
  </tr>
  <tr>
    <td>SS-OWFormer (25%)</td>
    <td>10.47</td>
    <td>36.68</td>
    <td>12.22</td>
    <td>27.87</td>
    <td>22.36</td>
  </tr>
  <tr>
    <td>OW-DETR (10%)</td>
    <td>4.83</td>
    <td>30.08</td>
    <td>8.24</td>
    <td>22.48</td>
    <td>17.11</td>
  </tr>
  <tr>
    <td>SS-OWFormer (10%)</td>
    <td>10.19</td>
    <td>35.02</td>
    <td>12.13</td>
    <td>26.18</td>
    <td>20.96</td>
  </tr>
</tbody>
</table>


### SS-OWOD Results on satellite OWOD Splits
<table align="center">
<thead>
  <tr>
    <th>Model</th>
    <th>Evaluation</th>
    <th>mAP</th>
    <th>U-Recall</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td rowspan="2">Baseline</td>
    <td>Task-1</td>
    <td>64.9</td>
    <td>2.5</td>
  </tr>
  <tr>
    <td>Task-2</td>
    <td>68.1</td>
    <td>-</td>
  </tr>
  <tr>
    <td rowspan="2">SS-OWFormer</td>
    <td>Task-1</td>
    <td>66.7</td>
    <td>7.6</td>
  </tr>
  <tr>
    <td>Task-2</td>
    <td>70.9</td>
    <td>-</td>
  </tr>
</tbody>
</table>

## Qualitative Examples 
<p align="center" ><img width='850' src = "https://i.imgur.com/w0VIDYd.jpg"></p> 

<p align="center" ><img width='800' src = "https://i.imgur.com/p0DMQUA.jpg"></p> 

## Acknowledgement 
We are thankful to [ORE](https://github.com/JosephKJ/iOD), [MMRotate](https://github.com/open-mmlab/mmrotate), and [OW-DETR](https://github.com/akshitac8/OW-DETR) for releasing their models and code as open-source contributions.

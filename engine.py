# ------------------------------------------------------------------------
# Deformable DETR
# Copyright (c) 2020 SenseTime. All Rights Reserved.
# Licensed under the Apache License, Version 2.0 [see LICENSE for details]
# ------------------------------------------------------------------------
# Modified from DETR (https://github.com/facebookresearch/detr)
# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
# ------------------------------------------------------------------------
 
"""
Train and eval functions used in main.py
"""
import math
import os
import sys
from typing import Iterable
from util.misc import NestedTensor
import torchshow as ts
 
import torch
import util.misc as utils
from datasets.coco_eval import CocoEvaluator
from datasets.open_world_eval import OWEvaluator
from datasets.panoptic_eval import PanopticEvaluator
from datasets.data_prefetcher import data_prefetcher
from util.box_ops import box_xyxy_to_cxcywh, box_cxcywh_to_xyxy
from util.plot_utils import plot_prediction
import matplotlib.pyplot as plt
from copy import deepcopy
 
def train_one_epoch(model: torch.nn.Module, criterion: torch.nn.Module,
                    data_loader: Iterable, optimizer: torch.optim.Optimizer,
                    device: torch.device, epoch: int, nc_epoch: int, max_norm: float = 0, enableFrozen=False, F_model=None, F_criterion=None):
    
    enableSSL = True

    if enableSSL :
        F_model.eval()
        F_criterion.eval()


    model.train()
    criterion.train()
    metric_logger = utils.MetricLogger(delimiter="  ")
    metric_logger.add_meter('lr', utils.SmoothedValue(window_size=1, fmt='{value:.6f}'))
    metric_logger.add_meter('class_error', utils.SmoothedValue(window_size=1, fmt='{value:.2f}'))
    metric_logger.add_meter('grad_norm', utils.SmoothedValue(window_size=1, fmt='{value:.2f}'))
    header = 'Epoch: [{}]'.format(epoch)
    print_freq = 10
    prefetcher = data_prefetcher(data_loader, device, prefetch=True)
    samples, targets = prefetcher.next()

    if enableSSL :
        for _ in metric_logger.log_every(range(len(data_loader)), print_freq, header):

            samples_og = NestedTensor(samples.tensors, samples.mask)
            samples_aug = NestedTensor(samples.aug, samples.mask)

            target_annotation = [targets[0]['annotation'],targets[1]['annotation']]
            
            if enableFrozen :
                outputs = model(samples_og, enableSSL=2, samples_aug=samples_aug)    
                A_fz1, B_fz1 = F_model.module.frozen_forward(samples_og, enableSSL=2)
                A_fz2, B_fz2 = F_model.module.frozen_forward(samples_aug, enableSSL=2)
                outputs['ssl_out_f'] = [A_fz1,A_fz2,B_fz1,B_fz2]
            
            else :
                #For Task 1 Alone 
                assert (target_annotation == [True,True])
                outputs = model(samples_og, enableSSL=1, samples_aug=samples_aug)

            if target_annotation == [True,True] :
                loss_dict = criterion(samples_og, outputs, targets, epoch, enableSSL=1) ## samples variable needed for feature selection
            elif target_annotation == [False,False] :
                loss_dict = criterion(samples_og, outputs, targets, epoch, enableSSL=1)
            elif target_annotation == [False,True] :
                loss_dict = criterion(samples_og, outputs, targets, epoch, enableSSL=3)
            elif target_annotation == [True,False] :
                loss_dict = criterion(samples_og, outputs, targets, epoch, enableSSL=4)
            
            weight_dict = deepcopy(criterion.weight_dict)
            ## condition for starting nc loss computation after certain epoch so that the F_cls branch has the time
            ## to learn the within classes seperation.
            if epoch < nc_epoch: 
                for k,v in weight_dict.items():
                    if 'NC' in k:
                        weight_dict[k] = 0
            if target_annotation == [False,False] :
                for k,v in weight_dict.items():
                    if 'ssl' not in k:
                        weight_dict[k] = 0
                    else :
                        weight_dict[k] = 0.1
                        
            losses = sum(loss_dict[k] * weight_dict[k] for k in loss_dict.keys() if k in weight_dict)
            # reduce losses over all GPUs for logging purposes
            loss_dict_reduced = utils.reduce_dict(loss_dict)
            ## Just printing NOt affectin gin loss function
            loss_dict_reduced_unscaled = {f'{k}_unscaled': v
                                        for k, v in loss_dict_reduced.items()}
            loss_dict_reduced_scaled = {k: v * weight_dict[k]
                                        for k, v in loss_dict_reduced.items() if k in weight_dict}
            losses_reduced_scaled = sum(loss_dict_reduced_scaled.values())
    
            loss_value = losses_reduced_scaled.item()
    
            if not math.isfinite(loss_value):
                print("Loss is {}, stopping training".format(loss_value))
                print(loss_dict_reduced)
                sys.exit(1)
    
            optimizer.zero_grad()
            losses.backward()
            if max_norm > 0:
                grad_total_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm)
            else:
                grad_total_norm = utils.get_total_grad_norm(model.parameters(), max_norm)
            optimizer.step()
    
            metric_logger.update(loss=loss_value, **loss_dict_reduced_scaled, **loss_dict_reduced_unscaled)
            if 'class_error' in loss_dict_reduced :
                metric_logger.update(class_error=loss_dict_reduced['class_error'])
            else :
                metric_logger.update(class_error=0)
            metric_logger.update(lr=optimizer.param_groups[0]["lr"])
            metric_logger.update(grad_norm=grad_total_norm)
    
            samples, targets = prefetcher.next()

    else :

        for _ in metric_logger.log_every(range(len(data_loader)), print_freq, header):
            outputs = model(samples)
            loss_dict = criterion(samples, outputs, targets, epoch) ## samples variable needed for feature selection
            weight_dict = deepcopy(criterion.weight_dict)
            ## condition for starting nc loss computation after certain epoch so that the F_cls branch has the time
            ## to learn the within classes seperation.
            if epoch < nc_epoch: 
                for k,v in weight_dict.items():
                    if 'NC' in k:
                        weight_dict[k] = 0
            
            losses = sum(loss_dict[k] * weight_dict[k] for k in loss_dict.keys() if k in weight_dict)
            # reduce losses over all GPUs for logging purposes
            loss_dict_reduced = utils.reduce_dict(loss_dict)
            ## Just printing NOt affectin gin loss function
            loss_dict_reduced_unscaled = {f'{k}_unscaled': v
                                        for k, v in loss_dict_reduced.items()}
            loss_dict_reduced_scaled = {k: v * weight_dict[k]
                                        for k, v in loss_dict_reduced.items() if k in weight_dict}
            losses_reduced_scaled = sum(loss_dict_reduced_scaled.values())
    
            loss_value = losses_reduced_scaled.item()
    
            if not math.isfinite(loss_value):
                print("Loss is {}, stopping training".format(loss_value))
                print(loss_dict_reduced)
                sys.exit(1)
    
            optimizer.zero_grad()
            losses.backward()
            if max_norm > 0:
                grad_total_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm)
            else:
                grad_total_norm = utils.get_total_grad_norm(model.parameters(), max_norm)
            optimizer.step()
    
            metric_logger.update(loss=loss_value, **loss_dict_reduced_scaled, **loss_dict_reduced_unscaled)
            metric_logger.update(class_error=loss_dict_reduced['class_error'])
            metric_logger.update(lr=optimizer.param_groups[0]["lr"])
            metric_logger.update(grad_norm=grad_total_norm)
    
            samples, targets = prefetcher.next()
    # gather the stats from all processes
    metric_logger.synchronize_between_processes()
    print("Averaged stats:", metric_logger)
    return {k: meter.global_avg for k, meter in metric_logger.meters.items()}

## ORIGINAL FUNCTION
@torch.no_grad()
def evaluate(model, criterion, postprocessors, data_loader, base_ds, device, output_dir, args):
    model.eval()
    criterion.eval()
    metric_logger = utils.MetricLogger(delimiter="  ")
    header = 'Test:'
    iou_types = tuple(k for k in ('segm', 'bbox') if k in postprocessors.keys())
    coco_evaluator = OWEvaluator(base_ds, iou_types, args)
 
    panoptic_evaluator = None
    if 'panoptic' in postprocessors.keys():
        panoptic_evaluator = PanopticEvaluator(
            data_loader.dataset.ann_file,
            data_loader.dataset.ann_folder,
            output_dir=os.path.join(output_dir, "panoptic_eval"),
        )
 
    for samples, targets in metric_logger.log_every(data_loader, 10, header):
        samples = samples.to(device)
        targets = [{k: v.to(device) for k, v in t.items()} for t in targets]
        outputs = model(samples)

        orig_target_sizes = torch.stack([t["orig_size"] for t in targets], dim=0)
        results = postprocessors['bbox'](outputs, orig_target_sizes)
 
        if 'segm' in postprocessors.keys():
            target_sizes = torch.stack([t["size"] for t in targets], dim=0)
            results = postprocessors['segm'](results, outputs, orig_target_sizes, target_sizes)
        res = {target['image_id'].item(): output for target, output in zip(targets, results)}
        if coco_evaluator is not None:
            coco_evaluator.update(res)
 
        if panoptic_evaluator is not None:
            res_pano = postprocessors["panoptic"](outputs, target_sizes, orig_target_sizes)
            for i, target in enumerate(targets):
                image_id = target["image_id"].item()
                file_name = f"{image_id:012d}.png"
                res_pano[i]["image_id"] = image_id
                res_pano[i]["file_name"] = file_name
 
            panoptic_evaluator.update(res_pano)
 
    # gather the stats from all processes
    metric_logger.synchronize_between_processes()
    # print("Averaged stats:", metric_logger)
    if coco_evaluator is not None:
        coco_evaluator.synchronize_between_processes()
    if panoptic_evaluator is not None:
        panoptic_evaluator.synchronize_between_processes()
 
    # accumulate predictions from all images
    if coco_evaluator is not None:
        coco_evaluator.accumulate()
        coco_evaluator.summarize()
    panoptic_res = None
    if panoptic_evaluator is not None:
        panoptic_res = panoptic_evaluator.summarize()
    stats = {k: meter.global_avg for k, meter in metric_logger.meters.items()}
    if coco_evaluator is not None:
        if 'bbox' in postprocessors.keys():
            stats['coco_eval_bbox'] = coco_evaluator.coco_eval['bbox'].stats.tolist()
        if 'segm' in postprocessors.keys():
            stats['coco_eval_masks'] = coco_evaluator.coco_eval['segm'].stats.tolist()
    if panoptic_res is not None:
        stats['PQ_all'] = panoptic_res["All"]
        stats['PQ_th'] = panoptic_res["Things"]
        stats['PQ_st'] = panoptic_res["Stuff"]
    return stats, coco_evaluator
 
@torch.no_grad()
def viz(model, criterion, postprocessors, data_loader, base_ds, device, output_dir):
    import numpy as np
    os.makedirs(output_dir, exist_ok=True)
    model.eval()
    criterion.eval()
 
    metric_logger = utils.MetricLogger(delimiter="  ")
    metric_logger.add_meter('class_error', utils.SmoothedValue(window_size=1, fmt='{value:.2f}'))
 
    for samples, targets in data_loader:
        samples = samples.to(device)
        targets = [{k: v.to(device) for k, v in t.items()} for t in targets]
        top_k = len(targets[0]['boxes'])
 
        outputs = model(samples)

        indices = outputs['pred_logits'][0].softmax(-1)[..., 1].sort(descending=True)[1][:top_k]
        predictied_boxes = torch.stack([outputs['pred_boxes'][0][i] for i in indices]).unsqueeze(0)
        logits = torch.stack([outputs['pred_logits'][0][i] for i in indices]).unsqueeze(0)
        fig, ax = plt.subplots(1, 3, figsize=(10,3), dpi=200)
 
        img = samples.tensors[0].cpu().permute(1,2,0).numpy()
        img = img * np.array([0.229, 0.224, 0.225]) + np.array([0.485, 0.456, 0.406])
        img = (img * 255)
        img = img.astype('uint8')
        h, w = img.shape[:-1]
 
        # Pred results
        plot_prediction(samples.tensors[0:1], predictied_boxes, logits, ax[1], plot_prob=False)
        ax[1].set_title('Prediction (Ours)')
 
        # GT Results
        plot_prediction(samples.tensors[0:1], targets[0]['boxes'].unsqueeze(0), torch.zeros(1, targets[0]['boxes'].shape[0], 4).to(logits), ax[2], plot_prob=False)
        ax[2].set_title('GT')
 
        for i in range(3):
            ax[i].set_aspect('equal')
            ax[i].set_axis_off()
 
        plt.savefig(os.path.join(output_dir, f'img_{int(targets[0]["image_id"][0])}.jpg'))
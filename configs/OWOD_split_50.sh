#!/usr/bin/env bash

set -x

EXP_DIR=exps/OWOD_50/OWOD_t1
PY_ARGS=${@:1}

python -u main_open_world.py \
    --output_dir ${EXP_DIR} --dataset owod --num_queries 100 --eval_every 2 \
    --PREV_INTRODUCED_CLS 0 --CUR_INTRODUCED_CLS 20 --data_root 'data/OWOD' --train_set 't1_train' --test_set 'all_task_test' --num_classes 81 \
    --unmatched_boxes --epochs 50 --top_unk 5 --featdim 1024 --NC_branch --nc_loss_coef 0.1 --nc_epoch 9 --lr_drop 34 \
    --data_sub 'data/OWOD/VOC2007/ImageSets/t1_train.txt' \
    --backbone 'dino_resnet50' \
    ${PY_ARGS}

EXP_DIR=exps/OWOD_50/OWOD_t2
PY_ARGS=${@:1}

python -u main_open_world.py \
    --output_dir ${EXP_DIR} --dataset owod --num_queries 100 --eval_every 2 \
    --PREV_INTRODUCED_CLS 20 --CUR_INTRODUCED_CLS 20 --data_root 'data/OWOD' --train_set 't2_train' --test_set 'all_task_test' --num_classes 81 \
    --unmatched_boxes --epochs 56 --top_unk 5 --lr 2e-5 --featdim 1024 --NC_branch --nc_loss_coef 0.1 --nc_epoch 9 \
    --backbone 'dino_resnet50' \
    --data_sub 'data/OWOD/VOC2007/ImageSets/t2_train_50.txt' \
    --pretrain 'exps/OWOD_50/OWOD_t1/checkpoint0049.pth' \
    --Fresume 'exps/OWOD_50/OWOD_t1/checkpoint0049.pth' \
    ${PY_ARGS}


EXP_DIR=exps/OWOD_50/OWOD_t2_ft
PY_ARGS=${@:1}

python -u main_open_world.py \
    --output_dir ${EXP_DIR} --dataset owod --num_queries 100 --eval_every 2 \
    --PREV_INTRODUCED_CLS 20 --CUR_INTRODUCED_CLS 20 --data_root 'data/OWOD' --train_set 't2_ft' --test_set 'all_task_test' --num_classes 81 \
    --unmatched_boxes --epochs 101 --top_unk 5 --featdim 1024 --NC_branch --nc_loss_coef 0.1 --nc_epoch 9 --lr_drop 30 \
    --backbone 'dino_resnet50' \
    --pretrain 'exps/OWOD_50/OWOD_t2/checkpoint0054.pth' \
    --data_sub 'data/OWOD/VOC2007/ImageSets/t2_ft_50.txt' \
    --Fresume 'exps/OWOD_50/OWOD_t1/checkpoint0049.pth' \
    ${PY_ARGS}


EXP_DIR=exps/OWOD_50/OWOD_t3
PY_ARGS=${@:1}

python -u main_open_world.py \
    --output_dir ${EXP_DIR} --dataset owod --num_queries 100 --eval_every 2 \
    --PREV_INTRODUCED_CLS 40 --CUR_INTRODUCED_CLS 20 --data_root 'data/OWOD' --train_set 't3_train' --test_set 'all_task_test' --num_classes 81 \
    --unmatched_boxes --epochs 106 --lr 2e-5 --top_unk 5 --featdim 1024 --NC_branch --nc_loss_coef 0.1 --nc_epoch 9 \
    --backbone 'dino_resnet50' \
    --pretrain 'exps/OWOD_50/OWOD_t2_ft/checkpoint0099.pth' \
    --data_sub 'data/OWOD/VOC2007/ImageSets/t3_train_50.txt' \
    --Fresume 'exps/OWOD_50/OWOD_t2_ft/checkpoint0099.pth' \
    ${PY_ARGS}

EXP_DIR=exps/OWOD_50/OWOD_t3_ft
PY_ARGS=${@:1}

python -u main_open_world.py \
    --output_dir ${EXP_DIR} --dataset owod --num_queries 100 --eval_every 2 \
    --PREV_INTRODUCED_CLS 40 --CUR_INTRODUCED_CLS 20 --data_root 'data/OWOD' --train_set 't3_ft' --test_set 'all_task_test' --num_classes 81 \
    --unmatched_boxes --epochs 136 --top_unk 5 --featdim 1024 --NC_branch --nc_loss_coef 0.1 --nc_epoch 9 --lr_drop 25 \
    --backbone 'dino_resnet50' \
    --pretrain 'exps/OWOD_50/OWOD_t3/checkpoint0104.pth' \
    --data_sub 'data/OWOD/VOC2007/ImageSets/t3_ft_50.txt' \
    --Fresume 'exps/OWOD_50/OWOD_t2_ft/checkpoint0099.pth' \
    ${PY_ARGS}


EXP_DIR=exps/OWOD_50/OWOD_t4
PY_ARGS=${@:1}

python -u main_open_world.py \
    --output_dir ${EXP_DIR} --dataset owod --num_queries 100 --eval_every 2 \
    --PREV_INTRODUCED_CLS 60 --CUR_INTRODUCED_CLS 20 --data_root 'data/OWOD' --train_set 't4_train' --test_set 'all_task_test' --num_classes 81 \
    --unmatched_boxes --epochs 141 --lr 2e-5 --top_unk 5 --featdim 1024 --NC_branch --nc_loss_coef 0.1 --nc_epoch 9 \
    --backbone 'dino_resnet50' \
    --pretrain 'exps/OWOD_50/OWOD_t3_ft/checkpoint0134.pth' \
    --data_sub 'data/OWOD/VOC2007/ImageSets/t4_train_50.txt' \
    --Fresume 'exps/OWOD_50/OWOD_t3_ft/checkpoint0134.pth' \
    ${PY_ARGS}


EXP_DIR=exps/OWOD_50/OWOD_t4_ft
PY_ARGS=${@:1}

python -u main_open_world.py \
    --output_dir ${EXP_DIR} --dataset owod --num_queries 100 --eval_every 2 \
    --PREV_INTRODUCED_CLS 60 --CUR_INTRODUCED_CLS 20 --data_root 'data/OWOD' --train_set 't4_ft' --test_set 'all_task_test' --num_classes 81 \
    --unmatched_boxes --epochs 161 --top_unk 5 --featdim 1024 --NC_branch --nc_loss_coef 0.1 --nc_epoch 9 --lr_drop 15 \
    --backbone 'dino_resnet50' \
    --pretrain 'exps/OWOD_50/OWOD_t4/checkpoint0139.pth' \
    --data_sub 'data/OWOD/VOC2007/ImageSets/t4_ft_50.txt' \
    --Fresume 'exps/OWOD_50/OWOD_t3_ft/checkpoint0134.pth' \
    ${PY_ARGS}
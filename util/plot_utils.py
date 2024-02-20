import torch
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path, PurePath
from util.box_ops import box_cxcywh_to_xyxy
import itertools

 
VOC_CLASS_NAMES_COCOFIED = [
    "airplane",  "dining table", "motorcycle",
    "potted plant", "couch", "tv"
]

BASE_VOC_CLASS_NAMES = [
    "aeroplane", "diningtable", "motorbike",
    "pottedplant",  "sofa", "tvmonitor"
]

VOC_CLASS_NAMES = [
    "aeroplane","bicycle","bird","boat","bus","car",
    "cat","cow","dog","horse","motorbike","sheep","train",
    "elephant","bear","zebra","giraffe","truck","person"
]

T2_CLASS_NAMES = [
    "traffic light","fire hydrant","stop sign",
    "parking meter","bench","chair","diningtable",
    "pottedplant","backpack","umbrella","handbag",
    "tie","suitcase","microwave","oven","toaster","sink",
    "refrigerator","bed","toilet","sofa"
]

T3_CLASS_NAMES = [
    "frisbee","skis","snowboard","sports ball",
    "kite","baseball bat","baseball glove","skateboard",
    "surfboard","tennis racket","banana","apple","sandwich",
    "orange","broccoli","carrot","hot dog","pizza","donut","cake"
]

T4_CLASS_NAMES = [
    "laptop","mouse","remote","keyboard","cell phone","book",
    "clock","vase","scissors","teddy bear","hair drier","toothbrush",
    "wine glass","cup","fork","knife","spoon","bowl","tvmonitor","bottle"
]

UNK_CLASS = ["unknown"]

VOC_COCO_CLASS_NAMES = tuple(itertools.chain(VOC_CLASS_NAMES, T2_CLASS_NAMES, T3_CLASS_NAMES, T4_CLASS_NAMES, UNK_CLASS))
print(VOC_COCO_CLASS_NAMES)

CLASSES = list(VOC_COCO_CLASS_NAMES)
# colors for visualization
COLORS = [[0.000, 0.447, 0.741], [0.850, 0.325, 0.098], [0.929, 0.694, 0.125],
          [0.494, 0.184, 0.556], [0.466, 0.674, 0.188], [0.301, 0.745, 0.933]]

 

def plot_logs(logs, fields=('class_error', 'loss_bbox_unscaled', 'mAP'), ewm_col=0, log_name='log.txt'):
    '''
    Function to plot specific fields from training log(s). Plots both training and test results.

 

    :: Inputs - logs = list containing Path objects, each pointing to individual dir with a log file
              - fields = which results to plot from each log file - plots both training and test for each field.
              - ewm_col = optional, which column to use as the exponential weighted smoothing of the plots
              - log_name = optional, name of log file if different than default 'log.txt'.

 

    :: Outputs - matplotlib plots of results in fields, color coded for each log file.
               - solid lines are training results, dashed lines are test results.

 

    '''
    func_name = "plot_utils.py::plot_logs"

 

    # verify logs is a list of Paths (list[Paths]) or single Pathlib object Path,
    # convert single Path to list to avoid 'not iterable' error

 

    if not isinstance(logs, list):
        if isinstance(logs, PurePath):
            logs = [logs]
            print(f"{func_name} info: logs param expects a list argument, converted to list[Path].")
        else:
            raise ValueError(f"{func_name} - invalid argument for logs parameter.\n \
            Expect list[Path] or single Path obj, received {type(logs)}")

 

    # verify valid dir(s) and that every item in list is Path object
    for i, dir in enumerate(logs):
        if not isinstance(dir, PurePath):
            raise ValueError(f"{func_name} - non-Path object in logs argument of {type(dir)}: \n{dir}")
        if dir.exists():
            continue
        raise ValueError(f"{func_name} - invalid directory in logs argument:\n{dir}")

 

    # load log file(s) and plot
    dfs = [pd.read_json(Path(p) / log_name, lines=True) for p in logs]

 

    fig, axs = plt.subplots(ncols=len(fields), figsize=(16, 5))

 

    for df, color in zip(dfs, sns.color_palette(n_colors=len(logs))):
        for j, field in enumerate(fields):
            if field == 'mAP':
                coco_eval = pd.DataFrame(pd.np.stack(df.test_coco_eval.dropna().values)[:, 1]).ewm(com=ewm_col).mean()
                axs[j].plot(coco_eval, c=color)
            else:
                df.interpolate().ewm(com=ewm_col).mean().plot(
                    y=[f'train_{field}', f'test_{field}'],
                    ax=axs[j],
                    color=[color] * 2,
                    style=['-', '--']
                )
    for ax, field in zip(axs, fields):
        ax.legend([Path(p).name for p in logs])
        ax.set_title(field)

 

def plot_precision_recall(files, naming_scheme='iter'):
    if naming_scheme == 'exp_id':
        # name becomes exp_id
        names = [f.parts[-3] for f in files]
    elif naming_scheme == 'iter':
        names = [f.stem for f in files]
    else:
        raise ValueError(f'not supported {naming_scheme}')
    fig, axs = plt.subplots(ncols=2, figsize=(16, 5))
    for f, color, name in zip(files, sns.color_palette("Blues", n_colors=len(files)), names):
        data = torch.load(f)
        # precision is n_iou, n_points, n_cat, n_area, max_det
        precision = data['precision']
        recall = data['params'].recThrs
        scores = data['scores']
        # take precision for all classes, all areas and 100 detections
        precision = precision[0, :, :, 0, -1].mean(1)
        scores = scores[0, :, :, 0, -1].mean(1)
        prec = precision.mean()
        rec = data['recall'][0, :, 0, -1].mean()
        print(f'{naming_scheme} {name}: mAP@50={prec * 100: 05.1f}, ' +
              f'score={scores.mean():0.3f}, ' +
              f'f1={2 * prec * rec / (prec + rec + 1e-8):0.3f}'
              )
        axs[0].plot(recall, precision, c=color)
        axs[1].plot(recall, scores, c=color)
    axs[0].set_title('Precision / Recall')
    axs[0].legend(names)
    axs[1].set_title('Scores / Recall')
    axs[1].legend(names)
    return fig, axs

 

def plot_opencv(boxes, output):
    for (x, y, w, h) in boxes:
        # draw the region proposal bounding box on the image
        color = [random.randint(0, 255) for j in range(0, 3)]
        cv2.rectangle(output, (x, y), (x + w, y + h), color, 2)
    plt.imshow(output)
    plt.show()

 

def plot_image(ax, img, norm):
    if norm:
        img = img * np.array([0.229, 0.224, 0.225]) + np.array([0.485, 0.456, 0.406])
        img = (img * 255)
    img = img.astype('uint8')
    ax.imshow(img)

 

def rescale_bboxes(out_bbox, size):
    img_w, img_h = size
    b = box_cxcywh_to_xyxy(out_bbox)
    b = b * torch.tensor([img_w, img_h, img_w, img_h], dtype=torch.float32).to(out_bbox)
    return b

def plot_prediction_indices(image, boxes, ax=None, plot_prob=True):    
    if ax is None:
        ax = plt.gca()
    plot_results_indices(image[0].permute(1, 2, 0).detach().cpu().numpy(), boxes, ax, plot_prob=plot_prob)

 

def plot_results_indices(pil_img, boxes, ax, plot_prob=True, norm=True):
    from matplotlib import pyplot as plt
    image = plot_image(ax, pil_img, norm)
    if boxes is not None:
        for (xmin, ymin, xmax, ymax) in boxes.tolist():
            ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                       fill=False, color='r', linewidth=2))
    ax.grid('off')

 

def _plot_prediction_indices(image, boxes, ax=None, plot_prob=True):    
    if ax is None:
        ax = plt.gca()
    _plot_results_indices(image[0].permute(1, 2, 0).detach().cpu().numpy(), boxes, ax, plot_prob=plot_prob)

 

def _plot_results_indices(pil_img, boxes, ax, plot_prob=True, norm=True):
    from matplotlib import pyplot as plt
    image = plot_image(ax, pil_img, norm)
    if boxes is not None:
        for (xmin, ymin, xmax, ymax) in boxes.tolist():
            ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                       fill=False, color='b', linewidth=2))
    ax.grid('off')

 

def plot_prediction(image, scores, boxes, labels, ax=None, plot_prob=True):    
    if ax is None:
        ax = plt.gca()
    plot_results(image[0].permute(1, 2, 0).detach().cpu().numpy(), scores, boxes, labels, ax, plot_prob=plot_prob)

def plot_results(pil_img, scores, boxes, labels, ax, plot_prob=True, norm=True):
    from matplotlib import pyplot as plt
    image = plot_image(ax, pil_img, norm)
    colors = COLORS * 100
    if boxes is not None:
        for sc, cl, (xmin, ymin, xmax, ymax), c in zip(scores, labels, boxes.tolist(), colors):
            ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                       fill=False, color=c, linewidth=2))
            
            text = f'{CLASSES[cl]}: {sc:0.2f}'
            ax.text(xmin, ymin, text, fontsize=5, bbox=dict(facecolor='yellow', alpha=0.5))
    ax.grid('off')
 

def plot_prediction_GT(image, boxes, labels, ax=None, plot_prob=True):
    bboxes_scaled0 = rescale_bboxes(boxes, list(image.shape[2:])[::-1])    
    if ax is None:
        ax = plt.gca()
    plot_results_GT(image[0].permute(1, 2, 0).detach().cpu().numpy(), bboxes_scaled0, labels, ax, plot_prob=plot_prob)
 

def plot_results_GT(pil_img, boxes, labels, ax, plot_prob=True, norm=True):
    from matplotlib import pyplot as plt
    image = plot_image(ax, pil_img, norm)
    colors = COLORS * 100
    if boxes is not None:
        for cl, (xmin, ymin, xmax, ymax), c in zip(labels, boxes.tolist(), colors):
            ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                       fill=False, color=c, linewidth=2))
            
            text = f'{CLASSES[cl]}'
            ax.text(xmin, ymin, text, fontsize=5, bbox=dict(facecolor='yellow', alpha=0.5))
    ax.grid('off')
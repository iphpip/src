import torch
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
from config import load_config
import os

config = load_config()

def save_model(model, model_name, fusion_method):
    # 保存模型到融合策略子文件夹
    model_dir = os.path.join(config['model_save_dir'], fusion_method)
    model_path = os.path.join(model_dir, f'{fusion_method}_{model_name}.pth')
    torch.save(model.state_dict(), model_path)

def visualize_results(y_true, y_pred, label_encoder, model_name, fusion_method):
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(12, 15))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=label_encoder.classes_, yticklabels=label_encoder.classes_)
    plt.xlabel('Predicted Labels')
    plt.ylabel('True Labels')
    plt.title(f'{fusion_method}_{model_name} Confusion Matrix')
    vis_dir = os.path.join(config['visualization_dir'], fusion_method)
    vis_path = os.path.join(vis_dir, f'{fusion_method}_{model_name}_confusion_matrix.png')
    if not os.path.exists(os.path.dirname(vis_path)):
        os.makedirs(os.path.dirname(vis_path))
    plt.savefig(vis_path)
    plt.close()

def plot_fusion_metrics(weights_history, attack_types, fusion_method):
    plt.figure(figsize=(12, 8))
    # 绘制动态权重变化曲线
    plt.subplot(1, 2, 1)
    for i, w in enumerate(weights_history.T):
        plt.plot(w, label=f'Model {i+1}')
    plt.title(f'{fusion_method} Dynamic Weight Adjustment')
    
    # 绘制攻击类型分布
    plt.subplot(1, 2, 2)
    sns.countplot(x=attack_types)
    plt.title(f'{fusion_method} Attack Type Distribution')
    vis_dir = os.path.join(config['visualization_dir'], fusion_method)
    vis_path = os.path.join(vis_dir, f'{fusion_method}_fusion_metrics.png')
    if not os.path.exists(os.path.dirname(vis_path)):
        os.makedirs(os.path.dirname(vis_path))
    plt.savefig(vis_path)
    plt.close()